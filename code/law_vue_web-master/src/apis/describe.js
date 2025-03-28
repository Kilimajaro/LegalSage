import httpInstance from '@/utils/http'


// 补充案情
export function addDescribe(query) {
  // console.log(query)
  return httpInstance({
    method: 'post', // 指定请求方法为POST
    url: '/case_discrption', // 目标路由
    data: {
      // 发送的数据
      query: query,
    },
    transformRequest: [
      function (data) {
        // 对数据进行处理，使其符合'application/x-www-form-urlencoded'格式
        let ret = ''
        for (let it in data) {
          ret += encodeURIComponent(it) + '=' + encodeURIComponent(data[it]) + '&'
        }
        return ret
      },
    ],
  })
}