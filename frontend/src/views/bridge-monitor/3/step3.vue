<template>
  <div class="step-wrap">
    <div v-if="props.questionType === 'Corrosion'" class="left-side side">
      <img :src="firstImageSrc" alt="segmented_image" class="img">
      <img :src="secondImageSrc" alt="processed_image" class="img">
    </div>
    <div v-else class="left-side side">
      <img :src="props.result ? props.result.segmented_image_url : crack2" alt="crack2" class="img">
      <img :src="props.result ? props.result.image_url : crack3" alt="crack3" class="img">
    </div>
    <div class="right-side side">
      <el-form v-if="props.questionType === 'Corrosion'" label-width="230px" label-position="left" :inline="false">
        <el-form-item label="Good percentage" style="margin-bottom: 25px;">
          <div class="form-inner">
            <div style="flex: 1;">
              <el-progress :text-inside="true" :stroke-width="24" :percentage="31.19" status="warning" />
            </div>
          </div>
        </el-form-item>
        <el-form-item label="Mild corrosion percentage" style="margin-bottom: 25px;">
          <div class="form-inner">
            <div style="flex: 1;">
              <el-progress :text-inside="true" :stroke-width="24" :percentage="35.16" status="success" />
            </div>
          </div>
        </el-form-item>
        <el-form-item label="Severe corrosion percentage" style="margin-bottom: 25px;">
          <div class="form-inner">
            <div style="flex: 1;">
              <el-progress :text-inside="true" :stroke-width="24" :percentage="33.65" status="success" />
            </div>
          </div>
        </el-form-item>
        <el-form-item label="Total corrosion percentage" style="margin-bottom: 25px;">
          <div class="form-inner">
            <div style="flex: 1;">
              <el-progress :text-inside="true" :stroke-width="24" :percentage="68.81" status="warning" />
            </div>
          </div>
        </el-form-item>
        <el-form-item label="Predicted solution" style="margin-bottom: 25px;">
          <div class="form-inner">cut out corroded section and apply radius for paint system.</div>
        </el-form-item>
        <el-form-item label="Ground truth" style="margin-bottom: 25px;">
          <div class="form-inner">cut out corroded section and apply radius for paint system.</div>
        </el-form-item>
      </el-form>
      <el-form v-else label-width="230px" label-position="left" :inline="false">
        <el-form-item label="Crack number" style="margin-bottom: 25px;">
          <div class="form-inner">
            <div style="flex: 1;">
              <el-progress :text-inside="true" :stroke-width="24" :percentage="30" status="warning">
                <template #default="{ percentage }">
                  <div>{{ percentage }}</div>
                </template>
              </el-progress>
            </div>
          </div>
        </el-form-item>
        <el-form-item label="Crack length" style="margin-bottom: 25px;">
          <div class="form-inner">
            <div style="flex: 1;">
              <el-progress :text-inside="true" :stroke-width="24" :percentage="25.8" status="success">
                <template #default="{ percentage }">
                  <div>{{ percentage }} m</div>
                </template>
              </el-progress>
            </div>
          </div>
        </el-form-item>
        <el-form-item label="Crack depth" style="margin-bottom: 25px;">
          <div class="form-inner">
            <div style="flex: 1;">
              <el-progress :text-inside="true" :stroke-width="24" :percentage="33.65" status="success">
                <template #default="{ percentage }">
                  <div>{{ percentage }} cm</div>
                </template>
              </el-progress>
            </div>
          </div>
        </el-form-item>
        <el-form-item label="Predicted solution" style="margin-bottom: 25px;">
          <div class="form-inner">Structural reinforcement techniques such as steel reinforcement and filling seismic
            materials to repair and strengthen the cracks, enhancing the structural stability and safety of the
            building.</div>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import corrosion2 from '@/assets/detection/corrosion2.png'
import corrosion3 from '@/assets/detection/corrosion3.png'
import crack2 from '@/assets/detection/crack2.png'
import crack3 from '@/assets/detection/crack3.png'

const props = defineProps({
  // activeStep: {
  //   type: Number,
  //   default: 0
  // },
  questionType: {
    type: String,
    default: ''
  },
  result: {
    type: Object,
    default: () => ({})
  },
  segmentedImageData: {
    type: Object,
    default: null
  },

})

const localSegmentedImageData = ref(null)

watch(() => props.segmentedImageData, (newVal) => {
  console.log('segmentedImageData in Step3:', newVal)
  localSegmentedImageData.value = newVal
}, { immediate: true, deep: true })

watch(() => props.result, (newVal) => {
  console.log('result in Step3:', newVal)
}, { immediate: true, deep: true })

const firstImageSrc = computed(() => {
  console.log('Computing firstImageSrc:', localSegmentedImageData.value)
  if (localSegmentedImageData.value && localSegmentedImageData.value.url) {
    return localSegmentedImageData.value.url
  }
  return props.questionType === 'Corrosion' ? corrosion2 : crack2
})

const secondImageSrc = computed(() => {
  console.log('Computing secondImageSrc:', props.result)
  if (props.result && props.result.image_url) {
    return props.result.image_url
  }
  return props.questionType === 'Corrosion' ? corrosion3 : crack3
})

onMounted((
  
) => { })
onBeforeUnmount(() => { })
</script>

<style lang='scss' scoped>
.step-wrap {
  height: 100%;
  display: flex;
  align-items: stretch;

  .side {
    flex: 1;
    height: 100%;

    &.left-side {
      display: flex;
      align-items: center;
      justify-content: space-around;

      .img {
        flex: 1;
        width: 0;
        height: 100%;
        object-fit: contain;
      }
    }

    &.right-side {
      padding: 20px;

      .form-inner {
        width: 100%;
        display: flex;
        align-items: center;

        >div {
          &:first-child {
            font-weight: bold;
          }
        }
      }
    }
  }
}
</style>