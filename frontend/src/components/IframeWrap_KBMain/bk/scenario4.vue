<template>
  <div class="scenario">
    <h2>Evaluating Crack on Reinforced Concrete</h2>
    <div class="scenario-introduction">
      <p>This scenario is employed to access severity and extent rating for Crack on Reinforced Concrete. The knowledge outlined in Network Rail Standard "Condition Marking of Bridges (NR/L3/CIV/006/2C)" is utilized to formulate maintenance solutions. These bodies of knowledge are represented in the proposed ontological knowledge base, using a semantic, logic-based format that enables computational processing.</p>
      <img src="/imgs/KBMain/Scenario-crackConcrete2.png" alt="Maintenance Scenario 4" width=100%>
    </div>
    <div class="scenario-implementation">
      <h3>Scenario Implementation (User Input)</h3>
      <div class="input-section">
        <label>Select an option:</label>
        <select v-model="corrosionEvidence">
          <option>Evidence of corrosion of reinforcement</option>
          <option>No evidence of corrosion of reinforcement</option>
        </select>
        
        <label>Enter Crack Width (mm):</label>
        <input v-model.number="crackWidth" type="number" min="0" step="0.1">
        
        <label>Enter Total Length of Cracks (%) of Principal Dimension:</label>
        <input v-model.number="crackLength" type="number" min="0" max="100">
        
        <button @click="processInput">Process</button>
      </div>
      <div class="reasoning-result" v-if="reasoningResult.length > 0">
        <h4>Reasoning Result:</h4>
        <ul>
          <li v-for="(item, index) in reasoningResult" :key="index">{{ item }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Scenario4',
  data() {
    return {
      corrosionEvidence: '',
      crackWidth: 0,
      crackLength: 0,
      reasoningResult: []
    }
  },
  methods: {
    processInput() {
      // Here you would typically call an API or use a more complex logic
      // For demonstration, we'll just push a simple result
      this.reasoningResult = [
        `Corrosion Evidence: ${this.corrosionEvidence}`,
        `Crack Width: ${this.crackWidth}mm`,
        `Crack Length: ${this.crackLength}% of Principal Dimension`
      ]
    }
  }
}
</script>

<style scoped>
.input-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
}
</style>
