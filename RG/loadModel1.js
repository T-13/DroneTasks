var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);
camera.position.z = 3;
var renderer = new THREE.WebGLRenderer();
renderer.setSize(240, 240);
container = document.getElementById( 'canvas1' );
container.appendChild(renderer.domElement);


var keyLight = new THREE.DirectionalLight(new THREE.Color('hsl(30, 100%, 75%)'), 1.0);
keyLight.position.set(-100, 0, 100);

var fillLight = new THREE.DirectionalLight(new THREE.Color('hsl(240, 100%, 75%)'), 0.75);
fillLight.position.set(100, 0, 100);

var backLight = new THREE.DirectionalLight(0xffffff, 1.0);
backLight.position.set(100, 0, -100).normalize();

scene.add(keyLight);
scene.add(fillLight);
scene.add(backLight);
//controls = new THREE.OrbitControls(camera, renderer.domElement);
//create the shape

var mtlLoader = new THREE.MTLLoader();
mtlLoader.setTexturePath('object/');
mtlLoader.setPath('/object/');
mtlLoader.load('Drone_obj.mtl', function (materials) {
    materials.preload();
    var objLoader = new THREE.OBJLoader();
    objLoader.setMaterials(materials);
    objLoader.setPath('/object/');
    objLoader.load('Drone_obj.obj', function (object) {
        scene.add(object);
        object.position.z = 0;
        object.scale.set( 3, 3, 3 )
    });
});

var update = function () {
    scene.rotation.x += 0.01;
    scene.rotation.y += 0.01;
};

//draw scene
var render = function () {
    renderer.render(scene, camera);
};

//run game loop (update, render, repeat)
var GameLoop = function () {
    requestAnimationFrame(GameLoop);
    update();
    render();
};

GameLoop();