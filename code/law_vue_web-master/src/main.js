import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

// 引入初始化样式
import '@/styles/common.scss'

// 测试api
// import { directAsk } from '@/apis/ask'
// directAsk('打人了怎么办').then((res) => {
//   console.log(res)
// })

// 注册懒加载
import { lazyPlugin } from '@/directives/index'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(lazyPlugin)

app.mount('#app')
