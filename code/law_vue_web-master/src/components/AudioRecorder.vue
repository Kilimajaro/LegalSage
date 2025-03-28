<template>
  <div class="audio-recorder">
    <!-- 按钮区域 -->
    <div class="buttons">
      <el-button type="primary" @click="toggleRecording" :disabled="isRecognizing" size="large" style="font-size: 1.2rem" color="#89a8b2">
        {{ isRecording ? '停止录制' : '开始录制' }}
      </el-button>
      <el-button type="success" @click="startRecognition" :disabled="!audioBlob || isRecognizing" size="large" style="font-size: 1.2rem; color: black" color="#e5e1da">
        识别音频
      </el-button>
    </div>

    <!-- 录制状态 -->
    <div class="status">
      <p v-if="isRecording">正在录制...</p>
      <p v-else-if="audioBlob">录制完成！</p>
      <p v-else>请开始录制音频。</p>
    </div>

    <!-- 识别结果显示 -->
    <div class="result" v-if="recognitionResult">
      <h3>识别结果：</h3>
      <p>{{ recognitionResult }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { uploadAndRecognizeSpeech } from '@/apis/speechAPI'

// 状态变量
const isRecording = ref(false) // 是否正在录制
const isRecognizing = ref(false) // 是否正在识别
const audioBlob = ref(null) // 录制的音频 Blob
const recognitionResult = ref('') // 识别结果
let mediaRecorder = null // MediaRecorder 实例

// 开始/停止录制
const toggleRecording = async () => {
  if (isRecording.value) {
    stopRecording()
  } else {
    startRecording()
  }
}

// 开始录制
const startRecording = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    mediaRecorder = new MediaRecorder(stream)

    // 存储音频数据块
    const audioChunks = []
    mediaRecorder.ondataavailable = (event) => {
      audioChunks.push(event.data)
    }

    // 录制结束时生成 Blob
    mediaRecorder.onstop = () => {
      audioBlob.value = new Blob(audioChunks, { type: 'audio/wav' })
      console.log('录制完成，音频 Blob:', audioBlob.value)
    }

    mediaRecorder.start()
    isRecording.value = true
  } catch (error) {
    console.error('无法访问麦克风:', error)
    alert('无法访问麦克风，请检查权限设置。')
  }
}

// 停止录制
const stopRecording = () => {
  if (mediaRecorder && mediaRecorder.state !== 'inactive') {
    mediaRecorder.stop()
    isRecording.value = false
  }
}

// 发送音频到后台进行识别
const startRecognition = async () => {
  if (!audioBlob.value) return

  isRecognizing.value = true
  recognitionResult.value = ''

  try {
    const response = await uploadAndRecognizeSpeech(audioBlob.value)
    // 显示识别结果
    recognitionResult.value = response.response || '无识别结果'
  } catch (error) {
    console.error('音频识别失败:', error)
    recognitionResult.value = '识别失败，请稍后重试。'
  } finally {
    isRecognizing.value = false
  }
}
</script>

<style scoped lang="scss">
.audio-recorder {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
}

.buttons {
  margin-bottom: 20px;
}

.status p {
  font-size: 14px;
  color: #666;
}

.result {
  margin-top: 20px;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
  text-align: left;

}
</style>
