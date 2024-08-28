<template>
  <div class="monitor-com-wrap">
    <transition name="el-fade-in-linear">
      <div class="control">
        <div class="play"
             @click="changeCarStatus">
          <svg-icon v-show="['未开始'].includes(carStatus)"
                    icon-class="play-fill"
                    style="font-size: 34px;color: var(--el-color-success)" />
          <svg-icon v-show="carStatus === '运行中'"
                    icon-class="play-fill"
                    style="font-size: 34px;color: var(--el-color-info)" />
          <svg-icon v-show="carStatus === '结束'"
                    icon-class="restart-line"
                    style="font-size: 34px;" />
        </div>
        <div class="line">
          <div class="car"
               :style="{ left: `${position}px` }">
            <svg-icon icon-class="car-2"
                      style="font-size: 34px;color: var(--el-color-primary)" />
          </div>
        </div>
      </div>
    </transition>

    <transition name="el-fade-in-linear">
      <div class="panel right">
        <div class="title">Acceleration</div>
        <div class="content">
          <div :id="`l1-chart-dom-${props.monitorType}`"
               style="height: 220px;"></div>
        </div>
        <div class="title">Amplitude</div>
        <div class="content">
          <div :id="`l2-chart-dom-${props.monitorType}`"
               style="height: 220px;"></div>
        </div>
        <div class="title">Displacement</div>
        <div class="content">
          <div :id="`l3-chart-dom-${props.monitorType}`"
               style="height: 220px;"></div>
        </div>
        <div class="title">Vibration Config</div>
        <div class="content">
          <el-form label-width="80px"
                   label-position="left">
            <el-form-item label="Points">
              <el-select v-model="form.points"
                         @change="OnFormChange">
                <el-option v-for="item in options.points"
                           :key="item"
                           :label="item"
                           :value="item">
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="Amplitude">
              <el-select v-model="form.amplitude"
                         @change="OnFormChange">
                <el-option v-for="item in options.amplitude"
                           :key="item"
                           :label="item"
                           :value="item">
                </el-option>
              </el-select>
            </el-form-item>
          </el-form>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import * as echarts from 'echarts'
import useAppStore from '@/store/modules/app'

const props = defineProps({
  monitorType: {
    type: Number,
    default: 1
  }
})
// const activeBtn = ref(0)

const appStore = useAppStore()
const form = computed(() => appStore.vibrationConfig)
const options = {
  points: [10, 30, 50, 100, 300, 500, 1000],
  amplitude: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
}
function OnFormChange () {
  appStore.setVibrationConfig(form.value)
}

// 时间轴
let animationId = null
const position = ref(0)
const carStatus = ref('未开始') // 未开始、运行中、暂停、结束
// 屏幕宽度
const len = window.innerWidth * 0.3 - 30
const time = 5000
const speed = (len / time) * (1000 / 60)
let timer = null

function changeCarStatus () {
  if (['未开始'].includes(carStatus.value)) {
    carStatus.value = '运行中'
    animationId = requestAnimationFrame(moveCar)
    // 定时器-更新图表
    timer = setInterval(() => {
      updateChart()
    }, 1000)
    // 地图上的汽车模型开始移动
    window.carManager && window.carManager.start()
    // 地图上的波浪线开始摆动
    window.waveLine && window.waveLine.start()
  } else if (carStatus.value === '结束') {
    resetCar()
    clearInterval(timer)
  }
}
function moveCar () {
  if (position.value >= len) {
    carStatus.value = '结束'
    cancelAnimationFrame(animationId)
    clearInterval(timer)
    // 地图上的波浪线停止
    window.waveLine && window.waveLine.stop()
  } else {
    position.value += speed
    animationId = requestAnimationFrame(moveCar)
  }
}
function resetCar () {
  position.value = 0
  carStatus.value = '未开始'
  clearInterval(timer)
  cancelAnimationFrame(animationId)
  initChart()

  // 地图上的汽车模型复位
  window.carManager && window.carManager.reset()
  // 地图上的波浪线停止
  window.waveLine && window.waveLine.stop()
}

