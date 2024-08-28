<template>
  <el-dialog v-model="dialogVisible"
             title="Intelligent Assistant"
             width="860px"
             draggable
             append-to-body
             class="custom-dialog">
    <div class="custom-dialog-body">
      <ChatCom :showBg="false"></ChatCom>
    </div>
  </el-dialog>
</template>

<script setup>
import ChatCom from './index.vue'

const dialogVisible = ref(false)
function changeVisible () {
  dialogVisible.value = !dialogVisible.value
}

// 暴露方法给父组件
defineExpose({ changeVisible })
onMounted(() => { })
onBeforeUnmount(() => { })
</script>

<style lang='scss'
       scoped>
      .custom-dialog-body {
        height: 700px;
        width: 800px;
        display: flex;
        justify-content: space-between;
        align-items: center;

        .qa-list {
          min-width: 420px;
        }

        .xz-chat-wrap .input {
          width: 420px;
          height: 50px;
          background: transparent;
        }

        .xz-chat-wrap .content {
          width: 400px;
          height: 100%;
          margin: 0 auto;
          padding: 80px 0 100px;
          position: relative;
          z-index: 3;
          overflow-y: auto;
        }
      }
    </style>
