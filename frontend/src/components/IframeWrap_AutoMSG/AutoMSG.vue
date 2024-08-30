<template>
  <div>
    <h1>Automated Bridge Maintenance Strategy Generation</h1>
    <h2>System Architecture</h2>
    <img src="/imgs/autoMSG/framework.png" alt="System Architecture Diagram" class="system-diagram" width="50%"
      style="display: block; margin: auto; width: 50%;">
    <p>This microservice is driven by a multi-model neural network model, which is trained by the data from CGR. The
      backend model learns the knowledge from both the image of damage and the solution provided by experts. This model
      has the ability of self-learning
      and can generate solutions for unseen damages.</p>
    <h2>Dataset</h2>
    <p>The data used for training is provided by CGR, which is a record of defect identification and maintenance. The
      images of defect and the corresponding maintenance solutions are extracted through a pre-processing algorithm and
      used as the input data
      to train the neural network model.</p>
    <img src="/imgs/autoMSG/table.png" alt="dataset-preview" class="dataset-preview" width="50%"
      style="display: block; margin: auto; width: 50%;">
    <!-- <div class="dataset-preview">
        <table>
            <tr>
                <th>ID</th>
                <th>Date</th>
                <th>Defect Image</th>
                <th>Maintenance Solution</th>
            </tr>
            <tr>
                <td>1</td>
                <td>06/07/2023</td>
                <td><img src="https://via.placeholder.com/100x100.png?text=Defect+1" alt="Defect 1"></td>
                <td>Apply epoxy injection to seal cracks</td>
            </tr>
            <tr>
                <td>2</td>
                <td>08/15/2023</td>
                <td><img src="https://via.placeholder.com/100x100.png?text=Defect+2" alt="Defect 2"></td>
                <td>Replace corroded reinforcement bars</td>
            </tr>
        </table>
    </div> -->
    <h2>Demo</h2>
    <p>Upload your image of damage</p>
    <div class="file-upload">
      <div id="drop-zone" class="drop-zone">
        <input type="file" id="file-input" class="file-input" accept="image/*">
        <div class="icon-text">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="17 8 12 3 7 8"></polyline>
            <line x1="12" y1="3" x2="12" y2="15"></line>
          </svg>
          <span>Drag and drop file here</span>
        </div>
        <p class="file-size-limit">Limit 20MB per file</p>
      </div>
      <button id="browse-button" class="browse-button">Browse files</button>
    </div>

    <div v-if="results.length > 0" class="results-container">
      <h3>Results:</h3>
      <table class="results-table">
        <thead>
          <tr>
            <th>Predicted Solution</th>
            <th>Ground Truth</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(result, index) in results" :key="index">
            <td>{{ result.predictedSolution }}</td>
            <td>{{ result.groundTruth }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AutomatedMaintenance',
  data() {
    return {
      results: [],
      predictedSolution: '',
      groundTruth: ''
    }
  },
  mounted() {
    const dropZone = document.getElementById('drop-zone')
    const fileInput = document.getElementById('file-input')
    const browseButton = document.getElementById('browse-button');

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
      dropZone.addEventListener(eventName, this.preventDefaults, false)
      document.body.addEventListener(eventName, this.preventDefaults, false)
    });

    ['dragenter', 'dragover'].forEach(eventName => {
      dropZone.addEventListener(eventName, this.highlight, false)
    });

    ['dragleave', 'drop'].forEach(eventName => {
      dropZone.addEventListener(eventName, this.unhighlight, false)
    })

    dropZone.addEventListener('drop', this.handleDrop, false)

    fileInput.addEventListener('change', () => {
      this.handleFiles(fileInput.files)
    })

    browseButton.addEventListener('click', () => {
      fileInput.click()
    })
  },
  methods: {
    preventDefaults(e) {
      e.preventDefault()
      e.stopPropagation()
    },
    highlight() {
      const dropZone = document.getElementById('drop-zone')
      dropZone.classList.add('active')
    },
    unhighlight() {
      const dropZone = document.getElementById('drop-zone')
      dropZone.classList.remove('active')
    },
    handleDrop(e) {
      const dt = e.dataTransfer
      const files = dt.files
      this.handleFiles(files)
    },
    handleFiles(files) {
      if (files.length) {
        console.log('File selected:', files[0].name)
        this.uploadFile(files[0])
      }
    },
    async uploadFile(file) {
      const formData = new FormData()
      formData.append('image', file)

      try {
        const response = await fetch('/api/am_generate_solution', {
          method: 'POST',
          body: formData
        })

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }

        const data = await response.json()
        this.predictedSolution = data.predicted_solution
        this.groundTruth = data.ground_truth || 'Not available'

        console.log('Success:', data)
      } catch (error) {
        console.error('Error:', error)
      }
    },
  }
}
</script>

<style scoped>
h1,
h2 {
  color: #2c3e50;
  margin-bottom: 10px;
}

h1 {
  margin-bottom: 20px;
}

p {
  line-height: 32px;
  font-size: 16px;
}

.system-diagram {
  max-width: 100%;
  height: auto;
  margin: 20px 0;
}

.dataset-preview {
  max-width: 100%;
  height: auto;
  margin: 20px 0;
}

/* .dataset-preview {
    overflow-x: auto;
    margin-bottom: 30px;
} */

.dataset-preview table {
  width: 100%;
  border-collapse: collapse;
}

.dataset-preview th,
.dataset-preview td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.dataset-preview th {
  background-color: #f2f2f2;
}

.file-upload {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.drop-zone {
  border: 2px dashed #ccc;
  border-radius: 4px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: border 0.3s ease;
}

.drop-zone.active {
  border-color: #007bff;
}

.icon-text {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 10px;
}

.icon-text svg {
  margin-bottom: 10px;
}

.file-input {
  display: none;
}

.file-size-limit {
  font-size: 12px;
  color: #666;
}

.browse-button {
  background-color: #f0f0f0;
  border: none;
  padding: 10px 20px;
  margin-top: 10px;
  cursor: pointer;
  border-radius: 4px;
  font-size: 14px;
  width: 100%;
}

.browse-button:hover {
  background-color: #e0e0e0;
}
</style>
