import request from '@/utils/request'

export const segmentImage = (formData) => {
    return request({
        url: '/ip_segment_image',
        method: 'post',
        data: formData
    })
}

export const quantifyImages = (data) => {
    return request({
        url: '/ip_quantifiaction',
        method: 'post',
        data
    })
}