import axios from 'axios'

const service = axios.create({
    baseURL: 'http://localhost:5000',
});

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
        // 直接返回响应数据，不进行额外的检查
        return response.data
    },
    error => {
        console.log('err' + error)
            // 检查错误响应是否包含我们期望的数据格式
        if (error.response && error.response.data && typeof error.response.data === 'string' && error.response.data.includes('severity rating')) {
            // 如果是我们期望的数据格式，直接返回数据
            return error.response.data
        }
        // // 否则，显示错误消息
        // ElMessage({
        //     message: error.message,
        //     type: 'error',
        //     duration: 5 * 1000
        // })
        return Promise.reject(error)
    }
)

export default service