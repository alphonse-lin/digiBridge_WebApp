<template>
    <div class="iot-sensors">
      <div class="sensor-column">
        <h2>Air Bus Sensor</h2>
        <p>Description of Air Bus Sensor...</p>
        <div class="sensor-image" >
          <img src="/imgs/iotSensors/airbus-sensor.jpg" width="100%" alt="Air Bus Sensor" />
        </div>
        <div class="sensor-installation">
            <img src="/imgs/iotSensors/airbus-sensor-installation.jpg" width="100%" alt="Air Bus Sensor Installation" >
        </div>
        <el-button type="primary" @click="goToGuanyuPage('airbus')">Air Bus Sensor</el-button>
      </div>
  
      <div class="sensor-column">
        <h2>Tonghe Sensor</h2>
        <p>Description of Tonghe Sensor...</p>
        <div class="sensor-image">
          <img src="/imgs/iotSensors/tonghe-sensor.jpg" width="100%" alt="Tonghe Sensor" />
        </div>
        <div class="sensor-installation">
          <img src="/imgs/iotSensors/tonghe-sensor-installation.jpg" width="100%" alt="Tonghe Sensor Installation" >
        </div>
        <el-button type="primary" @click="goToGuanyuPage('tonghe')">Tonghe Sensor</el-button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { useRouter } from 'vue-router';
  import useAppStore from '@/store/modules/app'
  
  const router = useRouter();
  const appStore = useAppStore();
  
  const goToGuanyuPage = (sensorType) => {
    // 这里需要根据实际情况设置正确的路由和参数
    router.push(`/guanyu-page?sensor=${sensorType}`);
    // 如果需要设置 monitorType 和触发事件，可以添加以下代码：
    // appStore.setMonitorType(someValue);
    // setTimeout(() => {
    //   Bus.emit('someEvent');
    // }, 500);
  }
  </script>
  
  <style scoped>
  .iot-sensors {
    display: flex;
    gap: 20px;
  }
  
  .sensor-column {
    flex: 1;
    padding: 20px;
    border: 1px solid #eee;
    border-radius: 5px;
  }
  
  h2 {
    margin-bottom: 10px;
    text-align: center;
  }
  
  .sensor-image, .sensor-installation {
    margin-bottom: 20px;
    text-align: center;
    width: 100%;
  }
  
  .sensor-image img {
    max-width: 100%;
    height: auto;
    margin-bottom: 10px;
    margin-top: 10px;
    text-align: center;
    width: 100%;
  }
  
  el-button {
    width: 100%;
    margin-top: 10px;
    margin-bottom: 10px;
    text-align: center;
  }
  </style>