<template>
  <div class="scenario-content">
    <h2>Evaluating Coatings to Metal</h2>

    <div class="sub-section">
      <h3>Scenario Introduction</h3>
      <p style="text-align: justify; padding: 10px;">This scenario is employed to access severity and extent rating for
        coatings to metal. The knowledge outlined in Network Rail Standard "Condition Marking of Bridges
        (NR/L3/CIV/006/2C)" and "Specification for the Use of Protective Coating Systems (NR/L3/CIV/040)" is utilized to
        formulate maintenance solutions. These bodies of knowledge are represented in the proposed ontological knowledge
        base, using a semantic, logic-based format that enables computational processing.</p>
      <img src="/imgs/KBMain/Scenario-coating.png" alt="Maintenance Scenario 2" class="scenario-image" width="100%">
    </div>

    <div class="sub-section user-input">
      <h3>Scenario Implementation (User Input)</h3>
      <h4 class="reasoning-result">Input coating defects</h4>
      <div class="input-group">
        <label>Select an option:</label>
        <select v-model="selectedOption">
          <option>All coating intact, no visible defects or no coating applied</option>
          <option>All coating intact, surface defects/abrasion (no corrosion of underlying metal)</option>
          <option>Flaking or blistering of top coat (no corrosion of underlying metal)</option>
          <option>Corrosion spots showing through coating</option>
          <option>Complete loss of coating to parent metal</option>
        </select>
      </div>
      <div class="input-group">
        <label>Enter Percentage of surface of the element occupied by coating defect(%):</label>
        <input v-model.number="defectPercentage" type="number" min="0" max="100">
      </div>
      <button @click="runCoatingDefectReasoner" :disabled="coatingDefect_loading">Run the reasoner</button>
      <p v-if="coatingDefect_loading">Processing, please wait...</p>

      <div v-if="coatingDefectResult.length > 0">
      <div v-for="(item, index) in coatingDefectResult" :key="index" class="result-section">
        <h4 class="reasoning-result">Reasoning result</h4>
        <div v-if="item.error" class="error-message">
          {{ item.error }}
        </div>
        <div v-else>
          <div class="result-item"><strong>Name:</strong> {{ item.name }}</div>
          <div class="result-item"><strong>Percentage:</strong> {{ item.percentage }}%</div>
          <div class="result-item"><strong>Severity Rating:</strong> {{ item.severityRating }}</div>
          <div class="result-item"><strong>Extent Rating:</strong> {{ item.extentRating }}</div>
          <div class="result-item"><strong>Maintenance Decision:</strong> {{ item.maintenanceDecision }}</div>
          <div class="result-item"><strong>Protective Coating System:</strong> <br> {{ item.protectiveCoatingSystem }}</div>
        </div>
      </div>
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
      selectedOption: 'All coating intact, no visible defects or no coating applied',
      defectPercentage: 0,
      coatingDefectResult: [],
      coatingDefect_loading: false,
      optionMap: {
        'All coating intact, no visible defects or no coating applied': '0',
        'All coating intact, surface defects/abrasion (no corrosion of underlying metal)': '1',
        'Flaking or blistering of top coat (no corrosion of underlying metal)': '2',
        'Corrosion spots showing through coating': '3',
        'Complete loss of coating to parent metal': '4'
      },
    }
  },
  methods: {
    async runCoatingDefectReasoner() {
      this.coatingDefect_loading = true;
      this.coatingDefectResult = [];
      try {
        const result = await processCoatingDefect({
          option: this.selectedOption,
          percentage: this.defectPercentage
        });
        console.log(result);
        const parsedResult = this.parseCoatingDefectResult(result);
        this.coatingDefectResult = [parsedResult];
      } catch (error) {
        console.error('Error in runCoatingDefectReasoner:', error);
        this.coatingDefectResult = [{ error: error.message || 'An error occurred while processing the request.' }];
      } finally {
        this.coatingDefect_loading = false;
      }
    },

    parseCoatingDefectResult(data) {
      if (typeof data === 'string') {
        try {
          data = JSON.parse(data);
        } catch (e) {
          console.error('Failed to parse response as JSON:', e);
          return { error: 'Unable to parse the result.' };
        }
      }

      if (data.result2 && data.result2.length > 0) {
        const result = data.result2[0];
        return {
          name: result.name,
          percentage: result.percentage,
          severityRating: result.severityRating,
          extentRating: result.extentRating,
          maintenanceDecision: result.maintenanceDecision,
          protectiveCoatingSystem: result.protectiveCoatingSystem
        };
      } else if (Array.isArray(data.message)) {
        const result = {};
        const match = data.message[0].match(/coatingdefect1\((.*?)%\), its severity rating is (.*?), and its extent rating is (.*?)\. (.*?), and based on/);
        if (match) {
          result.name = 'coatingdefect1';
          result.percentage = parseFloat(match[1]);
          result.severityRating = match[2];
          result.extentRating = parseFloat(match[3]);
          result.maintenanceDecision = match[4];
          result.protectiveCoatingSystem = data.message[0].split('its protective coating system is ')[1];
        } else {
          return { error: 'Unable to parse the result from message.' };
        }
        return result;
      }

      return { error: 'Unexpected response format.' };
    }
  },
  mounted() {
    console.log('Scenario2 mounted')
  }
}
</script>

<style scoped>
.reasoning-result {
  text-decoration: underline;
}

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
</style>