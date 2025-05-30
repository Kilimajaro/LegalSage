'''
注意打开VPN！！！
注意本地文件系统的IP会变，需要修改
'''
import gradio as gr
import requests
import base64
from docx import Document
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract
from lightrag.llm import openai_complete_if_cache
import speech_recognition as sr
import time
import json

# 设置大模型参数
async def llm_model_func(prompt, system_prompt=None, history_messages=[], **kwargs):
    return await openai_complete_if_cache(
        "qwen-turbo",
        prompt,
        system_prompt=system_prompt,
        history_messages=history_messages,
        api_key="sk-ad3f81c2a0934b3289501e9d4e3d6452",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        **kwargs,
    )

# 问答函数
async def ask_question(question: str):
    answer = await llm_model_func(prompt=question)
    # 清洗输出，移除所有星号（*）
    cleaned_answer = answer.replace("*", "")
    return cleaned_answer


# # 定义执行test.py文件的函数
# def run_test_py():
#     # 读取py文件内容
#     with open(r"test.py", "r",encoding="utf-8") as f:
#         code = f.read()
#     # 执行py文件内容
#     exec(code)

# 语音识别函数
def recognize_speech(audio_file_path):
    r = sr.Recognizer()
    # 确保音频文件路径是有效的
    if not audio_file_path:
        return "未接收到音频文件"

    try:
        with sr.AudioFile(audio_file_path) as source:
            # 读取音频文件并进行识别
            audio_data = r.record(source)
            text = r.recognize_google(audio_data, language='zh-CN')
            return text
    except sr.UnknownValueError:
        return "未能识别您的语音输入"
    except sr.RequestError as e:
        return f"语音识别连接超时; {e}"
    except Exception as e:
        return f"An error occurred: {e}"
    
def loading(progress_demo=gr.Progress()):
    x=4
    progress_demo(0, desc="Starting...")
    time.sleep(0.1)
    for i in progress_demo.tqdm(range(x)):
        time.sleep(0.1)
    res=f'加载完毕，链接在左下角，请您下载打开！'
    return res

# 定义下载文件的函数
def download_file():
    # 返回一个包含下载链接的HTML内容
    time.sleep(0.5)
    filename = "knowledge_graph_民法典.html"
    return f"<a href='http://10.128.23.194:5000/download/knowledge_graph_民法典.html' target='_blank'>知识图谱推理情况下载</a>"

# 定义查询函数
def query_api(query, mode):
    try:
        response = requests.post("http://127.0.0.1:8020/query", json={"query": query, "mode": mode})
        response.raise_for_status()  # 如果响应状态码不是200，将抛出异常
        return response.json()["data"]
    except requests.exceptions.RequestException as e:
        return f"Error: Unable to query the API - {e}"

# 更新历史消息的函数
def update_history(query, response):
    return f"⚖️用户：{query}\n⚖️法小询：{response}"
# 定义插入文本函数
def insert_text(text):
    global case_description
    case_description += text  # 更新案情描述
    url = "http://127.0.0.1:8020/insert"  # 确保URL正确
    response = requests.post(url, json={"text": text})  # 使用字符串作为键
    if response.status_code == 200:
        return "已经了解了您提供的信息" + "\n" + response.json()["message"]
    else:
        return "Error: Unable to insert text"

def insert_file(file):
    if file.name.endswith('.txt'):
        with open(file, 'r', encoding='utf-8') as f:
            file_data = f.read()
    elif file.name.endswith('.docx'):
        doc = Document(file)
        file_data = "\n".join([para.text for para in doc.paragraphs])
    elif file.name.endswith('.pdf'):
        with open(file, 'rb') as f:
            pdf_reader = PdfReader(f)
            file_data = "\n".join([page.extract_text() for page in pdf_reader.pages])
    elif file.name.endswith(('.png', '.jpg', '.jpeg')):  # 支持常见的图片格式
        image = Image.open(file)
        file_data = pytesseract.image_to_string(image, lang='chi_sim+eng')  # 假设需要识别中英文
