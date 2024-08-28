import { bridges } from '@/api'

class ModelManager {
  constructor (viewer) {
    this.viewer = viewer
    this.modelEntity = null
  }

  loadModel (options) {
    const { id, longitude, latitude } = options

    // 根据 id 获取模型的渲染参数
    const bridge = bridges.find(item => item.id === Number(id))
    const { scale, radians } = bridge

    const position = Cesium.Cartesian3.fromDegrees(longitude, latitude, 0)
    const heading = Cesium.Math.toRadians(radians)
    const pitch = 0
    const roll = 0
    const hpr = new Cesium.HeadingPitchRoll(heading, pitch, roll)
    const orientation = Cesium.Transforms.headingPitchRollQuaternion(position, hpr)

    this.modelEntity = this.viewer.entities.add({
      id: `model-${id}`,
      name: `model-${id}`,
      position,
      orientation,
      model: {
        show: true,
        uri: new URL('/models/bridge2.gltf', import.meta.url).href,
        scale,
        // scale: scale * 1.7,
        minimumPixelSize: 128,
        maximumScale: 20000,
        incrementallyLoadTextures: true,
        runAnimations: true,
        clampAnimations: true,
        shadows: Cesium.ShadowMode.ENABLED
      }
    })

    // 设置跟踪实体
    this.viewer.trackedEntity = this.modelEntity
    window.modelEntity = this.modelEntity
  }

  unloadModel () {
    if (this.modelEntity) {
      this.viewer.entities.remove(this.modelEntity)
      this.modelEntity = null
      window.modelEntity = null
    }
  }
}

export default ModelManager

// 使用示例
// const viewer = new Cesium.Viewer('cesiumContainer')
// const modelManager = new ModelManager(viewer)
// modelManager.loadModel()
