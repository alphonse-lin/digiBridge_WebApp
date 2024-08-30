<template>
  <div class="scenario">
    <h2>Evaluating Coatings to Metal</h2>
    <div class="scenario-introduction">
      <p>This scenario is employed to access severity and extent rating for coatings to metal. The knowledge outlined in Network Rail Standard "Condition Marking of Bridges (NR/L3/CIV/006/2C)" and "Specification for the Use of Protective Coating Systems (NR/L3/CIV/040)" is utilized to formulate maintenance solutions. These bodies of knowledge are represented in the proposed ontological knowledge base, using a semantic, logic-based format that enables computational processing.</p>
      <img src="/imgs/KBMain/Scenario-coating.png" alt="Maintenance Scenario 2" width=100%>
    </div>
    <div class="scenario-implementation">
      <h3>Scenario Implementation (User Input)</h3>
      <div class="input-section">
        <label>Select an option:</label>
        <select v-model="selectedOption">
          <option>All coating intact, no visible defects or no coating applied</option>
          <option>All coating intact, surface defects/abrasion (no corrosion of underlying metal)</option>
          <option>Flaking or blistering of top coat (no corrosion of underlying metal)</option>
          <option>Corrosion spots showing through coating</option>
          <option>Complete loss of coating to parent metal</option>
        </select>
        
        <label>Enter Percentage of surface of the element occupied by coating defect(%):</label>
        <input v-model.number="defectPercentage" type="number" min="0" max="100">
        
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
import { processCoatingDefect } from '@/api/bridge'

export default {
  name: 'Scenario2',
  data() {
    return {
      selectedOption: '',
      defectPercentage: 0,
      reasoningResult: []
    }
  },
  methods: {
    async processInput() {
      try {
        const result = await processCoatingDefect({
          option: this.selectedOption,
          percentage: this.defectPercentage
        })
        this.reasoningResult = result.data || [result.error]
      } catch (error) {
        console.error('Error in processInput:', error)
        this.reasoningResult = [error.message]
      }
    }
  },
  mounted() {
    console.log('Scenario2 mounted')
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
