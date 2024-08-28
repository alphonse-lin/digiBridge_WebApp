<template>
  <el-dialog
    :title="props.selected ? props.selected.label : 'Dialog'"
    v-model="visible"
    width="1000px">
    <div style="height: 100%;">
      <KBasedMaintenance
        v-if="selected.id && selected.id === '4-1-1'"></KBasedMaintenance>
      <iframe v-else>
        :src="props.selected.url"
        frameborder="0"
        width="100%"
        height="100%"></iframe>
    </div>
</el-dialog>
</template>

<script setup>
import { ref } from 'vue'
import KBasedMaintenance from './KBasedMaintenance.vue';

const props = defineProps({
  selected: {
    type: Object,
    default: () => { }
  }
})

// watch(
//   () => props.selected,
//   (n) => {
//     console.log('%c n: ', 'background-color: pink', n)
//   },
//   { immediate: true, deep: true }
// )

const visible = ref(false)
function changeVisible () {
  visible.value = !visible.value
}

defineExpose({ changeVisible })
onMounted(() => { })
onBeforeUnmount(() => { })
</script>

<style scoped>
.knowledge-based-maintenance {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.module-buttons {
  display: flex;
  justify-content: center;
  padding: 20px;
  background-color: #f0f0f0;
}

.module-buttons .el-button {
  margin: 0 10px;
}

.iframe-container {
  flex-grow: 1;
  overflow: hidden;
}

iframe {
  border: none;
}
</style>