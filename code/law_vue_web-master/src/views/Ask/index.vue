<template>
  <div class="ask-container">
    <HeaderNav />
    <el-tabs v-model="activeTab" @tab-click="handleTabClick" class="ask-tabs">
      <el-tab-pane name="request">
        <template #label>
          <span style="font-size: 1.3rem" class="label-3">专业咨询</span>
        </template>
      </el-tab-pane>
      <el-tab-pane label="案情描述与证据上传" name="describe">
        <template #label>
          <span style="font-size: 1.3rem" class="label-3">案情描述与证据上传</span>
        </template>
      </el-tab-pane>
      <el-tab-pane label="评估文书与存档" name="document">
        <template #label>
          <span style="font-size: 1.3rem" class="label-3">评估文书与存档</span>
        </template>
      </el-tab-pane>
    </el-tabs>

    <RouterView />
  </div>
</template>

<script setup>
import HeaderNav from '@/components/HeaderNav.vue'
import { ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import 'element-plus/es/components/message/style/css'
import { useDirectAskStore } from '@/stores/ask'
import { onMounted } from 'vue'

const route = useRoute()
// 加载页面时，如果http://localhost:5173/ask?q=ddd  把q取出来
const question = route.query.q
const directAskStore = useDirectAskStore()

// 只要加载，就获取根据传过来的question去请求数据
onMounted(() => {
  if (question) {
    try {
      directAskStore.getDirectAskResult(question)
    } catch (error) {
      ElMessage.error('请求失败，请稍后重试')
    }
  }
})

const router = useRouter()

const activeTab = ref(route.name || '')
console.log('activeTab', activeTab.value)

const handleTabClick = (tab) => {
  const targetName = tab.paneName === '' ? '' : tab.paneName
  router.push({ name: targetName })
}

watch(
  () => route.name,
  (newVal) => {
    activeTab.value = newVal || ''
  },
)
</script>

<style scoped lang="scss">
.ask-container {
  .ask-tabs {
    margin-top: 7rem;
  }

  .ask-tabs :deep(.el-tabs__nav) {
    background-color: white;
    /* 更改标签背景色 */
  }

  .ask-tabs :deep(.el-tabs__item) {
    font-size: 16px;
    /* 调整字体大小 */
    padding: 0 30px;
    /* 增加内边距 */
    color: #b3c8cf;
  }

  .ask-tabs :deep(.el-tabs__item.is-active) {
    color: #89a8b2;
    /* 激活状态的颜色 */
  }
  .ask-tabs :deep(.el-tabs__active-bar) {
    background-color: #89a8b2; /* 设置选中时横线的颜色 */
  }
}
</style>
