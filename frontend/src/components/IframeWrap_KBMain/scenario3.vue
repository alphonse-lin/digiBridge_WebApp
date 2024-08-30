<template>
  <div class="scenario">
    <h2>Evaluating Crack on Masonry</h2>
    <div class="scenario-introduction">
      <p>This scenario is employed to access severity and extent rating for Crack on Masonry. The knowledge outlined in Network Rail Standard "Condition Marking of Bridges (NR/L3/CIV/006/2C)" is utilized to formulate maintenance solutions. These bodies of knowledge are represented in the proposed ontological knowledge base, using a semantic, logic-based format that enables computational processing.</p>
      <img src="/imgs/KBMain/Scenario-crackMasonry.png" alt="Maintenance Scenario 3" width=100% height=100%>
      <img src="/imgs/KBMain/Scenario-crackMasonry1.png" alt="Maintenance Scenario 3 Additional" width=100% height=100%>
    </div>
    <div class="scenario-implementation">
      <h3>Scenario Implementation (User Input)</h3>
      <div class="input-section">
        <label>Select Crack Location:</label>
        <select v-model="crackLocation">
          <option>BarrelArch</option>
          <option>FaceRings</option>
          <option>Abutment</option>
          <option>Pier</option>
          <option>WingWall</option>
          <option>SpandrelWall</option>
          <option>Parapet</option>
          <option>Padstone/Cills</option>
        </select>
        
        <label>Select Crack Type:</label>
        <select v-model="crackType">
          <option>Longitudinal crack</option>
          <option>Diagonal crack</option>
          <option>Transverse crack</option>
          <option>Ring crack</option>
          <option>Vertical crack</option>
          <option>Horizontal crack</option>
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
import { processCrackOnMasonry } from '@/api/bridge'

export default {
  name: 'Scenario3',
  data() {
    return {
      crackLocation: '',
      crackType: '',
      crackWidth: 0,
      crackLength: 0,
      reasoningResult: []
    }
  },
  methods: {
    async processInput() {
      try {
        const result = await processCrackOnMasonry({
          location: this.crackLocation,
          type: this.crackType,
          width: this.crackWidth,
          length: this.crackLength
        })
        this.reasoningResult = result.data || [result.error]
      } catch (error) {
        console.error('Error in processInput:', error)
        this.reasoningResult = [error.message]
      }
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
