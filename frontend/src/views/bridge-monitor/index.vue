<template>
  <div class="bridge-monitor">
    <div class="types">
      <el-radio-group v-model="monitorType"
                      size="large">
        <el-radio-button v-for="r in radios"
                         :key="r.label"
                         :value="r.label">
          <el-tooltip :content="r.name"
                      placement="top"
                      effect="dark">
            <el-icon class="type-icon">
              <component :is="r.com"
                         :monitorType="monitorType"></component>
            </el-icon>
          </el-tooltip>
        </el-radio-button>
      </el-radio-group>
    </div>

    <monitor1 v-if="monitorType === 1"></monitor1>
    <monitor2 v-if="monitorType === 2"></monitor2>
    <monitor3 v-if="monitorType === 3"></monitor3>
    <monitor5 v-if="monitorType === 4"></monitor5>
    <monitor4 v-if="monitorType === 5"></monitor4>
  </div>
</template>

<script setup>
import {
  Odometer, Operation, UploadFilled, VideoPlay, Share, Notebook, Tickets, Ticket, Collection, TrendCharts
} from '@element-plus/icons-vue'
import monitor1 from './monitor1.vue'
import monitor2 from './monitor2.vue'
import monitor3 from './monitor3.vue'
import monitor4 from './monitor4.vue'
import monitor5 from './monitor5.vue'
import useAppStore from '../../store/modules/app'
import { bridges } from '@/api'
import Bus from '@/utils/bus'

const appStore = useAppStore()
const monitorType = computed({
  get: () => appStore.monitorType,
  set: val => appStore.setMonitorType(val)
})
const radios = shallowRef([
  { label: 1, com: Odometer, name: 'Bridge Detail' },
  { label: 2, com: Operation, name: 'Sensors' },
  { label: 3, com: UploadFilled, name: 'Detection' },
  { label: 4, com: Share, name: 'Result' },
  { label: 5, com: VideoPlay, name: 'Analog' },
  { label: 6, com: Notebook, name: 'Drone Station' },
  { label: 7, com: Tickets, name: 'Image Processing' },
  { label: 8, com: Ticket, name: 'DT Synchronisation' },
  { label: 9, com: Collection, name: 'Data Streaming' },
  { label: 10, com: TrendCharts, name: 'Structural Health Monitoring' }
])

const leftDblClickId = computed(() => appStore.leftDblClickId)
watch(
  () => monitorType.value,
  (n, o) => {
    if (n === 2) {
      // TODO: 移除小车模型
      window.carManager && window.carManager.unloadModel()
      window.waveLine && window.waveLine.clear()
      // 添加传感器点位
      const id = Number(leftDblClickId.value.split('point-bridge-')[1])
      const bridge = bridges.find(item => item.id === id)
      setTimeout(() => {
        bridge.sensors.forEach((s) => {
          window.pointManager.addPoint({
            type: 'sensor',
            id: `point-sensor-${s.id}`,
            position: s.position
          })
        })
      }, 200)
    } else if (n === 5) {
      // 移除所有传感器点位
      window.pointManager && window.pointManager.removeAllPoints('point-sensor-')
      // TODO: 添加小车模型
      const id = Number(leftDblClickId.value.split('point-bridge-')[1])
      window.carManager && window.carManager.loadModel({ id })
      // 添加波浪线
      window.waveLine && window.waveLine.render({ id })
    } else {
      // 移除所有传感器点
      window.pointManager && window.pointManager.removeAllPoints('point-sensor-')
      // TODO: 移除小车模型
      window.carManager && window.carManager.unloadModel()
      // 移除波浪线
      window.waveLine && window.waveLine.clear()
      if (n > 5) {
        Bus.emit('monitor-type-change', String(n - 5))
      }
    }
  },
  { immediate: true }
)

onMounted(() => {
  Bus.on('monitorShow', (v) => {
    monitorType.value = Number(v)
  })
})
onBeforeUnmount(() => { })
</script>

<style lang='scss' scoped>
.bridge-monitor {
  transition: all 0.3s;

  .types {
    min-width: 788px;
    position: fixed;
    bottom: 40px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 100;

    .type-icon {
      font-size: 24px;
      width: 40px;
    }
  }
}
</style>
