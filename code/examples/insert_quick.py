from pydantic import BaseModel
import os
from lightrag import LightRAG, QueryParam
from lightrag.llm import openai_complete_if_cache, openai_embedding
from lightrag.utils import EmbeddingFunc
import numpy as np
from typing import Optional
import asyncio
import nest_asyncio
from fastapi import FastAPI, HTTPException
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
        "qwen-turbo",
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


def insert_all_files_in_folder(folder_path):
    # Read all .txt files from the folder_path directory
     texts = []
     for filename in os.listdir(folder_path):
          if filename.endswith(".txt"):
               file_path = os.path.join(folder_path, filename)
               with open(file_path, "r", encoding="utf-8") as file:
                    texts.append(file.read())
               rag.insert(texts)


# 指定你的文件夹路径
folder_path = r"D:\Important\Others\24CAIL&LAIC&法创杯\JEC-QA\reference_book\民法"
insert_all_files_in_folder(folder_path)