import { bridges } from '@/api'

let appStore = null
class WaveLine {
    constructor(viewer, store) {
        this.viewer = viewer
        this.startPoint = [] // 起点
        this.endPoint = [] // 终点
        this.waveOffset = 5 // 波浪偏移
        this.isMoving = false
        this.waveEntity = null
        appStore = store
    }

    render(options) {
        // 根据 id 获取桥梁参数
        const { id: bridgeId } = options
        const bridge = bridges.find(item => item.id === Number(bridgeId))
        this.startPoint = bridge.line.position1
        this.endPoint = bridge.line.position2

        // 渲染只有两个点的线
        const wavePoints = [
            ...this.startPoint,
            ...this.endPoint
        ]
        this.renderWave(wavePoints)
    }

    animateWave() {
        if (this.isMoving) {
            const wavePoints = this.calculateWavePoints_2()
                //console.log('经度:', wavePoints);
            const positions = Cesium.Cartesian3.fromDegreesArrayHeights(wavePoints)
            this.waveEntity.polyline.positions = positions
            const fn = this.animateWave.bind(this)
                // requestAnimationFrame(fn())
            setTimeout(() => {
                fn()
            }, 100)
        } else {
            const wavePoints = [
                ...this.startPoint,
                ...this.endPoint
            ]
            const positions = Cesium.Cartesian3.fromDegreesArrayHeights(wavePoints)
            this.waveEntity.polyline.positions = positions
        }
    }

    start() {
        this.isMoving = true
        this.animateWave()
    }

    stop() {
        this.isMoving = false
        this.animateWave()
    }

    clear(all = true) {
        if (this.waveEntity) {
            this.viewer.entities.remove(this.waveEntity)
            this.waveEntity = null
        }
        if (all) {
            this.isMoving = false
            this.startPoint = []
            this.endPoint = []
        }
    }

    renderWave(wavePoints) {
        this.waveEntity = this.viewer.entities.add({
            polyline: {
                positions: Cesium.Cartesian3.fromDegreesArrayHeights(wavePoints),
                width: 10,
                loop: true,
                material: new Cesium.PolylineGlowMaterialProperty({
                    glowPower: 0.1,
                    color: Cesium.Color.CYAN
                })
            }
        })
    }

    calculateWavePoints() {
        const amplitude = appStore.vibrationConfig.amplitude // 振幅
        const numPoints = appStore.vibrationConfig.points // 假设有100个点
        const wavePoints = []
        for (let i = 0; i <= numPoints; i++) {
            const t = i / numPoints
            const x = (1 - t) * this.startPoint[0] + t * this.endPoint[0]
            const y = (1 - t) * this.startPoint[1] + t * this.endPoint[1]
            const randomOffset = Math.floor(Math.random() * 3) + amplitude
            const z = (1 - t) * this.startPoint[2] + t * this.endPoint[2] + amplitude * Math.sin(randomOffset * Math.PI * t + this.waveOffset)
            wavePoints.push(x, y, z)
            console.log(x, y, z)
                // console.log('%c x, y, z: ', 'background-color: pink', x, y, z)
        }
        wavePoints.push(this.endPoint[0], this.endPoint[1], this.endPoint[2])
        wavePoints.unshift(this.startPoint[0], this.startPoint[1], this.startPoint[2])
        return wavePoints
    }

    //TODO: Gai
    calculateWavePoints_2() {
        // Access amplitude from the store's vibrationConfig
        const amplitude = appStore.vibrationConfig.amplitude;
        const numPoints = 13; // Assuming there are 14 points for now
        const wavePoints = [];

        // Preset data points
        const x_list = [-3.8374481752852208, -3.8373658820897307, -3.837267225673308, -3.837177131850714, -3.8370883029608196, -3.8370254904685774, -3.836909032204294, -3.836838228272638, -3.836668748908954, -3.836557024799434, -3.8363222247770925, -3.8362577252921333, -3.836128012133131];
        const y_list = [51.651702041605084, 51.651707541241095, 51.651717677559404, 51.65171282735335, 51.651713390194445, 51.651710780420956, 51.65170825009955, 51.65170064462051, 51.65169576916278, 51.65168879933586, 51.65168124846957, 51.65167820113891, 51.651672794390116];

        // Generate wave points
        for (let i = 0; i < numPoints; i++) {
            const t = i / numPoints;
            const x = x_list[i];
            //const y = y_list[i];
            const y = (1 - t) * this.startPoint[1] + t * this.endPoint[1]
            let z = 8.04;

            if (i % 2 !== 0) {
                const randomOffset = Math.floor(Math.random() * 3) + amplitude;
                z = (1 - t) * this.startPoint[2] + t * this.endPoint[2] + amplitude * Math.sin(randomOffset * Math.PI * t + this.waveOffset);
                //z = 7.3
            }

            wavePoints.push(x, y, z);
        }

        // Assuming startPoint and endPoint are part of this instance
        //wavePoints.push(this.endPoint[0], this.endPoint[1], this.endPoint[2])
        //wavePoints.unshift(this.startPoint[0], this.startPoint[1], this.startPoint[2])
        return wavePoints
    }
}

export default WaveLine