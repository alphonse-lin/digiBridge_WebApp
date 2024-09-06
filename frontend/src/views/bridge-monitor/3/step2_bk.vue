<template>
  <div class="image-selection">
    <h2>Select Segmented Images</h2>
    <el-row :gutter="20">
      <el-col :span="4" v-for="(image, index) in images" :key="index">
        <div class="image-item">
          <el-checkbox v-model="image.selected" @change="updateSelection(index)"></el-checkbox>
          <el-image 
            :src="image.url" 
            :alt="'Image ' + (index + 1)" 
            class="preview-image"
            :preview-src-list="[image.url]"
            :initial-index="0"
            fit="cover"
            :z-index="10000"
          >
            <template #error>
              <div class="image-slot">
                <el-icon><icon-picture /></el-icon>
              </div>
            </template>
          </el-image>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, defineExpose } from 'vue'
import { ElImage, ElIcon } from 'element-plus'
import { Picture as IconPicture } from '@element-plus/icons-vue'

const props = defineProps({
  result: Object
})

const images = ref([
  { url: '/segments/20240807-200015/cutout_0.png', selected: true },
  { url: '/segments/20240807-200015/cutout_1.png', selected: true },
  { url: '/segments/20240807-200015/cutout_2.png', selected: true },
  { url: '/segments/20240807-200015/cutout_3.png', selected: true },
  { url: '/segments/20240807-200015/cutout_4.png', selected: true },
  { url: '/segments/20240807-200015/cutout_5.png', selected: true },
  { url: '/segments/20240807-200015/cutout_6.png', selected: true },
  { url: '/segments/20240807-200015/cutout_7.png', selected: true },
  { url: '/segments/20240807-200015/cutout_8.png', selected: true },
  { url: '/segments/20240807-200015/cutout_9.png', selected: true },
  { url: '/segments/20240807-200015/cutout_10.png', selected: true },
  { url: '/segments/20240807-200015/cutout_11.png', selected: true },
  { url: '/segments/20240807-200015/cutout_12.png', selected: true },
  { url: '/segments/20240807-200015/cutout_13.png', selected: true },
  { url: '/segments/20240807-200015/cutout_14.png', selected: true },
  { url: '/segments/20240807-200015/cutout_15.png', selected: true },
  { url: '/segments/20240807-200015/cutout_16.png', selected: true },
  { url: '/segments/20240807-200015/cutout_17.png', selected: true },
  { url: '/segments/20240807-200015/cutout_18.png', selected: true },
  { url: '/segments/20240807-200015/cutout_19.png', selected: true },
  { url: '/segments/20240807-200015/cutout_20.png', selected: true },
])

watch(() => props.result, (newResult) => {
  if (newResult && newResult.segmented_images) {
    images.value = newResult.segmented_images.map(url => ({ url, selected: true }))
  }
}, { immediate: true })

const updateSelection = (index) => {
  console.log(`Image ${index + 1} selection changed to ${images.value[index].selected}`)
}

const getSelectedImages = () => {
  return images.value.filter(img => img.selected).map(img => img.url)
}

const submitSelection = () => {
  const selectedImages = getSelectedImages()
  console.log('Selected images:', selectedImages)
  // 这里应该发送选中的图片到后端进行处理
  // 例如：fetch('/api/process-images', { method: 'POST', body: JSON.stringify({ images: selectedImages }) })
}

// 暴露方法给父组件
defineExpose({
  getSelectedImages,
  submitSelection
})
</script>

<style scoped>
.image-selection {
  padding: 20px;
}

.image-item {
  position: relative;
  margin-bottom: 20px;
}

.preview-image {
  width: 100%;
  height: 150px; /* 设置一个固定高度以保持一致性 */
  object-fit: cover;
  cursor: pointer;
}

.el-checkbox {
  position: absolute;
  top: 10px;
  left: 10px;
  z-index: 1;
  background-color: rgba(255, 255, 255, 0.7);
  padding: 2px;
}

.submit-section {
  margin-top: 20px;
  text-align: center;
}

.image-slot {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  background: #f5f7fa;
  color: #909399;
  font-size: 30px;
}
</style>