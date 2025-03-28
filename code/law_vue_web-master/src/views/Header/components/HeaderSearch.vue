<template>
  <div class="search-bar">
    <div class="title">
      ⚖️ 法小询v2.0
    </div>
    <div class="subtitle">
      您的个性化法律咨询专家
    </div>
    <el-input v-model="searchQuery" placeholder="请输入想搜索的内容" clearable @keyup.enter="handleSearch" class="search-input">
      <template #append>
        <el-button :icon="Search" @click="handleSearch" class="search-button"></el-button>
      </template>
    </el-input>
  </div>
</template>


<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { Search } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';
import 'element-plus/es/components/message/style/css';

const searchQuery = ref('');

const router = useRouter();

function handleSearch() {
  if (searchQuery.value) {
    router.push({ path: '/ask', query: { q: searchQuery.value } });
  } else {
    ElMessage.warning('请输入搜索内容');
  }
}
</script>


<style scoped lang="scss">
.search-bar {
  // display: flex;
  background-color: transparent !important;
  justify-content: center;
  position: absolute;
  top: 40rem;
  width: 100%;


  .title {
    font-family: 'Arial', sans-serif;
    font-size: 3em;
    font-weight: bold;
    text-align: center;
    color: #89a8b2;

  }

  .subtitle {
    font-family: 'Arial', sans-serif;
    font-size: 1.5em;
    text-align: center;
    color: #e5e1da;
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
}

.el-input {
  width: 50rem;
  border-radius: 2rem;
}
</style>
