<template>
  <div class="step-wrap">
    <div id="chartData-chart"
         style="height: 100%;"></div>
  </div>
</template>

<script setup>
import * as echarts from 'echarts'
import chartData from './chartData.json'

const props = defineProps({
  activeStep: {
    type: Number,
    default: 0
  }
})
watch(() => props.activeStep, () => {
  if (props.activeStep === 1) {
    setTimeout(() => {
      initGraphChart()
    }, 100)
  }
})

let chart = null
function initGraphChart () {
  const chartDom = document.getElementById('chartData-chart')
  if (!chartDom) return
  if (chart !== null && chart !== '' && chart !== undefined) {
    chart.dispose()
  }
  chart = echarts.init(chartDom)
  const option = {
    tooltip: {},
    legend: [
      {
        data: chartData.categories.map(function (a) {
          return a.name
        })
      }
    ],
    series: [
      {
        name: 'Les Miserables',
        type: 'graph',
        layout: 'none',
        data: chartData.nodes,
        links: chartData.links,
        categories: chartData.categories,
        roam: true,
        label: {
          show: true,
          position: 'right',
          formatter: '{b}'
        },
        labelLayout: {
          hideOverlap: true
        },
        scaleLimit: {
          min: 0.4,
          max: 2
        },
        lineStyle: {
          color: 'source',
          curveness: 0.3
        }
      }
    ]
  }
  chart.setOption(option)
}

onMounted(() => { })
onBeforeUnmount(() => { })
</script>

<style lang='scss'
       scoped>
      .step-wrap {
        height: 100%;
      }
    </style>
