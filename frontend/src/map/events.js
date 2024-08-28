import { bridges } from '@/api'
import Bus from '@/utils/bus'

let appStore = null
let eventHandler = null
let timer = null

function initEvent (mapViewer, store) {
  appStore = store
  eventHandler = new Cesium.ScreenSpaceEventHandler(mapViewer.canvas)
  // 左击事件
  eventHandler.setInputAction((event) => {
    // 使用定时器，避免点击事件和双击事件冲突
    clearTimeout(timer)
    timer = setTimeout(() => {
      // 获取点击的屏幕坐标
      const pickedObject = mapViewer.scene.pick(event.position)
      // 如果点击了一个对象
      if (Cesium.defined(pickedObject)) {
        if (window.tileSet !== null && pickedObject.primitive === window.tileSet) {
          // TODO:高亮点击的节点
        } else if (pickedObject?.primitive?.id.id.startsWith('point-bridge-')) {
          appStore.setLeftDblClickId('')
          appStore.setLeftClickId(pickedObject.id.id)
          window.modelManager.unloadModel() // 卸载模型
          // window.tilesRenderer.clearTileSet()

          const position = mapViewer.scene.pickPosition(event.position)
          if (Cesium.defined(position)) {
            // 将 XYZ 坐标转换为经纬度坐标
            const cartographic = Cesium.Ellipsoid.WGS84.cartesianToCartographic(position)
            const longitude = Cesium.Math.toDegrees(cartographic.longitude)
            const latitude = Cesium.Math.toDegrees(cartographic.latitude)
            // 将相机视角调整到点击点附近
            mapViewer.camera.flyTo({
              destination: Cesium.Cartesian3.fromDegrees(longitude, latitude, 5000),
              duration: 1
            })
          }
        } else if (pickedObject?.primitive?.id.id.startsWith('point-sensor-')) {
          // 传感器点位
          window.pointManager.onClickSensorPoint(pickedObject.id.id)
        } else {
          // console.log('%c pickedObject: ', 'background-color: pink', pickedObject)
          if (pickedObject.id.id.startsWith('model-')) {
            const p = getDegreesByPosition(mapViewer, event.position)
            Bus.emit('model-click', { id: appStore.bridgeId, p })
          }
        }
      } else {
        appStore.setLeftClickId('')
      }
    }, 300)
  }, Cesium.ScreenSpaceEventType.LEFT_CLICK)

  // 双击事件
  eventHandler.setInputAction((event) => {
    clearTimeout(timer)
    // 获取点击的屏幕坐标
    const pickedObject = mapViewer.scene.pick(event.position)
    // 如果点击了一个对象
    if (Cesium.defined(pickedObject)) {
      // 点击桥梁
      if (pickedObject?.primitive?.id.id.startsWith('point-bridge-')) {
        onDblclick(mapViewer, pickedObject.id.id)
      }
    } else {
      appStore.setLeftDblClickId('')
    }
  }, Cesium.ScreenSpaceEventType.LEFT_DOUBLE_CLICK)
}

function onDblclick (mapViewer, id) {
  appStore.setLeftClickId('')
  appStore.setLeftDblClickId(id)

  const bridgeId = Number(id.split('point-bridge-')[1])
  appStore.setBridgeId(bridgeId)
  const bridge = bridges.find(item => item.id === bridgeId)
  const { position } = bridge

  const p = mapViewer.scene.pickPosition(position)
  if (Cesium.defined(p)) {
    // 加载模型
    window.modelManager.loadModel({
      id: bridgeId,
      longitude: position[0],
      latitude: position[1]
    })
    // 3dTiles 方式加载模型
    // window.tilesRenderer.loadTileSet({
    //   position: {
    //     longitude: position[0],
    //     latitude: position[1],
    //     height: 0
    //   },
    //   heading: radians + 90,
    //   pitch: 0,
    //   roll: 0,
    //   scale
    // })
  }
}

// 创建一个高亮的材质
// const highlightMaterial = new Cesium.Material({
//   fabric: {
//     type: 'Color',
//     uniforms: {
//       color: new Cesium.Color(1.0, 0.0, 0.0, 0.5) // 设置高亮颜色，这里为红色半透明
//     }
//   }
// })
// 高亮指定节点
// function highlightNode (nodeId) {
//   // 遍历模型的节点
//   window.tileSet.allTilesAvailablePromise.then(function () {
//     window.tileSet._root.traverse(function (node) {
//       if (node.id === nodeId) {
//         // 应用高亮材质
//         node.content.material = highlightMaterial
//       }
//     })
//   })
// }

// 获取点击位置的经纬度坐标-设置sensor的位置-辅助函数
function getDegreesByPosition (mapViewer, position) {
  const cartesian = mapViewer.scene.pickPosition(position)
  const cartographic = Cesium.Cartographic.fromCartesian(cartesian)
  // 将地理坐标转换为经纬度和高度
  const longitude = Cesium.Math.toDegrees(cartographic.longitude)
  const latitude = Cesium.Math.toDegrees(cartographic.latitude)
  const height = cartographic.height
  console.log('%c Degrees: ', 'background-color: pink', [longitude, latitude, height])
  return [longitude, latitude, height]
}

export { initEvent, eventHandler, onDblclick }
