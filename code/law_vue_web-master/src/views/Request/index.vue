<template>
  <div>
    <textFrame />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { directAsk } from '@/apis/ask'
import textFrame from './components/textFrame.vue'
import { onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import 'element-plus/es/components/message/style/css';
import { useDirectAskStore } from '@/stores/ask'

  ;
</script>

<style scoped lang="scss">
.ask-container {
  // display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

#app {
  background-color: blue;
}

.custom-message {
  background-color: #f0f9eb;
  /* 浅绿色背景 */
  color: #67c23a;
  /* 文字颜色 */
}
</style>
