<template>
  <el-dialog v-model="dialogVisible"
             title="Segment Image"
             width="1200px"
             append-to-body
             class="custom-dialog">
    <div class="custom-dialog-body">
      <iframe src="http://localhost:8080/"
              frameborder="0"
              style="width: 100%;height: 100%;border: none;"
              @load="setupMessageListener"></iframe>
    </div>
  </el-dialog>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const dialogVisible = ref(false)

const emit = defineEmits(['imageSegmented'])

function changeVisible () {
  dialogVisible.value = !dialogVisible.value
}

function setupMessageListener() {
  window.addEventListener('message', handleMessage)
}

function handleMessage(event) {
  // 确保消息来自你信任的源
  if (event.origin !== "http://localhost:8080") return;

  if (event.data.type === 'IMAGE_SAVED') {
    const imageUrl = 'imgs/cutOut/' + event.data.data.filename
    console.log('Segmented image saved:', imageUrl)
    dialogVisible.value = false
    // 发射事件，将图片信息传递给父组件
    emit('imageSegmented', { url: imageUrl, name: event.data.data.filename })
  }
}

// 暴露方法给父组件
defineExpose({ changeVisible })
onMounted(() => {
  setupMessageListener()
})

onBeforeUnmount(() => {
  window.removeEventListener('message', handleMessage)
})
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
