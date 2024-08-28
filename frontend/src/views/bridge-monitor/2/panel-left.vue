<template>
  <div class="panel left">
    <div class="title">Sensor Abnormal Status Count</div>
    <div class="content">
      <div :id="`rose-chart-dom-${props.monitorType}`"
           style="height: 240px;"></div>
    </div>
    <div class="title">Temperature</div>
    <div class="content">
      <div :id="`l1-chart-dom-${props.monitorType}`"
           style="height: 240px;"></div>
    </div>
    <div class="title">Humidity</div>
    <div class="content">
      <div :id="`l2-chart-dom-${props.monitorType}`"
           style="height: 240px;"></div>
    </div>
  </div>
</template>

<script setup>
import * as echarts from 'echarts'
import useAppStore from '@/store/modules/app'
import d from './data/index'

const appStore = useAppStore()
const sensorId = computed(() => appStore.sensorId)
const props = defineProps({
  monitorType: {
    type: Number,
    default: 1
  }
})
watch(
  () => sensorId.value,
  (n) => {
    if (n !== '') {
      nextTick(() => {
        initRoseChart()
        initLineChart(1, `l1-chart-dom-${props.monitorType}`)
        initLineChart(2, `l2-chart-dom-${props.monitorType}`)
      })
    }
  })

// 传感器异常检测
let roseChart = null
function initRoseChart () {
  const chartDom = document.getElementById(`rose-chart-dom-${props.monitorType}`)
  if (!chartDom) return
  if (roseChart !== null && roseChart !== '' && roseChart !== undefined) {
    roseChart.dispose()
  }
  roseChart = echarts.init(chartDom)
  const option = {
    legend: {
      top: 'bottom'
    },
    grid: {
      left: '5%',
      right: '5%',
      bottom: '5%',
      top: '5%',
      containLabel: true
    },
    series: [
      {
        name: '',
        type: 'pie',
        radius: [20, 60],
        center: ['50%', '38%'],
        roseType: 'area',
        itemStyle: {
          borderRadius: 2
        },
        data: [
          { value: 40, name: 'Jan' },
          { value: 38, name: 'Feb' },
          { value: 32, name: 'Mar' },
          { value: 30, name: 'Apr' },
          { value: 28, name: 'May' },
          { value: 26, name: 'Jun' }
        ]
      }
    ]
  }
  option && roseChart.setOption(option)
}

// lineChart common
const dict = {
  1: {
    instance: null,
    timer: null
  },
  2: {
    instance: null,
    timer: null
  }
}
function initLineChart (num, id) {
  const chartDom = document.getElementById(id)
  if (!chartDom) return
  if (dict[num].instance !== null && dict[num].instance !== '' && dict[num].instance !== undefined) {
    dict[num].instance.dispose()
  }
  dict[num].instance = echarts.init(chartDom)
  const colors = ['#5470C6', '#EE6666', '#91cc75', '#fac858', '#73c0de', '#3ba272']
  const option = {
    color: [colors[num]],
    tooltip: {
      trigger: 'none',
      axisPointer: {
        type: 'cross'
      }
    },
    legend: {
      show: false
    },
    grid: {
      top: '2%',
      bottom: 50
    },
    xAxis: [
      {
        type: 'category',
        axisTick: {
          alignWithLabel: true
        },
        axisLine: {
          onZero: false
        },
        axisPointer: {
          label: {
            formatter: function (params) {
              return (
                'time  ' +
                params.value +
                (params.seriesData.length ? '：' + params.seriesData[0].data : '')
              )
            }
          }
        },
        // prettier-ignore
        data: num === 1 ? d.temperature[0] : d.humidity[0]
      }
    ],
    yAxis: [
      {
        type: 'value'
      }
    ],
    series: [
      {
        name: 'time',
        type: 'line',
        // smooth: true,
        emphasis: {
          focus: 'series'
        },
        data: num === 1 ? d.temperature[1] : d.humidity[1]
      }
    ]
  }
  dict[num].instance.setOption(option)
}
// function updateChart (num) {
//   const
// }

onMounted(() => { })
onBeforeUnmount(() => { })
</script>

<style lang='scss'
       scoped>
      .content {
        margin-bottom: 20px;
      }
    </style>
