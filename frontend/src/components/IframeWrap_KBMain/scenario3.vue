<template>
  <div class="scenario-content">
    <h2>Evaluating Crack on Masonry</h2>

    <div class="sub-section">
      <h3>Scenario Introduction</h3>
      <p style="text-align: justify; padding: 10px;">This scenario is employed to access severity and extent rating for
        Crack on Masonry. The knowledge outlined in Network Rail Standard "Condition Marking of Bridges
        (NR/L3/CIV/006/2C)" is utilized to formulate maintenance solutions. These bodies of knowledge are represented in
        the proposed ontological knowledge base, using a semantic, logic-based format that enables computational
        processing.</p>
      <img src="/imgs/KBMain/Scenario-crackMasonry.png" alt="Maintenance Scenario 3" class="scenario-image">
      <img src="/imgs/KBMain/Scenario-crackMasonry1.png" alt="Maintenance Scenario 3 Additional" class="scenario-image">
    </div>

    <div class="sub-section user-input">
      <h3>Scenario Implementation (User Input)</h3>
      <h4 class="reasoning-result">Input crack defects</h4>
      <div class="input-group">
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
      </div>

      <div class="input-group">
        <label>Select Crack Type:</label>
        <select v-model="crackType">
          <option>Longitudinal crack</option>
          <option>Diagonal crack</option>
          <option>Transverse crack</option>
          <option>Ring crack</option>
          <option>Vertical crack</option>
          <option>Horizontal crack</option>
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

      <div v-if="reasoningResult.length > 0">
        <h4 class="reasoning-result">Reasoning result</h4>
        <div v-for="(item, index) in reasoningResult" :key="index" class="result-section">
          <div v-if="item.error" class="error-message">
            {{ item.error }}
          </div>
          <div v-else>
            <div class="result-item"><strong>Name:</strong> {{ item.name }}</div>
            <div class="result-item"><strong>Crack Type:</strong> {{ item.crackType }}</div>
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
import { processCrackOnMasonry } from '@/api/bridge'

export default {
  name: 'Scenario3',
  data() {
    return {
      crackLocation: 'BarrelArch',
      crackType: 'Longitudinal crack',
      crackWidth: 0,
      crackLength: 0,
      reasoningResult: [],
      loading: false,
      locationMap: {
        'BarrelArch': '1',
        'FaceRings': '2',
        'Abutment': '3',
        'Pier': '4',
        'WingWall': '5',
        'SpandrelWall': '6',
        'Parapet': '7',
        'Padstone/Cills': '8'
      },
      typeMap: {
        'Longitudinal crack': '1',
        'Diagonal crack': '2',
        'Transverse crack': '3',
        'Ring crack': '4',
        'Vertical crack': '5',
        'Horizontal crack': '6'
      }
    }
  },
  methods: {
    async processInput() {
      this.loading = true;
      this.reasoningResult = [];
      try {
        const result = await processCrackOnMasonry({
          location: this.locationMap[this.crackLocation],
          type: this.typeMap[this.crackType],
          width: this.crackWidth,
          length: this.crackLength
        });
        console.log('Received result:', result);
        this.reasoningResult = this.parseResult(result);
      } catch (error) {
        console.error('Error in processInput:', error);
        this.reasoningResult = [{ error: error.message || 'An error occurred while processing the request.' }];
      } finally {
        this.loading = false;
      }
    },
    parseResult(data) {
      if (typeof data === 'string') {
        try {
          data = JSON.parse(data);
        } catch (e) {
          console.error('Failed to parse response as JSON:', e);
          return [{ error: 'Unable to parse the result.' }];
        }
      }

      let results = [];

      if (data.result3 && Array.isArray(data.result3)) {
        results = data.result3;
      } else if (Array.isArray(data.message)) {
        results = data.message.map(msg => {
          const match = msg.match(/crackonmasonry\d+ \((.*?) crack, (\d+) mm wide and (\d+)% long\), its severity rating is (.*?), and its extent rating is (.*?)\.$/);
          if (match) {
            return {
              name: `crackonmasonry${msg.match(/crackonmasonry(\d+)/)[1]}`,
              crackType: match[1],
              maxWidth: parseFloat(match[2]),
              lengthpercentage: parseFloat(match[3]),
              severityRating: match[4],
              extentRating: parseFloat(match[5])
            };
          }
          return { error: 'Unable to parse the result from message.' };
        });
      }

      // 使用 Set 来去除重复项
      const uniqueResults = Array.from(new Set(results.map(JSON.stringify))).map(JSON.parse);

      // 只返回最新的结果（假设最新的结果在数组的最后）
      return uniqueResults.slice(-1);
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