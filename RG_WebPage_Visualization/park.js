$("a").click(function (event) {
    alert(event.target.id);
});

$(document).keyup(function (e) {
    if (e.keyCode == 27) {
        window.location = 'index.html';
    }
});
var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 3;
var renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

window.addEventListener('resize', function () {
    var width = window.innerWidth;
    var height = window.innerHeight;
    renderer.setSize(width, height);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
});
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
var geometry = new THREE.BoxGeometry(1000, 1000, 1000);
var cubeMaterials =
    [
        new THREE.MeshBasicMaterial({ map: new THREE.TextureLoader().load('images/posx.jpg'), side: THREE.DoubleSide }),
        new THREE.MeshBasicMaterial({ map: new THREE.TextureLoader().load('images/negx.jpg'), side: THREE.DoubleSide }),
        new THREE.MeshBasicMaterial({ map: new THREE.TextureLoader().load('images/posy.jpg'), side: THREE.DoubleSide }),
        new THREE.MeshBasicMaterial({ map: new THREE.TextureLoader().load('images/negy.jpg'), side: THREE.DoubleSide }),
        new THREE.MeshBasicMaterial({ map: new THREE.TextureLoader().load('images/posz.jpg'), side: THREE.DoubleSide }),
        new THREE.MeshBasicMaterial({ map: new THREE.TextureLoader().load('images/negz.jpg'), side: THREE.DoubleSide }),
    ];
var o;
var material = new THREE.MeshFaceMaterial(cubeMaterials);
//var material = new THREE.MeshFaceMaterial( {color: 0x00ff00} );
var cube = new THREE.Mesh(geometry, material);
scene.add(cube);
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
        object.position.z = -3;
        o = object;
        //controls = new THREE.OrbitControls(object, renderer.domElement);
    });
});
controls = new THREE.OrbitControls(camera, renderer.domElement);
var update = function () {
    o.position.y += 0.01;
    o.position.z += 0.01;
    o.position.x += 0.01;
    if (o.position.x > 5 || o.position.y > 5 || o.position.z > 5) {
        o.position.y = 0;
        o.position.z = 0;
        o.position.x = 0;
    }
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