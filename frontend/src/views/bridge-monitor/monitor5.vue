<template>
  <div class="monitor-com-wrap">
    <transition name="el-fade-in-linear">
      <div class="panel left">
        <div class="title">Bridge Components</div>
        <div v-if="warnShow"
             class="warning-area"
             style="margin-bottom: 20px;cursor: pointer;"
             @click="showTable">
          <el-icon class="icon">
            <WarningFilled />
          </el-icon>
          <div>Some information has been updated!</div>
        </div>
        <div v-else
             class="success-area"
             style="margin-bottom: 20px;cursor: pointer;"
             @click="showTable">
          <el-icon class="icon">
            <SuccessFilled />
          </el-icon>
          <div>No need to update!</div>
        </div>
        <ComTree :warnShow="warnShow"
                 @node-click="onNodeClick"></ComTree>
      </div>
    </transition>

    <transition name="el-fade-in-linear">
      <div v-show="Object.keys(activeNode).length"
           class="panel right">
        <div class="title">
          <div>Component Detail</div>
          <div style="flex: 1;text-align: right;cursor: pointer;"
               @click="onClose">
            <svg-icon icon-class="close-fill"
                      style="font-size: 22px;color: var(--el-color-info)" />
          </div>
        </div>
        <div>
          <el-table :data="nodeData"
                    border
                    stripe>
            <el-table-column prop="key"
                             label="attr">
            </el-table-column>
            <el-table-column prop="value"
                             label="value">
            </el-table-column>
          </el-table>
        </div>
        <div v-if="activeNode.isUpdate === 'Corrosion'"
             class="detection-wrap">
          <div class="title">Detection Result</div>
          <div class="img-wrap">
            <img :src="corrosion2"
                 alt="corrosion2"
                 class="img">
            <img :src="corrosion3"
                 alt="corrosion3"
                 class="img">
          </div>
          <div class="result">
            <div>Good percentage: <span style="color: var(--el-color-warning)">31.19%</span></div>
            <div>Mild corrosion percentage: <span>35.1%</span></div>
            <div>Severe corrosion percentage: <span>33%</span></div>
            <div>Total corrosion percentage: <span style="color: var(--el-color-warning)">68.8%</span></div>
          </div>
        </div>
        <div v-if="activeNode.isUpdate === 'Crack'"
             class="detection-wrap">
          <div class="title">Detection Result</div>
          <div class="img-wrap">
            <img :src="crack2"
                 alt="crack2"
                 class="img">
            <img :src="crack3"
                 alt="crack3"
                 class="img">
          </div>
          <div class="result">
            <div>Crack number: <span style="color: var(--el-color-warning)">3</span></div>
            <div>Crack length: <span>2.58m</span></div>
            <div>Crack depth: <span>3.5 cm</span></div>
          </div>
        </div>
      </div>
    </transition>

    <!-- 中间面板 -->
    <transition name="el-fade-in-linear">
      <div v-show="stepPanelShow"
           class="main-wrap">
        <div class="head">
          <div class="title">Inspection Result Collections</div>
          <div class="close"
               @click="onCloseCenter">
            <el-icon>
              <Close />
            </el-icon>
          </div>
        </div>
        <div class="main">
          <el-steps style="width: 100%;"
                    :active="activeStep"
                    finish-status="success"
                    simple>
            <el-step title="Inspection Result" />
            <el-step title="Components Relations" />
            <el-step title="Report Params" />
            <el-step title="Report Preview" />
          </el-steps>
          <div class="step-content">
            <Step1Com v-show="activeStep === 0"></Step1Com>
            <Step2Com v-show="activeStep === 1"
                      :activeStep="activeStep"></Step2Com>
            <Step3Com v-show="activeStep === 2"
                      :activeStep="activeStep"></Step3Com>
            <Step4Com v-show="activeStep === 3"
                      :activeStep="activeStep"></Step4Com>
          </div>
        </div>
        <div class="footer">
          <div>
            <el-button v-show="activeStep !== 0"
                       type="primary"
                       @click="onPrev">Back</el-button>
          </div>
          <div>
            <el-button v-show="activeStep === 0"
                       type="primary"
                       @click="onNext">Update</el-button>
            <el-button v-show="activeStep === 1"
                       type="primary"
                       @click="onNext">Next</el-button>
            <el-button v-show="activeStep === 2"
                       type="primary"
                       :activeStep="activeStep"
                       @click="onNext">Generate Report</el-button>
            <el-button v-show="activeStep === 3"
                       type="primary"
                       @click="onDownload">Download Report</el-button>
            <el-button v-show="activeStep === 3"
                       type="primary"
                       @click="onSubmit">Save</el-button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { WarningFilled, SuccessFilled, Close } from '@element-plus/icons-vue'
import ComTree from './5/com-tree.vue'
import { ElMessage } from 'element-plus'
import Step1Com from './5/step1.vue'
import Step2Com from './5/step2.vue'
import Step3Com from './5/step3.vue'
import Step4Com from './5/step4.vue'
import corrosion2 from '@/assets/detection/corrosion2.png'
import corrosion3 from '@/assets/detection/corrosion3.png'
import crack2 from '@/assets/detection/crack2.png'
import crack3 from '@/assets/detection/crack3.png'
import pdfUrl from '@/components/pdf-preview/detection-result.pdf'

// const props = defineProps()
const warnShow = ref(true)

const activeNode = ref({})
const nodeData = ref([])
function onNodeClick ({ node }) {
  activeNode.value = node
  nodeData.value = Object.keys(node).map(v => {
    return { key: v, value: node[v] }
  })
}
function onClose () {
  activeNode.value = {}
  nodeData.value = []
}

const stepPanelShow = ref(false)
function showTable () {
  stepPanelShow.value = true
  activeStep.value = 0
}
function onCloseCenter () {
  stepPanelShow.value = false
}

const activeStep = ref(0)
function onNext () {
  if (activeStep.value < 4) {
    activeStep.value++
  }
}
function onPrev () {
  if (activeStep.value > 0) {
    activeStep.value--
  }
}

function downloadURL (url, name) {
  const link = document.createElement('a')
  link.download = name
  link.href = url
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}
function onDownload () {
  downloadURL(pdfUrl, 'detection-result.pdf')
}
function onSubmit () {
  stepPanelShow.value = false
  ElMessage.success('Saved successfully!')
}
onMounted(() => { })
onBeforeUnmount(() => { })
</script>

<style lang='scss' scoped>
.monitor-com-wrap {

  .panel {
    transition: all 0.3s;
    width: 300px;
    max-height: calc(100vh - 100px);
    overflow-y: auto;
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

    &.right {
      .detection-wrap {
        margin-top: 20px;

        .img-wrap {
          height: 150px;
          display: flex;
          align-items: center;
          background-color: #fafafa;
          padding: 10px;
          border: 1px solid var(--el-border-color);
          border-radius: 4px;

          >.img {
            flex: 1;
            height: 100%;
            object-fit: contain;
          }
        }

        .result {
          margin-top: 20px;

          >div {
            line-height: 32px;

            span {
              font-weight: bold;
              color: var(--el-color-success);
            }
          }
        }
      }
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
        margin: 10px 0;
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
