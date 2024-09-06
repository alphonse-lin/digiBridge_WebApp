<template>
  <el-dialog :title="props.selected ? props.selected.label : 'Dialog'" v-model="visible" width="1000px">
    <div style="height: 100%;">
      <DroneSurvey v-if="selected.id && selected.id === '1-1'" @close-dialog="closeDialog"></DroneSurvey>
      <iframe v-else :src="props.selected.url" frameborder="0" width="100%" height="100%"></iframe>
    </div>
  </el-dialog>
</template>

<script setup>
import { ref } from 'vue'
import DroneSurvey from './DroneSurvey.vue'

const props = defineProps({
  selected: {
    type: Object,
    default: () => { }
  }
})

function closeDialog() {
  visible.value = false
}

// ... rest of the script remains unchanged
const visible = ref(false)
function changeVisible () {
  visible.value = !visible.value
}

// // 自定义事件，点击模型时，弹出面板
// const emits = defineEmits(['model-click'])

defineExpose({ changeVisible, closeDialog})
onMounted(() => { })
onBeforeUnmount(() => { })
</script>

<style lang='scss' scoped>
// ... styles remain unchanged</style>