# 可识别中英文
    # 检查文件是否为WAV格式
    elif file.name.endswith('.wav'):
        recognizer = sr.Recognizer()
        with sr.AudioFile(file) as source:
            audio_data = recognizer.record(source)  # 读取音频文件
            try:
                file_data = recognizer.recognize_google(audio_data, language='zh-CN')  # 使用Google语音识别
                print("Google 认为你说了:", file_data)
            except sr.UnknownValueError:
                print("Error: Google Web Speech API无法理解音频")
            except sr.RequestError as e:
                print(f"Error: 无法从Google Web Speech API获得结果; {e}")
    else:
        print("Error: Unsupported file type")

    # 将文件内容编码为base64
    file_data_base64 = base64.b64encode(file_data.encode('utf-8')).decode('utf-8')

    # 发送base64编码的文件到FastAPI后端
    try:
        url = "http://127.0.0.1:8020/insert"
        response = requests.post(url, json={"text": file_data_base64})  # 使用字符串作为键
    except requests.exceptions.RequestException as e:
        return file_data + '\n' + f"Error: Unable to connect to the server - {e}"

    if response.status_code == 200:
        return file_data + '\n' + response.json()["message"]
    else:
        return file_data + '\n' + "Error: Unable to insert file"

# 早期中立评估文书自动生成函数
async def wenshu(history):
    # 确保 history 是字符串类型
    if isinstance(history, list):
        history_str = ''.join(history)  # 将列表转换为字符串
    else:
        history_str = history  # 如果已经是字符串，则直接使用
    global case_description
    question = "基本案情："+ case_description + history_str + prompt3  # 将历史记录和prompt组合作为输入
    answer = await ask_question(question)  # 异步调用ask_question函数
    return answer  # 返回答案

# 加载主题文件
with open(r'code\examples\theme\themes_theme_schema@0.0.1.json', 'r', encoding='utf-8') as f:
    theme_dict = json.load(f)
# 传递字典给 from_dict 方法
my_theme = gr.Theme.from_dict(theme_dict)

js1 = """
function refresh() {
    const url = new URL(window.location);

    if (url.searchParams.get('__theme') !== 'light') {
        url.searchParams.set('__theme', 'light');
        window.location.href = url.href;
    }
}
"""

# 预设提示词
prompt1 = """
你作为早期中立评估助手——法小询，承担着为我提供法律咨询服务和出具早期中立评估报告的任务~让我们开始吧！
"""
prompt2='''
你必须在回答的最后，考虑民事案由确定原则、物权法和债法二分原则、法律适用范围等，模仿专业律师向我提问，引导我向你提供更多案件的重要细节！
'''
prompt3='''
请根据上面的对话历史，严格按照以下格式，生成一篇早期中立评估文书：
早期中立评估报告
案情：[根据案情描述，总结案情]
诉讼成本评估：[根据诉讼成本评估，评估案件诉讼成本]
诉讼建议：[根据案情和诉讼成本评估，给出诉讼建议]

---法小询v2.0
'''

def load_css():
    with open(r'code\examples\css\style.css', 'r') as file:
        css_content = file.read()
    return css_content

# 初始化会话历史
history = []
# 初始化案情描述
case_description = ""

