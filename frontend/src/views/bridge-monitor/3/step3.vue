<template>
    <div class="step-wrap">
      <div class="info-section">
        <p class="image-count">Number of selected images: {{ selectedImagesArray.length }}</p>
      <div class="image-section">
        <div v-if="selectedImagesArray.length === 0" class="no-images">No images selected</div>
        <div v-else class="image-grid">
          <div v-for="(imagePath, index) in selectedImagesArray" :key="index" class="image-item">
            <div class="image-wrapper">
              <el-image 
                :src="imagePath" 
                :alt="'Selected image ' + (index + 1)" 
                fit="cover"
                :preview-src-list="[imagePath]"
                :initial-index="0"
                :z-index="10000"
                @error="handleImageError(index, imagePath)"
              >
                <template #error>
                  <div class="image-slot">
                    <el-icon><icon-picture /></el-icon>
                  </div>
                </template>
              </el-image>
            </div>
            <p class="image-path">Image path: {{ imagePath }}</p>
              <div class="assessment-wrapper">
                <el-form v-if="props.questionType === 'Corrosion'" label-width="230px" label-position="left" :inline="false">
                  <el-form-item v-for="(item, key) in getRandomCorrosionAssessment()" :key="key" :label="item.label" style="margin-bottom: 25px;">
                    <div class="form-inner">
                      <div v-if="item.type === 'progress'" style="flex: 1;">
                        <el-progress :text-inside="true" :stroke-width="24" :percentage="item.value" :status="item.status" />
                      </div>
                      <div v-else class="form-inner">{{ item.value }}</div>
                    </div>
                  </el-form-item>
                </el-form>
                <el-form v-else label-width="230px" label-position="left" :inline="false">
                  <el-form-item v-for="(item, key) in getRandomCrackAssessment()" :key="key" :label="item.label" style="margin-bottom: 25px;">
                    <div class="form-inner">
                      <div v-if="item.type === 'progress'" style="flex: 1;">
                        <el-progress :text-inside="true" :stroke-width="24" :percentage="item.value" :status="item.status">
                          <template #default="{ percentage }">
                            <div>{{ item.unit ? `${percentage.toFixed(2)} ${item.unit}` : percentage.toFixed(2) }}</div>
                          </template>
                        </el-progress>
                      </div>
                      <div v-else class="form-inner">{{ item.value }}</div>
                    </div>
                  </el-form-item>
                </el-form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>

<script setup>
import { defineProps, computed } from 'vue'
import { ElImage, ElIcon } from 'element-plus'
import { Picture as IconPicture } from '@element-plus/icons-vue'

const props = defineProps({
  questionType: {
    type: String,
    default: ''
  },
  result: {
    type: Object,
    default: () => ({})
  },
  activeStep: Number,
  selectedImages: Object
})

const selectedImagesArray = computed(() => {
  return Object.values(props.selectedImages || {})
})

const corrosionAssessment = computed(() => {
  if (!props.result) return {}
  return {
    goodPercentage: { label: 'Good percentage', type: 'progress', value: props.result.goodPercentage, status: getStatus(props.result.goodPercentage) },
    mildCorrosion: { label: 'Mild corrosion percentage', type: 'progress', value: props.result.mildCorrosion, status: getStatus(props.result.mildCorrosion) },
    severeCorrosion: { label: 'Severe corrosion percentage', type: 'progress', value: props.result.severeCorrosion, status: getStatus(props.result.severeCorrosion) },
    totalCorrosion: { label: 'Total corrosion percentage', type: 'progress', value: props.result.totalCorrosion, status: getStatus(props.result.totalCorrosion) },
    predictedSolution: { label: 'Predicted solution', type: 'text', value: props.result.predictedSolution },
    groundTruth: { label: 'Ground truth', type: 'text', value: props.result.groundTruth }
  }
})

const crackAssessment = computed(() => {
  if (!props.result) return {}
  return {
    crackNumber: { label: 'Crack number', type: 'progress', value: props.result.crackNumber, status: getStatus(props.result.crackNumber) },
    crackLength: { label: 'Crack length', type: 'progress', value: props.result.crackLength, status: getStatus(props.result.crackLength), unit: 'm' },
    crackDepth: { label: 'Crack depth', type: 'progress', value: props.result.crackDepth, status: getStatus(props.result.crackDepth), unit: 'cm' },
    predictedSolution: { label: 'Predicted solution', type: 'text', value: props.result.predictedSolution }
  }
})

function getRandomCorrosionAssessment() {
  const goodPercentage = Math.random() * 100
  const mildCorrosion = Math.random() * (100 - goodPercentage)
  const severeCorrosion = 100 - goodPercentage - mildCorrosion
  const totalCorrosion = mildCorrosion + severeCorrosion

  return {
    goodPercentage: { label: 'Good percentage', type: 'progress', value: goodPercentage.toFixed(2), status: getStatus(goodPercentage) },
    mildCorrosion: { label: 'Mild corrosion percentage', type: 'progress', value: mildCorrosion.toFixed(2), status: getStatus(mildCorrosion) },
    severeCorrosion: { label: 'Severe corrosion percentage', type: 'progress', value: severeCorrosion.toFixed(2), status: getStatus(severeCorrosion) },
    totalCorrosion: { label: 'Total corrosion percentage', type: 'progress', value: totalCorrosion.toFixed(2), status: getStatus(totalCorrosion) },
    predictedSolution: { label: 'Predicted solution', type: 'text', value: 'cut out corroded section and apply radius for paint system.' },
    groundTruth: { label: 'Ground truth', type: 'text', value: 'cut out corroded section and apply radius for paint system.' }
  }
}

function getRandomCrackAssessment() {
  return {
    crackNumber: { label: 'Crack number', type: 'progress', value: (Math.random() * 100).toFixed(2), status: getStatus(Math.random() * 100) },
    crackLength: { label: 'Crack length', type: 'progress', value: (Math.random() * 100).toFixed(2), status: getStatus(Math.random() * 100), unit: 'm' },
    crackDepth: { label: 'Crack depth', type: 'progress', value: (Math.random() * 100).toFixed(2), status: getStatus(Math.random() * 100), unit: 'cm' },
    predictedSolution: { label: 'Predicted solution', type: 'text', value: 'Structural reinforcement techniques such as steel reinforcement and filling seismic materials to repair and strengthen the cracks, enhancing the structural stability and safety of the building.' }
  }
}

function getStatus(value) {
  if (value < 30) return 'success'
  if (value < 70) return 'warning'
  return 'exception'
}

function handleImageError(index, path) {
  console.error(`Failed to load image at index ${index}, path: ${path}`)
}

console.log('Selected images in Step3:', selectedImagesArray.value)

onMounted(() => { })
onBeforeUnmount(() => { })
</script>

<style lang='scss' scoped>
.step-wrap {
  height: 100%;
  padding: 20px;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.image-item {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
}

.image-wrapper {
  width: 100%;
  height: 200px; // 固定高度，保持一致性
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 10px;
}

.el-image {
  width: 100%;
  height: 100%;
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

.image-path {
  font-size: 12px;
  color: #666;
  word-break: break-all;
  margin-bottom: 10px;
}

.assessment-wrapper {
  flex-grow: 1;
}

.form-inner {
  width: 100%;
  display: flex;
  align-items: center;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .image-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .image-grid {
    grid-template-columns: 1fr;
  }
}
</style>