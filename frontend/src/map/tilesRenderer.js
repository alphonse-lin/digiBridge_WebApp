class TilesRenderer {
  constructor (viewer) {
    this.viewer = viewer
    this.tileSet = null
  }

  async loadTileSet (options) {
    const defaultUrl = new URL('/tiles/bridge/tileset.json', import.meta.url).href
    const { url = defaultUrl, position, heading, pitch, roll, scale } = options
    const { longitude = 0, latitude = 0, height = 0 } = position

    // 定位模型
    const positionCartesian = Cesium.Cartesian3.fromDegrees(longitude, latitude, height)
    const transformMatrix = Cesium.Transforms.eastNorthUpToFixedFrame(positionCartesian)
    // 旋转模型
    const rotationMatrix = Cesium.Matrix4.fromRotationTranslation(
      Cesium.Matrix3.fromHeadingPitchRoll(
        new Cesium.HeadingPitchRoll(
          Cesium.Math.toRadians(heading),
          Cesium.Math.toRadians(pitch),
          Cesium.Math.toRadians(roll)
        )
      )
    )
    // 缩放模型
    const scaleMatrix = Cesium.Matrix4.fromScale(new Cesium.Cartesian3(scale, scale, scale))
    // 模型变幻矩阵
    const modelMatrix = Cesium.Matrix4.multiply(
      Cesium.Matrix4.multiply(transformMatrix, rotationMatrix, new Cesium.Matrix4()),
      scaleMatrix,
      new Cesium.Matrix4()
    )

    this.tileSet = await Cesium.Cesium3DTileset.fromUrl(url, {
      boundingVolume: true // 是否显示包围盒
    })
    window.tileSet = this.tileSet
    this.tileSet.modelMatrix = modelMatrix
    this.tileSet.maximumScreenSpaceError = 1 // 所有层级都显示
    this.viewer.scene.primitives.add(this.tileSet)

    // 将相机视角调整到模型附近
    const offset = new Cesium.HeadingPitchRange(
      Cesium.Math.toRadians(-130),
      Cesium.Math.toRadians(-30),
      100.0
    )
    this.viewer.zoomTo(this.tileSet, offset)
  }

  clearTileSet () {
    if (this.tileSet) {
      this.viewer.scene.primitives.remove(this.tileSet)
      this.tileSet = null
      window.tileSet = null
    }
  }
}

export default TilesRenderer
