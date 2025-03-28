<script setup>
import HeaderNav from '@/components/HeaderNav.vue'
import HeaderSearch from './components/HeaderSearch.vue'
import { onMounted, onBeforeUnmount } from 'vue';
import bgImage from '@/assets/images/bg.jpg';

onMounted(() => {
  document.body.style.backgroundImage = `url(${bgImage})`;
  document.body.style.backgroundSize = 'cover';
  document.body.style.backgroundPosition = 'center';
  document.body.style.backgroundRepeat = 'no-repeat';
});

// 在组件卸载时恢复 body 样式
onBeforeUnmount(() => {
  document.body.style.backgroundImage = '';
  document.body.style.backgroundSize = '';
  document.body.style.backgroundPosition = '';
  document.body.style.backgroundRepeat = '';
});
</script>



<template>
  <div class="home">
    <HeaderNav />
    <HeaderSearch class="search-panel" />

  </div>

</template>



<style scoped lang="scss"></style>
