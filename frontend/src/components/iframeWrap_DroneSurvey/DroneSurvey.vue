<template>
  <div class="drone-survey">
    <div class="section concept">
      <h2>Drone Survey Concept</h2>
      <img src="/imgs/droneSurvey/concept.jpg" alt="Drone Survey Concept" class="full-width-image" />
      <p v-html="conceptDescription"></p>
    </div>

    <div class="section inspection">
      <h2>Drone Inspection Process</h2>
      <img src="/imgs/droneSurvey/drone_inspection.jpg" alt="Drone Inspection" class="full-width-image" />
      <p v-html="inspectionDescription"></p>
    </div>

    <el-card class="section image-analysis">
      <template #header>
        <h2>Bridge Image Analysis</h2>
      </template>
      <el-row :gutter="20">
        <el-col :span="16">
          <div class="main-image">
            <img :src="'/imgs/droneSurvey/' + selectedImage.imageName" :alt="selectedImage.imageName" />
          </div>
        </el-col>
        <el-col :span="8">
          <div class="image-options">
            <div v-for="image in bridgeData" :key="image.id" class="thumbnail-container">
              <img :src="'/imgs/droneSurvey/' + image.imageName" @click="selectImage(image)"
                :class="{ 'selected': image.id === selectedImage.id }" />
            </div>
          </div>
        </el-col>
      </el-row>
      <div class="action-buttons">
        <el-button type="primary" @click="submitImage">Submit Image</el-button>
      </div>
    </el-card>

    <el-card v-if="showLocationDecoding" class="section location-decoding">
      <template #header>
        <h2>Location Mapping</h2>
      </template>
      <div class="result">
        <p><strong>Latitude:</strong> {{ selectedImage.coordinates.lat }}, <strong>Longitude:</strong> {{ selectedImage.coordinates.lng }} <strong>Height:</strong> {{ selectedImage.coordinates.height }}</p>
      </div>
      <el-button type="success" @click="decode">Decode Coordinates</el-button>
      <div v-if="show3DCoordinates" class="result">
        <p><strong>X:</strong> {{ selectedImage.coordinates3D.x }}, <strong>Y:</strong> {{ selectedImage.coordinates3D.y }}, <strong>Z:</strong> {{ selectedImage.coordinates3D.z }}</p>
      </div>
      <el-button v-if="show3DCoordinates" type="warning" @click="attachStructure">Attach to Structure</el-button>
      <div v-if="showStructure" class="result">
        <p><strong>Bridge Component:</strong> {{ selectedImage.bridgeComponent }}</p>
      </div>
    </el-card>

    <el-card class="section further-processing">
      <template #header>
        <h2>Further Processing</h2>
      </template>
      <div class="centered-buttons">
        <el-button type="primary" @click="goToImageProcessing">Image Processing</el-button>
        <el-button type="primary">Damage Analysis</el-button>
        <el-button type="primary">Generate Report</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElButton, ElCard, ElRow, ElCol } from 'element-plus'
import bridgeData from '@/api/droneSurvey.json'
import useAppStore from '@/store/modules/app'
import Bus from '@/utils/bus'

const router = useRouter()
const appStore = useAppStore()
const emit = defineEmits(['close-dialog'])

const conceptDescription = ref('Drone surveys revolutionize bridge inspections by providing a <strong>safe</strong>, <strong>efficient</strong>, and <strong>comprehensive</strong> method to assess structural integrity. Using <strong>advanced imaging technology</strong> and <strong>AI-powered analysis</strong>, drones capture <strong>high-resolution images</strong> and data, enabling engineers to identify potential issues with unprecedented <strong>accuracy</strong> and <strong>speed</strong>.')

const inspectionDescription = ref('During a drone inspection, the <strong>UAV systematically scans</strong> the bridge structure, capturing <strong>detailed images</strong> and <strong>3D data</strong>. This process allows for the detection of <strong>cracks</strong>, <strong>corrosion</strong>, and other structural anomalies that might be missed in traditional inspections. The collected data is then <strong>processed and analyzed</strong> to create a comprehensive report on the bridge\'s condition.')

const selectedImage = ref({})
const showLocationDecoding = ref(false)
const show3DCoordinates = ref(false)
const showStructure = ref(false)

onMounted(() => {
  if (bridgeData.length > 0) {
    selectedImage.value = bridgeData[0]
  }
})

function selectImage(image) {
  selectedImage.value = image
  showLocationDecoding.value = false
  show3DCoordinates.value = false
  showStructure.value = false
}

function submitImage() {
  showLocationDecoding.value = true
}

function decode() {
  show3DCoordinates.value = true
}

function attachStructure() {
  showStructure.value = true
}

const goToImageProcessing = () => {
    const imageData = {
        file: selectedImage.value.imageName,
        url: `/imgs/droneSurvey/${selectedImage.value.imageName}`
    }
    console.log(imageData)
    emit('close-dialog')
    router.push('/bridge-monitor')
    appStore.setMonitorType(3)
    setTimeout(() => {
        Bus.emit('monitor3PanelShow', imageData)
    }, 500)  
}
</script>

<style scoped>
.drone-survey {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.section {
  margin-bottom: 30px;
}

.full-width-image {
  width: 100%;
  height: auto;
  object-fit: cover;
  margin-bottom: 20px;
}

.main-image img {
  width: 100%;
  max-height: 400px;
  object-fit: cover;
}

.image-options {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.thumbnail-container {
  width: calc(50% - 5px);
  height: 100px;
  overflow: hidden;
}

.image-options img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.3s ease;
}

.image-options img.selected {
  border-color: #409EFF;
}

.action-buttons {
  margin-top: 20px;
  text-align: center;
}

.result {
  margin: 20px 0;
  padding: 10px;
  background-color: #f0f9ff;
  border-radius: 4px;
}

.centered-buttons {
  display: flex;
  justify-content: center;
  gap: 10px;
}

h2 {
  margin-bottom: 20px;
  color: #333;
}

p {
  line-height: 1.6;
  color: #666;
}

.el-button {
  margin-right: 10px;
}
</style>