import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

// --- Инициализация ---
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x111122);

const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(4, 2, 5);

const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.setPixelRatio(window.devicePixelRatio);
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
document.getElementById('canvas-container').appendChild(renderer.domElement);

// --- Управление ---
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.autoRotate = true;
controls.autoRotateSpeed = 2.0;
controls.enableZoom = true;
controls.enablePan = true;
controls.maxPolarAngle = Math.PI / 2;
controls.target.set(0, 1, 0);

// --- Освещение ---
// Окружающий свет
const ambientLight = new THREE.AmbientLight(0x404060, 1.5);
scene.add(ambientLight);

// Основной свет сверху-спереди
const mainLight = new THREE.DirectionalLight(0xffffff, 2);
mainLight.position.set(2, 3, 4);
mainLight.castShadow = true;
mainLight.shadow.mapSize.width = 1024;
mainLight.shadow.mapSize.height = 1024;
mainLight.shadow.camera.near = 0.5;
mainLight.shadow.camera.far = 15;
mainLight.shadow.camera.left = -3;
mainLight.shadow.camera.right = 3;
mainLight.shadow.camera.top = 3;
mainLight.shadow.camera.bottom = -3;
scene.add(mainLight);

// Заполняющий свет снизу
const fillLight = new THREE.PointLight(0x4466ff, 1);
fillLight.position.set(0, -1, 2);
scene.add(fillLight);

// Контровой свет
const backLight = new THREE.PointLight(0xffaa33, 0.8);
backLight.position.set(-2, 1, -3);
scene.add(backLight);

// Добавляем легкую подсветку сбоку
const sideLight = new THREE.PointLight(0x88aaff, 0.8);
sideLight.position.set(-2, 1, 2);
scene.add(sideLight);

// Пол (полупрозрачный)
const gridHelper = new THREE.GridHelper(8, 20, 0x88aaff, 0x335588);
gridHelper.position.y = -0.5;
scene.add(gridHelper);

// --- Загрузка модели ---
const loader = new GLTFLoader();

// Показываем прогресс загрузки
const loadingDiv = document.getElementById('loading');

loader.load(
    window.modelPath,
    (gltf) => {
        const model = gltf.scene;
        
        // Включаем тени для всех частей модели
        model.traverse((node) => {
            if (node.isMesh) {
                node.castShadow = true;
                node.receiveShadow = true;
                // Если материал есть, настраиваем его
                if (node.material) {
                    // Для лучшего отражения света
                    if (Array.isArray(node.material)) {
                        node.material.forEach(m => {
                            m.roughness = 0.3;
                            m.metalness = 0.1;
                        });
                    } else {
                        node.material.roughness = 0.3;
                        node.material.metalness = 0.1;
                    }
                }
            }
        });
        
        // Масштабируем и позиционируем модель
        model.scale.set(0.1, 0.1, 0.1); // Подберите масштаб под вашу модель
        model.position.y = -0.5;
        model.rotation.y = Math.PI; // Развернем модель, если нужно
        
        scene.add(model);
        
        loadingDiv.style.opacity = '0';
        setTimeout(() => {
            loadingDiv.style.display = 'none';
        }, 500);
        
        console.log('Модель успешно загружена!');
    },
    (xhr) => {
        const percent = Math.floor((xhr.loaded / xhr.total) * 100);
        loadingDiv.textContent = `Загрузка модели... ${percent}%`;
    },
    (error) => {
        console.error('Ошибка загрузки модели:', error);
        loadingDiv.textContent = 'Ошибка загрузки модели 😕';
        loadingDiv.style.background = 'rgba(255,0,0,0.8)';
    }
);

// --- Анимация ---
function animate() {
    requestAnimationFrame(animate);

    // Автоматическое вращение
    controls.update();

    renderer.render(scene, camera);
}

animate();

// --- Обработка изменения размера окна ---
window.addEventListener('resize', onWindowResize, false);
function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}