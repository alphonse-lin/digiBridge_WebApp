<template>
  <div class="scenario-content">
    <h2>Bridge Safety Performance Evaluation</h2>
    
    <div class="sub-section">
      <h3>Scenario Introduction</h3>
      <img src="/imgs/KBMain/Scenario-Safety.png" alt="Bridge Safety Performance Evaluation" class="scenario-image">
    </div>

    <div class="sub-section user-input">
      <h3>Scenario Implementation (User Input)</h3>
      <h4>·input safety performance parameters</h4>
      <div class="input-group">
        <label>Bridge Age (years):</label>
        <input v-model.number="bridgeAge" type="number" min="0">
      </div>
      <div class="input-group">
        <label>Last Inspection Date:</label>
        <input v-model="lastInspectionDate" type="date">
      </div>
      <div class="input-group">
        <label>Observed Structural Issues:</label>
        <textarea v-model="structuralIssues" rows="3"></textarea>
      </div>
      <div class="input-group">
        <label>Traffic Load (tons/day):</label>
        <input v-model.number="trafficLoad" type="number" min="0">
      </div>
      <div class="input-group">
        <label>Environmental Conditions:</label>
        <select v-model="environmentalConditions">
          <option>Mild</option>
          <option>Moderate</option>
          <option>Severe</option>
        </select>
      </div>
      <button @click="evaluateSafety">Run the reasoner</button>

      <div v-if="evaluationResult" class="reasoning-result">
        <h4>·reasoning result</h4>
        <p>{{ evaluationResult }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Scenario8',
  data() {
    return {
      bridgeAge: null,
      lastInspectionDate: '',
      structuralIssues: '',
      trafficLoad: null,
      environmentalConditions: '',
      evaluationResult: ''
    }
  },
  methods: {
    evaluateSafety() {
      // Here you would typically call an API or use a more complex logic
      // For demonstration, we'll just set a simple result
      this.evaluationResult = `Based on the input data:
        Bridge Age: ${this.bridgeAge} years
        Last Inspection: ${this.lastInspectionDate}
        Structural Issues: ${this.structuralIssues}
        Traffic Load: ${this.trafficLoad} tons/day
        Environmental Conditions: ${this.environmentalConditions}
        
        A full safety performance evaluation would be performed using relevant standards and methodologies.`
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

input[type="number"],
input[type="date"],
select,
textarea {
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