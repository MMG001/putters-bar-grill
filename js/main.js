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

// Flipboard "MENU COMING SOON" tiles
(function () {
  var board = document.getElementById("flipboard");
  if (!board) return;
  var text = board.closest(".coming-hero") ? "COMING SOON" : "MENU COMING SOON";
  text.split("").forEach(function (ch, i) {
    var tile = document.createElement("span");
    if (ch === " ") {
      tile.className = "tile tile--space";
      tile.innerHTML = "&nbsp;";
    } else {
      tile.className = "tile";
      tile.textContent = ch;
      // subtle staggered "settle" animation unless reduced motion
      if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
        tile.style.opacity = "0";
        tile.style.transform = "rotateX(90deg)";
        tile.style.transition = "opacity .35s ease, transform .35s ease";
        tile.style.transitionDelay = i * 45 + "ms";
        requestAnimationFrame(function () {
          requestAnimationFrame(function () {
            tile.style.opacity = "1";
            tile.style.transform = "none";
          });
        });
      }
    }
    board.appendChild(tile);
  });
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

// Contact form -> compose email (static site, no backend)
(function () {
  var form = document.getElementById("contactForm");
  if (!form) return;
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    // EDIT: change to the bar's real email address
    var to = "info@puttersbargrill.com";
    var name = document.getElementById("cfName").value.trim();
    var email = document.getElementById("cfEmail").value.trim();
    var type = document.getElementById("cfType").value;
    var msg = document.getElementById("cfMsg").value.trim();
    var subject = "[" + type + "] Website message from " + name;
    var body = msg + "\n\n— " + name + "\n" + email;
    window.location.href = "mailto:" + to +
      "?subject=" + encodeURIComponent(subject) +
      "&body=" + encodeURIComponent(body);
  });
})();
