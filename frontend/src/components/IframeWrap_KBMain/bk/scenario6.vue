<template>
  <div class="scenario">
    <h2>Bridge Technical Condition Evaluation</h2>
    <div class="scope">
      <h3>Scope: 混凝土梁式桥（Concrete girder bridges），包括钢筋混凝土或预应力混凝土梁式桥。</h3>
    </div>
    <div class="hazard-input">
      <h3>Input hazard</h3>
      <div class="input-group">
        <label>Select Hazard Type on Superstructure 上部结构:</label>
        <select v-model="superstructureHazard">
          <option>Honeycomb 蜂窝/麻面</option>
          <option>Spalling 剥落/掉角</option>
          <option>Bugholes 空洞/孔洞</option>
          <option>Water Stain 渗水泛碱</option>
          <option>Crack 裂缝</option>
          <option>No visible defects 无病害</option>
        </select>
      </div>
      <div class="input-group">
        <label>Select Hazard Type on Substructure 下部结构:</label>
        <select v-model="substructureHazard">
          <option>Honeycomb On Pier 桥墩蜂窝/麻面</option>
          <option>Spalling On Pier 桥墩混凝土剥落/露筋</option>
          <option>Bugholes On Pier 桥墩空洞/孔洞</option>
          <option>Abrasion On Pier 桥墩磨损</option>
          <option>Crack On Pier 桥墩裂缝</option>
          <option>Spalling On Abutment 桥台混凝土剥落</option>
          <option>Bugholes On Abutment 桥台空洞/孔洞</option>
          <option>Abrasion On Abutment 桥台磨损</option>
          <option>No visible defects 无病害</option>
        </select>
      </div>
      <div class="input-group">
        <label>Select Hazard Type on Deck 桥面系:</label>
        <select v-model="deckHazard">
          <option>Abrasion 磨光/脱皮/露骨</option>
          <option>Spalling 剥落</option>
          <option>Crack 裂缝</option>
          <option>Defects On Expansion Joint 锚固区缺陷</option>
          <option>No visible defects 无病害</option>
        </select>
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
  name: 'Scenario6',
  data() {
    return {
      superstructureHazard: '',
      substructureHazard: '',
      deckHazard: '',
      evaluationResult: ''
    }
  },
  methods: {
    evaluateCondition() {
      // Here you would typically call an API or use a more complex logic
      // For demonstration, we'll just set a simple result
      this.evaluationResult = `Based on the input hazards:
        Superstructure: ${this.superstructureHazard}
        Substructure: ${this.substructureHazard}
        Deck: ${this.deckHazard}
        
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
