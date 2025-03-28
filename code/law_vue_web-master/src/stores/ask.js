import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { directAsk, clearHistory, findAsk, mixAsk } from '@/apis/ask'
import { useSharedStore } from './sharedStore'
// 把 直接查询的内容 放入 Pinia
export const useDirectAskStore = defineStore('directAsk', () => {
  // const directAnswer = ref('')
  // const history = ref([])

  const sharedStore = useSharedStore()
  const getDirectAskResult = async (query) => {
    const res = await directAsk(query)
    // directAnswer.value = res.response
    // history.value = Object.values(res.history)
    sharedStore.updateDirectAnswer(res.response)
    sharedStore.updateHistory(Object.values(res.history))
  }
  // const clearData = () => {
  //   directAnswer.value = ''
  //   history.value = []
  // }
  return {
    // directAnswer,
    // history,
    // getDirectAskResult,
    // clearData,
    getDirectAskResult,
    clearData: sharedStore.clearData,
    directAnswer: computed(() => sharedStore.directAnswer),
    history: computed(() => sharedStore.history),
  }
})

// 把 检索查询的内容 放入 Pinia
export const useFindAskStore = defineStore('findAsk', () => {
  // const directAnswer = ref('')
  // const history = ref([])
  const sharedStore = useSharedStore()
  const getFindAskResult = async (query) => {
    const res = await findAsk(query)
    // directAnswer.value = res.response
    // history.value = Object.values(res.history)
    sharedStore.updateDirectAnswer(res.response)
    sharedStore.updateHistory(Object.values(res.history))
  }
  // const clearData = () => {
  //   directAnswer.value = ''
  //   history.value = []
  // }
  return {
    // directAnswer,
    // history,
    // getFindAskResult,
    // clearData,
    getFindAskResult,
    clearData: sharedStore.clearData,
    directAnswer: computed(() => sharedStore.directAnswer),
    history: computed(() => sharedStore.history),
  }
})

// 把 混合查询的内容 放入 Pinia
export const useMixAskStore = defineStore('mixAsk', () => {
  // const directAnswer = ref('')
  // const history = ref([])
  const sharedStore = useSharedStore()
  const getMixAskResult = async (query) => {
    const res = await mixAsk(query)
    // directAnswer.value = res.response
    // history.value = Object.values(res.history)
    sharedStore.updateDirectAnswer(res.response)
    sharedStore.updateHistory(Object.values(res.history))
  }
  // const clearData = () => {
  //   directAnswer.value = ''
  //   history.value = []
  // }
  return {
    // directAnswer,
    // history,
    // getFindAskResult,
    // clearData,
    getMixAskResult,
    clearData: sharedStore.clearData,
    directAnswer: computed(() => sharedStore.directAnswer),
    history: computed(() => sharedStore.history),
  }
})
