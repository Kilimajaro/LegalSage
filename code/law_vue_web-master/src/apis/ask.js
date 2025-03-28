import httpInstance from '@/utils/http'

// 直接咨询
export function directAsk(query) {
  // console.log(query)
  return httpInstance({
    method: 'post', // 指定请求方法为POST
    url: '/direct_ask', // 目标路由
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

// 清空历史记录  @app.route("/clear_history", methods=["POST"])
export function clearHistory() {
  return httpInstance({
    url: '/clear_history',
    method: 'post',
  })
}

// 检索查询
export function findAsk(query) {
  // console.log(query)
  return httpInstance({
    method: 'post', // 指定请求方法为POST
    url: '/find_ask', // 目标路由
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

// 混合查询
export function mixAsk(query) {
  // console.log(query)
  return httpInstance({
    method: 'post', // 指定请求方法为POST
    url: '/mix_ask', // 目标路由
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
