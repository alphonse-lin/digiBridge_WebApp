<template>
  <div class="monitor-com-wrap">
    <div class="panel left">
      <div class="title"
           style="margin-top: 0;">Bridge Management</div>
      <div class="wrap">
        <div class="row">
          <div class="label">Event Count</div>
          <div class="num">3580</div>
        </div>
        <div class="row compare">
          <div class="item">
            <div>Year</div>
            <div>+2.3%</div>
          </div>
          <div class="item">
            <div>Month</div>
            <div>+5%</div>
          </div>
        </div>
        <div class="row percent">
          <div class="done">
            <el-tooltip content="done"
                        placement="top"
                        effect="dark">
              <div>2148</div>
            </el-tooltip>
          </div>
          <el-tooltip content="todo"
                      placement="top"
                      effect="dark">
            <div class="todo">1432</div>
          </el-tooltip>
        </div>
      </div>
      <div class="title">Structure Health Assessment</div>
      <div class="wrap chart-wrap">
        <div :id="`progress-dom-${props.monitorType}`"
             style="height: 200px;"></div>
      </div>
      <div class="title">Asset Count</div>
      <div class="wrap equs">
        <el-row :gutter="14"
                style="flex-wrap: wrap;">
          <el-col v-for="v in equipmentList"
                  :key="v.name"
                  :span="12">
            <div class="equ">
              <svg-icon style="margin-right: 10px;"
                        :icon-class="v.icon" />
              <div>{{ v.name }}</div>
              <div>{{ v.value }}</div>
            </div>
          </el-col>
        </el-row>
      </div>
    </div>
    <div class="panel right">
      <div class="title"
           style="margin-top: 0;">Live Monitoring</div>
      <div class="wrap photo-wrap">
        <el-image :src="imgUrl"
                  fit="fill"></el-image>
      </div>
      <div class="title">Sensor Energy Consumption Trends</div>
      <div class="wrap chart-wrap">
        <div id="chart-dom"
             style="height: 200px;"></div>
      </div>
      <div class="title">Maintenance Status</div>
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
  </div>
</template>

<script setup>
import * as echarts from 'echarts'
import imgUrl from '@/assets/live-photo-2.png'

const props = defineProps({
  monitorType: {
    type: Number,
    default: 1
  }
})

let progressChart = null
function initProgressChart (id) {
  const chartDom = document.getElementById(id)
  if (!chartDom) return
  if (progressChart !== null && progressChart !== '' && progressChart !== undefined) {
    progressChart.dispose()
  }
  const option = {
    series: [
      {
        type: 'gauge',
        startAngle: 180,
        endAngle: 0,
        center: ['50%', '85%'],
        radius: '130%',
        min: 0,
        max: 100,
        splitNumber: 8,
        axisLine: {
          lineStyle: {
            width: 10,
            color: [
              [0.25, '#FF6E76'],
              [0.5, '#FDDD60'],
              [0.75, '#58D9F9'],
              [1, '#7CFFB2']
            ]
          }
        },
        pointer: {
          icon: 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z',
          length: '12%',
          width: 20,
          offsetCenter: [0, '-60%'],
          itemStyle: {
            color: 'auto'
          }
        },
        axisTick: {
          length: 12,
          lineStyle: {
            color: 'auto',
            width: 4
          }
        },
        splitLine: {
          length: 20,
          lineStyle: {
            color: 'auto',
            width: 5
          }
        },
        axisLabel: {
          show: false,
          color: '#464646',
          fontSize: 20,
          distance: -60,
          rotate: 'tangential'
        },
        title: {
          offsetCenter: [0, '-10%'],
          fontSize: 20
        },
        detail: {
          fontSize: 30,
          offsetCenter: [0, '-35%'],
          valueAnimation: true,
          color: 'inherit'
        },
        data: [
          {
            value: 70,
            name: 'Grade Rating'
          }
        ]
      }
    ]
  }
  progressChart = echarts.init(chartDom)
  option && progressChart.setOption(option)
}

const equipmentList = shallowRef([
  { name: 'sensor', value: 12, icon: 'sensor-fill' },
  { name: 'equipment', value: 8, icon: 'device-fill' },
  { name: 'light', value: 4, icon: 'lightbulb-flash-fill' },
  { name: 'turnstile', value: 6, icon: 'toggle-fill' },
  { name: 'camera', value: 3, icon: 'camera-fill' },
  { name: 'extra', value: 2, icon: 'archive-fill' }
])

function initLineChart () {
  const chartDom = document.getElementById('chart-dom')
  if (!chartDom) return
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
        type: 'value',
        axisLabel: {
          formatter: '{value} W'
        }
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
        data: [230, 134, 120, 210, 132, 101, 90]
      },
      {
        name: 'Sensor 3',
        type: 'line',
        stack: 'Total',
        areaStyle: {},
        emphasis: {
          focus: 'series'
        },
        data: [120, 230, 90, 134, 210, 101, 132]
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

onMounted(() => {
  setTimeout(() => {
    // initPieChart('pie-dom-1')
    // initPieChart('pie-dom-2', ['#91cc75', '#5470c6'])
    initProgressChart(`progress-dom-${props.monitorType}`)
    initLineChart()
  }, 300)
})
onBeforeUnmount(() => { })
</script>

<style lang='scss'
       scoped>
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
        overflow-y: auto;

        .wrap {
          .row {
            display: flex;
            align-items: center;
            margin-bottom: 14px;

            .num {
              font-size: 40px;
              font-weight: 600;
              margin-left: 10px;
              flex: 1;
              text-align: center;
              color: var(--el-color-primary);
            }

            &.compare {
              display: flex;
              align-items: center;

              .item {
                height: 40px;
                flex: 1;
                display: flex;
                align-items: center;
                justify-content: space-between;

                &:last-child {
                  margin-left: 40px;
                }

                >div {
                  &:last-child {
                    flex: 1;
                    text-align: center;
                    font-size: 20px;
                    font-weight: bold;
                    color: var(--el-color-warning);
                  }
                }
              }
            }

            &.percent {
              height: 40px;
              background-color: #c8c9cc;
              border-radius: 20px;
              overflow: hidden;
              margin-bottom: 20px;

              .done {
                height: 100%;
                width: 60%;
                display: flex;
                align-items: center;
                justify-content: center;
                background-color: rgba(103, 194, 58, 1);
                border-right: 7px solid #fff;
                transform: skewX(-30deg);
                position: relative;
                left: -10px;

                >div {
                  transform: skewX(30deg);
                  font-size: 18px;
                  color: #fff;
                }
              }

              .todo {
                height: 100%;
                width: 40%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 18px;
                color: #fff;
              }
            }

            &.pie {
              display: flex;
              justify-content: space-between;

              >div {
                flex: 1;
                height: 140px;
              }
            }
          }

          &.equs {
            .equ {
              width: 100%;
              display: flex;
              align-items: center;
              height: 55px;
              // box-shadow: 0 0 5px 0 rgba(0, 0, 0, 0.1);
              margin-bottom: 14px;
              border-radius: 4px;
              padding: 0 5px;

              >div {
                margin-right: 10px;
                text-align: center;

                &:last-child {
                  flex: 1;
                  text-align: right;
                  font-weight: bold;
                  color: var(--el-color-primary);
                }
              }
            }
          }
        }

        &.left {
          left: 20px;
        }
      }
    </style>
