// sharedStore.js
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useSharedStore = defineStore('shared', () => {
  const directAnswer = ref('');
  const history = ref([]);

  const updateDirectAnswer = (newValue) => {
    directAnswer.value = newValue;
  };

  const updateHistory = (newHistory) => {
    history.value = newHistory;
  };

  const clearData = () => {
    directAnswer.value = '';
    history.value = [];
  };

  return {
    directAnswer: computed(() => directAnswer.value),
    history: computed(() => history.value),
    updateDirectAnswer,
    updateHistory,
    clearData,
  };
});