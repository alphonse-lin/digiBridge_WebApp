<template>
    <div class="dt-sync">
        <div class="section">
            <h1>Digital Twin Synchronisation for Crack Damage</h1>
        </div>


        <div class="section">
            <img src="/imgs/DTsync/diagram_backup/framework.png" width="100%" alt="Drone Survey Concept" />
        </div>

        <h2>Surface damage synchronised to its digital twin model</h2>

        <div class="section">
            <h3>🔁 Uploading Point Cloud model</h3>
            <input type="file" accept=".txt" @change="handlePointCloudUpload">
            <div ref="pointCloudContainer" class="model-viewer"></div>
        </div>

        <div class="section">
            <h3>📤 Initial finite element model</h3>
            <input type="file" accept=".stl" @change="handleStlUpload">
            <div ref="stlContainer" class="model-viewer"></div>
        </div>

        <div class="section">
            <h3>🔁 Digital twin model updating</h3>
            <el-button @click="synchronize_1">Synchronize</el-button>
            <div v-if="showVideo_1" class="video-container">
                <video width="50%" controls>
                    <source src="/imgs/DTsync/animation_backup/crack_updating.mp4" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            </div>
        </div>

        <div class="section">
            <h3>✨ Results of the updated structural analysis</h3>
            <el-button @click="synchronize_2">Synchronize</el-button>
            <div v-if="showVideo_2" class="video-container">
                <video width="50%" controls>
                    <source src="/imgs/DTsync/animation_backup/analysis animation.mp4" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as THREE from 'three'
import { STLLoader } from 'three/examples/jsm/loaders/STLLoader'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'

const pointCloudContainer = ref(null)
const stlContainer = ref(null)
let pointCloudScene, pointCloudCamera, pointCloudRenderer, pointCloudControls
let stlScene, stlCamera, stlRenderer, stlControls

const showVideo_1 = ref(false)
const showVideo_2 = ref(false)

function synchronize_1() {
    showVideo_1.value = true
}

function synchronize_2() {
    showVideo_2.value = true
}

onMounted(() => {
    nextTick(() => {  // 使用 nextTick 确保 DOM 已更新
        console.log("初始化")
        initStlViewer()
        initPointCloudViewer()
        console.log("开始加载")
        loadStlModel('/models/DTsync/stlfile.stl')
        loadPointCloudModel('/models/DTsync/4 - Cloud.txt')
        console.log("加载完成")
    })
})

onUnmounted(() => {
    // Clean up Three.js resources
    if (pointCloudRenderer) pointCloudRenderer.dispose()
    if (stlRenderer) stlRenderer.dispose()
})

function initPointCloudViewer() {
    pointCloudScene = new THREE.Scene()
    pointCloudScene.background = new THREE.Color(0xf0f0f0) // 设置浅色背景
    pointCloudCamera = new THREE.PerspectiveCamera(75, stlContainer.value.clientWidth / stlContainer.value.clientHeight, 0.1, 1000)
    pointCloudRenderer = new THREE.WebGLRenderer()
    pointCloudRenderer.setSize(stlContainer.value.clientWidth, stlContainer.value.clientHeight)
    pointCloudContainer.value.appendChild(pointCloudRenderer.domElement)

    pointCloudCamera.position.z = 5
    pointCloudControls = new OrbitControls(pointCloudCamera, pointCloudRenderer.domElement)

    const animate = () => {
        requestAnimationFrame(animate)
        pointCloudControls.update()
        pointCloudRenderer.render(pointCloudScene, pointCloudCamera)
    }
    animate()
}

const handlePointCloudUpload = (event) => {
    const file = event.target.files[0]
    if (file) {
        const reader = new FileReader()
        reader.onload = (e) => {
            const content = e.target.result
            const points = parsePointCloudData(content)
            renderPointCloud(points)
        }
        reader.readAsText(file)
    }
}

function loadPointCloudModel(url) {
    fetch(url)
        .then(response => response.text())
        .then(data => {
            const points = parsePointCloudData(data)
            renderPointCloud(points)
        })
        .catch(error => {
            console.error('Error loading point cloud model:', error)
        })
}

function parsePointCloudData(content) {
    return content.split('\n')
        .map(line => {
            const [x, y, z, r, g, b] = line.split(' ').map(Number)
            return { position: [x, y, z], color: getColorFromHeight(z) }
        })
        .filter(point => point.position.length === 3 && point.color.length === 3 && !point.position.some(isNaN) && !point.color.some(isNaN))
}

function getColorFromHeight( z) {
    const minZ = -0.5 // 根据你的数据调整
    const maxZ = 0.5 // 根据你的数据调整

    const normalizedZ = (z - minZ) / (maxZ - minZ)
    const logZ = Math.log1p((normalizedZ) * 9) / Math.log(10) // 对数缩放
    const color = new THREE.Color()
    color.setHSL((1.0 - logZ) * 0.7, 1.0, 0.5)
    return [color.r, color.g, color.b]
}

