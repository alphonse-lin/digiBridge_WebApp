<template>
  <el-dialog
    :title="props.selected ? props.selected.label : 'Dialog'"
    v-model="visible"
    width="1000px">
    <div style="height: 100%;">
      <KBasedMaintenance
        :initialStep="currentStep"
      ></KBasedMaintenance>
    </div>
  </el-dialog>
</template>

<script setup>
import { ref } from 'vue'
import KBasedMaintenance from './KBasedMaintenance.vue'

const props = defineProps({
  selected: {
    type: Object,
    default: () => ({})
  },
  showScenario: {
    type: Boolean,
    default: false
  }
})

const visible = ref(false)
const currentStep = ref(0)

function changeVisible(step = 0) {
  visible.value = !visible.value
  currentStep.value = step
}

defineExpose({ changeVisible })
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