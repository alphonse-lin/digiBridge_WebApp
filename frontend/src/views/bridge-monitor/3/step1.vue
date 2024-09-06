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

    <SegmentImage ref="refSegmentImage" @imageSegmented="handleSegmentedImage"></SegmentImage>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { Plus } from '@element-plus/icons-vue'
// import comImg from '@/assets/detection/com.png'
import defaultImage from '@/assets/detection/download.png'
import { ElMessage } from 'element-plus'
import SegmentImage from '@/components/segment-image/index.vue'


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
const formDesc = computed(() => type.value === 'Corrosion' ? 'Corrosion' : 'Crack')
const form = ref({
  bridgeName: 'Bridge 1',
  comName: '#90527',
  inspector: 'Frank',
  time: new Date(),
  photo: [   
    {
      name: 'default-image.jpg',
      url: defaultImage
    }],
  desc: formDesc
})

function setImage(imageData) {
  console.log('Setting image in Step1:', imageData) // 添加这行来调试
  if (imageData && imageData.file && imageData.url) {
    form.value.photo = [{
      name: imageData.file,
      url: imageData.url
    }]
  } else {
    console.error('Invalid imageData received in Step1:', imageData)
  }
}

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
// const handlePictureChange = (file, fileList) => {
//   console.log(file, fileList)
//   activeFile.value = file
//   refSegmentImg.value.changeVisible()
  
//   // 如果是第一次上传，替换默认图片
//   if (form.value.photo.length === 1 && form.value.photo[0].name === 'default-image.jpg') {
//     form.value.photo = fileList
//   }
// }

const handlePictureChange = (file, fileList) => {
  console.log(file, fileList)
  activeFile.value = file
  refSegmentImg.value.changeVisible()
  
  // If it's the first upload, replace the default image
  if (form.value.photo.length === 1 && form.value.photo[0].name === 'default-image.jpg') {
    form.value.photo = fileList
  }
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

function handleSegmentedImage(imageData) {
  console.log('Received segmented image in Step1:', imageData)
  if (imageData && imageData.url) {
    form.value.photo = [{
      name: imageData.name,
      url: imageData.url
    }]
    // 通知父组件图片已更新
    emits('segmentedImageUpdated', imageData)
  } else {
    console.error('Invalid imageData received in Step1:', imageData)
  }
}

const emits = defineEmits(['update:questionType', 'segmentedImageUpdated'])
function onRadioChange(v) {
  emits('update:questionType', v)
}
function getImgs() {
  return form.value.photo
}

// 暴露方法给父组件
defineExpose({ validateForm, getImgs, setImage })
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
