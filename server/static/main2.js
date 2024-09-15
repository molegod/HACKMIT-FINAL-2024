import * as THREE from 'three';
import * as GaussianSplats3D from 'https://unpkg.com/@mkkellogg/gaussian-splats-3d@0.4.0/build/gaussian-splats-3d.module.js'

const viewer = new GaussianSplats3D.Viewer({
    'cameraUp': [0, -1, -0.6],
    'initialCameraPosition': [-1, -4, 6],
    'initialCameraLookAt': [0, 4, 0],
    'sharedMemoryForWorkers': false
    // 'webXRMode': GaussianSplats3D.WebXRMode.VR
});

viewer.addSplatScene('static/public/pool.ply', {
    'splatAlphaRemovalThreshold': 5,
    'showLoadingUI': true,
    'position': [0, 1, 0],
    'rotation': [0, 0, 0, 1],
    'scale': [1.5, 1.5, 1.5],
    'dynamicScene': true,
})

.then(() => {
    viewer.start();
});