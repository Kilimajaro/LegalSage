<template>
  <div class="container">
    <askSearch />

    <AudioRecorder />

    <div class="output-container">
      <div class="text-frame-1">
        <div>本轮咨询输出</div>
        <br>
        <div class="answer-item-current">

          <!-- <p>{{ SharedStore.directAnswer }}</p> -->
          <div v-html="renderMarkdown(SharedStore.directAnswer)"></div>
        </div>
      </div>
      <br>
      <br>
      <div class="text-frame-2">
        <div>历史咨询输出</div>
        <br>
        <div v-for="(singleHistory, index) in SharedStore.history" :key="index" class="answer-item-history">
          <!-- <p>{{ singleHistory }}</p> -->
          <div v-html="renderMarkdown(singleHistory)"></div>
        </div>
      </div>

    </div>

  </div>


</template>

<script setup>
import { ref } from 'vue';
import askSearch from './askSearch.vue'
import { useSharedStore } from '@/stores/sharedStore'
import AudioRecorder from '@/components/AudioRecorder.vue'
// import VueMarkdown from "vue-markdown";
import { marked } from "marked";
const SharedStore = useSharedStore();

const renderMarkdown = (content) => {
      return marked.parse(content);
    }

</script>

<style scoped lang="scss">
.container {
  padding-bottom: 5rem;

  .output-container {
    display: flex;
    flex-direction: row;
    align-items: normal;

    // 当前的回答
    .text-frame-1 {
      border: 2px solid #b3c8cf;
      padding: 16px;
      border-radius: 8px;
      width: 120%;
      margin: 0 auto;
      margin-right: 2rem;

      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      // 设置最大高度，超过了就用滚动条
      max-height: 50rem;
      overflow-y: auto;
    }

    // 历史的回答
    .text-frame-2 {
      border: 2px solid #f1f0e8;
      padding: 16px;
      border-radius: 8px;
      width: 100%;
      margin: 0 auto;

      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      // 设置最大高度，超过了就用滚动条
      max-height: 50rem;
      overflow-y: auto;
    }


  }


  .answer-item-current {
    margin-bottom: 16px;
    background-color:#b3c8cf;

    p {
      margin: 0;
      color: #333;
      white-space: pre-wrap;
    }
  }

  .answer-item-history {
    margin-bottom: 16px;
    background-color:#f1f0e8;

    p {
      margin: 0;
      color: #333;
      white-space: pre-wrap;
    }

    textarea.history-input {
      width: 120%;
      height: auto;
      padding: 8px;
      border: 1px solid #ccc;
      border-radius: 4px;
      background-color: #fff;
      color: #333;
      resize: none;
      /* 禁止调整大小 */
      white-space: pre-wrap;
      overflow-y: auto;
      box-sizing: border-box;
    }
  }
}
</style>
