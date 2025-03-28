<template>
  <div class="container">
    <div class="get-document">
      <el-button type="info" class="getDocument-button" @click="getShowDocument" round>早期中立评估文书自动生成</el-button>
      <br>
      <br>
      <div class="document-show">
        <div class="document-content">
          <p>{{ documentContent }}</p>
        </div>
      </div>
    </div>


    <div class="download">
      <el-button type="info" class="download-button" @click="download" round>存档历史记录与评估文书</el-button>
      <br>
      <br>
      <div class="download-show">
        <div class="download-content">
          <p>{{ downloadContent }}</p>
        </div>
      </div>
    </div>


  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { getDocument, downloadDocument } from '@/apis/document'
import { ElMessage } from 'element-plus';
import 'element-plus/es/components/message/style/css';

const documentContent = ref('')
const downloadContent = ref('')
const showDocument = async () => {
  const res = await getDocument()
  documentContent.value = res.response
  ElMessage.success('获取成功')
}

const getShowDocument = () => {
  showDocument()
}

const download = async () => {
  downloadContent.value = ""
  const res = await downloadDocument()
  downloadContent.value = "文书内容:\n\n\n" + res.response
  const downloadLink = res.download_link
  console.log(downloadLink);

  ElMessage.info('开始下载文书')
  // 根据完整的downloadLink  直接进行下载
  // window.open(downloadLink);

  // 创建一个隐藏的 <a> 标签
  const link = document.createElement("a");
  link.href = downloadLink; // 设置下载链接
  link.download = "文书.txt"; // 设置文件名
  link.style.display = "none";

  // 将 <a> 标签添加到 DOM 中
  document.body.appendChild(link);

  // 触发点击事件
  link.click();

  // 移除 <a> 标签
  document.body.removeChild(link);
  ElMessage({
    message: '下载成功！ 请查看浏览器默认的下载文件夹。',
    type: 'success', // 这里设置为'success'会显示浅绿色背景
    customClass: 'custom-message', // 可以自定义类名以进一步定制样式
    duration: 20000, // 显示时长，单位为毫秒
  }
  )
}


</script>

<style scope lang="scss">
.container {
  margin: 0 auto;
  width: 100%;
  height: 100%;

  .get-document {
    margin-top: 20px;
    margin-bottom: 20px;

    .getDocument-button {
      width: 100%;
      height: 100%;
      font-size: 2rem;
      background-color: #89a8b2;
      // color: black;

    }

    .document-show {

      border: 2px solid gray;
      padding: 16px;
      border-radius: 8px;
      width: 100%;
      margin: 0 auto;

      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      // 设置最大高度，超过了就用滚动条
      max-height: 30rem;
      height: 30rem;
      overflow-y: auto;

      .document-content {
        width: 100%;
        height: 100%;
        font-size: 1rem;
        ;
        color: black;
        padding: 10px;
      }

      .document-content p {
        margin: 0;
        white-space: pre-wrap;
      }
    }
  }



  .download {
    margin-top: 3rem;
    margin-bottom: 20px;

    .download-button {
      width: 100%;
      height: 100%;
      font-size: 2rem;
      background-color: #e5e1da;
      color: black
    }

    .download-show {
      border: 2px solid gray;
      padding: 16px;
      border-radius: 8px;
      width: 100%;
      margin: 0 auto;

      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      // 设置最大高度，超过了就用滚动条
      max-height: 30rem;
      height: 30rem;
      overflow-y: auto;

      .download-content {
        width: 100%;
        height: 100%;
        font-size: 1rem;
        color: black;
        padding: 10px;
      }

      .download-content p {
        margin: 0;
        white-space: pre-wrap;
      }
    }
  }
}
</style>
