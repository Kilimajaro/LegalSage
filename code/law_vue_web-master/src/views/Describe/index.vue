<template>
  <div class="describe-container">
    <div class="case-container">
      <div class="describe-title">案情描述</div>
      <div>可以在此提供案情基本信息的描述，补充相关法律信息</div>

      <div class="search-container">
        <el-input v-model="searchQuery" placeholder="请输入文本描述" class="search-input">
          <template #append>
            <el-button :icon="Search" @click="handleAddDescribe" class="search-button"></el-button>
          </template>
        </el-input>
        <div class="btn-container">
          <el-button
            type="primary"
            class="clear-button"
            round
            @click="handleClear"
            size="large"
            style="width: 10rem; font-size: 1.2rem; color: black"
            color="#89a8b2"
            >清空内容</el-button
          >
        </div>
      </div>
      <AudioRecorder />
      <div style="margin-bottom: 1rem">补充结果</div>
      <div class="res-container">
        <div class="res-content">
          <p id="result-span">
            {{ resData }}
          </p>
        </div>
      </div>
    </div>

    <div class="file-container">
      <div class="describe-title" style="margin-top: 3rem">证据/文件上传</div>

      <div class="file-upload">
        <!-- 左侧：文件上传区域 -->
        <div class="left">
          <div style="margin-bottom: 1rem">
            事实证据与法律文件上传
            <span style="color: darkgreen"
              >(支持图像(.png/.jpg/.jpeg)、.txt文件、.pdf文件、.docx文档)</span
            >
          </div>

          <el-upload
            ref="uploadRef"
            action="http://localhost:5003/upload_file"
            :auto-upload="false"
            :on-success="handleSuccess"
            :on-error="handleError"
            :on-change="handleChange"
            :on-remove="handleRemove"
            :before-upload="beforeUpload"
            :limit="5"
            multiple
            drag
          >
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">将文件拖到此处，或<em style="color: #89a8b2">点击上传</em></div>
            <template #tip>
              <div class="el-upload__tip">支持多文件上传，单个文件大小不超过 10MB。</div>
            </template>
          </el-upload>

          <!-- 手动上传按钮 -->
          <el-button
            type="primary"
            style="margin-top: 20px; font-size: 1.2rem; color: black"
            @click="handleManualUpload"
            :disabled="fileList.length === 0"
            class="upload-button"
            size="large"
            color="#89a8b2"
          >
            开始上传
          </el-button>
        </div>

        <div class="right">
          <div style="margin-bottom: 1rem">文件上传结果</div>
          <div class="file-res-container">
            <div class="file-res-content">
              <p id="file-result-span">
                {{ fileResData }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Search } from '@element-plus/icons-vue'
import { ref } from 'vue'
import { addDescribe } from '@/apis/describe'
import AudioRecorder from '@/components/AudioRecorder.vue'
import { ElMessage } from 'element-plus'

const searchQuery = ref('')
const resData = ref('')
const fileResData = ref('')
const handleClear = () => {
  searchQuery.value = ''
}
const handleAddDescribe = async () => {
  if (searchQuery.value) {
    resData.value = ''
    const res = await addDescribe(searchQuery.value)
    resData.value = '补充结果：' + res.message
  }
}

// 获取 el-upload 的实例
const uploadRef = ref(null)

// 文件列表
const fileList = ref([])

// 文件状态改变时的回调
const handleChange = (file, fileListUpdated) => {
  // console.log('文件状态改变:', file, fileListUpdated);
  fileList.value = fileListUpdated
}

// 文件移除时的回调
const handleRemove = (file, fileListUpdated) => {
  // console.log('文件移除:', file, fileListUpdated);
  fileList.value = fileListUpdated
}

// 上传前的校验
const beforeUpload = (file) => {
  const isLt2M = file.size / 1024 / 1024 < 10 // 文件大小限制为 2MB
  if (!isLt2M) {
    ElMessage.warning('上传文件大小不能超过 10MB!')
    return false
  }
  return true
}

// 手动触发上传
const handleManualUpload = () => {
  if (uploadRef.value) {
    uploadRef.value.submit() // 调用 el-upload 的 submit 方法
    // uploadRef.value.clearFiles();
  }
}

// 上传成功时的回调
const handleSuccess = (response, file, fileListUpdated) => {
  // console.log('上传成功:', response, file, fileListUpdated);
  const status = response.status
  fileResData.value = '文件上传结果：' + response.message
  if (status === 'success') {
    ElMessage.success(`${file.name} 上传成功`)
  } else {
    ElMessage.error(`${file.name} 上传失败`)
  }
}
</script>

<style scope lang="scss">
.describe-container {
  .case-container {
    margin-bottom: 20px;

    .search-container {
      display: flex;
      justify-content: center; // 水平居中
      align-items: center; // 垂直居中
      background-color: white;
      justify-content: center;
      margin-top: 1rem;
      margin-bottom: 2rem;

      .search-input {
        width: 100%;
        height: 4rem;
        border-radius: 2rem;
        // 居中
        margin: 0 auto;

        .search-button {
          width: 4rem;
          height: 4rem;
          padding: 0;

          .el-icon {
            font-size: 30px !important;
          }
        }
      }

      .btn-container {
        margin-left: 1rem;
        display: flex; // 使用Flexbox布局
        justify-content: center; // 水平居中
        align-items: center; // 垂直居中
        height: 100%;

        .submit-button {
          font-size: 1rem; // 调整字体大小
          padding: 1rem;
        }
      }
    }

    .res-container {
      border: 2px solid grey;
      padding: 16px;
      border-radius: 8px;
      width: 100%;
      margin: 0 auto;

      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      // 设置最大高度，超过了就用滚动条
      height: 5rem;
      overflow-y: auto;

      .res-content {
        margin-bottom: 50px;

        #result-span {
          margin: 0;
          color: blue;
          font-size: 2rem;
          white-space: pre-wrap;
        }
      }
    }
  }

  .file-container {
    margin-bottom: 20px;

    .file-upload {
      width: 100%;
      height: 20rem;
      display: flex;

      .left {
        // background-color: lightblue;
        width: 50%;
        height: 100%;

        .el-upload__text {
          font-size: 1.5rem;
        }

        .el-upload__tip {
          margin-top: 8px;
          font-size: 1.5rem;
          color: #89a8b2;
        }

        .upload-button {
          margin-top: 20px;
          font-size: 1rem;
        }
      }

      .right {
        padding-left: 2rem;
        width: 50%;
        height: 100%;
      }

      .file-res-container {
        border: 2px solid grey;
        padding: 16px;
        border-radius: 8px;
        width: 100%;
        margin: 0 auto;

        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        // 设置最大高度，超过了就用滚动条
        height: 10rem;
        overflow-y: auto;

        .file-res-content {
          margin-bottom: 50px;

          #file-result-span {
            margin: 0;
            color: blue;
            font-size: 2rem;
            white-space: pre-wrap;
          }
        }
      }
    }
  }
}

.describe-title {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 20px;
  color: #89a8b2;
  text-align: center;
  padding-top: 1rem;
  padding-bottom: 1rem;
}
</style>
