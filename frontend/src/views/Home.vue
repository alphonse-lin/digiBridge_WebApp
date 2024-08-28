<template>
  <div class="page-wrap"
       ref="viewerContainer">
    <TopHeader class="top-head"></TopHeader>
    <div class="content-wrap">
      <router-view v-slot="{ Component }">
        <transition name="fade"
                    mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </div>
    <div class="chat-icon">
      <div @click="onChat">
        <svg-icon icon-class="robot-2-line"
                  style="font-size: 20px;" />
      </div>
    </div>
    <ChatDialog ref="refChatDialog"></ChatDialog>

    <transition name="el-fade-in-linear">
      <BridgeInfo v-show="bridgeInfoVisible"
                  :currentBridge="currentBridge"
                  :bridgeInfoVisible="bridgeInfoVisible"></BridgeInfo>
    </transition>

    <!-- <TestCom></TestCom> -->
  </div>
</template>

<script setup>
import TopHeader from '../components/TopHeader/index.vue'
// import TestCom from '../components/test-com/index.vue'
import ChatDialog from '../components/chat-com/dialog.vue'
import BridgeInfo from '../components/bridge-info/index.vue'
import useAppStore from '@/store/modules/app'
import { initEvent } from '@/map/events.js'
import PointManager from '@/map/point.js'
import ModelManager from '@/map/model.js'
import CarManager from '@/map/car.js'
import WaveLine from '@/map/waveLine.js'
// import TilesRenderer from '@/map/tilesRenderer.js'
import { bridges } from '@/api'

// 初始化地图
const appStore = useAppStore()
window.CESIUM_BASE_URL = 'libs/cesium'
const viewerContainer = ref(null)
const mapViewer = shallowRef(null)
function initMap () {
  Cesium.Ion.defaultAccessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIxMzU5OWY3NS1jN2U5LTQ2ZTgtOTcwOC1iNzNmYzc3ZDgwN2IiLCJpZCI6OTM4MjMsImlhdCI6MTY1MjYwODUzMX0.09nSxhqVYbqcTosrngVDICplwks6NwJpArjH1S5pF5o'
  mapViewer.value = new Cesium.Viewer(viewerContainer.value, {
    imageryProvider: new Cesium.BingMapsImageryProvider({
      url: 'https://dev.virtualearth.net',
      key: 'AicWh_KjXV9j-4PekYNc8V3-cWtF-YtlYld133rs8WMp3SwYhY-_iZY_UqzJYmpw',
      mapStyle: Cesium.BingMapsStyle.AERIAL_WITH_LABELS_ON_DEMAND
    }),
    // 隐藏 cesium 默认控件
    animation: false,
    fullscreenButton: false,
    timeline: false,
    geocoder: false,
    navigationHelpButton: false,
    homeButton: false,
    sceneModePicker: false,
    // baseLayerPicker: false,
    infoBox: false
  })
  removeDefault(mapViewer.value)
  // 设置相机位置
  mapViewer.value.camera.setView({
    // fromDegrees()方法，将经纬度和高程转换为世界坐标
    destination: Cesium.Cartesian3.fromDegrees(-3.836715, 51.651717, 10000),
    orientation: {
      heading: Cesium.Math.toRadians(0), // 方向，0 表示北向
      pitch: Cesium.Math.toRadians(-90), // 俯视角度，负值表示向下看
      roll: Cesium.Math.toRadians(0) // 侧倾角度
    }
  })
  // 全局存储地图对象
  appStore.setMapViewer(mapViewer.value)
  // 初始化地图事件
  initEvent(mapViewer.value, appStore)
  // 初始化点位处理类
  window.pointManager = new PointManager(mapViewer.value, appStore)
  // 初始化模型处理类
  window.modelManager = new ModelManager(mapViewer.value)
  // 初始化小车处理类
  window.carManager = new CarManager(mapViewer.value)
  // 初始化波浪线
  window.waveLine = new WaveLine(mapViewer.value, appStore)
  // window.tilesRenderer = new TilesRenderer(mapViewer.value)
}
function removeDefault (mapViewer) {
  mapViewer.cesiumWidget.creditContainer.style.display = 'none' // 隐藏ceisum标识
  mapViewer.cesiumWidget.screenSpaceEventHandler.removeInputAction(Cesium.ScreenSpaceEventType.LEFT_CLICK)
  mapViewer.cesiumWidget.screenSpaceEventHandler.removeInputAction(Cesium.ScreenSpaceEventType.LEFT_DOUBLE_CLICK)
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
function removeBridgePoints () {
  window.pointManager.removeAllPoints('point-bridge-')
}

const bridgeInfoVisible = ref(false)
const currentBridge = ref(null)
watch(() => appStore.leftClickId,
  (n) => {
    // if (n !== '' && n.startsWith('point-bridge-')) {
    router.push('/')
    appStore.setMonitorType(0)
    bridgeInfoVisible.value = n !== '' && n.startsWith('point-bridge-')
    currentBridge.value = bridges.find(v => v.id === Number(n.split('point-bridge-')[1]))
    // }
  })
const router = useRouter()
watch(() => appStore.leftDblClickId,
  (n) => {
    if (n !== '' && n.startsWith('point-bridge-')) {
      setTimeout(() => {
        router.push('/bridge-monitor')
        appStore.setMonitorType(1)
        removeBridgePoints()
      }, 0)
    }
  })

const refChatDialog = ref(null)
function onChat () {
  refChatDialog.value.changeVisible()
}

onMounted(() => {
  initMap()
  addBridgePoints()
})
</script>

<style lang='scss' scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.page-wrap {
  display: flex;

  .slider {
    height: 100%;
  }

  .content-wrap {
    flex: 1;
    height: 100%;
    width: 0;
    position: relative;
    // padding: 15px;

    .top-head {
      width: 100%;
      height: 60px;
      padding: 15px;
      position: absolute;
      top: 0;
      left: 0;
      z-index: 1000;
    }

    .content {
      width: 100%;
      height: 100%;
      // padding: 15px;
      // padding-top: 75px;
    }
  }

  .chat-icon {
    position: fixed;
    left: 20px;
    bottom: 45px;
    z-index: 1000;

    >div {
      width: 40px;
      height: 40px;
      background-color: var(--el-bg-color);
      border-radius: 50%;
      display: flex;
      justify-content: center;
      align-items: center;
      box-shadow: var(--el-box-shadow);
      cursor: pointer;
    }
  }
}
</style>
