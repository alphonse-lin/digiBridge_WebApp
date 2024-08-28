<template>
  <el-dialog v-model="dialogVisible"
             title="Segment Image"
             width="1200px"
             append-to-body
             class="custom-dialog">
    <div class="custom-dialog-body">
      <iframe src="http://sam.qianqianzhushou.cn"
              frameborder="0"
              style="width: 100%;height: 100%;border: none;"></iframe>
    </div>
  </el-dialog>
</template>

<script setup>
const dialogVisible = ref(false)
function changeVisible () {
  dialogVisible.value = !dialogVisible.value
}

// 暴露方法给父组件
defineExpose({ changeVisible })
onMounted(() => { })
onBeforeUnmount(() => { })
</script>

<style lang="scss" scoped>
.custom-dialog-body {
  height: 700px;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
