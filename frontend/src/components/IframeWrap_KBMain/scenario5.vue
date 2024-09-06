<template>
  <div class="scenario-content">
    <h2>Scenarios based on Chinese Standards</h2>
    <div class="sub-section">
      <p style="text-align: justify; padding: 10px;">These scenarios are employed to access the overall condition of bridges.</p>
      <p style="text-align: justify; padding: 10px;">The knowledge outlined in Chinese Standards is utilized:</p>
      <ul style="text-align: justify; padding: 10px;">
        <li>公路桥涵养护规范 Specifications for Maintenance of Highway Bridges and Culverts (JTG 5120-2021)</li>
        <li>公路桥涵设计通用规范 General Specifications for Design of Highway Bridges and Culverts (JTG D60-2015)</li>
        <li>公路桥梁技术状况评定标准 Standards for Technical Condition Evaluation of Highway Bridges (JTG/T H21-2021)</li>
        <li>公路桥梁承载能力检测评定规程 Specification for Inspection and Evaluation of Load-bearing Capacity of Highway Bridge
          (JTG/T J21-2011)</li>
        <li>公路桥梁加固设计规范 Specification for Strengthening Design of Highway Bridges (JTG/T J22-2008)</li>
        <li>公路桥梁加固施工技术规范 Technical Specification for Strengthening Construction of Highway Bridges (JTG/T J23-2008)
        </li>
        <li>公路桥梁水下构件检测技术规程 Technical Regulations for Inspection of Underwater CompOnents of Highway Bridges (T/CECS
          G:J56-2019)</li>
        <li>公路桥梁抗震性能评价细则 Guidelines for Aseismic Performance Evaluation of Highway Bridges (JTG/T 2231-02-2021)</li>
        <li>公路桥梁抗震设计规范 Specifications for Seismic Design of Highway Bridges (JTG/T 2231-01-2020)</li>
        <li>公路桥梁荷载试验规程 Load Test Methods for Highway Bridge (JTG/T J21 01-2015)</li>
      </ul>
      <p style="text-align: justify; padding: 10px;">These bodies of knowledge are represented in the proposed ontological knowledge base, using a semantic,
        logic-based format that enables computational processing.</p>
      <div class="scenario-image">
        <img src="/imgs/KBMain/Scenario-technical1.png" alt="Maintenance Scenario 5" width=100%>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  name: 'Scenario5'
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
  list-style-type: disc;
  padding-left: 0;
}

li {
  margin-bottom: 5px;
}
</style>
