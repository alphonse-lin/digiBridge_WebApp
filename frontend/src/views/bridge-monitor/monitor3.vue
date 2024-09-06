<template>
  <div class="monitor-com-wrap">
    <transition name="el-fade-in-linear">
      <div class="panel left">
        <div class="title">Bridge Components</div>
        <ComTree @node-click="onNodeClick"></ComTree>
      </div>
    </transition>

    <transition name="el-fade-in-linear">
      <div v-show="stepPanelShow" v-loading="loading" class="main-wrap">
        <div class="head">
          <div class="title">Bridge Component Detection</div>
          <div class="close" @click="onClose">
            <el-icon>
              <Close />
            </el-icon>
          </div>
        </div>
        <div class="main">
          <el-steps style="width: 100%;" :active="activeStep" finish-status="success" simple>
            <el-step title="Inspection Form" :icon="SuccessFilled" />
            <!-- <el-step title="Data Selection" :icon="SuccessFilled" /> -->
            <el-step title="Data Quantification" :icon="SuccessFilled" />
            <!-- <el-step title="Report Generation" /> -->
          </el-steps>
          <div class="step-content">
            <Step1Com v-model:questionType="questionType" v-show="activeStep === 0" ref="refStep1"
              :stepPanelShow="stepPanelShow" :activeStep="activeStep" />
            <!-- <Step2Com v-show="activeStep === 1" ref="refStep2" :activeStep="activeStep" :questionType="questionType"
              :result="result" /> -->
            <Step3Com v-show="activeStep === 1" :activeStep="activeStep" :questionType="questionType" :result="result"
              :segmentedImageData="selectedImages" />
          </div>
        </div>
        <div class="footer">
          <div>
            <el-button v-show="activeStep !== 0" type="primary" @click="onPrev">back</el-button>
          </div>
          <div>
            <el-button v-show="activeStep === 0" type="primary" @click="onNext">Data Submit</el-button>
            <el-button v-show="activeStep === 1" type="primary" :icon="Document" @click="onSubmit">Save
              result</el-button>
            <!-- <el-button v-show="activeStep === 2" type="primary" :icon="Document" @click="onSubmit">Save -->
          </div>
        </div>
      </div>
    </transition>

    <Step1Com v-model:questionType="questionType" v-show="activeStep === 0" ref="refStep1"
      :stepPanelShow="stepPanelShow" :activeStep="activeStep" @segmentedImageUpdated="handleSegmentedImageUpdate" />

    <Step3Com v-show="activeStep === 1" :activeStep="activeStep" :questionType="questionType" :result="result"
      :segmentedImageData="segmentedImageData" />
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import ComTree from './5/com-tree.vue'
import Step1Com from './3/step1.vue'
// import Step2Com from './3/step2.vue'
import Step3Com from './3/step3.vue'
import { Close, Document } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import Bus from '@/utils/bus'
import { bridges } from '@/api'
import { segmentImage, quantifyImages } from '@/api/bridge'
import { SuccessFilled } from '@element-plus/icons-vue'

const refStep2 = ref(null)
const selectedImages = ref([])
const segmentedImageData = ref(null)

// const props = defineProps()
const stepPanelShow = ref(false)
const questionType = ref('Corrosion') // 腐蚀/裂缝
function onNodeClick({ node }) {
  questionType.value = node.index % 2 === 0 ? 'Corrosion' : 'Crack'
  stepPanelShow.value = true
  activeStep.value = 0
}
function onClose() {
  stepPanelShow.value = false
}

