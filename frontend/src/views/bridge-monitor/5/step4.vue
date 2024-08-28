<template>
  <div class="step-wrap">
    <PdfPreview ref="refPdfPreview"></PdfPreview>
  </div>
</template>

<script setup>
import PdfPreview from '@/components/pdf-preview/index.vue'

const props = defineProps({
  activeStep: {
    type: Number,
    default: 0
  }
})
const refPdfPreview = ref(null)
watch(() => props.activeStep, (val) => {
  if (val === 3) {
    nextTick(() => {
      refPdfPreview.value.init()
    })
  }
})

onMounted(() => { })
onBeforeUnmount(() => { })
</script>

<style lang='scss'
       scoped>
      .step-wrap {
        height: 100%;
      }
    </style>
