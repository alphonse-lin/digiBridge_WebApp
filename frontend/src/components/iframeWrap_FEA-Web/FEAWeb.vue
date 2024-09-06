<template>
    <div class="fea-web">
      <div class="fea-intro">
        <h2>FEA Ansys Introduction</h2>
        <p>FEA (Finite Element Analysis) is a computerized method for predicting how a product reacts to real-world forces, vibration, heat, fluid flow, and other physical effects. Ansys is a popular software for performing FEA simulations.</p>
      </div>
      <div class="fea-buttons">
        <el-button type="primary" @click="showResult(1)">Show Result 1</el-button>
        <el-button type="primary" @click="showResult(4)">Show Result 4</el-button>
      </div>
      <div class="fea-content">
        <iframe :src="iframeSrc" style="width: 100%; height: 900px; border: none;"></iframe>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue'
  
  const currentResult = ref(1)
  
  const app = "https://kitware.github.io/paraview-glance/app"
  const datadir = "https://raw.githubusercontent.com/cc288/Ansys_Paraview_Web/main/"
  
  const iframeSrc = computed(() => {
    const file = `file${currentResult.value}.vtk`
    return `${app}?name=${file}&url=${datadir}${file}`
  })
  
  const showResult = (resultNumber) => {
    currentResult.value = resultNumber
  }
  </script>
  
  <style scoped>
  .fea-web {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
  
  .fea-intro, .fea-buttons {
    padding: 20px;
    border: 1px solid #eee;
    border-radius: 5px;
  }
  
  .fea-buttons {
    display: flex;
    justify-content: space-around;
  }
  </style>