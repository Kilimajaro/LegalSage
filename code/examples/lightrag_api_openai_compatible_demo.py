from pydantic import BaseModel
import os
from lightrag import LightRAG, QueryParam
from lightrag.llm import openai_complete_if_cache, openai_embedding
from lightrag.utils import EmbeddingFunc
import numpy as np
from typing import Optional
import asyncio
import nest_asyncio
from fastapi import FastAPI, HTTPException, Body
from typing import List

# Apply nest_asyncio to solve event loop issues
nest_asyncio.apply()

DEFAULT_RAG_DIR = r"code\民法"
app = FastAPI(title="LightRAG API", description="API for RAG operations")

# Configure working directory
WORKING_DIR = os.environ.get("RAG_DIR", f"{DEFAULT_RAG_DIR}")
print(f"WORKING_DIR: {WORKING_DIR}")
if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)

# LLM model function

async def llm_model_func(
    prompt, system_prompt=None, history_messages=[], **kwargs
) -> str:
    return await openai_complete_if_cache(
        "qwen-max-latest",
        prompt,
        system_prompt=system_prompt,
        history_messages=history_messages,
        api_key="sk-ad3f81c2a0934b3289501e9d4e3d6452",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        **kwargs,
    )
# Embedding function

async def embedding_func(texts: list[str]) -> np.ndarray:
    return await openai_embedding(
        texts,
        model="BAAI/bge-m3",
        api_key="sk-dghwfttrxpaecbtxqjoebhonisdrkuecffxzplpdkrbaqizp",
        base_url="https://api.siliconflow.cn/v1",
    )



# 换Embedding模型后记得修改dim参数
rag = LightRAG(
    working_dir=WORKING_DIR,
    llm_model_func=llm_model_func,
    embedding_func=EmbeddingFunc(
        embedding_dim=1024, max_token_size=32, func=embedding_func
    ),
)

# Data models


class QueryRequest(BaseModel):
    query: str
    mode: str = "hybrid"


class InsertRequest(BaseModel):
    text: str


class InsertFileRequest(BaseModel):
    file_path: str


class Response(BaseModel):
    status: str
    data: Optional[str] = None
    message: Optional[str] = None

class HistoryManager:
    def __init__(self):
        self.history = ""
        self.dialogue_count = 0

    async def get_history(self) -> str:
        return self.history

    async def add_to_history(self, query: str, result: str):
        # 将本轮查询和回答添加到历史中
        self.history += f"{query} {result} "
        self.dialogue_count += 1
        if self.dialogue_count % 11 == 0:
            # 每十一轮对话后，生成历史摘要
            self.history = await self.summarize_history(self.history)
        return self.history

    async def summarize_history(self, history: str) -> str:
        # 调用大模型生成摘要
        prompt = f"请将以下历史对话摘要为简短的段落：{history}"
        summary = await llm_model_func(prompt)
        return summary

history_manager = HistoryManager() 

@app.post("/query", response_model=Response)
async def query_endpoint(request: QueryRequest):
    try:
        loop = asyncio.get_event_loop()
        # 获取历史消息
        history = await history_manager.get_history()
        history_input = history +"以上是截取的历史消息,以帮助你全面的了解用户信息。下面请回答用户新的提问："
        combined_query = f"{history_input}{request.query} "
        # 假设rag.query是一个异步函数，我们需要传递合并后的查询
        result = await loop.run_in_executor(
            None, lambda: rag.query(combined_query, param=QueryParam(mode=request.mode))
        )
        # 将本轮查询和回答添加到历史中
        await history_manager.add_to_history(request.query, result)
        return Response(status="success", data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clear_history", response_model=Response)
async def clear_history_endpoint():
    try:
        history_manager.history = ""  # 直接将history属性设置为空字符串
        return Response(status="success", message="History cleared successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/insert", response_model=Response)
async def insert_endpoint(request: InsertRequest):
    max_retries = 10
    retries = 0
    while retries < max_retries:
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, lambda: rag.insert(request.text))
            return Response(status="success", message="Text inserted successfully")
        except Exception as e:
            retries += 1
            if retries == max_retries:
                raise HTTPException(status_code=500, detail=f"Failed to insert text after {max_retries} retries: {str(e)}")
            # Optionally, you can add a delay between retries to avoid overwhelming the system
            # await asyncio.sleep(1)  # Uncomment this line if you want to add a delay

@app.get("/health")
async def health_check():
    return {"status": "healthy"}



# @app.post("/insert_file")
# async def insert_file(file: UploadFile = File(...)):
#     try:
#         # 读取文件内容
#         content = await file.read()
#         try:
#             # 尝试 UTF-8 解码
#             content = content.decode('utf-8')
#         except UnicodeDecodeError:
#             # 如果 UTF-8 解码失败，尝试其他编码
#             content = content.decode('gbk')

#         # 使用 /insert 端点插入文件内容
#         return await insert_endpoint(InsertRequest(text=content))
#     except UnicodeDecodeError:
#         return JSONResponse(content={"status": "error", "message": "Failed to decode file content"})
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8020)

# Usage example
# To run the server, use the following command in your terminal:
# python lightrag_api_openai_compatible_demo.py

# Example requests:
# 1. Query:
# curl -X POST "http://127.0.0.1:8020/query" -H "Content-Type: application/json" -d "{\"query\": \"什么是先诉抗辩权？\", \"mode\": \"local\"}"

# 2. Insert text:
# curl -X POST "http://127.0.0.1:8020/insert" -H "Content-Type: application/json" -d "{\"text\": \"民法的基本原则有：1、平等原则； 2、自愿原则； 3、公平原则； 4、诚实信用原则； 5、公序良俗原则； 6、禁止权利滥用原则， 7、绿色原则\"}"

# 3. Insert file:
# curl -X POST "http://127.0.0.1:8020/insert_file" -H "Content-Type: application/json" -d '{"file_path": "path/to/your/file.txt"}'

# 4. Health check:
# curl -X GET "http://127.0.0.1:8020/health"
