<template>
  <div class="wrap shadow">
    <div class="brand">Brand</div>
    <MenuCom></MenuCom>
    <div class="menu-item setting">
      <el-icon class="icon">
        <setting />
      </el-icon>
      <div v-show="!titleShow"
           class="title">设置</div>
    </div>
    <div class="menu-item user">
      <el-icon class="icon">
        <User />
      </el-icon>
      <div v-show="!titleShow"
           class="title">个人中心</div>
    </div>
  </div>
</template>

<script setup>
import MenuCom from './menu.vue'
import useAppStore from '../../store/modules/app'
import { User, Setting } from '@element-plus/icons-vue'

const menuCollapse = computed(() => useAppStore().menuCollapse)
const titleShow = ref(false)
watch(menuCollapse, async (n, o) => {
  if (n === true) {
    titleShow.value = n
  } else {
    setTimeout(() => {
      titleShow.value = n
    }, 300)
  }
})
</script>

<style lang='scss' scoped>
.wrap {
  width: 100%;
  height: 100%;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: center;

  .menu-item {
    width: 100%;
    flex: 0 0 56px;
    padding: 0 20px;
    display: flex;
    align-items: center;
    font-size: var(--el-menu-item-font-size);
    color: var(--el-menu-text-color);
    display: flex;
    transition: border-color var(--el-transition-duration), background-color var(--el-transition-duration), color var(--el-transition-duration);

    &:hover {
      background-color: var(--el-menu-hover-bg-color);
    }

    .icon {
      display: inline-block;
      text-align: center;
      width: var(--el-menu-icon-width);
      text-align: center;
      font-size: 18px;
    }

    .title {
      margin-left: 5px;
      flex: 1;
    }
  }

  .brand {
    width: 100%;
    flex: 0 0 56px;
    background-color: var(--el-menu-hover-bg-color);
    display: flex;
    justify-content: center;
    align-items: center;
  }
}
</style>
