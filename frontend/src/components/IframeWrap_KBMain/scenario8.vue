<template>
  <div class="scenario">
    <h2>Bridge Safety Performance Evaluation</h2>
    <div class="scenario-image">
      <img src="/imgs/KBMain/Scenario-Safety.png" alt="Bridge Safety Performance Evaluation" width=100%>
    </div>
    <div class="evaluation-form">
      <h3>Safety Performance Evaluation Inputs</h3>
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
      <button @click="evaluateSafety">Evaluate Safety Performance</button>
    </div>
    <div v-if="evaluationResult" class="evaluation-result">
      <h3>Evaluation Result:</h3>
      <p>{{ evaluationResult }}</p>
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
.input-group {
  margin-bottom: 15px;
}
.scenario-image img {
  max-width: 100%;
  height: auto;
}
</style>
