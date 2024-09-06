<template>
  <div class="scenario-content">
    <h2>Evaluating Crack on Reinforced Concrete</h2>

    <div class="sub-section">
      <h3>Scenario Introduction</h3>
      <p style="text-align: justify; padding: 10px;">This scenario is employed to access severity and extent rating for
        Crack on Reinforced Concrete. The knowledge outlined in Network Rail Standard "Condition Marking of Bridges
        (NR/L3/CIV/006/2C)" is utilized to formulate maintenance solutions. These bodies of knowledge are represented in
        the proposed ontological knowledge base, using a semantic, logic-based format that enables computational
        processing.</p>
      <img src="/imgs/KBMain/Scenario-crackConcrete2.png" alt="Maintenance Scenario 4" class="scenario-image">
    </div>

    <div class="sub-section user-input">
      <h3>Scenario Implementation (User Input)</h3>
      <h4 class="reasoning-result">Input crack defects</h4>
      <div class="input-group">
        <label>Select an option:</label>
        <select v-model="corrosionEvidence">
          <option>Evidence of corrosion of reinforcement</option>
          <option>No evidence of corrosion of reinforcement</option>
        </select>
      </div>

      <div class="input-group">
        <label>Enter Crack Width (mm):</label>
        <input v-model.number="crackWidth" type="number" min="0" step="0.1">
      </div>

      <div class="input-group">
        <label>Enter Total Length of Cracks (%) of Principal Dimension:</label>
        <input v-model.number="crackLength" type="number" min="0" max="100">
      </div>

      <button @click="processInput" :disabled="loading">Run the reasoner</button>
      <p v-if="loading">Processing, please wait...</p>

      <div v-if="crackResult.length > 0">
        <div v-for="(item, index) in crackResult" :key="index" class="result-section">
          <h4 class="reasoning-result">Reasoning result</h4>
          <div v-if="item.error" class="error-message">
            {{ item.error }}
          </div>
          <div v-else>
            <div class="result-item"><strong>Name:</strong> {{ item.name }}</div>
            <div class="result-item"><strong>Max Width:</strong> {{ item.maxWidth }} mm</div>
            <div class="result-item"><strong>Length Percentage:</strong> {{ item.lengthpercentage }}%</div>
            <div class="result-item"><strong>Severity Rating:</strong> {{ item.severityRating }}</div>
            <div class="result-item"><strong>Extent Rating:</strong> {{ item.extentRating }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { processCrackOnReinforcedConcrete } from '@/api/bridge'

export default {
  name: 'Scenario4',
  data() {
    return {
      corrosionEvidence: 'Evidence of corrosion of reinforcement',
      crackWidth: 0,
      crackLength: 0,
      crackResult: [],
      loading: false,
      corrosionEvidenceMap: {
        'Evidence of corrosion of reinforcement': '1',
        'No evidence of corrosion of reinforcement': '2'
      }
    }
  },
  methods: {
    async processInput() {
      this.loading = true
      this.crackResult = []
      try {
        const result = await processCrackOnReinforcedConcrete({
          corrosionEvidence: this.corrosionEvidenceMap[this.corrosionEvidence],
          width: this.crackWidth,
          length: this.crackLength
        })
        console.log(result)
        const parsedResult = this.parseCrackResult(result);
        this.crackResult = [parsedResult];
      } catch (error) {
        console.error('Error in processInput:', error);
        this.crackResult = [{ error: error.message || 'An error occurred while processing the request.' }];
      } finally {
        this.loading = false;
      }
    },
    parseCrackResult(data) {
      if (typeof data === 'string') {
        try {
          data = JSON.parse(data);
        } catch (e) {
          console.error('Failed to parse response as JSON:', e);
          return { error: 'Unable to parse the result.' };
        }
      }

      let result;

      if (data.result4 && Array.isArray(data.result4) && data.result4.length > 0) {
        // 获取 result4 数组的最后一个元素
        result = data.result4[data.result4.length - 1];
        return {
          name: result.name,
          maxWidth: result.maxWidth[0] || 'N/A',
          lengthpercentage: result.lengthpercentage[0],
          severityRating: result.severityRating[0],
          extentRating: result.extentRating[0]
        };
      } else if (Array.isArray(data.message) && data.message.length > 0) {
        // 获取 message 数组的最后一个元素
        const lastMessage = data.message[data.message.length - 1];
        const match = lastMessage.match(/crackonreinforcedconcrete\d+\(\[(.*?)\] mm and \[(.*?)\]%\), its severity rating is \['(.*?)'\], and its extent rating is \[(.*?)\]/);
        if (match) {
          return {
            name: lastMessage.match(/crackonreinforcedconcrete(\d+)/)[0],
            maxWidth: match[1] || 'N/A',
            lengthpercentage: parseFloat(match[2]),
            severityRating: match[3],
            extentRating: parseFloat(match[4])
          };
        }
      }

      return { error: 'Unable to parse the result or no valid result found.' };
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
  background-color: #f8e5e5;
  /* 浅粉色 */
}

.user-input {
  background-color: #e5f8e5;
  /* 浅绿色 */
}

h2,
h3,
h4 {
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
select {
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

ul {
  list-style-type: none;
  padding-left: 0;
}

li {
  margin-bottom: 5px;
}

.reasoning-result {
  text-decoration: underline;
}
</style>