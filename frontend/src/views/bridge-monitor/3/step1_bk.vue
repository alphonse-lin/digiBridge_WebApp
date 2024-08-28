<template>
  <div class="step-wrap">
    <!-- <div class="left-side">
      <el-image :src="comImg"
                fit="contain"
                style="width: 100%;height: 100%;"></el-image>
    </div> -->
    <div class="right-side">
      <el-form :model="form" ref="refForm" :rules="rules" label-width="130px" label-position="left" :inline="false">
        <el-row :gutter="20">
          <el-col :span="12" :offset="0">
            <el-form-item label="Bridge name">
              <el-input v-model="form.bridgeName"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12" :offset="0">
            <el-form-item label="Component ID">
              <el-input v-model="form.comName"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12" :offset="0">
            <el-form-item label="Inspector">
              <el-input v-model="form.inspector"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12" :offset="0">
            <el-form-item label="Time" prop="time">
              <div style="width: 100%;">
                <el-date-picker v-model="form.time" type="datetime" placeholder="Select date and time"
                  style="width: 100%;" />
              </div>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="Type" prop="type">
          <el-radio-group v-model="type" @change="onRadioChange">
            <el-radio value="Corrosion">Corrosion</el-radio>
            <el-radio value="Crack">Crack</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item prop="photo">
          <template #label>
            <div>
              <div>Photos</div>
              <div>
                <el-button type="primary" link @click="onSegmentClick">Segment Tool</el-button>
              </div>
            </div>
          </template>
          <div>
            <!-- eslint-disable-next-line -->
            <el-upload v-model:file-list="form.photo"
              action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15" list-type="picture-card"
              :auto-upload="false" :on-preview="handlePictureCardPreview" :on-remove="handleRemove"
              :on-change="handlePictureChange">
              <el-icon>
                <Plus />
              </el-icon>
            </el-upload>
          </div>
        </el-form-item>
        <el-form-item label="Description" prop="desc">
          <el-input v-model="form.desc" placeholder="Please input" type="textarea"
            :autosize="{ minRows: 4, maxRows: 6 }" clearable></el-input>
        </el-form-item>
      </el-form>
    </div>

    <!-- 图片查看 -->
    <el-dialog v-model="dialogVisible" append-to-body>
      <div style="width: 100%;height: 100%;">
        <img w-full :src="dialogImageUrl" alt="Preview Image" style="width: 100%;height: 100%;" />
      </div>
    </el-dialog>

    <SegmentImage ref="refSegmentImage"></SegmentImage>
  </div>
</template>

<script setup>
import { Plus } from '@element-plus/icons-vue'
// import comImg from '@/assets/detection/com.png'
// import corrosion1 from '@/assets/detection/corrosion1.png'
import { ElMessage } from 'element-plus'
import SegmentImage from '@/components/segment-image/index.vue'

// import crack2 from '@/assets/detection/crack2.png'
// import co1 from '@/assets/detection/co1.png'
// import co2 from '@/assets/detection/co2.png'
// import co3 from '@/assets/detection/co3.png'
// import co4 from '@/assets/detection/co4.png'
// import co5 from '@/assets/detection/co5.png'
// import co6 from '@/assets/detection/co6.png'
// import co7 from '@/assets/detection/co7.png'
// import co8 from '@/assets/detection/co8.png'
// import co9 from '@/assets/detection/co9.png'
// import co10 from '@/assets/detection/co10.png'

const props = defineProps({
  questionType: { type: String, default: 'Corrosion' },
  stepPanelShow: { type: Boolean, default: false }
})
const type = ref(props.questionType)
watch(
  () => props.questionType,
  (newVal) => {
    type.value = newVal
  }
)
// watch(
//   () => props.stepPanelShow,
//   (n) => {
//     if (n) {
//       // 随机4张腐蚀照片
//       if (props.questionType === 'Corrosion') {
//         const imgs = [co1, co2, co3, co4, co5, co6, co7, co8, co9, co10].sort(() => Math.random() - 0.5).slice(0, 3)
//         form.value.photo = imgs.map((v, i) => { return { name: `co-${i}`, url: v } })
//       } else {
//         form.value.photo = [{ name: 'crack1', url: crack2 }]
//       }
//     }
//   }
// )
const formDesc = computed(() => type.value === 'Corrosion' ? 'Corrosion' : 'Crack')
const form = ref({
  bridgeName: 'Bridge 1',
  comName: '#90527',
  inspector: 'Frank',
  time: new Date(),
  photo: [],
  desc: formDesc
})
const rules = ref({
  time: [{ required: true, message: 'Please select time', trigger: 'blur' }],
  photo: [{ required: true, message: 'Please upload photo', trigger: 'blur' }],
  desc: [{ required: true, message: 'Please input description', trigger: 'blur' }]
})
const refSegmentImage = ref(null)
function onSegmentClick() {
  refSegmentImage.value.changeVisible()
}

const dialogImageUrl = ref('')
const dialogVisible = ref(false)
const handleRemove = (uploadFile, uploadFiles) => {
  console.log(uploadFile, uploadFiles)
}
const handlePictureCardPreview = (uploadFile) => {
  dialogImageUrl.value = uploadFile.url
  dialogVisible.value = true
}
const refSegmentImg = ref(null)
const activeFile = ref(null)
const handlePictureChange = (file, fileList) => {
  console.log(file, fileList)
  activeFile.value = file
  refSegmentImg.value.changeVisible()
}
// function onConfirm (file) {
//   const { name, uid } = form.value.photo.pop()
//   file.name = name
//   file.uid = uid
//   form.value.photo.push(file)
// }

const refForm = ref(null)
function validateForm() {
  return new Promise((resolve, reject) => {
    refForm.value.validate((valid) => {
      if (valid) {
        resolve(true)
      } else {
        ElMessage.warning('Please fill in the form correctly!')
        resolve(false)
      }
    })
  })
}

const emits = defineEmits(['update:questionType'])
function onRadioChange(v) {
  emits('update:questionType', v)
}
function getImgs() {
  return form.value.photo
}

// 暴露方法给父组件
defineExpose({ validateForm, getImgs })
onMounted(() => { })
onBeforeUnmount(() => { })
</script>

<style lang='scss' scoped>
.step-wrap {
  height: 100%;
  display: flex;
  justify-content: space-between;
  align-items: stretch;

  .left-side {
    flex: 1;
    width: 0;
    height: 100%;
    background-color: #f5f7fa;
    padding: 20px;
  }

  .right-side {
    flex: 1;
    width: 0;
    height: 100%;
    margin-left: 20px;

    .el-form-item {
      margin-bottom: 20px;
    }
  }
}
</style>
