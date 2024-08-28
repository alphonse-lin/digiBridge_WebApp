const sensorDefaultStyle = { pixelSize: 15, color: Cesium.Color.WHITE, outlineColor: Cesium.Color.fromCssColorString('#67C23A'), outlineWidth: 3, heightReference: Cesium.HeightReference.RELATIVE_TO_GROUND }
const sensorHighlightStyle = { pixelSize: 15, color: Cesium.Color.WHITE, outlineColor: Cesium.Color.fromCssColorString('#f56c6c'), outlineWidth: 3, heightReference: Cesium.HeightReference.RELATIVE_TO_GROUND }
const bridgeDefaultStyle = { pixelSize: 12, color: Cesium.Color.fromCssColorString('#00acc1'), outlineColor: Cesium.Color.WHITE, outlineWidth: 3, heightReference: Cesium.HeightReference.RELATIVE_TO_GROUND }

class PointManager {
  constructor (viewer, store) {
    this.viewer = viewer
    this.store = store
    this.points = {}
    this.activeSensor = ''
  }

  addPoint ({ type, id, position }) {
    const p = Cesium.Cartesian3.fromDegrees(...position)
    const style = type === 'sensor' ? sensorDefaultStyle : bridgeDefaultStyle
    const point = this.viewer.entities.add({
      id,
      position: p,
      point: style
    })
    this.points[id] = point
  }

  removePoint (id) {
    if (this.points[id]) {
      this.viewer.entities.remove(this.points[id])
      delete this.points[id]
    }
  }

  removeAllPoints (prefix) {
    for (const id in this.points) {
      if (id.startsWith(prefix)) {
        this.viewer.entities.remove(this.points[id])
        delete this.points[id]
      }
    }
  }

  // 点击某一点，高亮显示，否则恢复默认样式
  onClickSensorPoint (id) {
    this.activeSensor = this.activeSensor === id ? '' : id
    this.store.setSensorId(this.activeSensor)
    for (const key of Object.keys(this.points)) {
      if (key.startsWith('point-sensor-')) {
        if (this.activeSensor === '') {
          this.points[key].point.outlineColor = sensorDefaultStyle.outlineColor
        } else {
          this.points[key].point.outlineColor = key === id ? sensorHighlightStyle.outlineColor : sensorDefaultStyle.outlineColor
        }
      }
    }
  }
}

export default PointManager
