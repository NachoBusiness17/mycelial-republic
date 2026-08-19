if (!new URLSearchParams(location.search).has("gpu")) {
  /* SVG remains the record. Three.js is a readout. */
} else {
  document.body.classList.add("gpu");
  const THREE = await import("three");
  const canvas = document.getElementById("gpu");
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x111111);
  const camera = new THREE.PerspectiveCamera(50, 2, 0.1, 40);
  camera.position.set(0, 6, 8);
  camera.lookAt(0, 0, 0);
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: false });
  renderer.setPixelRatio(1);
  const mat = new THREE.LineBasicMaterial({ color: 0xf2f2f2, transparent: true });
  function box(x, z) {
    const s = 0.9;
    const p = [
      x - s, 0, z - s, x + s, 0, z - s,
      x + s, 0, z - s, x + s, 0, z + s,
      x + s, 0, z + s, x - s, 0, z + s,
      x - s, 0, z + s, x - s, 0, z - s
    ];
    const g = new THREE.BufferGeometry();
    g.setAttribute("position", new THREE.Float32BufferAttribute(p, 3));
    return new THREE.LineSegments(g, mat.clone());
  }
  const dirs = {
    north: box(0, -3),
    south: box(0, 3),
    east: box(3, 0),
    west: box(-3, 0),
    here: box(0, 0)
  };
  Object.values(dirs).forEach(function (m) { scene.add(m); });
  function resize() {
    const w = canvas.clientWidth || 480;
    const h = canvas.clientHeight || 128;
    renderer.setSize(w, h, false);
    camera.aspect = w / Math.max(h, 1);
    camera.updateProjectionMatrix();
  }
  resize();
  addEventListener("resize", resize);
  canvas.addEventListener("click", function (e) {
    const x = (e.offsetX / canvas.clientWidth) * 2 - 1;
    const y = -((e.offsetY / canvas.clientHeight) * 2 - 1);
    let dir = null;
    if (y > 0.35) dir = "north";
    else if (y < -0.35) dir = "south";
    else if (x > 0.35) dir = "east";
    else if (x < -0.35) dir = "west";
    if (dir && window.goDirWave) window.goDirWave(dir);
  });
  function tick() {
    const live = window.liveExits || new Set();
    ["north", "south", "east", "west"].forEach(function (d) {
      const m = dirs[d];
      const on = live.has(d);
      m.scale.setScalar(on ? 1 : 0.4);
      m.material.opacity = on ? 1 : 0.25;
    });
    renderer.render(scene, camera);
    requestAnimationFrame(tick);
  }
  tick();
}
