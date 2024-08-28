<template>
  <div v-if="props.currentBridge && Object.keys(props.currentBridge).length > 0"
       class="bridge-info">
    <div class="name">{{ props.currentBridge.name }}</div>
    <div class="title">Bridge Live Photo</div>
    <div class="wrap photo-wrap">
      <el-image :src="imgUrl"
                fit="fill"></el-image>
    </div>
    <div class="title">Health Marking Trend</div>
    <div class="wrap chart-wrap">
      <div id="chart-dom"
           style="height: 200px;"></div>
    </div>
    <div class="title">Event List</div>
    <div class="wrap list-wrap">
      <el-table :data="tableData"
                stripe
                size="small">
        <el-table-column prop="name"
                         label="Sensor"
                         width="80" />
        <el-table-column prop="time"
                         label="Time"
                         width="100" />
        <el-table-column prop="status"
                         label="Status"
                         width="100">
          <template #default="{ row }">
            <div style="font-weight: bold;"
                 :style="{ color: `var(--el-color-${row.status})` }">{{ row.status }}</div>
          </template>
        </el-table-column>
        <el-table-column prop="event"
                         label="Event"
                         width="200" />
      </el-table>

    </div>
  </div>
</template>

<script setup>
import imgUrl from '@/assets/home/live-photo.png'
import * as echarts from 'echarts'

const props = defineProps({
  currentBridge: {
    type: Object,
    default: () => { }
  },
  bridgeInfoVisible: {
    type: Boolean,
    default: false
  }
})
watch(
  () => props.bridgeInfoVisible,
  (val) => {
    if (val) {
      setTimeout(() => {
        initChart()
      }, 0)
    }
  })

function initChart () {
  const chartDom = document.getElementById('chart-dom')
  const myChart = echarts.init(chartDom)
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
        label: {
          backgroundColor: '#6a7985'
        }
      }
    },
    grid: {
      top: '10%',
      left: '0%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: [
      {
        type: 'category',
        boundaryGap: false,
        data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
      }
    ],
    yAxis: [
      {
        type: 'value'
      }
    ],
    series: [
      {
        name: 'Sensor 1',
        type: 'line',
        stack: 'Total',
        areaStyle: {},
        emphasis: {
          focus: 'series'
        },
        data: [120, 132, 101, 134, 90, 230, 210]
      },
      {
        name: 'Sensor 2',
        type: 'line',
        stack: 'Total',
        areaStyle: {},
        emphasis: {
          focus: 'series'
        },
        data: [220, 182, 191, 234, 290, 330, 310]
      },
      {
        name: 'Sensor 3',
        type: 'line',
        stack: 'Total',
        areaStyle: {},
        emphasis: {
          focus: 'series'
        },
        data: [150, 232, 201, 154, 190, 330, 410]
      },
      {
        name: 'Sensor 4',
        type: 'line',
        stack: 'Total',
        areaStyle: {},
        emphasis: {
          focus: 'series'
        },
        data: [320, 332, 301, 334, 390, 330, 320]
      }
    ]
  }

  option && myChart.setOption(option)
}

const tableData = [
  {
    name: 'Sensor 1',
    time: '12:00:00',
    status: 'success',
    event: 'Normal'
  },
  {
    name: 'Sensor 2',
    time: '12:00:00',
    status: 'warning',
    event: 'Vibration'
  },
  {
    name: 'Sensor 3',
    time: '12:00:00',
    status: 'danger',
    event: 'Broken'
  },
  {
    name: 'Sensor 4',
    time: '12:00:00',
    status: 'success',
    event: 'Normal'
  },
  {
    name: 'Sensor 5',
    time: '12:00:00',
    status: 'success',
    event: 'Normal'
  }
]

onMounted(() => { })
onBeforeUnmount(() => { })
</script>

<style lang='scss'
       scoped>

      .bridge-info {
        width: 300px;
        max-height: calc(100vh - 100px);
        overflow-y: auto;
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 4px;
        padding: 14px;
        box-shadow: var(--el-box-shadow);

        position: fixed;
        right: 20px;
        top: 80px;
        z-index: 100;

        .name {
          font-size: 22px;
          font-weight: 600;
          margin: 10px 0 30px;
          text-align: center;
        }

        .title {
          font-weight: 600;
          margin: 10px 0;
          font-style: italic;
        }

        .wrap {

          &.chart-wrap,
          &.list-wrap {
            padding: 10px;
            background-color: var(--el-bg-color);
            border-radius: 4px;
          }
        }
      }
    </style>
