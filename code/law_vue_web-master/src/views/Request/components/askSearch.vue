<template>
  <div class="search-bar">
    <el-input v-model="searchQuery" placeholder="请输入想搜索的内容" clearable @keyup.enter="handleSearch" class="search-input">
      <template #append>
        <el-button :icon="Search" @click="handleSearch" class="search-button"></el-button>
      </template>
    </el-input>
    <div class="btn-container">
      <el-select v-model="select" placeholder="请选择" class="select-container" size="large" style="width: 12rem">
        <el-option label="直接咨询" value="1" style="font-size: 1.2rem; margin-bottom: 0.5rem;"></el-option>
        <el-option label="检索咨询" value="2" style="font-size: 1.2rem; margin-bottom: 0.5rem;"></el-option>
        <el-option label="混合咨询" value="3" style="font-size: 1.2rem; margin-bottom: 0.5rem;"></el-option>
      </el-select>
      <!--  删除历史记录的按钮-->
      <el-button type="danger" class="delete-button" @click="handleDeleteHistory" round size="large" style="font-size: 1.2rem; color: black" color="#b3c8cf">清空历史记录</el-button>

    </div>

  </div>
</template>


<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { Search } from '@element-plus/icons-vue';
import { directAsk, clearHistory } from '@/apis/ask';
import { ElMessage } from 'element-plus';
import 'element-plus/es/components/message/style/css'; // 如果需要单独引入样式
import { useDirectAskStore, useFindAskStore, useMixAskStore } from '@/stores/ask'
import { useSharedStore } from '@/stores/sharedStore'

// 初始化 select 变量，并设置默认值为 "1"
const select = ref('1');


const directAskStore = useDirectAskStore();
const findAskStore = useFindAskStore();
const SharedStore = useSharedStore();
const mixAskStore = useMixAskStore();

const searchQuery = ref('');
async function handleSearch() {
  if (searchQuery.value.trim() === '') {
    ElMessage.warning('请输入搜索内容');
    return;
  }
  if (select.value === '1') {
    await directAskStore.getDirectAskResult(searchQuery.value);
  } else if (select.value === '2') {
    await findAskStore.getFindAskResult(searchQuery.value);
  } else if (select.value === '3') {
    await mixAskStore.getMixAskResult(searchQuery.value);
  }


  ElMessage({
    message: '已查询出结果！',
    type: 'success', // 这里设置为'success'会显示浅绿色背景
    customClass: 'custom-message', // 可以自定义类名以进一步定制样式
    duration: 3000, // 显示时长，单位为毫秒
  });

}

async function handleDeleteHistory() {
  try {
    await clearHistory();
    SharedStore.clearData();
    console.log('清空历史记录成功');
    ElMessage({
      message: '历史记录已清空',
      type: 'success', // 这里设置为'success'会显示浅绿色背景
      customClass: 'custom-message', // 可以自定义类名以进一步定制样式
      duration: 3000, // 显示时长，单位为毫秒
    });
  } catch (error) {
    console.error('清空历史记录失败:', error);
  }
}
</script>


<style scoped lang="scss">
.search-bar {
  display: flex;
  justify-content: center; // 水平居中
  align-items: center; // 垂直居中
  background-color: white;
  justify-content: center;
  margin-top: 10px;

  .title {
    font-family: 'Arial', sans-serif;
    font-size: 3em;
    font-weight: bold;
    text-align: center;
    color: #007bff;

  }

  .subtitle {
    font-family: 'Arial', sans-serif;
    font-size: 1.5em;
    text-align: center;
    color: #6c757d;
    margin-bottom: 1rem;
  }

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

    .delete-button {
      font-size: 1rem; // 调整字体大小
      padding: 1rem;
    }

    .select-container {
      width: 7rem;
      margin-left: 1rem;
      margin-right: 2rem;

      .el-select {
        font-size: 1rem
      }

    }
  }
}

.el-input {
  width: 50rem;
  border-radius: 2rem;
}

.custom-message {
  background-color: #f0f9eb;
  /* 浅绿色背景 */
  color: #67c23a;
  /* 文字颜色 */
}
</style>
