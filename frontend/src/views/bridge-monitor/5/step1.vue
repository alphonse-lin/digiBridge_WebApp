<template>
  <div class="step-wrap">
    <div class="query-wrap">
      <el-form :inline="true"
               :model="queryForm"
               class="demo-form-inline">
        <el-form-item style="margin-bottom: 0;margin-right: 10px;">
          <el-input v-model="queryForm.name"
                    placeholder="Component Name" />
        </el-form-item>
        <el-form-item style="margin-bottom: 0;margin-right: 10px;">
          <el-input v-model="queryForm.bridgeName"
                    placeholder="Bridge Name" />
        </el-form-item>
        <el-form-item style="margin-bottom: 0;margin-right: 10px;">
          <el-date-picker v-model="queryForm.time"
                          type="date"
                          placeholder="Pick Date" />
        </el-form-item>
        <el-form-item style="margin-bottom: 0;margin-right: 10px;">
          <el-button type="primary"
                     :icon="Search"></el-button>
        </el-form-item>
      </el-form>
      <el-button :icon="Refresh"></el-button>
    </div>
    <el-table :data="tableData"
              border
              stripe>
      <el-table-column type="index"
                       width="50"
                       align="center" />
      <el-table-column v-for="col in columns"
                       :prop="col.id"
                       :key="col.id"
                       :label="col.label"
                       :width="col.width">
        <template #default="{ row }">
          <div v-if="col.id === 'imgs'"
               style="display: flex; align-items: center">
            <el-image v-for="(img, i) in row.srcList"
                      :key="img"
                      style="width: 20px;height: 20px;margin-right: 5px;border-radius: 2px;"
                      :src="img"
                      :preview-src-list="row.srcList"
                      :initial-index="i"
                      :preview-teleported="true" />
          </div>
          <div v-else>{{ row[col.id] }}</div>
        </template>
      </el-table-column>
      <el-table-column label="Operation"
                       width="180">
        <template #default="{ row }">
          <el-button type="primary"
                     link>Edit</el-button>
          <el-button type="danger"
                     link>Delete</el-button>
          <div style="display: none;">{{ row }}</div>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { Refresh, Search } from '@element-plus/icons-vue'
// eslint-disable-next-line
import corrosion1 from '/imgs/corrosion1.png'
// eslint-disable-next-line
import corrosion2 from '/imgs/corrosion2.png'
// eslint-disable-next-line
import crack1 from '/imgs/crack1.png'
// eslint-disable-next-line
import crack2 from '/imgs/crack2.png'

const queryForm = reactive({
  name: '',
  bridgeName: '',
  time: ''
})

// const props = defineProps()
// 部件名称、桥梁名称、巡检时间、巡检结果、巡检人员、备注
const columns = ref([
  { id: 'name', label: 'Component Name', width: '160' },
  { id: 'bridgeName', label: 'Bridge Name', width: '160' },
  { id: 'time', label: 'Inspection Time', width: '160' },
  { id: 'person', label: 'Inspector', width: '160' },
  { id: 'imgs', label: 'Photo' },
  { id: 'result', label: 'Result' },
  { id: 'pdf', label: 'Report' }
])
const tableData = ref([
  {
    name: 'Com 1',
    bridgeName: 'River Neath Swing Bridge',
    time: '2024-3-15',
    result: 'Corrosion: L5',
    person: 'Frank',
    pdf: '无',
    srcList: [corrosion1]
  },
  {
    name: 'Com 2',
    bridgeName: 'River Neath Swing Bridge',
    time: '2024-3-15',
    result: 'Corrosion: L4',
    person: 'Frank',
    pdf: '无',
    srcList: [corrosion2]
  },
  {
    name: 'Com 3',
    bridgeName: 'River Neath Swing Bridge',
    time: '2024-3-15',
    result: 'Crack: L3',
    person: 'Frank',
    pdf: '无',
    srcList: [crack1, crack2]
  }
])

// function fn () {}

onMounted(() => { })
onBeforeUnmount(() => { })
</script>

<style lang='scss'
       scoped>
      .step-wrap {
        height: 100%;
      }
    </style>