function renderPointCloud(points) {
    const geometry = new THREE.BufferGeometry()
    const vertices = new Float32Array(points.flatMap(point => point.position))
    const colors = new Float32Array(points.flatMap(point => point.color))
    geometry.setAttribute('position', new THREE.BufferAttribute(vertices, 3))
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3))

    const material = new THREE.PointsMaterial({ size: 0.05, vertexColors: true })
    const pointCloud = new THREE.Points(geometry, material)

    pointCloudScene.clear()
    pointCloudScene.add(pointCloud)

    const box = new THREE.Box3().setFromObject(pointCloud)
    const center = box.getCenter(new THREE.Vector3())
    const size = box.getSize(new THREE.Vector3())
    const maxDim = Math.max(size.x, size.y, size.z)
    const scale = 10 / maxDim
    pointCloud.scale.set(scale, scale, scale)
    pointCloud.position.sub(center.multiplyScalar(scale))

    pointCloudCamera.position.z = 5
    pointCloudControls.reset()
}

function initStlViewer() {
    if (!stlContainer.value) return  // 确保容器存在

    stlScene = new THREE.Scene()
    stlScene.background = new THREE.Color(0xf0f0f0)
    stlCamera = new THREE.PerspectiveCamera(75, stlContainer.value.clientWidth / stlContainer.value.clientHeight, 0.1, 1000)
    stlRenderer = new THREE.WebGLRenderer()
    stlRenderer.setSize(stlContainer.value.clientWidth, stlContainer.value.clientHeight)
    stlContainer.value.appendChild(stlRenderer.domElement)

    stlCamera.position.z = 5
    stlControls = new OrbitControls(stlCamera, stlRenderer.domElement)

    // 添加动画循环
    function animate() {
        requestAnimationFrame(animate)
        stlControls.update()
        stlRenderer.render(stlScene, stlCamera)
    }
    animate()
}

function loadStlModel(url) {
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.arrayBuffer();
        })
        .then(data => {
            const geometry = new STLLoader().parse(data);
            renderStl(geometry);
            // 添加这一行，确保控制器更新和重新渲染
            // stlControls.update();
        })
        .catch(error => {
            console.error('Error loading STL model:', error);
        });
}

function handleStlUpload(event) {
  const file = event.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => {
      try {
        const geometry = new STLLoader().parse(e.target.result)
        renderStl(geometry)
      } catch (error) {
        console.error('Error parsing STL file:', error)
      }
    }
    reader.onerror = (e) => {
      console.error('Error reading file:', e)
    }
    reader.readAsArrayBuffer(file)
  }
}

function renderStl(geometry) {
    if (!stlScene) {
        console.error('STL scene is not initialized')
        return
    }
    stlScene.clear();
    // const material = new THREE.MeshPhongMaterial({ color: 0xaaaaaa, specular: 0x111111, shininess: 200 });
    const material = new THREE.MeshPhysicalMaterial({
        color: 0xb2ffc8,
        // envMap: envTexture,
        metalness: 0.25,
        roughness: 0.1,
        opacity: 1.0,
        transparent: true,
        transmission: 0.99,
        clearcoat: 1.0,
        clearcoatRoughness: 0.25,
    })
    const mesh = new THREE.Mesh(geometry, material);


    stlScene.add(mesh);
    

    // 添加灯光
    const light1 = new THREE.DirectionalLight(0xffffff, 1);
    light1.position.set(1, 1, 1).normalize();
    stlScene.add(light1);

    const light2 = new THREE.DirectionalLight(0xffffff, 1);
    light2.position.set(-1, -1, -1).normalize();
    stlScene.add(light2);

    stlScene.add(new THREE.AmbientLight(0x222222));

    // 居中并缩放STL模型
    const box = new THREE.Box3().setFromObject(mesh);
    const center = box.getCenter(new THREE.Vector3());
    const size = box.getSize(new THREE.Vector3());
    const maxDim = Math.max(size.x, size.y, size.z);
    const scale = 10 / maxDim;
    mesh.scale.set(scale, scale, scale);
    mesh.position.sub(center.multiplyScalar(scale));

    // 调整相机位置
    stlCamera.position.set(0, 0, 10);
    stlCamera.lookAt(0, 0, 0);

    // 重置并更新控制器
    stlControls.reset();
    stlControls.update();

    // 渲染场景
    stlRenderer.render(stlScene, stlCamera);
}

</script>

<style scoped>
h1,
h2,
h3 {
    color: #2c3e50;
    margin-bottom: 10px;
}

.tab {
    overflow: hidden;
    border: 1px solid #ccc;
    background-color: #f1f1f1;
}

.tab button {
    background-color: inherit;
    float: left;
    border: none;
    outline: none;
    cursor: pointer;
    padding: 14px 16px;
    transition: 0.3s;
    width: 100%;
    text-align: center;
}

.tab button:hover {
    background-color: #ddd;
}

.tab button.active {
    background-color: #ccc;
}

.tabcontent {
    padding: 6px 12px;
    border: 1px solid #ccc;
    border-top: none;
}

.section {
    margin-bottom: 30px;
}

.input-group {
    margin-bottom: 15px;
}

label {
    display: block;
    margin-bottom: 5px;
}

#results,
.viewer {
    background-color: #f0f0f0;
    padding: 15px;
    border-radius: 5px;
}

.viewer {
    width: 100%;
    height: 400px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 18px;
    color: #666;
    margin-top: 20px;
}

#viewer img {
    max-width: 100%;
    max-height: 100%;
}

.model-viewer {
    width: 100%;
    height: 400px;
    background-color: #f0f0f0;
    padding: 15px;
    border-radius: 5px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.video-container {
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>