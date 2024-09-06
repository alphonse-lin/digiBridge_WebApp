<template>
  <div>
    <h1>Knowledge-based Maintenance</h1>
    
    <div class="mb-4" style="width: 100%; text-align: center;">
      <el-button @click="navigateToStep(0)" type="info">Main</el-button>
      <el-button @click="navigateToStep(1)" type="info">Bridge Maintenance Ontology</el-button>
      <el-button @click="navigateToStep(2)" type="info">Maintenance Scenario</el-button>
      <el-button @click="navigateToStep(3)" type="info">Integrating Experimental Data</el-button>
    </div>
    <div class="step-content">
      <component :is="currentStepComponent" :activeStep="activeStep"></component>
      <iframe v-if="activeStep === 1" 
              src="https://jyl61.github.io/BMO/index.html" 
              style="width: 100%; height: 80vh; border: none;">
      </iframe>
      <scenario2 v-if="activeStep === 2"></scenario2>
      <scenario3 v-if="activeStep === 3"></scenario3>
    </div>
    <br>

    <div class="container" v-if="activeStep === 0">
      <!-- 原有的内容 -->
      <p>Welcome to the Knowledge-based Maintenance website. This platform aims to provide insights and solutions for maintenance scenarios and bridge maintenance ontology.</p>

      <div class="module-block">
        <p>The following figure shows a proposed framework, which is knowledge driven and targets the development of suitable knowledge networking mechanisms to drive numerous tools. Specifically, this roadmap uses semantic web technology, BIM, and IoTs to integrate maintenance data with embedded big data methods support to enable smart reasoning and holistic maintenance decision-making.</p>

        <div class="image-container">
          <img :src="knowledgeImageUrl" alt="Knowledge Framework" class="module-image">
        </div>

        <p>Three key components:<br>
        smart raw data acquisition. maintenance big data are collected in a large volume and comprehensively throughout the whole bridge lifecycle.<br>
        data and information unification through BIM. In a data-driven manner, a BIM platform is used for real-time data/information sharing and multiparty collaboration with high-performance computing power.<br>
        and dynamic ontological knowledge processing. In a knowledge-driven manner, a dynamic semantic knowledge base is used for intelligent semantic recognition, semantic information integration, numerical-based and logical-based reasoning, and holistic decision-making. The collaboration of these three crucial components allows the whole framework to work seamlessly and effectively.</p>
      </div>

      <!-- 其他模块块 -->
    </div>
  </div>
</template>

<script>
import scenario2 from './scenario.vue'
import scenario3 from './ExData.vue'

export default {
  name: 'KnowledgeBasedMaintenance',
  components: {
    scenario2,
    scenario3
  },
  props: {
    initialStep: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      activeStep: this.initialStep,
      maintenanceScenarioUrl: '/knowledge-basedscenario',
      experimentalDataUrl: '/experimental-data',
      knowledgeImageUrl: '/imgs/KBMain/knowledge.png'
    }
  },
  watch: {
    initialStep(newValue) {
      this.navigateToStep(newValue);
    }
  },
  computed: {
    currentStepComponent() {
      if (this.activeStep === 0) return 'Step1Com'
      return null
    }
  },
  methods: {
    navigateToStep(step) {
      this.activeStep = step
      console.log('Navigating to step:', step);
    }
  },
  mounted() {
    console.log('!!!!!!!!!!!!!!!!!!!')
    console.log(this.initialStep)
    // this.navigateToStep(this.initialStep);
  }
}
</script>

<style scoped>
/* 您的原有样式 */
.module-buttons {
  display: flex;
  justify-content: space-around;
  margin-bottom: 20px;
}

.container {
  max-width: 800px;
  margin: 0 auto;
}

.module-block {
  margin-bottom: 30px;
}

.module-title {
  font-size: 1.5em;
  margin-bottom: 10px;
}

.image-container {
  text-align: center;
  margin: 20px 0;
}

.module-image {
  max-width: 100%;
  height: auto;
}

.footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>