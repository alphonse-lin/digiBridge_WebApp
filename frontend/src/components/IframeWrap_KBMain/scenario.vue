<template>
  <div class="maintenance-scenario">
    <header>
      <h1>Maintenance Scenario</h1>
    </header>
    
    <div class="mb-4" style="width: 100%; text-align: center;">
      <el-button plain @click="setStandard('all')" type="info">All Standards</el-button>
      <el-button plain @click="setStandard('UK')" type="info">UK Standards</el-button>
      <el-button plain @click="setStandard('Chinese')" type="info">Chinese Standards</el-button>
      <el-button plain @click="showOntology" type="info">Show Ontology</el-button>
    </div>

    <div class="content">
      <div class="scenario-list" style="height:80vh">
        <h2 
          v-for="scenario in filteredScenarios" 
          :key="scenario.id"
          @click="setCurrentScenario(scenario.id)"
          :class="{ 'active': currentScenario === scenario.id }"
        >
          {{ scenario.title }}
        </h2>
      </div>

      <div class="scenario-content" style="height:80vh">
        <iframe v-if="showingOntology" src="https://jyl61.github.io/BMO/webvowl/index.html" style="width: 100%; height: 100%; border: none;"></iframe>
        <!-- <keep-alive v-else>
          <component :is="currentScenarioComponent" v-if="currentScenarioComponent" ></component>
        </keep-alive> -->
        <component v-else-if="currentScenarioComponent" :is="currentScenarioComponent"></component>
      </div>
    </div>
  </div>
</template>

<script>
import Scenario1 from './scenario1.vue'
import Scenario2 from './scenario2.vue'
import Scenario3 from './scenario3.vue'
import Scenario4 from './scenario4.vue'
import Scenario5 from './scenario5.vue'
import Scenario6 from './scenario6.vue'
import Scenario7 from './scenario7.vue'
import Scenario8 from './scenario8.vue'
import Scenario9 from './scenario9.vue'

export default {
  name: 'MaintenanceScenario',
  components: {
    Scenario1,
    Scenario2,
    Scenario3,
    Scenario4,
    Scenario5,
    Scenario6,
    Scenario7,
    Scenario8,
    Scenario9
  },
  data() {
    return {
      currentScenario: 1,
      currentStandard: 'all',
      showingOntology: false,
      scenarios: [
        { id: 1, title: 'Evaluating Corrosion on Metal', standard: 'UK' },
        { id: 2, title: 'Evaluating Coatings to Metal', standard: 'UK' },
        { id: 3, title: 'Evaluating Crack on Masonry', standard: 'UK' },
        { id: 4, title: 'Evaluating Crack on Reinforced Concrete', standard: 'UK' },
        { id: 5, title: 'Scenarios based on Chinese Standards', standard: 'Chinese' },
        { id: 6, title: 'Bridge Technical Condition Evaluation', standard: 'Chinese' },
        { id: 7, title: 'Bridge Material Condition Evaluation', standard: 'Chinese' },
        { id: 8, title: 'Bridge Safety Performance Evaluation', standard: 'Chinese' },
        { id: 9, title: 'Bridge Strengthening Design', standard: 'Chinese' },
      ]
    }
  },
  computed: {
    filteredScenarios() {
      if (this.currentStandard === 'all') {
        return this.scenarios
      }
      return this.scenarios.filter(scenario => scenario.standard === this.currentStandard)
    },
    currentScenarioComponent() {
      const componentName = `Scenario${this.currentScenario}`
      console.log('Current scenario component:', componentName)
      return componentName
    }
  },
  methods: {
    setStandard(standard) {
      this.currentStandard = standard
      this.showingOntology = false
      if (this.filteredScenarios.length > 0) {
        this.setCurrentScenario(this.filteredScenarios[0].id)
      }
    },
    setCurrentScenario(id) {
      console.log('Setting current scenario to:', id)
      this.currentScenario = id
      this.showingOntology = false
    },
    showOntology() {
      this.showingOntology = true
    }
  },
  watch: {
    currentScenario(newVal, oldVal) {
      console.log(`Scenario changed from ${oldVal} to ${newVal}`)
    }
  }
}
</script>

<style scoped>
.maintenance-scenario {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.content {
  display: flex;
  flex: 1;
}

.scenario-list {
  width: 250px;
  overflow-y: auto;
  padding: 10px;
  border-right: 1px solid #ccc;
}

.scenario-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.scenario-list h2 {
  cursor: pointer;
  padding: 10px;
  margin: 5px 0;
  border-radius: 5px;
}

.scenario-list h2.active {
  font-weight: bold;
  background-color: #f0f0f0;
}

/* Add more styles as needed */
</style>