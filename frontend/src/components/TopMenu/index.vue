<template>
  <div class="custom-menu">
    <el-menu mode="horizontal" background-color="#333" text-color="#fff" active-text-color="#E6A23C" @select="onSelect">
      <div v-for="item in menus" :key="item.id">
        <el-sub-menu v-if="item.children && item.children.length > 0" :index="item.id">
          <template #title>{{ item.label }}</template>
          <el-menu-item v-for="v in item.children" :key="v.id" :index="v.id">{{ v.label }}</el-menu-item>
        </el-sub-menu>
        <el-menu-item v-else :index="item.id">{{ item.label }}</el-menu-item>
      </div>
    </el-menu>

    <IframeWrap ref="refIframeWrap" :selected="selected"></IframeWrap>
    <IframeWrap_AutoMSG ref="refIframeWrap_AutoMSG" :selected="selected"></IframeWrap_AutoMSG>
    <IframeWrap_KBMain ref="refIframeWrap_KBMain" :selected="selected"></IframeWrap_KBMain>
  </div>
</template>

<script setup>
import { menus } from './menu.js'
import IframeWrap_AutoMSG from '@/components/IframeWrap_AutoMSG/index.vue'
import IframeWrap_KBMain from '@/components/IframeWrap_KBMain/index.vue'
import IframeWrap from '@/components/IframeWrap/index.vue'
import Bus from '@/utils/bus'
import useAppStore from '@/store/modules/app'

const appStore = useAppStore()
const router = useRouter()
const refIframeWrap = ref(null)
const refIframeWrap_AutoMSG = ref(null)
const refIframeWrap_KBMain = ref(null)
const selected = ref(null)
function onSelect(val) {
  if (val.includes('-')) {
    const father = menus.find(v => v.id === val.split('-')[0])
    selected.value = father.children.find(v => v.id === val)
  } else {
    selected.value = menus.find(v => v.id === val)
  }
  console.log(selected.value)
  if (selected.value.id === '2-1') {
    router.push('/bridge-monitor')
    appStore.setMonitorType(3)
    setTimeout(() => {
      Bus.emit('monitor3PanelShow')
    }, 500)
  } else if (selected.value.id === '4-1-1') {
    refIframeWrap_KBMain.value.changeVisible()
  }  
  else if (selected.value.id === '4-1-2') {
    refIframeWrap_AutoMSG.value.changeVisible()
  } 
  else {
    refIframeWrap.value.changeVisible()
  }
}

onMounted(() => {
  Bus.on('monitor-type-change', (v) => {
    onSelect(v)
  })
})
onBeforeUnmount(() => { })
</script>

<style lang='scss' scoped>
.custom-menu {
  flex: 1;
  width: 0;
  margin-left: 15px;
  overflow-x: auto;
  border-radius: 20px;
  overflow: hidden;
}
</style>

<style lang='scss'>
.custom-menu {
  .el-menu {
    overflow: hidden;
    // background-color: transparent;
    border-bottom: 0 !important;

    >div {

      &:first-child {
        >li {
          border-top-left-radius: 20px;
          border-bottom-left-radius: 20px;
          overflow: hidden;
        }
      }

      &:last-child {
        >li {
          border-top-right-radius: 20px;
          border-bottom-right-radius: 20px;
          overflow: hidden;
        }
      }

      >li {
        // height: 40px;
        // background-color: #313131;
        // color: #fff;

        // &:hover {
        //   background-color: #5b5a5a !important;
        //   color: #fff !important;
        // }
      }
    }
  }
}
</style>