with gr.Blocks(theme=my_theme, css=load_css(), js=js1) as demo:
    gr.Image(r"code\examples\css\logo.png", elem_classes="logo-image", interactive=False, container=False, show_share_button=False, show_download_button=False, show_fullscreen_button=False, show_label=False)
    # 设置标题并应用样式
    title_html = """
<div style="font-family: 'Arial', sans-serif; font-size: 2em; font-weight: bold; text-align: center; color: #007bff;">
    ⚖️ 法小询v2.0
</div>
<div style="font-family: 'Arial', sans-serif; font-size: 1.2em; text-align: center; color: #6c757d;">
    您的个性化法律咨询专家
</div>
    """
    title_component = gr.Markdown(title_html)

    with gr.Tab("专业咨询"):
        # 创建查询输入区域
        with gr.Row():
            with gr.Column():
                query_input = gr.Textbox(label="当事人咨询")
                mode_select = gr.Radio(label="咨询模式", choices=["local", "global", "hybrid"], value="local")
            with gr.Column():
                query_button = gr.Button("问一问(*^▽^*)")
                # 创建清空历史记录按钮
                clear_history_button = gr.Button("清空历史记录")
        # 创建本轮输出结果区域
        output_textbox = gr.Textbox(label="本轮咨询输出", lines=5)
        # 创建历史消息显示区域
        history_textbox = gr.Textbox(label="咨询历史", value="\n".join(history), lines=8, interactive=False, visible=True)
        with gr.Row():
            microphone_input = gr.Audio(sources=["microphone"], type="filepath", label="录制音频")
            recognize_button = gr.Button("识别语音")
        speech_result = gr.Textbox(label="识别结果")

        # 当按钮被点击时，调用recognize_speech函数
        recognize_button.click(recognize_speech, inputs=[microphone_input], outputs=[speech_result])
        
        def on_query(query, mode):
            global history  
            if not history:  # 如果历史记录为空，加入预设提示词
                final_query = prompt1 + query  + prompt2 
            else:
                final_query = query + prompt2  # 如果历史记录不为空，直接使用用户输入作为查询语句
            response = query_api(final_query, mode)
            new_history = update_history(query, response)
            history.append(new_history)
            return response, "\n".join(history)  # 返回新的咨询输出和更新后的历史

        query_button.click(on_query, inputs=[query_input, mode_select], outputs=[output_textbox, history_textbox])

        def clear_history():
            global history  # 声明使用全局变量
            # 发送请求到后端清空历史记录
            response = requests.post("http://127.0.0.1:8020/clear_history")
            if response.status_code == 200:
                history = []  # 清空前端维护的历史记录列表
                return ""  # 返回空字符串以清空前端的历史记录显示
            else:
                return "Error: Unable to clear history"

        clear_history_button.click(clear_history, outputs=[history_textbox])
    
    with gr.Tab("案情描述与证据上传"):
        # 创建插入文本界面
        insert_text_iface = gr.Interface(
            fn=insert_text,
            inputs=gr.Textbox(label="输入文本描述"),
            outputs=gr.Textbox(label="补充结果"),
            title="案情描述",
            description="可以在此提供案情基本信息的描述，补充相关法律信息"
        )
        with gr.Row():
            microphone_input = gr.Audio(sources=["microphone"], type="filepath", label="录制音频")
            recognize_button = gr.Button("识别语音")
        speech_result = gr.Textbox(label="识别结果")

        # 当按钮被点击时，调用recognize_speech函数
        recognize_button.click(recognize_speech, inputs=[microphone_input], outputs=[speech_result])
    
        # 创建插入文件界面
        insert_file_iface = gr.Interface(
            fn=insert_file,
            inputs=gr.File(label="支持图像(.png/.jpg/.jpeg)、音频(.wav)、.txt文件、.pdf文件、.docx文档、.txt文件"),
            outputs=gr.Textbox(label="文件上传结果"),
            title="证据/文件上传",
            description="事实证据与法律文件上传"
        )
    
    with gr.Tab("评估文书与知识图谱"):
        # 添加早期中立评估文书自动生成按钮
        wenshu_button = gr.Button("早期中立评估文书自动生成")
        # 创建一个Textbox组件用于显示生成的文书
        wenshu_output = gr.Textbox(label="文书生成结果")
        # 当按钮被点击时，调用wenshu函数，并将返回的结果显示在wenshu_output中
        wenshu_button.click(wenshu, inputs=[history_textbox], outputs=[wenshu_output])
        
        download_button = gr.Button("查看知识图谱推理情况")
        output2=gr.Textbox(label="知识图谱正火速赶来...")
        output1 = gr.HTML()
        download_button.click(fn=loading, inputs=[], outputs=output2)
        download_button.click(fn=download_file, inputs=[], outputs=output1)

# 启动Gradio界面
demo.launch(share=True)