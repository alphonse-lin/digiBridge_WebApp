import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import ElementPlus from 'element-plus'
// import locale from 'element-plus/es/locale/lang/zh-cn' // 中文语言
// element-plus 自定义主题文件
import './styles/element/index.scss'
import './styles/index.scss'

// svg图标
import 'virtual:svg-icons-register'
import SvgIcon from '@/components/svg-icon/index.vue'

const app = createApp(App)
app.component('svg-icon', SvgIcon)
app.use(router)
app.use(store)
app.use(ElementPlus)
// app.use(ElementPlus, { locale })
app.mount('#app')
