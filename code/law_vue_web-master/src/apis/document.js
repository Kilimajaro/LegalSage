import httpInstance from '@/utils/http'

// 补充案情
export function getDocument() {
  // console.log(query)
  return httpInstance({
    method: 'get', // 指定请求方法为POST
    url: '/get_wenshu', // 目标路由
  })
}

export function downloadDocument() {
  // console.log(query)
  return httpInstance({
    method: 'get', // 指定请求方法为POST
    url: '/download_wenshu', // 目标路由
  })
}
