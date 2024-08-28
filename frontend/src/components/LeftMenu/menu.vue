<template>
  <el-menu default-active="2"
           router
           class="el-menu-vertical"
           :collapse="menuCollapse">
    <el-sub-menu v-for="menu in menus"
                 :key="menu.label"
                 :index="menu.label">
      <template #title>
        <el-icon>
          <Files />
        </el-icon>
        <span>{{ menu.label }}</span>
      </template>
      <el-menu-item v-for="item in menu.children"
                    :key="item.index"
                    :index="item.index">{{ item.label }}</el-menu-item>
    </el-sub-menu>
  </el-menu>
</template>

<script setup>
import useAppStore from '../../store/modules/app'
import { Files } from '@element-plus/icons-vue'

const menuCollapse = computed(() => useAppStore().menuCollapse)
const menus = ref([])
menus.value = [
  {
    label: 'Element-plus',
    children: [
      { label: 'index', index: '/element' }
    ]
  },
  {
    label: 'Three.js',
    children: [
      { label: 'index', index: '/three' }
    ]
  },
  {
    label: 'Harp.gl',
    children: [
      { label: 'index', index: '/harp' }
    ]
  },
  {
    label: 'Others',
    children: [
      { label: 'suncalc', index: '/others/suncalc' },
      { label: '流光特效', index: '/others/canvas-light' },
      { label: 'bubbles', index: '/others/bubbles' },
      { label: '图片翻书效果', index: '/others/book-imgs' },
      { label: '水印', index: '/others/water-mark' }
    ]
  }
]
</script>

<style lang="scss" scoped>
.el-menu-vertical {
  height: 100%;
  overflow-y: auto;
  border-right: 0;
  display: flex;
  flex-direction: column;

  &:not(.el-menu--collapse) {
    width: 240px;
  }

  .brand {
    height: 60px;
    width: 100%;
    position: absolute;
    top: 0;
    left: 0;
    z-index: 1000;
    background-color: pink;
  }

  .empty {
    flex: 1;
  }
}
</style>
