<template>
  <div class="scenario-content">
    <h2>Bridge Material Condition Evaluation</h2>
    
    <div class="sub-section">
      <h3>Scenario Introduction</h3>
      <h4>Scope: Concrete Strength Evaluation 混凝土强度评定; Concrete Carbonation Depth Evaluation 混凝土碳化深度评定</h4>
      <img src="/imgs/KBMain/Scenario-material1.png" alt="Maintenance Scenario 7" class="scenario-image">
    </div>

    <div class="sub-section user-input">
      <h3>Scenario Implementation (User Input)</h3>
      <h4>·input material condition parameters</h4>
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
      <button @click="evaluateCondition">Run the reasoner</button>

      <div v-if="evaluationResult" class="reasoning-result">
        <h4>·reasoning result</h4>
        <p>{{ evaluationResult }}</p>
      </div>
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
.scenario-content {
  font-family: Arial, sans-serif;
}

.sub-section {
  margin-bottom: 20px;
  padding: 15px;
  border-radius: 5px;
}

.introduction {
  background-color: #f8e5e5; /* 浅粉色 */
}

.user-input {
  background-color: #e5f8e5; /* 浅绿色 */
}

h2, h3, h4 {
  color: #333;
}

.scenario-image {
  max-width: 100%;
  height: auto;
  margin-top: 10px;
}

.input-group {
  margin-bottom: 10px;
}

.input-group label {
  display: block;
  margin-bottom: 5px;
}

input[type="number"] {
  width: 100%;
  padding: 5px;
  margin-bottom: 10px;
}

button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}

.reasoning-result {
  margin-top: 20px;
  padding: 10px;
  background-color: #f0f0f0;
  border-radius: 4px;
}
</style>