<template>
  <el-dialog :title="props.selected ? props.selected.label : 'Dialog'"
             v-model="visible"
             width="1500px">
    <div style="height: 80vh;">
      <iframe :src="props.selected.url"
              frameborder="0"
              width="100%"
              height="100%"></iframe>
    </div>
  </el-dialog>
</template>

<script setup>
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

<style lang='scss' scoped>
.wrap-dom {
  transition: all 0.3s;
  width: 1000px;
  max-height: calc(100vh - 100px);
  overflow-y: auto;
  background-color: var(--el-bg-color);
  border-radius: 4px;
  padding: 14px;
  box-shadow: var(--el-box-shadow);

  position: fixed;
  left: 50%;
  transform: translateX(-50%);
  top: 80px;
  z-index: 110;
}
</style>
