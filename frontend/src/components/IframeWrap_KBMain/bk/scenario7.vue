<template>
  <div class="scenario">
    <h2>Bridge Material Condition Evaluation</h2>
    <div class="scope">
      <h3>Scope: Concrete Strength Evaluation 混凝土强度评定; Concrete Carbonation Depth Evaluation 混凝土碳化深度评定</h3>
    </div>
    <div class="scenario-image">
      <img src="/imgs/KBMain/Scenario-material1.png" alt="Maintenance Scenario 7" width=100%>
    </div>
    <div class="evaluation-input">
      <div class="input-group">
        <label>混凝土设计强度等级:</label>
        <input v-model="designStrength" type="number" step="0.1">
      </div>
      <div class="input-group">
        <label>混凝土实测强度值:</label>
        <input v-model="measuredStrength" type="number" step="0.1">
      </div>
      <div class="input-group">
        <label>测区混凝土碳化深度平均值:</label>
        <input v-model="carbonationDepth" type="number" step="0.1">
      </div>
      <div class="input-group">
        <label>实测保护层厚度平均值:</label>
        <input v-model="protectiveLayerThickness" type="number" step="0.1">
      </div>
      <button @click="evaluateCondition">Evaluate Condition</button>
    </div>
    <div v-if="evaluationResult" class="evaluation-result">
      <h3>Evaluation Result:</h3>
      <p>{{ evaluationResult }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Scenario7',
  data() {
    return {
      designStrength: null,
      measuredStrength: null,
      carbonationDepth: null,
      protectiveLayerThickness: null,
      evaluationResult: ''
    }
  },
  methods: {
    evaluateCondition() {
      // Here you would typically call an API or use a more complex logic
      // For demonstration, we'll just set a simple result
      this.evaluationResult = `Based on the input data:
        Design Strength: ${this.designStrength}
        Measured Strength: ${this.measuredStrength}
        Carbonation Depth: ${this.carbonationDepth}
        Protective Layer Thickness: ${this.protectiveLayerThickness}
        
        A full evaluation would be performed using the relevant Chinese standards.`
    }
  }
}
</script>

<style scoped>
.input-group {
  margin-bottom: 15px;
}
</style>
