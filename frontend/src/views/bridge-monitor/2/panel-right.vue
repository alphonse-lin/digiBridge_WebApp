<template>
  <div class="panel right">
    <div class="more-icon">
      <el-button type="primary"
                 link
                 @click="showMore">Sensor Management
        <svg-icon icon-class="share-circle-fill"
                  style="margin-left: 10px;"></svg-icon></el-button>
    </div>
    <div class="title">Acceleration</div>
    <div class="content">
      <div :id="`l4-chart-dom-${props.monitorType}`"
           style="height: 240px;"></div>
    </div>
    <div class="title">Amplitude</div>
    <div class="content">
      <div :id="`l5-chart-dom-${props.monitorType}`"
           style="height: 240px;"></div>
    </div>
    <div class="title">Displacement</div>
    <div class="content">
      <div :id="`l6-chart-dom-${props.monitorType}`"
           style="height: 240px;"></div>
    </div>
  </div>
</template>

<script setup>
import * as echarts from 'echarts'
import useAppStore from '@/store/modules/app'
import acceleration from './data/acceleration.js'
import amplitude from './data/amplitude.js'
import displacement from './data/displacement.js'
import ffreqs from './data/ffreqs.js'
import d from './data/index'
import { max, min } from 'lodash-es'

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
      clearTimeout(timer)
      nextTick(() => {
        const n = Math.floor(Math.random() * 5) + 1
        console.log('%c n: ', 'background-color: pink', n)
        initLineChart(4, `l4-chart-dom-${props.monitorType}`, n)
        initLineChart_2(5, `l5-chart-dom-${props.monitorType}`, n)
        initLineChart(6, `l6-chart-dom-${props.monitorType}`, n)
        
        setTimeout(() => {
          dict_update[4].update()
          dict_update[5].update()
          dict_update[6].update()
          // updateChart()
        }, 1000)
      })
    }
  })

const emits = defineEmits(['show-more'])
function showMore () {
  emits('show-more')
}

const dict_update = {
  4: { chart: null, update: updateChart },
  5: { chart: null, update: updateChart_2 },
  6: { chart: null, update: updateChart },
};

const dict = {
  4: null,
  5: null,
  6: null
}
function initLineChart (num, id, index) {
  const chartDom = document.getElementById(id)
  if (!chartDom) return
  if (dict[num] !== null && dict[num] !== '' && dict[num] !== undefined) {
    dict[num].dispose()
  }
  dict[num] = echarts.init(chartDom)
  const colors = ['#5470C6', '#EE6666', '#91cc75', '#fac858', '#73c0de', '#3ba272', '#5470C6']
  const option = {
    color: [colors[num]],
    animation: false,
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
        data: d.x
      }
    ],
    yAxis: [
      {
        type: 'value'
        // min: Math.min(...d[n]),
        // max: Math.max(...d[n])
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
        data: num === 4 ? acceleration[index] : num === 5 ? amplitude[index] : displacement[index]
      }
    ]
  }
  dict[num].setOption(option)
}

//TODO: Gai
function initLineChart_2 (num, id, index) {
  const chartDom = document.getElementById(id)
  const ffreqsData = ffreqs[index];
  if (!chartDom) return
  if (dict[num] !== null && dict[num] !== '' && dict[num] !== undefined) {
    dict[num].dispose()
  }
  dict[num] = echarts.init(chartDom)
  const colors = ['#5470C6', '#EE6666', '#91cc75', '#fac858', '#73c0de', '#3ba272', '#5470C6']
  const option = {
    color: [colors[num]],
    animation: false,
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
    xAxis: {
      type: 'category',
      data: ffreqsData,
      axisLabel: {
        formatter: '{value} Hz'
      },
      axisTick: {
        alignWithLabel: true
      },
      axisLine: {
        onZero: false
      }
    },
    yAxis: [
      {
        type: 'value',
      }
    ],
    series: [
      {
        name: 'amplitude',
        type: 'line',
        emphasis: {
          focus: 'series'
        },
        data: amplitude[index]
      }
    ]
  };

  dict[num].setOption(option);
}

let timer = null
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

function updateChart () {
  // 使用getOption和setOption更新随机数据
  // const keys = Object.keys(dict)
  const keys= [4,6]
  const len = 1 // 每次20个数据
  const speed = 30 // 1s更新一次
  keys.forEach((k) => {
    const xData = dict[k].getOption().xAxis[0].data
    const yData = dict[k].getOption().series[0].data
    const xd = xData.slice(len)
    const yd = yData.slice(len)
    xd.push(xDataCom(xData.pop()))
    yd.push(...yData.slice(0, len))
    dict[k].setOption({
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

//TODO: Gai
function updateChart_2() {
  // 使用getOption和setOption更新随机数据
  //const keys = [Object.keys(dict)];
  const keys = [5];
  const len = 1; // 每次添加1个数据
  const speed = 30; // 1s更新一次

  keys.forEach((k) => {
    const xData = dict[k].getOption().xAxis[0].data;
    const yData = dict[k].getOption().series[0].data;
    // const xd = xData.slice(len)
    const yd = yData.slice(len)
    // xd.push(...xData.slice(0, len));
    yd.push(...yData.slice(0, len));
    dict[k].setOption({
      // xAxis: {
      //   data: xd
      // },
      series: [
        {
          data: yd
        }
      ]
    })
  })
  timer = setTimeout(() => {
    updateChart_2()
  }, speed)
}

onMounted(() => { })
onBeforeUnmount(() => { })
</script>

<style lang='scss' scoped>
.more-icon {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  color: var(--el-color-primary);
}
</style>
