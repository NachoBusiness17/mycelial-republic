/* CFMBT app.js — loads data/case.json only; fills fields; never auto-truths.
   A null stays a placeholder and its chip reads not-proven. No network calls
   beyond this one same-origin fetch. */
(function () {
  "use strict";

  function setText(el, value) {
    el.textContent = value;
  }

  function fillField(key, value, el) {
    if (value === null || value === undefined || value === "" ||
        (Array.isArray(value) && value.length === 0)) {
      // leave the placeholder text; score it not-proven
      const chip = document.createElement("span");
      chip.className = "chip np";
      chip.textContent = " not-proven";
      el.appendChild(chip);
      return;
    }
    if (Array.isArray(value)) {
      el.textContent = value.join(" · ");
    } else {
      setText(el, String(value));
    }
  }

  function walk(obj, prefix) {
    Object.keys(obj).forEach(function (k) {
      const key = prefix ? prefix + "." + k : k;
      const value = obj[k];
      if (value !== null && typeof value === "object" && !Array.isArray(value)) {
        walk(value, key);
        return;
      }
      document.querySelectorAll('[data-field="' + key + '"]').forEach(function (el) {
        fillField(key, value, el);
      });
    });
  }

  function links(obj, prefix) {
    Object.keys(obj).forEach(function (k) {
      const key = prefix ? prefix + "." + k : k;
      const value = obj[k];
      if (value !== null && typeof value === "object" && !Array.isArray(value)) {
        links(value, key);
        return;
      }
      if (typeof value === "string" && value && elIsLink(key)) {
        document.querySelectorAll('a[data-field="' + key + '"]').forEach(function (a) {
          a.href = value;
          a.textContent = value;
        });
      }
    });
  }

  function elIsLink(key) {
    return /url$/.test(key);
  }

  function main() {
    // Explain drawer
    const toggle = document.getElementById("explain-toggle");
    const drawer = document.getElementById("explain");
    if (toggle && drawer) {
      toggle.addEventListener("click", function (e) {
        e.preventDefault();
        drawer.hidden = !drawer.hidden;
      });
      const close = document.getElementById("explain-close");
      if (close) close.addEventListener("click", function () { drawer.hidden = true; });
    }

    fetch("data/case.json", { credentials: "omit" })
      .then(function (r) { return r.json(); })
      .then(function (c) { walk(c, ""); links(c, ""); })
      .catch(function () {
        // fetch blocked (file:// or offline): placeholders stay, chips not added.
        // The printed page still reads with not-proven semantics.
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", main);
  } else {
    main();
  }
})();
