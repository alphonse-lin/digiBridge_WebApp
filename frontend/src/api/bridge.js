import request from '@/utils/request'


export const generateSolution = (formData) => {
    return request({
        url: '/am_generate_solution',
        method: 'post',
        data: formData,
        headers: { 'Content-Type': 'multipart/form-data' }
    })
}

export const addFeedback = (data) => {
    return request({
        url: '/am_add_feedback',
        method: 'post',
        data
    })
}

export const processCorrosionAuto = (data) => {
    return request({
        url: '/ow_process_corrosionAuto',
        method: 'post',
        timeout: 60000,
        data,
        validateStatus: function(status) {
            return status >= 200 && status < 300 // 默认值
        }
    })
}

export const uploadFile = (formData) => {
    return request({
        url: '/ow_upload',
        method: 'post',
        data: formData,
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
}

export const processCorrosion = (data) => {
    return request({
        url: '/ow_process_corrosion',
        method: 'post',
        timeout: 60000,
        data
    })
}

// Scenario 2 functions
export const processCoatingDefect = (data) => {
    return request({
        url: '/ow_process_coating_defect',
        method: 'post',
        timeout: 60000,
        data
    })
}

// Scenario 3 functions
export const processCrackOnMasonry = (data) => {
    return request({
        url: '/ow_process_crackOnMasonry',
        method: 'post',
        data,
        timeout: 60000
    })
}

// Scenario 4 functions
export const processCrackOnReinforcedConcrete = (data) => {
        return request({
            url: '/ow_process_crackOnReinforcedConcrete',
            method: 'post',
            data
        })
    }
    // endregion

// Region: ImageProcessing
// Image segmentation and quantification
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
    // endregion