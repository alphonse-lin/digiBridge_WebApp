<template>
    <el-dialog :title="props.selected ? props.selected.label : 'Dialog'" v-model="visible" width="1000px">
        <div style="height: 100%;">
            <IoTSensors v-if="selected.id && selected.id === '1-2'"></IoTSensors>
            <iframe v-else :src="props.selected.url" frameborder="0" width="100%" height="100%"></iframe>
        </div>
    </el-dialog>
</template>

<script setup>
import { ref } from 'vue'
import IoTSensors from './IoTSensors.vue'

const props = defineProps({
    selected: {
        type: Object,
        default: () => { }
    }
})

// ... rest of the script remains unchanged
const visible = ref(false)
function changeVisible() {
    visible.value = !visible.value
}

defineExpose({ changeVisible })
onMounted(() => { })
onBeforeUnmount(() => { })
</script>

<style lang='scss' scoped>
// ... styles remain unchanged</style>