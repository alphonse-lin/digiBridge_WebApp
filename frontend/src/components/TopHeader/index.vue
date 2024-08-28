<template>
  <div class="header-nav">
    <div class="logo"
         @click="onHome">
      <div>Digi</div>
      <div>Bridge</div>
    </div>
    <div class="tools">
      <div style="margin-left: 15px;">
        <el-select :model-value="bridgeId"
                   placeholder="Select Bridge"
                   clearable
                   filterable
                   style="width: 140px;"
                   size="large"
                   class="bridge-select"
                   @change="onBridgeIdChange"
                   @clear="onHome">
          <el-option v-for="item in bridges"
                     :key="item.id"
                     :label="item.name"
                     :value="item.id">
          </el-option>
        </el-select>
      </div>
    </div>

    <TopMenu></TopMenu>

    <div v-show="isDark"
         class="dark-btn"
         title="暗夜模式"
         @click="changeTheme">
      <el-icon>
        <Sunny />
      </el-icon>
    </div>
    <div v-show="!isDark"
         class="dark-btn"
         title="暗夜模式"
         @click="changeTheme">
      <el-icon>
        <Moon />
      </el-icon>
    </div>
  </div>
</template>

<script setup>
import useAppStore from '@/store/modules/app'
import { bridges } from '@/api'
import { onDblclick } from '@/map/events'
import TopMenu from '@/components/TopMenu/index.vue'
import { Sunny, Moon } from '@element-plus/icons-vue'

const appStore = useAppStore()
const isDark = computed(() => appStore.isDark)
watch(
  () => isDark.value,
  (val) => {
    if (val) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  },
  { immediate: true }
)
function changeTheme () {
  appStore.setTheme()
}

const router = useRouter()
function onHome (changeRoute = true) {
  appStore.setMonitorType(0)
  // 重置左侧点击和双击的桥梁 id
  appStore.setLeftClickId('')
  appStore.setLeftDblClickId('')
  // 卸载模型
  window.modelManager.unloadModel()
  // 添加桥梁点
  addBridgePoints()
  // window.tilesRenderer.clearTileSet()
  if (changeRoute) {
    appStore.setBridgeId(-1)
    router.push('/')
    appStore.mapViewer.camera.flyTo({
      destination: Cesium.Cartesian3.fromDegrees(-3.836715, 51.651717, 10000),
      duration: 2,
      orientation: {
        heading: Cesium.Math.toRadians(0), // 方向，0 表示北向
        pitch: Cesium.Math.toRadians(-90), // 俯视角度，负值表示向下看
        roll: Cesium.Math.toRadians(0) // 侧倾角度
      }
    })
  }
}
// 添加桥梁位置
function addBridgePoints () {
  bridges.forEach((bridge) => {
    const { id, position } = bridge
    window.pointManager.addPoint({
      type: 'bridge',
      id: `point-bridge-${id}`,
      position
    })
  })
}

const bridgeId = computed(() => {
  return appStore.bridgeId === -1 ? '' : appStore.bridgeId
})
function onBridgeIdChange (val) {
  if (!val) return
  if (router.currentRoute.value.path !== '/') {
    onHome(false)
  }
  onDblclick(appStore.mapViewer, `point-bridge-${val}`)
}
</script>

<style lang="scss" scoped>
.header-nav {
  width: calc(100% - 40px);
  display: flex;
  align-items: center;

  position: fixed;
  left: 20px;
  top: 20px;
  z-index: 1000;

  .logo {
    height: 40px;
    display: flex;
    align-items: center;
    font-size: 16px;
    background-color: rgba(239, 239, 239, 0.8);
    // box-shadow: var(--el-box-shadow-light);
    padding: 0 20px;
    border-radius: 24px;
    cursor: pointer;

    >div {
      &:first-child {
        font-size: 22px;
        color: #0052b4;
        font-weight: bold;
        margin-right: 5px;
      }
    }
  }

  .tools {
    display: flex;
    align-items: center;
  }

  .dark-btn {
    margin-left: 15px;
    height: 40px;
    width: 40px;
    border-radius: 50%;
    background-color: var(--el-bg-color);
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    display: none;
  }
}
</style>

<style>
.bridge-select {
  .el-select__wrapper {
    border-radius: 20px;
  }
}
</style>
