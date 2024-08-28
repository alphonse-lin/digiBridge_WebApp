import { bridges } from '@/api'

class CarManager {
    constructor(viewer) {
        this.viewer = viewer
        this.startPosition = null
        this.endPosition = null
        this.duration = 5000

        this.car = null
        this.animationInterval = null
        this.startTime = null
    }

    loadModel(options) {
        // 根据 id 获取桥梁参数
        const { id: bridgeId } = options
        const bridge = bridges.find(item => item.id === Number(bridgeId))

        const { scale, car } = bridge
        const { id, radians, position1, position2 } = car
        this.startPosition = Cesium.Cartesian3.fromDegrees(...position1)
        this.endPosition = Cesium.Cartesian3.fromDegrees(...position2)
        const heading = Cesium.Math.toRadians(radians)
        const pitch = 0
        const roll = 0
        const hpr = new Cesium.HeadingPitchRoll(heading, pitch, roll)
        const orientation = Cesium.Transforms.headingPitchRollQuaternion(this.startPosition, hpr)

        this.car = this.viewer.entities.add({
            id: `car-model-${id}`,
            name: `car-model-${id}`,
            position: this.startPosition,
            orientation,
            model: {
                show: true,
                uri: new URL('/models/train/scene.gltf',
                    import.meta.url).href,
                scale: scale * 1,
                // minimumPixelSize: 128,
                // maximumScale: 20000,
                // incrementallyLoadTextures: true,
                runAnimations: true
            }
        })
    }

    unloadModel() {
        if (this.car) {
            this.viewer.entities.remove(this.car)
            this.car = null
        }
    }

    start() {
        if (this.car && !this.animationInterval) {
            const numSteps = 100 // 分为 100 步
            const stepDuration = this.duration / numSteps
            let step = 0

            this.startTime = Cesium.JulianDate.now()

            this.animationInterval = setInterval(() => {
                step++
                if (step > numSteps) {
                    clearInterval(this.animationInterval)
                    this.animationInterval = null
                } else {
                    const progress = step / numSteps

                    // 根据插值比例更新小车位置
                    const position = Cesium.Cartesian3.lerp(this.startPosition, this.endPosition, progress, new Cesium.Cartesian3())
                    this.car.position.setValue(position)
                }
            }, stepDuration)
        }
    }

    reset() {
        if (this.car) {
            this.car.position.setValue(this.startPosition)
            clearInterval(this.animationInterval)
            this.animationInterval = null
        }
    }

    clear() {
        this.pause()
        this.scene.remove(this.car)
        this.car = null
    }
}

export default CarManager