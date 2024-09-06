<template>
  <div class="scenario-content">
    <h2>Evaluating Corrosion on Metal</h2>

    <div class="sub-section">
      <h3>Scenario Introduction</h3>
      <p style="text-align: justify; padding: 10px;">
        This scenario is employed for bridges requiring substantial maintenance
        due to extensive corrosion affecting structural elements. The knowledge
        outlined in Network Rail Standard "Condition Marking of Bridges
        (NR/L3/CIV/006/2C)" is utilized to assess the severity and extent
        ratings of metallic components within these bridges. These bodies of
        knowledge are represented in the proposed ontological knowledge base,
        using a semantic, logic-based format that enables computational
        processing.
      </p>
      <img src="/imgs/KBMain/Scenario-corrision.png" alt="Maintenance Scenario1" class="scenario-image" width=100%>
    </div>

    <div class="sub-section autoload">
      <h3>Scenario Implementation (Autoload)</h3>
      <h4 class="reasoning-result">Autoload corrosion defects</h4>
      <div class="input-group">
        <label>The depth of corrosion (mm):</label>
        <input v-model="autoloadDepth" type="number">
      </div>
      <div class="input-group">
        <label>The percentage of surface of the element occupied by corrosion (%):</label>
        <input v-model="autoloadPercentage" type="number">
      </div>
      <button @click="runAutoloadReasoner" :disabled="autoload_loading">Run the reasoner</button>
      <p v-if="autoload_loading">Processing, please wait...</p>

      <div v-if="autoloadResult && autoloadResult.severityRating" class="result-section">
        <h4 class="reasoning-result">Reasoning result</h4>
        <div v-if="autoloadResult.depth !== undefined" class="result-item">
          <strong>Depth:</strong> {{ autoloadResult.depth }} mm
        </div>
        <div v-if="autoloadResult.percentage !== undefined" class="result-item">
          <strong>Percentage:</strong> {{ autoloadResult.percentage }}%
        </div>
        <div class="result-item">
          <strong>Severity Rating:</strong> {{ autoloadResult.severityRating }}
        </div>
        <div class="result-item">
          <strong>Extent Rating:</strong> {{ autoloadResult.extentRating }}
        </div>
        <div class="result-item">
          <strong>Maintenance Solution:</strong> <br /> {{ autoloadResult.maintenanceSolution }}
        </div>
      </div>
      <div v-else-if="autoloadResult && autoloadResult.error" class="error-message">
        {{ autoloadResult.error }}
      </div>
    </div>

    <div class="sub-section file-input">
      <h3>Scenario Implementation (File Input)</h3>
      <h4 class="reasoning-result">Upload JSON File</h4>
      <input type="file" @change="handleFileUpload" accept=".json">
      <button @click="runFileReasoner" :disabled="fileUpload_loading">Run the reasoner</button>
      <p v-if="fileUpload_loading">Processing, please wait...</p>

      <div v-if="fileResult.length > 0">
        <div v-for="(item, index) in fileResult" :key="index" class="result-section">
        <h4 class="reasoning-result">Reasoning result</h4>
          <div v-if="item.error" class="error-message">
            {{ item.error }}
          </div>
          <div v-else>
            <div class="result-item"><strong>Name:</strong> {{ item.name }}</div>
            <div class="result-item"><strong>Depth:</strong> {{ item.depth }} mm</div>
            <div class="result-item"><strong>Percentage:</strong> {{ item.percentage }}%</div>
            <div class="result-item"><strong>Severity Rating:</strong> {{ item.severityRating }}</div>
            <div class="result-item"><strong>Extent Rating:</strong> {{ item.extentRating }}</div>
            <div class="result-item"><strong>Maintenance Solution:</strong> <br> {{ item.maintenanceSolution }}</div>
          </div>
        </div>
      </div>
    </div>

    <div class="sub-section user-input">
      <h3>Scenario Implementation (User Input)</h3>
      <h4 class="reasoning-result">Input corrosion defects</h4>
      <div class="input-group">
        <label>The depth of corrosion (mm):</label>
        <input v-model="userInputDepth" type="number">
      </div>
      <div class="input-group">
        <label>The percentage of surface of the element occupied by corrosion (%):</label>
        <input v-model="userInputPercentage" type="number">
      </div>
      <button @click="runUserInputReasoner" :disabled="userInput_loading">Run the reasoner</button>
      <p v-if="userInput_loading">Processing, please wait...</p>

      <div v-if="userInputResult.length > 0">
        <div v-for="(item, index) in userInputResult" :key="index" class="result-section">
          <h4 class="reasoning-result">Reasoning result</h4>
          <div v-if="item.error" class="error-message">
            {{ item.error }}
          </div>
          <div v-else>
            <div class="result-item"><strong>Name:</strong> {{ item.name }}</div>
            <div class="result-item"><strong>Depth:</strong> {{ item.depth }} mm</div>
            <div class="result-item"><strong>Percentage:</strong> {{ item.percentage }}%</div>
            <div class="result-item"><strong>Severity Rating:</strong> {{ item.severityRating }}</div>
            <div class="result-item"><strong>Extent Rating:</strong> {{ item.extentRating }}</div>
            <div class="result-item"><strong>Maintenance Solution:</strong> <br> {{ item.maintenanceSolution }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { processCorrosionAuto, uploadFile, processCorrosion } from '@/api/bridge'

export default {
  name: 'Scenario1',
  data() {
    return {
      autoload_loading: false,
      fileUpload_loading: false,
      userInput_loading: false,
      autoloadResult: null,
      autoloadDepth: 20,
      autoloadPercentage: 30,
      autoloadResult: [],
      fileContent: null,
      fileResult: [],
      userInputDepth: 0,
      userInputPercentage: 0,
      userInputResult: []
    }
  },
  methods: {
    async runAutoloadReasoner() {
      this.autoload_loading = true;
      this.autoloadResult = null; // 重置结果
      try {
        const response = await processCorrosionAuto({
          depth: this.autoloadDepth,
          percentage: this.autoloadPercentage
        });
        // 直接使用后端返回的数据
        this.autoloadResult = this.AutoloadParseResult(response)
      } catch (error) {
        console.error('Error in runAutoloadReasoner:', error);
        this.autoloadResult = {
          error: error.response?.data?.message || 'An error occurred while processing the request.'
        };
      } finally {
        this.autoload_loading = false;
      }
    },
    AutoloadParseResult(data) {
      if (typeof data === 'string') {
        // 如果数据是字符串，尝试解析为JSON
        try {
          data = JSON.parse(data);
        } catch (e) {
          console.error('Failed to parse response as JSON:', e);
          return { error: 'Unable to parse the result.' };
        }
      }

      if (data.result00) {
        // 使用result00对象中的数据
        return {
          depth: data.result00.maxDepth[0],
          percentage: data.result00.percentage[0],
          severityRating: data.result00.severityRating[0],
          extentRating: data.result00.extentRating[0],
          maintenanceSolution: data.result00.maintenanceDecision[0]
        };
      } else if (Array.isArray(data.message)) {
        // 如果没有result00对象，尝试从message数组解析数据
        const result = {};
        const severityMatch = data.message[0].match(/severity rating is \['(.*)'\], and its extent rating is \[(.*)\]/);
        const maintenanceMatch = data.message[1].match(/maintenance solution .* is \['(.*)'\]/);

        if (severityMatch && maintenanceMatch) {
          result.severityRating = severityMatch[1];
          result.extentRating = severityMatch[2];
          result.maintenanceSolution = maintenanceMatch[1];
          // 注意：这种方法无法获取depth和percentage，因为它们不在message中
        } else {
          return { error: 'Unable to parse the result from message.' };
        }

        return result;
      }

      return { error: 'Unexpected response format.' };
    },

    async handleFileUpload(event) {
      const file = event.target.files[0]
      this.fileContent = file // Store the file object directly
    },
    async runFileReasoner() {
      this.fileUpload_loading = true;
      if (this.fileContent) {
        const formData = new FormData()
        formData.append('file', this.fileContent)

        try {
          const uploadResponse = await uploadFile(formData)
          const parsedResult = this.parseFileResult(uploadResponse)
          this.fileResult = [parsedResult]
        } catch (error) {
          console.error('Error processing file:', error)
          this.fileResult = [{ error: error.message || 'An error occurred while processing the file.' }]
        } finally {
          this.fileUpload_loading = false;
        }
      }
    },
    parseFileResult(data) {
      if (typeof data === 'string') {
        try {
          data = JSON.parse(data)
        } catch (e) {
          console.error('Failed to parse response as JSON:', e)
          return { error: 'Unable to parse the result.' }
        }
      }

      if (data.result0) {
        return {
          name: data.result0.name,
          depth: data.result0.maxDepth[0],
          percentage: data.result0.percentage[0],
          severityRating: data.result0.severityRating[0],
          extentRating: data.result0.extentRating[0],
          maintenanceSolution: data.result0.maintenanceDecision[0]
        }
      } else if (Array.isArray(data.message)) {
        const result = {}
        const severityMatch = data.message[0].match(/corrosion3\(\[(.*?)\] mm and \[(.*?)\]%\), its severity rating is \['(.*)'\], and its extent rating is \[(.*)\]/)
        const maintenanceMatch = data.message[1].match(/maintenance solution .* is \['(.*)'\]/)

        if (severityMatch && maintenanceMatch) {
          result.name = 'corrosion3'
          result.depth = parseFloat(severityMatch[1])
          result.percentage = parseFloat(severityMatch[2])
          result.severityRating = severityMatch[3]
          result.extentRating = parseInt(severityMatch[4])
          result.maintenanceSolution = maintenanceMatch[1]
        } else {
          return { error: 'Unable to parse the result from message.' }
        }

        return result
      }

      return { error: 'Unexpected response format.' }

    },

    async runUserInputReasoner() {
      this.userInput_loading = true;
      try {
        const result = await processCorrosion({
          depth: this.userInputDepth,
          percentage: this.userInputPercentage
        })
        const parsedResult = this.parseUserInputResult(result)
        this.userInputResult = [parsedResult]
      } catch (error) {
        console.error('Error in runUserInputReasoner:', error)
        this.userInputResult = [{ error: error.message || 'An error occurred while processing the request.' }]
      } finally {
        this.userInput_loading = false;
      }
    },

    parseUserInputResult(data) {
      if (typeof data === 'string') {
        try {
          data = JSON.parse(data)
        } catch (e) {
          console.error('Failed to parse response as JSON:', e)
          return { error: 'Unable to parse the result.' }
        }
      }

      if (data.result1) {
        return {
          name: data.result1.name,
          depth: data.result1.maxDepth[0],
          percentage: data.result1.percentage[0],
          severityRating: data.result1.severityRating[0],
          extentRating: data.result1.extentRating[0],
          maintenanceSolution: data.result1.maintenanceDecision[0]
        }
      } else if (Array.isArray(data.message)) {
        const result = {}
        const severityMatch = data.message[0].match(/corrosion2\(\[(.*?)\] mm and \[(.*?)\]%\), its severity rating is \['(.*)'\], and its extent rating is \[(.*)\]/)
        const maintenanceMatch = data.message[1].match(/maintenance solution .* is \['(.*)'\]/)

        if (severityMatch && maintenanceMatch) {
          result.name = 'corrosion2'
          result.depth = parseFloat(severityMatch[1])
          result.percentage = parseFloat(severityMatch[2])
          result.severityRating = severityMatch[3]
          result.extentRating = parseFloat(severityMatch[4])
          result.maintenanceSolution = maintenanceMatch[1]
        } else {
          return { error: 'Unable to parse the result from message.' }
        }

        return result
      }

      return { error: 'Unexpected response format.' }
    }
  },
  mounted() {
    console.log('Scenario1 mounted')
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

.autoload {
  background-color: #f5e5b8;
  /* 浅黄色 */
}

.file-input {
  background-color: #e5f0f8;
  /* 浅蓝色 */
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
input[type="file"] {
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

.result-section {
  margin-top: 20px;
  padding: 15px;
  background-color: #f0f0f0;
  border-radius: 5px;
}

.result-item {
  margin-bottom: 10px;
}

.error-message {
  color: red;
  margin-top: 10px;
}
.reasoning-result{
  text-decoration: underline;
  font-weight: bold;
}
</style>