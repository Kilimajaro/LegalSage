import httpInstance from '@/utils/http'; // 引入封装好的 axios 实例

export const uploadAndRecognizeSpeech = async (audioBlob) => {
  try {
    // 创建 FormData 并附加音频文件
    const formData = new FormData();
    formData.append('file', audioBlob, 'recording.wav'); // 注意字段名与后端一致

    // 发送 POST 请求到后端
    const response = await httpInstance.post('/upload_recognize_speech', formData, {
      headers: {
        'Content-Type': 'multipart/form-data', // 设置 Content-Type
      },
    });

    return response; // 返回后端响应数据
  } catch (error) {
    console.error('音频上传或识别失败:', error);
    throw error; // 抛出错误以便调用方处理
  }
};