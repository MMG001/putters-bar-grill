// Putters Bar & Grill — site scripts

// Mobile nav toggle
(function () {
  var toggle = document.getElementById("navToggle");
  var nav = document.getElementById("mainNav");
  if (!toggle || !nav) return;
  toggle.addEventListener("click", function () {
    var open = nav.classList.toggle("is-open");
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
  });
  nav.addEventListener("click", function (e) {
    if (e.target.tagName === "A") {
      nav.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
    }
  });
})();

// Duplicate ticker content so the loop is seamless
(function () {
  var track = document.getElementById("tickerTrack");
  if (!track) return;
  track.appendChild(track.firstElementChild.cloneNode(true));
})();

// Scroll reveal
(function () {
  var items = document.querySelectorAll(".reveal");
  if (!items.length) return;
  if (!("IntersectionObserver" in window) ||
      window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    items.forEach(function (el) { el.classList.add("is-visible"); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });
  items.forEach(function (el) { io.observe(el); });
})();

// Hero parallax
(function () {
  var bg = document.getElementById("heroBg");
  if (!bg) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  var ticking = false;
  function update() {
    // hero sits at the top of the page, so scrollY maps directly
    var y = window.scrollY * 0.35;
    bg.style.transform = "translate3d(0," + y + "px,0)";
    ticking = false;
  }
  window.addEventListener("scroll", function () {
    if (!ticking) {
      ticking = true;
      requestAnimationFrame(update);
    }
  }, { passive: true });
  update();
})();

// Form submit -> FormSubmit AJAX endpoint (shows inline status)
function wireForm(formId, subjectFn) {
  var form = document.getElementById(formId);
  if (!form) return;
  var status = document.getElementById(formId + "Status");
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var btn = form.querySelector('[type="submit"], button:not([type])');
    var data = new FormData(form);
    if (data.get("_honey")) return; // bot
    data.append("_subject", subjectFn(data));
    if (btn) { btn.disabled = true; }
    status.textContent = "Sending\u2026";
    status.className = "form-status";
    fetch("https://formsubmit.co/ajax/hurley.puttersverona@yahoo.com", {
      method: "POST",
      body: data,
      headers: { "Accept": "application/json" }
    }).then(function (r) { return r.json(); }).then(function (res) {
      if (res.success === "true" || res.success === true) {
        status.textContent = "Got it \u2014 thanks! We\u2019ll get back to you soon.";
        status.className = "form-status form-status--ok";
        form.reset();
      } else { throw new Error(); }
    }).catch(function () {
      status.textContent = "Something went wrong \u2014 please call us at (608) 497-0170 or email hurley.puttersverona@yahoo.com.";
      status.className = "form-status form-status--err";
    }).finally(function () { if (btn) { btn.disabled = false; } });
  });
}
wireForm("contactForm", function (d) {
  return "[" + (d.get("type") || "General") + "] Website message from " + d.get("name");
});
wireForm("careersForm", function (d) {
  return "[Application: " + (d.get("role") || "Any role") + "] " + d.get("name");
});

// Menu category tabs
(function () {
  var btns = document.querySelectorAll(".tab-btn");
  if (!btns.length) return;
  btns.forEach(function (btn) {
    btn.addEventListener("click", function () {
      document.querySelectorAll(".tab-btn").forEach(function (b) {
        b.classList.remove("is-active");
        b.setAttribute("aria-selected", "false");
      });
      document.querySelectorAll(".tab-panel").forEach(function (p) {
        p.classList.remove("is-active");
      });
      btn.classList.add("is-active");
      btn.setAttribute("aria-selected", "true");
      var panel = document.getElementById(btn.dataset.tab);
      if (panel) panel.classList.add("is-active");
    });
  });
})();

// Gallery lightbox
(function () {
  var box = document.getElementById("lightbox");
  if (!box) return;
  var img = document.getElementById("lightboxImg");
  var cap = document.getElementById("lightboxCaption");
  var count = document.getElementById("lightboxCount");
  var items = [];
  var idx = 0;
  var lastFocus = null;

  function activeItems() {
    var panel = document.querySelector(".tab-panel.is-active") || document;
    return Array.prototype.slice.call(panel.querySelectorAll(".gallery-item"));
  }

  function show(i) {
    items = activeItems();
    if (!items.length) return;
    idx = (i + items.length) % items.length;
    var it = items[idx];
    var pic = it.querySelector("img");
    img.src = pic.currentSrc || pic.src;
    img.alt = pic.alt || "";
    var label = it.querySelector("figcaption span");
    cap.textContent = label ? label.textContent : "";
    count.textContent = (idx + 1) + " / " + items.length;
  }

  function open(i) {
    lastFocus = document.activeElement;
    show(i);
    box.classList.add("is-open");
    box.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
    document.getElementById("lightboxClose").focus();
  }

  function close() {
    box.classList.remove("is-open");
    box.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
    img.src = "";
    if (lastFocus) lastFocus.focus();
  }

  document.addEventListener("click", function (e) {
    var it = e.target.closest(".gallery-item");
    if (it) open(activeItems().indexOf(it));
  });
  document.addEventListener("keydown", function (e) {
    var it = e.target.closest && e.target.closest(".gallery-item");
    if (it && (e.key === "Enter" || e.key === " ")) {
      e.preventDefault();
      open(activeItems().indexOf(it));
    }
  });

  document.getElementById("lightboxClose").addEventListener("click", close);
  document.getElementById("lightboxPrev").addEventListener("click", function () { show(idx - 1); });
  document.getElementById("lightboxNext").addEventListener("click", function () { show(idx + 1); });
  box.addEventListener("click", function (e) { if (e.target === box) close(); });

  document.addEventListener("keydown", function (e) {
    if (!box.classList.contains("is-open")) return;
    if (e.key === "Escape") close();
    if (e.key === "ArrowLeft") show(idx - 1);
    if (e.key === "ArrowRight") show(idx + 1);
  });
})();
