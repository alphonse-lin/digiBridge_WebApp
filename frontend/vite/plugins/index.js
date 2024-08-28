import vue from '@vitejs/plugin-vue'

import createAutoImport from './auto-import' // 自动引入
import cesium from './cesium' // cesium
import createSvgIcon from './svg-icon'

export default function createVitePlugins (viteEnv, isBuild = false) {
  const vitePlugins = [vue()]
  vitePlugins.push(createAutoImport())
  vitePlugins.push(cesium())
  vitePlugins.push(createSvgIcon(isBuild))
  return vitePlugins
}
