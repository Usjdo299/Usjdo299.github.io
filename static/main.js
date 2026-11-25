(function () {
  "use strict";

  var ICONS = {
    code: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 16"/></svg>',
    cpu: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="14" x2="23" y2="14"/><line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="14" x2="4" y2="14"/></svg>',
    globe: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>',
    car: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 11l1.7-4.2A2 2 0 0 1 8.6 5.5h6.8a2 2 0 0 1 1.9 1.3L19 11"/><path d="M3 11h18a1 1 0 0 1 1 1v4h-2"/><path d="M3 12v4h2"/><circle cx="7.5" cy="16.5" r="1.8"/><circle cx="16.5" cy="16.5" r="1.8"/><path d="M9.3 16.5h5.4"/></svg>',
    pin: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>',
    star: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>',
    book: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>',
    mail: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>',
    link: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>',
    github: '<svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8Z"/></svg>'
  };

  function icon(name) { return ICONS[name] || ICONS.link; }

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }

  function setText(id, value) {
    var el = document.getElementById(id);
    if (el) el.textContent = value == null ? "" : value;
  }

  var firstRender = true;

  function render(c) {
    if (!c) return;
    document.documentElement.style.setProperty("--accent", c.accent || "#9a7434");
    document.title = c.siteTitle || document.title;

    var mark = document.getElementById("brandMark");
    if (mark) mark.innerHTML = esc(c.firstName) + " <span>" + esc(c.lastName) + "</span>";

    setText("heroKicker", c.kicker);
    var name = document.getElementById("heroName");
    if (name) name.innerHTML = esc(c.firstName) + " <em>" + esc(c.lastName) + "</em>";
    setText("heroArabic", c.arabicName);
    setText("heroBio", c.bio);

    var cta = document.getElementById("heroCta");
    if (cta) cta.innerHTML = icon("mail") + "<span>Get in touch</span>";

    setText("aboutTitle", c.aboutTitle);
    setText("aboutP1", c.aboutP1);
    setText("aboutP2", c.aboutP2);
    setText("focusTitle", c.focusTitle);
    setText("contactTitle", c.contactTitle);
    setText("contactText", c.contactText);
    setText("footerAr", c.footerAr);
    setText("footerText", c.footerText);

    var facts = document.getElementById("factsBox");
    if (facts) {
      facts.innerHTML =
        factRow("pin", "Based in", c.factLocation) +
        factRow("code", "Craft", c.factCraft) +
        factRow("cpu", "Currently learning", c.factLearning);
    }

    var grid = document.getElementById("cardsGrid");
    if (grid) {
      grid.innerHTML = "";
      (c.cards || []).forEach(function (card) {
        var el = document.createElement("div");
        el.className = "card";
        el.innerHTML = '<div class="ico">' + icon(card.icon) + "</div><h3></h3><p></p>";
        el.querySelector("h3").textContent = card.title || "";
        el.querySelector("p").textContent = card.text || "";
        grid.appendChild(el);
      });
    }

    var row = document.getElementById("linksRow");
    if (row) {
      row.innerHTML = "";
      (c.links || []).forEach(function (l) {
        if (!l || !l.url) return;
        var a = document.createElement("a");
        a.className = "btn " + (l.style === "ghost" ? "btn-ghost" : "btn-solid");
        a.href = l.url;
        a.target = "_blank";
        a.rel = "noopener";
        a.innerHTML = icon(l.icon) + "<span></span>";
        a.querySelector("span").textContent = l.label || l.url;
        row.appendChild(a);
      });
    }

    if (!firstRender) {
      // Preview re-render from the admin panel: keep everything visible.
      document.querySelectorAll("[data-reveal]").forEach(function (el) { el.classList.add("in"); });
    }
    firstRender = false;
  }

  function factRow(ic, k, v) {
    return '<div class="fact"><div class="ico">' + icon(ic) + '</div><div><div class="k">' +
      esc(k) + '</div><div class="v">' + esc(v) + "</div></div></div>";
  }

  render(window.SITE_CONTENT);

  // Live preview messages from the admin panel (same origin only)
  window.addEventListener("message", function (ev) {
    if (ev.origin !== location.origin) return;
    if (ev.data && ev.data.type === "ali-preview" && ev.data.content) render(ev.data.content);
  });

  // Sticky header border
  var header = document.getElementById("siteHeader");
  function onScroll() { if (header) header.classList.toggle("scrolled", window.scrollY > 8); }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // Scroll reveal
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { threshold: 0.12 });
    document.querySelectorAll("[data-reveal]").forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll("[data-reveal]").forEach(function (el) { el.classList.add("in"); });
  }
})();
