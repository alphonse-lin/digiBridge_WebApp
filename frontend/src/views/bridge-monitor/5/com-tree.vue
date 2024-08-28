<template>
  <div class="com-wrap">
    <div class="filter-wrap">
      <el-input v-model="filterText"
                style="flex: 1;"
                placeholder="Filter keyword"
                clearable />
      <el-switch v-if="props.warnShow"
                 v-model="justUpdate"
                 :active-value="true"
                 :inactive-value="false"
                 style="margin-left: 10px;">
      </el-switch>
    </div>
    <div class="tree-wrap"
         ref="refTreeWrap">
      <el-tree class="tree"
               default-expand-all
               ref="refTree"
               :data="treeData"
               :props="defaultProps"
               :filter-node-method="filterNode"
               @node-click="onNodeClick" />
    </div>
  </div>
</template>

<script setup>
import bridgeCom from '@/api/bridgeCom.json'

const props = defineProps({
  warnShow: {
    type: Boolean,
    default: false
  }
})
const arr = bridgeCom.filter(v => v.mesh)
for (let i = 0; i < arr.length; i++) {
  arr[i].label = arr[i].name
  arr[i].index = i + 1
}
const justUpdate = ref(false)
const treeData = computed(v => {
  return justUpdate.value ? arr.filter(j => j.isUpdate) : arr
})
const customNodeClass = (data, node) => {
  if (data.isUpdate) {
    return 'is-update'
  }
  return null
}
const defaultProps = {
  children: 'children',
  label: 'label',
  class: customNodeClass
}
// 筛选
const filterText = ref('')
const refTree = ref(null)
watch(filterText, (val) => {
  refTree.value.filter(val)
})
const filterNode = (value, data) => {
  if (!value) return true
  return data.label.includes(value)
}

const emits = defineEmits(['node-click'])
function onNodeClick (node, data, TreeNode) {
  emits('node-click', { node, data, TreeNode })
}

onMounted(() => { })
onBeforeUnmount(() => { })
</script>

<style lang='scss'
       scoped>
      .com-wrap {
        flex: 1;
        height: 0;
        display: flex;
        flex-direction: column;

        .filter-wrap {
          display: flex;
          align-items: center;
          margin-bottom: 10px;
        }

        .tree-wrap {
          flex: 1;
          height: 0;
          overflow-y: auto;
        }
      }
    </style>
