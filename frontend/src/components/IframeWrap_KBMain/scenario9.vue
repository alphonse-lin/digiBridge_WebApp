<template>
  <div class="scenario-content">
    <h2>Bridge Strengthening Design</h2>
    
    <div class="sub-section">
      <h3>Scenario Introduction</h3>
      <img src="/imgs/KBMain/Scenario-Strengthening.png" alt="Bridge Strengthening Design" class="scenario-image">
    </div>

    <div class="sub-section user-input">
      <h3>Scenario Implementation (User Input)</h3>
      <h4>·input strengthening design parameters</h4>
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
      <button @click="generateDesign">Run the reasoner</button>

      <div v-if="designResult" class="reasoning-result">
        <h4>·reasoning result</h4>
        <p>{{ designResult }}</p>
      </div>
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