<template>
  <div class="monitor-com-wrap">
    <transition name="el-fade-in-linear">
      <div v-show="sensorId === ''"
           class="panel left">
        <div class="title">Equipment Detection</div>
        <div class="content jcfw">
          <el-row :gutter="20">
            <el-col v-for="v in objList"
                    :key="v.label"
                    :span="8"
                    :offset="0">
              <div class="item">
                <div class="icon-wrap">
                  <svg-icon style="margin-right: 10px;color: #989898"
                            :icon-class="v.icon" />
                  <div class="value"
                       :style="{ color: v.color ? v.color : '' }">{{ v.value }} {{ v.unit }}</div>
                </div>
                <div class="label">{{ v.label }}</div>
              </div>
            </el-col>
          </el-row>
        </div>
        <div class="title">Air Quality</div>
        <div class="content"
             style="margin-bottom: 20px;">
          <div :id="`pop-chart-dom-${props.monitorType}`"
               style="height: 260px;"></div>
        </div>
        <div class="title">Indicator Overall Score</div>
        <div class="content sbwhd">
          <div v-for="o in goodList"
               :key="o.label">
            <div class="label">{{ o.label }}</div>
            <div class="value">
              <div
                   :style="{ width: `${o.value}%`, backgroundColor: o.value > o.warn ? 'var(--el-color-warning)' : 'var(--el-color-success)' }">
                {{ o.value }}</div>
            </div>
          </div>
        </div>
      </div>
    </transition>
    <transition name="el-fade-in-linear">
      <div v-show="sensorId === ''"
           class="panel right">
        <div class="clock">{{ clockContent }}</div>
        <div class="title">Safety Indicators</div>
        <div class="content aqzs">
          <el-table :data="tableData"
                    border
                    stripe>
            <el-table-column prop="name"
                             label="Indicator"></el-table-column>
            <el-table-column prop="value"
                             label="Value"></el-table-column>
          </el-table>

        </div>
        <div class="title">Vehicle Type Count</div>
        <div class="content cxtj">
          <div :id="`pie-chart-dom-${props.monitorType}`"
               class="chart"
               style="height: 120px;"></div>
          <div class="num">
            <div>large <span>{{ carlist[0] }}</span> units</div>
            <div>medium <span>{{ carlist[1] }}</span> units</div>
            <div>small <span>{{ carlist[2] }}</span> units</div>
          </div>
        </div>
        <div class="title">Bridge Management</div>
        <div class="content qlgl">
          <div :id="`single-chart-dom-${props.monitorType}`"
               style="height: 200px;"></div>
        </div>
      </div>
    </transition>

    <transition name="el-fade-in-linear">
      <panelLeft v-show="sensorId !== ''"
                 :monitorType="monitorType"></panelLeft>
    </transition>
    <transition name="el-fade-in-linear">
      <panelRight v-show="sensorId !== ''"
                  :monitorType="monitorType"
                  @show-more="onShowMore"></panelRight>
    </transition>
    <!-- MoreDetail -->
    <transition name="el-fade-in-linear">
      <MoreDetail v-show="showMore"
                  :showMore="showMore"
                  @close="onShowMore"></MoreDetail>
    </transition>
  </div>
</template>

<script setup>
// import { randomColor } from '@/utils'
import * as echarts from 'echarts'
import { popChartOption, singleChartOption } from './2'
import panelLeft from './2/panel-left.vue'
import panelRight from './2/panel-right.vue'
import MoreDetail from './2/more-detail.vue'
import useAppStore from '@/store/modules/app'

const appStore = useAppStore()
const sensorId = computed(() => appStore.sensorId)

const props = defineProps({
  monitorType: {
    type: Number,
    default: 1
  }
})

const showMore = ref(false)
function onShowMore () {
  showMore.value = !showMore.value
}

// 检测设备
const objList = ref([
  { label: 'Monitoring', icon: 'home-wifi-fill', value: 66 },
  { label: 'Abnormal', icon: 'error-warning-fill', value: 43, color: 'var(--el-color-warning)' },
  { label: 'Coverage rate', icon: 'percent-line', value: 44 },
  { label: 'Found', icon: 'search-line', value: 32, color: 'var(--el-color-danger)' },
  { label: 'Finished', icon: 'tools-fill', value: 30, color: 'var(--el-color-success)' },
  { label: 'Average', icon: 'time-line', value: 6, unit: 'min' }
])

// 空气检测
function initPopChart () {
  const chartDom = document.getElementById(`pop-chart-dom-${props.monitorType}`)
  if (!chartDom) return
  const myChart = echarts.init(chartDom)
  const option = popChartOption
  option && myChart.setOption(option)
}

