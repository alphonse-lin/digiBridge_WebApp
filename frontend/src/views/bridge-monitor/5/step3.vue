<template>
  <div ref="stepW"
       class="step-wrap">
    <iframe src="https://book.douban.com/"
            frameborder="0"
            width="100%"
            :height="height"></iframe>
  </div>
</template>

<script setup>
const props = defineProps({
  activeStep: {
    type: Number,
    default: 0
  }
})
watch(
  () => props.activeStep,
  (n) => {
    if (n === 2) {
      setTimeout(() => {
        comHeight()
      }, 200)
    }
  },
  { immediate: true }
)
const stepW = ref(null)
const height = ref(100)
function comHeight () {
  height.value = stepW.value.clientHeight - 10 + 'px'
  console.log('%c height.value: ', 'background-color: pink', height.value)
}

onMounted(() => { })
onBeforeUnmount(() => { })
</script>

<style lang='scss' scoped>
.step-wrap {
  min-height: 100%;
}
</style>
