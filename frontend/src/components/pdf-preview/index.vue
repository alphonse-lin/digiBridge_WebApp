<template>
  <div v-loading="pdfLoading"
       element-loading-text="Loading PDF..."
       class="doc-wrap">
    <div v-for="(item, index) in pageNum"
         :key="item">
      <div class="canvas-wrap">
        <canvas :id="`pdf-canvas-${item}`"></canvas>
        <span class="page-num">Page {{ index + 1 }} of {{ pageNum }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import * as pdfJs from 'pdfjs-dist'
import 'pdfjs-dist/build/pdf.worker.entry'
import testPdf from './detection-result.pdf'

const pdfPath = ref(null)
const pdfLoading = ref(true)
const pageNum = ref(0)
let pdfCtx = null
const defaultWidth = 1000

function init (path) {
  pdfPath.value = null
  // pdfPath.value = path
  pdfPath.value = testPdf
  pdfLoading.value = true

  setTimeout(() => {
    pdfJs.getDocument(pdfPath.value)
      .promise
      .then((pdf) => {
        pdfCtx = pdf
        pageNum.value = pdf.numPages
        nextTick(() => {
          renderPdf(1)
        })
      })
      .catch((err) => {
        console.log('%c PDF 加载失败: ', 'background-color: pink', err)
      })
      .finally(() => {
        pdfLoading.value = false
      })
  }, 1500)
}

function renderPdf (num = 1) {
  pdfCtx.getPage(num)
    .then((page) => {
      const canvas = document.getElementById(`pdf-canvas-${num}`)
      const ctx = canvas.getContext('2d')

      const canvasWidth = (defaultWidth - 60) > 1000 ? 1000 : (defaultWidth - 60)

      const viewport2 = page.getViewport({ scale: 1 })
      const viewportRatio = viewport2.height / viewport2.width
      const scale1 = canvasWidth / viewport2.width
      const viewport = page.getViewport({ scale: scale1 })
      const canvasHeight = Math.floor(canvasWidth * viewportRatio)
      const scale = 1
      canvas.width = canvasWidth * scale
      canvas.height = canvasHeight * scale

      // canvas css 宽高
      canvas.style.width = `${canvasWidth * scale}px`
      canvas.style.height = `${canvasHeight * scale}px`

      page.render({
        canvasContext: ctx,
        viewport
      })

      if (num < pageNum.value) {
        renderPdf(num + 1)
      } else {
        pdfLoading.value = false
      }
    })
}

defineExpose({ init })
</script>

<style lang='scss'
       scoped>
      .doc-wrap {
        width: 100%;
        height: 100%;
        overflow-y: auto;

        .canvas-wrap {
          max-width: 1000px;
          margin: 0 auto;
          position: relative;
          border: 3px solid var(--el-fill-color-light);
          border-top-width: 1.5px;
          border-bottom-width: 1.5px;

          .page-num {
            width: 140px;
            position: absolute;
            bottom: 20px;
            left: 50%;
            margin-left: -70px;
            text-align: center;
            font-size: 14px;
            color: var(--el-color-primary);
          }
        }
      }
    </style>
