import { useDark, useToggle } from '@vueuse/core'

const useAppStore = defineStore(
    'app', {
        state: () => ({
            isDark: false,
            menuCollapse: false,
            mapViewer: null, // 地图实例
            leftClickId: '',
            leftDblClickId: '',
            bridgeId: -1,
            monitorType: 1,
            sensorId: '',
            vibrationConfig: {
                points: 10,
                amplitude: 1
            }
        }),
        actions: {
            setTheme() {
                this.isDark = !this.isDark
                const elementDark = useDark()
                const toggleDark = useToggle(elementDark)

                if (this.isDark) {
                    toggleDark(true)
                } else {
                    toggleDark(false)
                }
            },
            setMenuCollapse(val) {
                if (val) {
                    this.menuCollapse = val
                } else {
                    this.menuCollapse = !this.menuCollapse
                }
            },
            setMapViewer(viewer) {
                this.mapViewer = viewer
            },
            setLeftClickId(id) {
                this.leftClickId = id
            },
            setLeftDblClickId(id) {
                this.leftDblClickId = id
            },
            setMonitorType(type) {
                this.monitorType = type
            },
            setBridgeId(id) {
                this.bridgeId = id
            },
            setSensorId(id) {
                this.sensorId = id
            },
            setVibrationConfig(config) {
                this.vibrationConfig = config
            }
        }
    })

export default useAppStore