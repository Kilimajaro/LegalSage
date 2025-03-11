from flask import Flask, send_from_directory

app = Flask(__name__)

# 文件存储的目录
FILE_DIRECTORY = 'D:/Important/Others/24CAIL&LAIC&法创杯'

@app.route('/download/<path:filename>')
def download(filename):
    # 检查文件名是否包含非法路径字符
    if '..' in filename.split('/') or ':' in filename:
        return "Error: Invalid file path.", 400

    # 发送文件
    return send_from_directory(directory=FILE_DIRECTORY, path=filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)