// 设备完好度排行
const goodList = ref([
  { label: 'Temperature & Humidity', value: 66, warn: 50 },
  { label: 'Inclination', value: 43, warn: 50 },
  { label: 'Wind Speed & Direction', value: 44, warn: 50 },
  { label: 'Deflection', value: 32, warn: 50 },
  { label: 'Prestressing Force', value: 30, warn: 50 },
  { label: 'GNSS', value: 55, warn: 50 },
  { label: 'Crack', value: 43, warn: 50 },
  { label: 'Vibration', value: 54, warn: 50 },
  { label: 'Video', value: 44, warn: 50 }
])

// 时钟
const clockContent = ref('')
function displayTime () {
  const now = new Date()
  const hours = now.getHours()
  const minutes = now.getMinutes()
  const seconds = now.getSeconds()
  const s = seconds < 10 ? '0' + seconds : seconds
  const timeString = hours + ' : ' + minutes + ' : ' + s
  clockContent.value = timeString
}
setInterval(() => {
  displayTime()
}, 1000) // 每秒钟更新一次时间

// 安全指数
const tableData = ref([])
tableData.value = [
  { id: 1, name: 'Inclination', value: '2.23°' },
  { id: 2, name: 'Handling Rate', value: '99.23%' },
  { id: 3, name: 'Deflection', value: '99.23%' },
  { id: 4, name: 'Coverage Rate', value: '99.23%' },
  { id: 5, name: 'Inclination', value: '2.23°' },
  { id: 6, name: 'Handling Rate', value: '99.23%' }
]

// 车型统计
const carlist = ref([40, 38, 32])
function randomCar () {
  carlist.value = carlist.value.map(() => Math.floor(Math.random() * 100))
}
setInterval(() => {
  randomCar()
  nextTick(() => {
    initPieChart()
  })
}, 2000)
function initPieChart () {
  const chartDom = document.getElementById(`pie-chart-dom-${props.monitorType}`)
  if (!chartDom) return
  const myChart = echarts.init(chartDom)
  const option = {
    series: [
      {
        type: 'pie',
        radius: [10, 50],
        center: ['50%', '50%'],
        roseType: 'area',
        itemStyle: {
          borderRadius: 2
        },
        label: {
          show: false
        },
        data: carlist.value.map((v, i) => {
          return {
            value: v,
            name: ['Large', 'Medium', 'Small'][i]
          }
        })
      }
    ]
  }
  option && myChart.setOption(option)
}

// 桥梁管理
function initSingleChart () {
  const chartDom = document.getElementById(`single-chart-dom-${props.monitorType}`)
  if (!chartDom) return
  const myChart = echarts.init(chartDom)
  const option = singleChartOption
  option && myChart.setOption(option)
}

onMounted(() => {
  initPopChart()
  initPieChart()
  initSingleChart()
})
onBeforeUnmount(() => {
  clearInterval(displayTime)
})
</script>

<style lang='scss'
       scoped>

      .panel {
        transition: all 0.3s;
        width: 300px;
        min-height: 800px;
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
          left: 20px;
        }

        &.right {
          .clock {
            font-size: 40px;
            font-weight: 600;
            flex: 1;
            text-align: center;
            color: var(--el-color-primary);
            margin: 20px 0;
          }
        }

        .content {
          margin-bottom: 20px;

          // 空气检测
          &.jcfw {
            .item {
              margin-bottom: 20px;
              width: 100%;

              .icon-wrap {
                display: flex;
                align-items: center;
                margin-bottom: 10px;
                width: 100%;

                .value {
                  flex: 1;
                  font-size: 18px;
                  font-weight: 600;
                  text-align: center;
                }
              }

              .label {
                // text-align: center;
                font-size: 12px;
                font-weight: bold;
              }
            }
          }

          // 设备完好度排行
          &.sbwhd {

            >div {
              display: flex;
              align-items: center;
              margin-bottom: 14px;
              text-align: center;

              .value {
                flex: 1;
                margin-left: 10px;
                border-radius: 4px;
                background-color: rgba(0, 0, 0, 0.1);

                >div {
                  height: 20px;
                  line-height: 20px;
                  color: #fff;
                  font-size: 12px;
                  text-align: center;
                }
              }
            }
          }

          &.cxtj {
            display: flex;
            align-items: stretch;

            .chart {
              flex: 1;
            }

            .num {
              flex: 1;
              margin-left: 10px;
              display: flex;
              flex-direction: column;
              justify-content: space-around;
              align-items: center;

              >div {
                font-size: 14px;

                >span {
                  font-weight: bold;
                  color: var(--el-color-primary);
                  margin: 0 5px;
                }
              }
            }
          }
        }
      }
    </style>
