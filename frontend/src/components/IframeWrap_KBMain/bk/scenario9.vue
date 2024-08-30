<template>
  <div class="scenario">
    <h2>Bridge Strengthening Design</h2>
    <div class="scenario-image">
      <img src="/imgs/KBMain/Scenario-Strengthening.png" alt="Bridge Strengthening Design" width=100%>
    </div>
    <div class="design-form">
      <h3>Strengthening Design Inputs</h3>
      <div class="input-group">
        <label>Bridge Type:</label>
        <select v-model="bridgeType">
          <option>Concrete Girder</option>
          <option>Steel Truss</option>
          <option>Arch</option>
          <option>Cable-stayed</option>
        </select>
      </div>
      <div class="input-group">
        <label>Current Load Capacity (tons):</label>
        <input v-model.number="currentLoadCapacity" type="number" min="0">
      </div>
      <div class="input-group">
        <label>Target Load Capacity (tons):</label>
        <input v-model.number="targetLoadCapacity" type="number" min="0">
      </div>
      <div class="input-group">
        <label>Main Structural Issues:</label>
        <textarea v-model="structuralIssues" rows="3"></textarea>
      </div>
      <div class="input-group">
        <label>Budget Constraints (USD):</label>
        <input v-model.number="budget" type="number" min="0">
      </div>
      <button @click="generateDesign">Generate Strengthening Design</button>
    </div>
    <div v-if="designResult" class="design-result">
      <h3>Strengthening Design Recommendation:</h3>
      <p>{{ designResult }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Scenario9',
  data() {
    return {
      bridgeType: '',
      currentLoadCapacity: null,
      targetLoadCapacity: null,
      structuralIssues: '',
      budget: null,
      designResult: ''
    }
  },
  methods: {
    generateDesign() {
      // Here you would typically call an API or use a more complex logic
      // For demonstration, we'll just set a simple result
      this.designResult = `Based on the input data:
        Bridge Type: ${this.bridgeType}
        Current Load Capacity: ${this.currentLoadCapacity} tons
        Target Load Capacity: ${this.targetLoadCapacity} tons
        Structural Issues: ${this.structuralIssues}
        Budget: $${this.budget}
        
        A detailed strengthening design would be generated using relevant standards and engineering principles.`
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
