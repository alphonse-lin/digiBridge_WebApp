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
    <img src="/imgs/autoMSG/table.png" alt="dataset-preview" class="dataset-preview"
      style="display: block; margin: auto; width: 90%;">
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

    <p v-if="processing" class="processing-message">Processing it, Please Wait...</p>

    <div v-if="uploadedImage || predictedSolution" class="results-container">
      <h3>Results:</h3>
      <div class="result-content">
        <div v-if="uploadedImage" class="uploaded-image">
          <h4>Uploaded Image:</h4>
          <img :src="uploadedImage" alt="Uploaded image" />
        </div>
        <div v-if="predictedSolution" class="solution-details">
          <h4>Predicted Solution:</h4>
          <p>{{ predictedSolution }}</p>
          <h4 v-if="groundTruth">Ground Truth:</h4>
          <p v-if="groundTruth">{{ groundTruth }}</p>

          <h4>Feedback:</h4>
          <textarea v-model="feedback" placeholder="Enter your feedback here" rows="4"
            class="feedback-input"></textarea>
          <button @click="submitFeedback" class="submit-feedback">Submit Feedback</button>
        </div>
      </div>
    </div>

    <div v-if="feedbackSubmitted" class="feedback-message">
      Feedback submitted successfully!
    </div>
  </div>
</template>

<script>
import { generateSolution, addFeedback } from '@/api/bridge'

export default {
  name: 'AutomatedMaintenance',
  data() {
    return {
      results: [],
      predictedSolution: '',
      groundTruth: '',
      uploadedImage: null,
      processing: false,
      feedback: '',
      feedbackSubmitted: false,
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

        // 创建一个本地 URL 来显示上传的图片
        this.uploadedImage = URL.createObjectURL(files[0])
      }
    },
    async uploadFile(file) {
      const formData = new FormData()
      formData.append('file', file)

      try {
        console.log('Uploading file:', file.name)
        this.processing = true
        const response = await generateSolution(formData)
        console.log('Response:', response)
        this.predictedSolution = response.predicted_solution
        this.groundTruth = response.ground_truth || 'Not available'
        this.imageName = response.image_name // Store the image name
        console.log('Success:', response)
      } catch (error) {
        console.error('Error:', error)
        // ... error handling code ...
      } finally {
        this.processing = false
      }
    },

    async submitFeedback() {
      if (!this.feedback.trim()) {
        alert('Please enter feedback before submitting.')
        return
      }

      try {
        const response = await addFeedback({
          image_name: this.imageName,
          feedback: this.feedback
        })
        console.log('Feedback submitted:', response)
        this.feedbackSubmitted = true
        this.feedback = '' // Clear the feedback input
        setTimeout(() => {
          this.feedbackSubmitted = false
        }, 3000) // Hide the message after 3 seconds
      } catch (error) {
        console.error('Error submitting feedback:', error)
        alert('Failed to submit feedback. Please try again.')
      }
    }
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
  width: 80%;
  margin: auto;
  align-items: center;
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

.processing-message {
  text-align: center;
  font-weight: bold;
  color: #007bff;
  margin: 20px 0;
}

.results-container {
  margin-top: 20px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.result-content {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.uploaded-image {
  flex: 1;
  min-width: 300px;
  background-color: #e9ecef;
  padding: 15px;
  border-radius: 8px;
}

.uploaded-image img {
  max-width: 100%;
  height: auto;
  border-radius: 4px;
}

.solution-details {
  flex: 1;
  min-width: 300px;
  background-color: #e9ecef;
  padding: 15px;
  border-radius: 8px;
}

h4 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #2c3e50;
}

.solution-details p {
  background-color: #ffffff;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 15px;
}

.feedback-input {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  resize: vertical;
}

.submit-feedback {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.submit-feedback:hover {
  background-color: #0056b3;
}

.feedback-message {
  text-align: center;
  color: #28a745;
  margin-top: 10px;
  font-weight: bold;
}
</style>
