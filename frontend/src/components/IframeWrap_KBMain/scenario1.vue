<template>
  <div class="scenario-content">
    <h2>Evaluating Corrosion on Metal</h2>
    
    <div class="sub-section">
      <h3>Scenario Introduction</h3>
      <p>
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

    <div class="sub-section">
      <h3>Scenario Implementation (Autoload)</h3>
      <h4>·autoload corrosion defects</h4>
      <div class="input-group">
        <label>The depth of corrosion (mm):</label>
        <input v-model="autoloadDepth" type="number">
      </div>
      <div class="input-group">
        <label>The percentage of surface of the element occupied by corrosion (%):</label>
        <input v-model="autoloadPercentage" type="number">
      </div>
      <button @click="runAutoloadReasoner">Run the reasoner</button>

      <div v-if="autoloadResult.length > 0">
        <h4>·reasoning result</h4>
        <ul>
          <li v-for="(item, index) in autoloadResult" :key="index">{{ item }}</li>
        </ul>
      </div>
    </div>

    <div class="sub-section">
      <h3>Scenario Implementation (File Input)</h3>
      <h4>·upload JSON File</h4>
      <input type="file" @change="handleFileUpload" accept=".json">
      <button @click="runFileReasoner">Run the reasoner</button>

      <div v-if="fileResult.length > 0">
        <h4>·reasoning result</h4>
        <ul>
          <li v-for="(item, index) in fileResult" :key="index">{{ item }}</li>
        </ul>
      </div>
    </div>

    <div class="sub-section">
      <h3>Scenario Implementation (User Input)</h3>
      <h4>·input corrosion defects</h4>
      <div class="input-group">
        <label>The depth of corrosion (mm):</label>
        <input v-model="userInputDepth" type="number">
      </div>
      <div class="input-group">
        <label>The percentage of surface of the element occupied by corrosion (%):</label>
        <input v-model="userInputPercentage" type="number">
      </div>
      <button @click="runUserInputReasoner">Run the reasoner</button>

      <div v-if="userInputResult.length > 0">
        <h4>·reasoning result</h4>
        <ul>
          <li v-for="(item, index) in userInputResult" :key="index">{{ item }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Scenario1',
  data() {
    return {
      autoloadDepth: 0,
      autoloadPercentage: 0,
      autoloadResult: [],
      fileContent: null,
      fileResult: [],
      userInputDepth: 0,
      userInputPercentage: 0,
      userInputResult: []
    }
  },
  methods: {
    async makeRequest(endpoint, data) {
      try {
        const response = await fetch(`/api${endpoint}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data)
        })

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }

        return await response.json()
      } catch (error) {
        console.error(`Error in ${endpoint}:`, error)
        return { error: error.message }
      }
    },
    async runAutoloadReasoner() {
      const result = await this.makeRequest('/ow_process_corrosionAuto', {
        depth: this.autoloadDepth,
        percentage: this.autoloadPercentage
      })
      this.autoloadResult = result.data || [result.error]
    },
    async handleFileUpload(event) {
      const file = event.target.files[0]
      const formData = new FormData()
      formData.append('file', file)

      try {
        const response = await fetch('/api/ow_upload', {
          method: 'POST',
          body: formData
        })

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }

        this.fileContent = await response.json()
      } catch (error) {
        console.error('Error uploading file:', error)
        this.fileContent = { error: error.message }
      }
    },
    async runFileReasoner() {
      if (this.fileContent) {
        const result = await this.makeRequest('/ow_process_corrosion', this.fileContent)
        this.fileResult = result.data || [result.error]
      }
    },
    async runUserInputReasoner() {
      const result = await this.makeRequest('/ow_process_corrosion', {
        depth: this.userInputDepth,
        percentage: this.userInputPercentage
      })
      this.userInputResult = result.data || [result.error]
    }
  },
  mounted() {
    console.log('Scenario1 mounted')
  }
}
</script>

<style scoped>
.scenario {
  /* Add your styles here */
}

.scenario-introduction, .scenario-implementation {
  margin-bottom: 20px;
}

img {
  max-width: 100%;
  height: auto;
}

/* Add more styles as needed */
</style>