const dict = {
  1: null,
  2: null,
  3: null
}
const defaultXData = ['01', '02', '03', '04', '05', '06', '07']
const defaultYData = [10, 15, 25, 15, 21, 25, 22]
function initLineChart (num, id, xData, yData, color) {
  const chartDom = document.getElementById(id)
  if (!chartDom) return
  if (dict[num] !== null && dict[num] !== '' && dict[num] !== undefined) {
    dict[num].dispose()
  }
  dict[num] = echarts.init(chartDom)
  const option = {
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: xData
    },
    yAxis: {
      type: 'value'
    },
    grid: {
      left: '2%',
      right: '5%',
      bottom: '5%',
      top: '5%',
      containLabel: true
    },
    series: [
      {
        data: yData,
        type: 'line',
        smooth: true,
        areaStyle: {
          opacity: 0.8,
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            {
              offset: 0,
              color: color[0]
            },
            {
              offset: 1,
              color: color[1]
            }
          ])
        }
      }
    ]
  }
  dict[num].setOption(option)
}
function initChart () {
  setTimeout(() => {
    initLineChart(1, `l1-chart-dom-${props.monitorType}`, defaultXData, defaultYData, ['rgb(0, 221, 255)', 'rgb(77, 119, 255)'])
    initLineChart(2, `l2-chart-dom-${props.monitorType}`, defaultXData, defaultYData, ['rgb(1, 191, 236)', 'rgb(128, 255, 165)'])
    initLineChart(3, `l3-chart-dom-${props.monitorType}`, defaultXData, defaultYData, ['rgb(255, 191, 0)', 'rgb(224, 62, 76)'])
  }, 0)
}
function updateChart () {
  // 使用getOption和setOption更新随机数据
  const keys = Object.keys(dict)
  keys.forEach((k) => {
    const xData = dict[k].getOption().xAxis[0].data
    const yData = dict[k].getOption().series[0].data
    for (let i = 0; i < 7; i++) {
      xData.push(String(xData.length + 1))
      yData.push(Math.floor(Math.random() * 10 + 30))
    }
    dict[k].setOption({
      xAxis: {
        data: xData
      },
      series: [
        {
          data: yData
        }
      ]
    })
  })
}

onMounted(() => {
  initChart()
})
onBeforeUnmount(() => { })
</script>

<style lang='scss'
       scoped>
      .monitor-com-wrap {

        .btns {
          >div {
            width: 30px;
            height: 30px;
            border: 4px solid #fff;
            position: fixed;
            z-index: 100;
            border-radius: 50%;
            cursor: pointer;
            transition: all 0.3s;
            background-color: rgba(255, 255, 255, 0.6);

            &:hover {
              box-shadow: 0 0 10px #fff;
            }

            &:nth-child(1) {
              top: 413px;
              left: 530px;
            }

            &:nth-child(2) {
              top: 458px;
              left: 715px;
            }

            &:nth-child(3) {
              top: 500px;
              left: 860px;
            }
          }
        }

        .control {
          position: fixed;
          bottom: 135px;
          left: 50%;
          transform: translateX(-50%);
          z-index: 101;
          // width: 800px;

          display: flex;
          align-items: center;
          padding: 10px 30px;
          border-radius: 28px;
          background-color: rgba(255, 255, 255, 0.8);
          box-shadow: var(--el-box-shadow);

          .line {
            width: 30vw;
            height: 4px;
            border-radius: 5px;
            background-color: #555;
            margin: 0 20px;
            position: relative;

            .car {
              width: 34px;
              height: 34px;
              // background-color: pink;
              position: absolute;
              top: -18px;
              // left: 0;
              transition: all 0.3s;
              z-index: 20;
            }
          }

          .play,
          .close {
            cursor: pointer;
          }
        }

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
        }
      }
    </style>
