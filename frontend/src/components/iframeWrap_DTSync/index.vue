<template>
    <el-dialog 
      :title="props.selected ? props.selected.label : 'Dialog'" 
      v-model="visible" 
      width="1000px"
      :destroy-on-close="true"
    >
      <div style="height: 100%;">
        <DTSync v-if="selected.id && selected.id === '2-2'"></DTSync>
        <iframe v-else :src="props.selected.url" frameborder="0" width="100%" height="100%"></iframe>
      </div>
    </el-dialog>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import DTSync from './DTSync.vue'
  
  const props = defineProps({
    selected: {
      type: Object,
      default: () => ({})
    }
  })
  
  const visible = ref(false)
  
  function changeVisible() {
    visible.value = !visible.value
  }
  
  defineExpose({ changeVisible })
  </script>
  
  <style lang='scss' scoped>
  :deep(.el-dialog__body) {
    height: calc(100vh - 200px);
    overflow-y: auto;
  }
  </style>