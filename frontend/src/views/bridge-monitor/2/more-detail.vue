<template>
  <div class="more-detail">
    <div class="head">
      <div class="title">Sensor management</div>
      <div class="close"
           @click="onClose">
        <el-icon>
          <Close />
        </el-icon>
      </div>
    </div>
    <div class="main">
      <div class="query-wrap">
        <div>
          <el-date-picker v-model="form.date"
                          type="date"
                          placeholder="Pick a day"
                          :clearable="false"
                          style="width: 200px" />
        </div>
        <div>
          <el-select v-model="form.bridge"
                     placeholder="Select a bridge"
                     style="width: 200px"
                     clearable>
            <el-option v-for="item in options.bridge"
                       :key="item.value"
                       :label="item.label"
                       :value="item.value" />
          </el-select>
        </div>
        <div>
          <el-select v-model="form.sensor"
                     placeholder="Select a sensor"
                     style="width: 200px"
                     clearable>
            <el-option v-for="item in options.sensor"
                       :key="item.value"
                       :label="item.label"
                       :value="item.value" />
          </el-select>
        </div>
        <div>
          <el-button type="primary"
                     :icon="Search"
                     @click="onSearch">Search</el-button>
        </div>
      </div>

      <div class="status-cards">
        <el-row :gutter="20">
          <el-col :span="6"
                  v-for="card in cards"
                  :key="card.title">
            <div class="card"
                 :style="{
                  backgroundColor: `rgba(${card.color}, 0.3)`,
                  color: `rgba(${card.color})`,
                  borderColor: `rgba(${card.color})`
                }">
              <div>{{ card.title }}</div>
              <div style="font-size: 24px;margin-top: 10px;">{{ card.value }}<span> {{ card.unit }}</span></div>
              <svg-icon :icon-class="card.icon"
                        :style="{ color: `rgba(${card.color})`, fontSize: '40px', position: 'absolute', right: '30px', bottom: '28px' }" />
            </div>
          </el-col>
        </el-row>
      </div>

      <!-- sensors charts -->
      <div class="charts">
        <el-row :gutter="20">
          <el-col v-for="v in options.sensor"
                  :key="v.value"
                  :span="12"
                  :offset="0">
            <div class="chart-wrap">
              <div class="title">{{ v.label }}</div>
              <div :id="`sensor-chart-${v.value}`"
                   class="chart"
                   style="height: 280px;"></div>
            </div>
          </el-col>
        </el-row>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Close, Search } from '@element-plus/icons-vue'
import * as echarts from 'echarts'
import { sensorChartOption } from './index'
import acceleration from './data/acceleration.js'
import d from './data/index'

const props = defineProps({
  showMore: {
    type: Boolean,
    default: false
  }
})
//TODO: Gai
watch(() => props.showMore, (n) => {
  if (n) {
    nextTick(() => {
      clearTimeout(timer)
      const n = Math.floor(Math.random() * 6) + 1
      initLineChart(1, 'sensor-chart-1', 1)
      initLineChart(2, 'sensor-chart-2', 2)
      initLineChart(3, 'sensor-chart-3', 3)
      initLineChart(4, 'sensor-chart-4', 5)

      setTimeout(() => {
        updateChart()
      }, 1000)
    })
  }
})

const emits = defineEmits(['close'])
function onClose () {
  emits('close')
}

const form = reactive({
  date: new Date(),
  bridge: '',
  sensor: ''
})
const options = {
  bridge: [
    { value: '1', label: 'River Neath Swing Bridge' },
    { value: '2', label: 'Kidwelly Viaduct' },
    { value: '3', label: 'Changeshan Bridge' },
    { value: '4', label: 'Central Station' }
  ],
  sensor: [
    { value: '1', label: 'Sensor 1' },
    { value: '2', label: 'Sensor 2' },
    { value: '3', label: 'Sensor 3' },
    { value: '4', label: 'Sensor 4' }
  ]
}
function onSearch () {
  console.log(form)
}

// banner
const cards = ref([
  { title: 'Count', value: '400', unit: '', color: 'var(--el-color-success-rgb)', icon: 'function-fill' },
  { title: 'Average Value', value: '100', unit: '', color: 'var(--el-color-success-rgb)', icon: 'pulse-fill' },
  { title: 'Peak Value', value: '200', unit: '', color: 'var(--el-color-warning-rgb)', icon: 'bar-chart-fill' },
  { title: 'Abnormal Count', value: '2', unit: '', color: 'var(--el-color-danger-rgb)', icon: 'error-warning-fill' }
])

// charts
const dict = {
  1: { instance: null, dataObj: acceleration},
  2: { instance: null, dataObj: acceleration},
  3: { instance: null, dataObj: acceleration},
  4: { instance: null, dataObj: acceleration}
}
function initLineChart (num, id, index) {
  const chartDom = document.getElementById(id)
  if (!chartDom) return
  if (dict[num].instance !== null && dict[num].instance !== '' && dict[num].instance !== undefined) {
    dict[num].instance.dispose()
  }
  dict[num].instance = echarts.init(chartDom)
  const option = sensorChartOption(d.x, dict[num].dataObj[index])
  dict[num].instance.setOption(option)
}
function xDataCom (str) {
  let m = str.split(':')[0]
  let s = str.split(':')[1]
  if (s.startsWith('0')) {
    s = Number(s.substring(1)) + 1
  } else {
    if (s === '59') {
      s = '00'
      m = Number(m) + 1
    } else {
      s = Number(s) + 1
    }
  }
  return `${m}:${s}`
}
let timer = null
function updateChart () {
  // 使用getOption和setOption更新随机数据
  const keys = Object.keys(dict)
  const len = 1 // 每次20个数据
  const speed = 30 // 1s更新一次
  keys.forEach((k) => {
    const xData = dict[k].instance.getOption().xAxis[0].data
    const yData = dict[k].instance.getOption().series[0].data
    const xd = xData.slice(len)
    const yd = yData.slice(len)
    xd.push(xDataCom(xData.pop()))
    yd.push(...yData.slice(0, len))
    dict[k].instance.setOption({
      xAxis: {
        data: xd
      },
      series: [
        {
          data: yd
        }
      ]
    })
  })
  timer = setTimeout(() => {
    updateChart()
  }, speed)
}

onMounted(() => { })
onBeforeUnmount(() => { })
</script>

<style lang='scss' scoped>
.more-detail {
  width: 1200px;
  height: 70vh;
  position: fixed;
  top: 50%;
  left: 50%;
  z-index: 110;
  transform: translate(-50%, -50%);
  background-color: var(--el-bg-color);
  padding: 20px;
  box-shadow: var(--el-box-shadow-dark);
  border-radius: 4px;
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
    width: 100%;
    overflow-y: auto;
    overflow-x: hidden;

    .status-cards {
      width: 100%;
      margin-bottom: 20px;

      .card {
        box-sizing: border-box;
        padding: 20px 30px;
        border-radius: 4px;
        border-left: 8px solid #ccc;
        font-weight: bold;
        position: relative;
      }
    }

    .charts {
      .chart-wrap {
        width: 100%;
        border-radius: 4px;
        margin-bottom: 20px;

        .title {
          font-size: 20px;
          margin-bottom: 10px;
        }

        // .chart {
        //   background-color: pink;
        // }
      }
    }
  }
}
</style>
