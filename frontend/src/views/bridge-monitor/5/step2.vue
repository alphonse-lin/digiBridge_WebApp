<template>
  <div class="step-wrap">
    <div id="mountNode"
         style="height: 100%;"></div>
  </div>
</template>

<script setup>
import G6 from '@antv/g6'
import testData from './test.json'

const props = defineProps({
  activeStep: {
    type: Number,
    default: 0
  }
})
watch(() => props.activeStep, () => {
  if (props.activeStep === 1) {
    dataParse()
    setTimeout(() => {
      initGraphChart()
    }, 1000)
  }
})

let d = {}
function dataParse () {
  const nodeAttributes = testData.classAttribute.map(v => {
    const keys = Object.keys(v.label)
    return {
      id: v.id,
      label: typeof v.label === 'string' ? v.label : v.label[keys[0]],
      individuals: v.individuals
    }
  })
  const nodes = testData.class.map(v => {
    const obj1 = {
      id: v.id,
      label: v.type,
      cluster: v.type
    }
    const obj2 = nodeAttributes.find(j => j.id === v.id)
    return Object.assign({}, obj1, obj2 || {})
  })
  const edges = testData.propertyAttribute.filter(v => v.domain !== v.range).map(v => {
    return {
      source: v.domain,
      target: v.range,
      label: typeof v.label === 'string' ? v.label : v.label['IRI-based']
    }
  })
  d = { nodes, edges }
}

const graph = shallowRef(null)
function initGraphChart () {
  const colors = ['#BDD2FD', '#BDEFDB', '#C2C8D5', '#FBE5A2', '#F6C3B7', '#B6E3F5', '#D3C6EA', '#FFD8B8', '#AAD8D8', '#FFD6E7']
  const strokes = ['#5B8FF9', '#5AD8A6', '#5D7092', '#F6BD16', '#E8684A', '#6DC8EC', '#9270CA', '#FF9D4D', '#269A99', '#FF99C3']

  const nodes = d.nodes
  const clusterMap = new Map()
  let clusterId = 0
  nodes.forEach(function (node) {
    // cluster
    if (node.cluster && clusterMap.get(node.cluster) === undefined) {
      clusterMap.set(node.cluster, clusterId)
      clusterId++
    }
    const cid = clusterMap.get(node.cluster)
    if (!node.style) {
      node.style = {}
    }
    node.style.fill = colors[cid % colors.length]
    node.style.stroke = strokes[cid % strokes.length]
  })

  const container = document.getElementById('mountNode')
  const width = container.clientWidth || 800
  const height = container.clientHeight || 500
  graph.value = new G6.Graph({
    container: 'mountNode', // 容器 id 或容器本身
    width, // Number，必须，图的宽度
    height, // Number，必须，图的高度
    // fitView: true,
    // fitCenter: true,
    modes: {
      default: ['drag-canvas', 'drag-node', 'zoom-canvas']
    },
    layout: {
      type: 'force2',
      preventOverlap: true,
      linkDistance: 150, // 可选，边长
      nodeSize: 80,
      workerEnabled: true,
      gpuEnabled: true,
      width,
      height
    },
    // layout: {
    //   type: 'forceAtlas2',
    //   preventOverlap: true,
    //   kr: 80,
    //   center: [300, 300]
    // },
    animate: true,
    defaultNode: {
      // type: 'rect',
      // size: [100, 50]
      size: 80
    },
    defaultEdge: {
      style: {
        endArrow: {
          path: 'M 0,0 L 8,4 L 8,-4 Z',
          fill: '#e2e2e2'
        }
      }
    }
  })
  graph.value.data(d)
  graph.value.render()
}

onMounted(() => { })
onBeforeUnmount(() => { })
</script>

<style lang='scss'
       scoped>
      .step-wrap {
        height: 100%;
      }
    </style>