const activeStep = ref(0)
const refStep1 = ref(null)
const loading = ref(false)
// 上传图片
function uploadImage() {
  return new Promise((resolve, reject) => {
    const imgs = refStep1.value.getImgs()
    const formData = new FormData()
    imgs.forEach(img => {
      formData.append('file', img)
    })

    fetch('/upload_image', {
      method: 'POST',
      body: formData
    })
      .then(response => {
        if (response.ok) {
          console.log('图片上传成功')
          resolve()
        } else {
          //修改
          console.error('图片上传失败')
          resolve()
        }
      })
      .catch(error => {
        reject(error)
      })
  })
}
const result = ref(null)
// 获取检测结果
function getResult() {
  return new Promise((resolve, reject) => {
    fetch('/process')
      .then(res => {
        if (res.ok) {
          console.log('获取检测结果成功')
          // mock data
          result.value = {
            image_url: '',
            segmented_image_url: '',
            file_path: ''
          }
          // result.value = res.result_data
          resolve()
        } else {
          console.error('获取检测结果失败')
        }
      })
      .catch(error => {
        reject(error)
      })
  })
}

async function onNext() {
  console.log('Received segmented image data in monitor3:', segmentedImageData)
  if (activeStep.value === 0) {
    const validateResult = await refStep1.value.validateForm()
    if (!validateResult) return
    await uploadImage()
    await getResult()
  } else if (activeStep.value === 1) {
    // 可以在这里添加 Step2 的任何验证逻辑
    selectedImages.value = refStep2.value.getSelectedImages()
    console.log('selectedImages', selectedImages.value)
  }

  if (activeStep.value < 2) {  // 修改这里，允许从 Step2 跳转到 Step3
    activeStep.value++
  }
}
function onPrev() {
  if (activeStep.value > 0) {
    activeStep.value--
  }
}

function onSubmit() {
  stepPanelShow.value = false
  ElMessage.success('Saved successfully!')
  Bus.emit('showKBasedMaintenance', { showScenario: 2 })
}

function handleSegmentedImageUpdate(imageData) {
  console.log('Received segmented image data in monitor3:', imageData)
  segmentedImageData.value = imageData
}

onMounted(() => {
  // 监听点击模型事件，点击模型时，弹出面板
  // 左侧腐蚀，右侧裂缝
  Bus.on('model-click', ({ id, p }) => {
    const bridge = bridges.find(b => b.id === Number(id))
    // console.log('model-click', bridge.position[0], p[0])
    questionType.value = bridge.position[0] > p[0] ? 'Corrosion' : 'Crack'
    stepPanelShow.value = true
    activeStep.value = 0
  })
  Bus.on('monitor3PanelShow', (imageData) => {
    console.log('Received imageData:', imageData) // 添加这行来调试
    stepPanelShow.value = true
    activeStep.value = 0

    if (imageData && refStep1.value) {
      refStep1.value.setImage(imageData)
    } else {
      console.error('imageData or refStep1 is undefined', { imageData, refStep1: refStep1.value })
    }
  })
})
onBeforeUnmount(() => { Bus.off('monitor3PanelShow') })
</script>

<style lang='scss' scoped>
.monitor-com-wrap {

  .panel {
    transition: all 0.3s;
    width: 300px;
    max-height: calc(100vh - 100px);
    background-color: var(--el-bg-color);
    border-radius: 4px;
    padding: 14px;
    box-shadow: var(--el-box-shadow);

    position: fixed;
    right: 20px;
    top: 80px;
    z-index: 100;

    &.left {
      right: unset;
      left: 20px;
      height: calc(100vh - 200px);
      display: flex;
      flex-direction: column;
    }
  }

  .main-wrap {
    width: 1200px;
    height: 70vh;
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 100;
    overflow-y: auto;
    background-color: var(--el-bg-color);
    box-shadow: var(--el-box-shadow);
    border-radius: 4px;
    padding: 20px;

    display: flex;
    flex-direction: column;

    .head {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;

      .title {
        font-size: 20px;
      }

      .close {
        cursor: pointer;
      }
    }

    .main {
      flex: 1;
      height: 0;
      overflow-y: auto;

      display: flex;
      flex-direction: column;

      .step-content {
        margin-top: 10px;
        margin-bottom: 10px;
        flex: 1;
        height: 0;
        overflow-y: auto;
      }
    }

    .footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
  }
}
</style>
