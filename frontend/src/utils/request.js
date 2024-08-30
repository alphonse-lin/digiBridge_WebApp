import axios from 'axios'

const service = axios.create({
    baseURL: process.env.VUE_APP_BASE_API, // url = base url + request url
    timeout: 5000 // request timeout
})

// 请求拦截器
service.interceptors.request.use(
    config => {
        // 在发送请求之前做些什么
        return config
    },
    error => {
        // 处理请求错误
        console.log(error) // for debug
        return Promise.reject(error)
    }
)

// 响应拦截器
service.interceptors.response.use(
    response => {
        const res = response.data
            // 根据自定义错误码判断请求是否成功
        if (res.code !== 20000) {
            // 处理错误
            return Promise.reject(new Error(res.message || 'Error'))
        } else {
            return res
        }
    },
    error => {
        console.log('err' + error) // for debug
        ElMessage({
            message: error.message,
            type: 'error',
            duration: 5 * 1000
        })
        return Promise.reject(error)
    }
)

export default service