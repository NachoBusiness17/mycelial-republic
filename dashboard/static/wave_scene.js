(function () {
  var home = { x: 0, y: 0, w: 720, h: 280 };
  var cam = { x: 0, y: 0, w: 720, h: 280 };
  var dragging = false, moved = false, lastX = 0, lastY = 0;

  function applyCam(svg) {
    svg.setAttribute("viewBox", cam.x + " " + cam.y + " " + cam.w + " " + cam.h);
  }

  function resetCam(svg) {
    cam.x = home.x; cam.y = home.y; cam.w = home.w; cam.h = home.h;
    applyCam(svg);
  }

  function bindCam(svg) {
    if (svg.getAttribute("data-cam") === "1") return;
    svg.setAttribute("data-cam", "1");
    svg.style.touchAction = "none";
    svg.addEventListener("wheel", function (e) {
      e.preventDefault();
      var factor = e.deltaY > 0 ? 1.08 : 0.92;
      var nw = Math.min(1600, Math.max(220, cam.w * factor));
      var nh = nw * (home.h / home.w);
      var mx = e.offsetX / (svg.clientWidth || 1);
      var my = e.offsetY / (svg.clientHeight || 1);
      cam.x += (cam.w - nw) * mx;
      cam.y += (cam.h - nh) * my;
      cam.w = nw;
      cam.h = nh;
      applyCam(svg);
    }, { passive: false });
    svg.addEventListener("pointerdown", function (e) {
      if (e.button !== 0) return;
      if (e.target && e.target.closest && e.target.closest("[data-exit],[data-look],[data-talk]")) return;
      dragging = true;
      moved = false;
      lastX = e.clientX;
      lastY = e.clientY;
      svg.style.cursor = "grabbing";
      svg.setPointerCapture(e.pointerId);
    });
    svg.addEventListener("pointermove", function (e) {
      if (!dragging) return;
      var dx = e.clientX - lastX;
      var dy = e.clientY - lastY;
      if (dx || dy) moved = true;
      lastX = e.clientX;
      lastY = e.clientY;
      var sx = cam.w / (svg.clientWidth || 1);
      var sy = cam.h / (svg.clientHeight || 1);
      cam.x -= dx * sx;
      cam.y -= dy * sy;
      applyCam(svg);
    });
    function endDrag() {
      dragging = false;
      svg.style.cursor = "grab";
    }
    svg.addEventListener("pointerup", endDrag);
    svg.addEventListener("pointercancel", endDrag);
    svg.addEventListener("dblclick", function (e) {
      if (e.target && e.target.closest && e.target.closest("[data-exit],[data-look],[data-talk]")) return;
      resetCam(svg);
    });
  }

  window.mountRoomSvg = function (html) {
    var graph = document.getElementById("graph");
    if (!graph || !html) return;
    var live = graph.querySelector("svg[data-scene='room']");
    var box = document.createElement("div");
    box.innerHTML = html;
    var next = box.querySelector("svg[data-scene='room']");
    if (live && next) {
      ["world", "props", "people", "exits", "labels"].forEach(function (name) {
        var a = live.querySelector('g[data-layer="' + name + '"]');
        var b = next.querySelector('g[data-layer="' + name + '"]');
        if (a && b) a.innerHTML = b.innerHTML;
      });
      applyCam(live);
      bindCam(live);
      return;
    }
    graph.innerHTML = html;
    var svg = graph.querySelector("svg[data-scene='room']");
    if (!svg) return;
    var vb = (svg.getAttribute("viewBox") || "0 0 720 280").trim().split(/\s+/).map(Number);
    home.x = cam.x = vb[0] || 0;
    home.y = cam.y = vb[1] || 0;
    home.w = cam.w = vb[2] || 720;
    home.h = cam.h = vb[3] || 280;
    bindCam(svg);
  };
})();
