/* TKC Talent — Durga Puja 2026 conversion + AI-mode attribution tracking */
(function () {
  "use strict";
  if (window.__tkcDurgaTracking) return;
  window.__tkcDurgaTracking = true;

  var AI_REFERRERS = [
    ["chatgpt.com", "ChatGPT"], ["chat.openai.com", "ChatGPT"], ["openai.com", "OpenAI"],
    ["perplexity.ai", "Perplexity"], ["gemini.google.com", "Gemini"], ["bard.google.com", "Gemini"],
    ["copilot.microsoft.com", "Copilot"], ["bing.com/chat", "Copilot"], ["claude.ai", "Claude"],
    ["you.com", "You.com"], ["poe.com", "Poe"], ["grok.com", "Grok"], ["x.ai", "Grok"],
    ["deepseek.com", "DeepSeek"], ["mistral.ai", "Mistral"], ["phind.com", "Phind"],
    ["andisearch.com", "Andi"], ["arc.net", "Arc Search"]
  ];

  function params() {
    try { return new URLSearchParams(window.location.search); } catch (e) { return new URLSearchParams(); }
  }

  function detectSource() {
    var qs = params();
    var ref = document.referrer || "";
    var utm = (qs.get("utm_source") || "").toLowerCase();
    var host = "";
    try { host = ref ? new URL(ref).hostname.replace(/^www\./, "") : ""; } catch (e) { host = ""; }
    var probe = (host + (ref.split(host)[1] || "")).toLowerCase();

    for (var i = 0; i < AI_REFERRERS.length; i++) {
      if (probe.indexOf(AI_REFERRERS[i][0]) !== -1) {
        return { mode: "ai", engine: AI_REFERRERS[i][1], referrer: host || ref };
      }
      if (utm && AI_REFERRERS[i][0].split(".")[0] === utm) {
        return { mode: "ai", engine: AI_REFERRERS[i][1], referrer: "utm:" + utm };
      }
    }
    if (/^(ai|llm|aio|ai_mode|ai-overview|chatbot)$/.test(utm) || qs.get("ai") === "1") {
      return { mode: "ai", engine: qs.get("utm_medium") || utm || "unknown", referrer: "utm:" + utm };
    }
    if (host.indexOf("google.") === 0 || host.indexOf(".google.") !== -1) {
      return { mode: "search", engine: "Google", referrer: host };
    }
    return { mode: host ? "referral" : "direct", engine: host || "direct", referrer: host };
  }

  var SOURCE = detectSource();
  var PAGE = document.body.getAttribute("data-tkc-page") || location.pathname;

  function track(name, extra) {
    var payload = {
      page_group: "durga_puja_2026",
      page_path: PAGE,
      traffic_mode: SOURCE.mode,
      ai_engine: SOURCE.engine,
      ai_referrer: SOURCE.referrer
    };
    for (var k in extra) if (Object.prototype.hasOwnProperty.call(extra, k)) payload[k] = extra[k];
    if (typeof window.gtag === "function") window.gtag("event", name, payload);
    (window.dataLayer = window.dataLayer || []).push(Object.assign({ event: name }, payload));
  }

  // Session-level attribution ping (fires once per page view)
  track(SOURCE.mode === "ai" ? "ai_mode_session" : "durga_page_view", {
    referrer_full: document.referrer || "(none)"
  });

  // CTA clicks: WhatsApp, call, enquiry links
  document.addEventListener(
    "click",
    function (event) {
      var link = event.target && event.target.closest ? event.target.closest("a[href]") : null;
      if (!link) return;
      var href = link.getAttribute("href") || "";
      var label = (link.textContent || "").replace(/\s+/g, " ").trim().slice(0, 80);
      var section =
        (link.closest("section") && link.closest("section").id) ||
        link.getAttribute("data-cta-section") ||
        "unknown";

      if (href.indexOf("wa.me") !== -1 || href.indexOf("api.whatsapp.com") !== -1) {
        track("whatsapp_click", { cta_label: label, cta_section: section, cta_type: "whatsapp" });
        track("generate_lead", { cta_type: "whatsapp", cta_section: section, value: 1, currency: "INR" });
      } else if (href.indexOf("tel:") === 0) {
        track("call_click", { cta_label: label, cta_section: section, cta_type: "call" });
        track("generate_lead", { cta_type: "call", cta_section: section, value: 1, currency: "INR" });
      } else if (href.indexOf("mailto:") === 0) {
        track("email_click", { cta_label: label, cta_section: section, cta_type: "email" });
      } else if (href.indexOf("/durga-puja-2026/") !== -1 && location.pathname.indexOf("/durga-puja-2026/") === -1) {
        track("durga_internal_link_click", { cta_label: label, link_url: href });
      }
    },
    true
  );

  // Section engagement — helps see which keyword cluster AI traffic reads
  if ("IntersectionObserver" in window) {
    var seen = {};
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          var id = entry.target.id;
          if (!entry.isIntersecting || !id || seen[id]) return;
          seen[id] = true;
          track("section_view", { section_id: id });
        });
      },
      { threshold: 0.4 }
    );
    document.querySelectorAll("section[id]").forEach(function (node) {
      observer.observe(node);
    });
  }

  // Scroll depth
  var depths = [25, 50, 75, 100];
  var fired = {};
  window.addEventListener(
    "scroll",
    function () {
      var doc = document.documentElement;
      var max = doc.scrollHeight - window.innerHeight;
      if (max <= 0) return;
      var pct = Math.round(((window.scrollY || doc.scrollTop) / max) * 100);
      depths.forEach(function (d) {
        if (pct >= d && !fired[d]) {
          fired[d] = true;
          track("scroll_depth", { percent_scrolled: d });
        }
      });
    },
    { passive: true }
  );
})();
