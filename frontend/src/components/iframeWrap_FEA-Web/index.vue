<template>
    <el-dialog :title="props.selected ? props.selected.label : 'Dialog'" v-model="visible" width="1000px">
      <div style="height: 100%;">
        <FEAWeb v-if="selected.id && selected.id === '3-1-1'"></FEAWeb>
        <iframe v-else :src="props.selected.url" frameborder="0" width="100%" height="100%"></iframe>
      </div>
    </el-dialog>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import FEAWeb from './FEAWeb.vue'
  
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
  // ... styles remain unchanged
  </style>