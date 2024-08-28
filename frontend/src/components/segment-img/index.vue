<template>
  <el-dialog v-model="dialogVisible"
             title="Segment Image"
             width="1200px"
             append-to-body
             class="custom-dialog"
             :close-on-click-modal="false"
             @open="onOpen">
    <div class="dialog-body">
      <canvas id="outputCanvas"
              width="1168"
              height="600"></canvas>
      <img id="image1"
           :src="imgUrl"
           alt="imgUrl"
           @click="handleMouseMove">
      <img v-if="contextStore.maskImg"
           id="image2"
           :src="contextStore.maskImg?.src"
           alt="maskImg"
           class="img-top">
    </div>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="onCancel">Cancel</el-button>
        <el-button type="primary"
                   @click="onConfirm">Confirm</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { InferenceSession, Tensor } from 'onnxruntime-web'
import npyjs from 'npyjs'
import { throttle } from 'underscore'
import { useContextStore } from '@/store/modules/context.js'
import * as ort from 'onnxruntime-web'
import { base64ToFile } from '@/utils/index.js'

import { handleImageScale } from './helpers/scaleHelper.js'
import { onnxMaskToImage } from './helpers/maskUtils.js'
import { modelData } from './helpers/onnxModelAPI.js'

const props = defineProps({
  activeFile: {
    type: Object,
    default: () => { }
  }
})

const dialogVisible = ref(false)
function changeVisible () {
  dialogVisible.value = !dialogVisible.value
}

const imgUrl = ref('')
watch(() => props.activeFile,
  (n) => {
    if (n && n !== null) {
      imgUrl.value = n.url
    }
  }, { deep: true, immediate: true })

// Onnxruntime configuration
ort.env.debug = false
// set global logging level
ort.env.logLevel = 'verbose'
// override path of wasm files - for each file
ort.env.wasm.numThreads = 2
ort.env.wasm.simd = true
// ort.env.wasm.proxy = true;
ort.env.wasm.wasmPaths = {
  'ort-wasm.wasm': import.meta.env.VITE_APP_ORT_WASM,
  'ort-wasm-simd.wasm': import.meta.env.VITE_APP_ORT_WASM_SIMD,
  'ort-wasm-threaded.wasm': import.meta.env.VITE_APP_ORT_WASM_THREADED,
  'ort-wasm-simd-threaded.wasm': import.meta.env.VITE_APP_ORT_WASM_SIMD_THREADED
}

// Define embedding and model paths
const IMAGE_EMBEDDING = './src/assets/onnx/sam_embedding.npy'
const MODEL_DIR = './src/assets/onnx/sam_onnx_quantized.onnx'

const model = ref(null)
const tensor = ref(null)
const modelScale = ref(null)
// 图片加载成功
function loadImage (url) {
  return new Promise((resolve, reject) => {
    const img = new Image()
    img.src = url
    img.onload = () => {
      const { height, width, samScale } = handleImageScale(img)

      modelScale.value = {
        height, // 原始图像大小
        width, // 原始图像大小
        samScale // 被调整到最长边长1024的图像的缩放比例
      }

      img.width = width
      img.height = height
      contextStore.setImage(img)
      resolve()
    }
  })
}
/**
 * 获取鼠标位置并将(x, y)坐标缩放回原始图像的比例。\
 * 使用setClicks更新点击状态， 并通过App.tsx中的useEffect ，触发ONNX模型运行生成一个新的mask
 */
function handleMouseMove (event) {
  const fn = (e) => {
    const el = e.target
    const rect = el.getBoundingClientRect()
    let x = e.clientX - rect.left
    let y = e.clientY - rect.top
    const imageScale = contextStore.image
      ? contextStore.image.width / el.offsetWidth
      : 1
    x *= imageScale
    y *= imageScale
    const click = { x, y, clickType: 1 }
    if (click) contextStore.setClicks([click])
  }
  throttle(fn(event), 15)
}
async function initModel () {
  try {
    InferenceSession.create(MODEL_DIR)
      .then(async (session) => {
        model.value = session
        tensor.value = await loadNpyTensor(IMAGE_EMBEDDING, 'float32')
      })
  } catch (e) {
    console.log(e)
  }
}
// 解码 Numpy 文件成一个张量
async function loadNpyTensor (tensorFile, dType) {
  // eslint-disable-next-line
  const npLoader = new npyjs()
  const npArray = await npLoader.load(tensorFile)
  // @ts-ignore
  const tensor = new Tensor(dType, npArray.data, npArray.shape)
  return tensor
}
/**
 *  跑ONNX模型
 */
const contextStore = useContextStore()
async function runONNX () {
  try {
    if (
      model.value === null ||
      contextStore.clicks === null ||
      tensor.value === null ||
      modelScale.value === null
    ) {
      // xx
    } else {
      const feeds = modelData({
        clicks: contextStore.clicks,
        tensor: tensor.value,
        modelScale: modelScale.value
      })
      if (feeds === undefined) return

      // Run the SAM ONNX model with the feeds returned from modelData()
      const results = await model.value?.run(feeds)
      const output = results[model.value?.outputNames[0]]

      // The predicted mask returned from the ONNX model is an array which is
      // rendered as an HTML image using onnxMaskToImage() from maskUtils.tsx.
      contextStore.setMaskImg(
        onnxMaskToImage(output.data, output.dims[2], output.dims[3])
      )
    }
  } catch (e) {
    console.log(e)
  }
}
watch(
  () => contextStore.clicks,
  () => {
    runONNX()
  })

async function onOpen () {
  await loadImage(imgUrl.value)
  initModel()
}
const emits = defineEmits(['cancel', 'confirm'])
function onCancel () {
  dialogVisible.value = false
  emits('cancel')
}
function mergeImages () {
  const canvas = document.getElementById('outputCanvas')
  const ctx = canvas.getContext('2d')
  const img1 = document.getElementById('image1')
  const img2 = document.getElementById('image2')

  // 设置 canvas 的尺寸
  canvas.width = Math.max(img1.width, img2.width)
  canvas.height = Math.max(img1.height, img2.height)
  const { width, height } = modelScale.value

  // 绘制第一张图片
  ctx.drawImage(img1, 0, 0, width / 2, height / 2)
  // 绘制第二张图片
  ctx.globalAlpha = 0.5
  ctx.drawImage(img2, 0, 0, width / 2, height / 2)
  const dataUrl = canvas.toDataURL('image/png')
  return dataUrl
}
function onConfirm () {
  const fileName = 'mask.png'
  const b64 = mergeImages()
  const rawObj = base64ToFile(b64.split(',')[1], fileName)
  const file = {
    name: fileName,
    percentage: 0,
    status: 'ready',
    size: rawObj.file.size,
    raw: rawObj.file,
    uid: rawObj.file.lastModified,
    url: rawObj.blobUrl
  }
  // console.log('%c file: ', 'background-color: pink', file)
  emits('confirm', file)
  contextStore.setMaskImg(null)
  dialogVisible.value = false
}

// 暴露方法给父组件
defineExpose({ changeVisible })
onMounted(() => { })
onBeforeUnmount(() => { })
</script>

<style lang='scss' scoped>
.dialog-body {
  height: 600px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: relative;

  #outputCanvas {
    position: absolute;
    top: 0;
    left: 0;
    z-index: -1
  }

  img {
    width: auto;
    height: 100%;
    object-fit: contain;
  }

  .img-top {
    position: absolute;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    z-index: 2;
    opacity: 0.5;
    pointer-events: none;
  }
}
</style>
