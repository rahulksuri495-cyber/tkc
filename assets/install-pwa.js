(function () {
  if (window.__tkcInstallInit) return;
  window.__tkcInstallInit = true;

  var STORAGE_KEY = 'tkc-install-dismissed-v2';
  var SESSION_KEY = 'tkc-install-session-id';
  var deferredPrompt = null;
  var bannerImpressionSent = false;
  var pillImpressionSent = false;

  // --- Session id (correlates all PWA events for a single user journey) ---
  function getSessionId() {
    try {
      var id = localStorage.getItem(SESSION_KEY);
      if (id) return id;
      var rand = (typeof crypto !== 'undefined' && crypto.getRandomValues)
        ? Array.from(crypto.getRandomValues(new Uint8Array(8))).map(function (b) {
            return b.toString(16).padStart(2, '0');
          }).join('')
        : Math.random().toString(16).slice(2) + Math.random().toString(16).slice(2);
      id = 'pwa_' + Date.now().toString(36) + '_' + rand;
      localStorage.setItem(SESSION_KEY, id);
      return id;
    } catch (_) {
      return 'pwa_ephemeral_' + Date.now().toString(36);
    }
  }

  // --- Analytics (GA4 + dataLayer, safe if absent) ---
  function track(eventName, params) {
    try {
      var payload = Object.assign({
        event_category: 'pwa_install',
        install_session_id: getSessionId(),
        page_path: location.pathname + location.search,
        page_location: location.href,
        prompt_available: !!deferredPrompt,
        platform: isIOS() ? 'ios' : (isAndroid() ? 'android' : 'desktop')
      }, params || {});
      if (typeof window.gtag === 'function') {
        window.gtag('event', eventName, payload);
      }
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push(Object.assign({ event: eventName }, payload));
    } catch (_) {}
  }

  function isAndroid() {
    return /android/i.test(window.navigator.userAgent);
  }

  // --- Service worker registration (guarded for Lovable preview) ---
  (function registerSW() {
    if (!('serviceWorker' in navigator)) return;
    try {
      var host = location.hostname;
      var search = location.search || '';
      var inIframe = window.top !== window.self;
      var isPreviewHost =
        host.startsWith('id-preview--') ||
        host.startsWith('preview--') ||
        host === 'lovableproject.com' || host.endsWith('.lovableproject.com') ||
        host === 'lovableproject-dev.com' || host.endsWith('.lovableproject-dev.com') ||
        host === 'beta.lovable.dev' || host.endsWith('.beta.lovable.dev');
      var killSwitch = search.indexOf('sw=off') !== -1;

      if (inIframe || isPreviewHost || killSwitch) {
        navigator.serviceWorker.getRegistrations().then(function (regs) {
          regs.forEach(function (r) {
            if (r.active && r.active.scriptURL && r.active.scriptURL.indexOf('/sw.js') !== -1) {
              r.unregister();
            }
          });
        }).catch(function () {});
        return;
      }

      window.addEventListener('load', function () {
        navigator.serviceWorker.register('/sw.js', { scope: '/' }).catch(function () {});
      });
    } catch (_) {}
  })();

  function isStandalone() {
    return (
      window.matchMedia('(display-mode: standalone)').matches ||
      window.navigator.standalone === true
    );
  }

  function isIOS() {
    return /iphone|ipad|ipod/i.test(window.navigator.userAgent) && !window.MSStream;
  }

  function injectStyles() {
    if (document.getElementById('tkc-install-styles')) return;
    var s = document.createElement('style');
    s.id = 'tkc-install-styles';
    s.textContent = [
      '.tkc-install-banner{position:fixed;left:0;right:0;top:0;z-index:10000;',
      'display:flex;align-items:center;justify-content:center;gap:14px;',
      'padding:10px 56px 10px 16px;',
      'background:linear-gradient(90deg,#0a0a0a 0%,#1a1a1a 50%,#0a0a0a 100%);',
      'border-bottom:1px solid rgba(201,161,74,.35);',
      'font-family:"Space Grotesk",ui-sans-serif,system-ui,sans-serif;',
      'color:#fff;box-shadow:0 4px 20px rgba(0,0,0,.4);',
      'transform:translateY(-100%);transition:transform .35s ease}',
      '.tkc-install-banner.is-visible{transform:none}',
      '.tkc-install-banner .tkc-ib-text{font-size:14px;font-weight:500;letter-spacing:.01em;',
      'display:flex;align-items:center;gap:10px;flex-wrap:wrap;justify-content:center;text-align:center}',
      '.tkc-install-banner .tkc-ib-text strong{color:#e8c87b;font-weight:700}',
      '.tkc-install-banner .tkc-ib-cta{display:inline-flex;align-items:center;gap:6px;',
      'padding:8px 18px;border-radius:999px;border:0;',
      'background:linear-gradient(135deg,#c9a14a,#e8c87b);color:#0a0a0a;',
      'font-family:inherit;font-weight:700;font-size:13px;letter-spacing:.02em;',
      'cursor:pointer;text-transform:uppercase;box-shadow:0 4px 14px rgba(201,161,74,.4);',
      'transition:transform .15s ease}',
      '.tkc-install-banner .tkc-ib-cta:hover{transform:scale(1.04)}',
      '.tkc-install-banner .tkc-ib-cta svg{width:14px;height:14px}',
      '.tkc-install-banner .tkc-ib-close{position:absolute;right:10px;top:50%;',
      'transform:translateY(-50%);background:transparent;border:0;color:#fff;',
      'font-size:22px;line-height:1;cursor:pointer;opacity:.6;padding:4px 8px}',
      '.tkc-install-banner .tkc-ib-close:hover{opacity:1}',
      '@media (max-width:640px){.tkc-install-banner{padding:10px 44px 10px 12px;gap:8px}',
      '.tkc-install-banner .tkc-ib-text{font-size:12px;gap:6px}',
      '.tkc-install-banner .tkc-ib-cta{padding:7px 14px;font-size:12px}}',
      'body.tkc-has-install-banner{padding-top:56px}',
      '@media (max-width:640px){body.tkc-has-install-banner{padding-top:76px}}',
      /* Persistent floating pill (always visible until installed) */
      '.tkc-install-pill{position:fixed;right:18px;bottom:18px;z-index:9998;',
      'display:inline-flex;align-items:center;gap:8px;padding:11px 18px;',
      'border-radius:999px;border:1px solid rgba(255,255,255,.12);',
      'background:linear-gradient(135deg,#c9a14a,#e8c87b);color:#0a0a0a;',
      'font-family:"Space Grotesk",ui-sans-serif,system-ui,sans-serif;',
      'font-weight:700;font-size:13px;letter-spacing:.03em;text-transform:uppercase;',
      'cursor:pointer;box-shadow:0 8px 24px rgba(0,0,0,.35),0 2px 8px rgba(201,161,74,.35);',
      'transition:transform .15s ease,box-shadow .2s ease;opacity:0;transform:translateY(12px)}',
      '.tkc-install-pill.is-visible{opacity:1;transform:none}',
      '.tkc-install-pill:hover{transform:translateY(-2px) scale(1.03);box-shadow:0 12px 30px rgba(201,161,74,.5)}',
      '.tkc-install-pill svg{width:16px;height:16px}',
      '@media (max-width:640px){.tkc-install-pill{right:12px;bottom:12px;padding:10px 14px;font-size:12px}}',
      '.tkc-install-pill-close{position:fixed;right:8px;bottom:44px;z-index:9999;',
      'width:22px;height:22px;border-radius:999px;border:1px solid rgba(0,0,0,.15);',
      'background:#0a0a0a;color:#e8c87b;font-family:"Space Grotesk",system-ui,sans-serif;',
      'font-size:14px;line-height:1;cursor:pointer;padding:0;',
      'display:none;align-items:center;justify-content:center;',
      'box-shadow:0 4px 12px rgba(0,0,0,.35)}',
      '.tkc-install-pill-close.is-visible{display:inline-flex}',
      '.tkc-install-pill-close:hover{background:#1a1a1a}',
      '@media (max-width:640px){.tkc-install-pill-close{right:4px;bottom:38px}}',
      '.tkc-ios-hint{position:fixed;left:12px;right:12px;bottom:12px;z-index:9999;',
      'background:#0a0a0a;color:#fff;border:1px solid rgba(201,161,74,.4);',
      'border-radius:14px;padding:14px 16px;font-family:Inter,system-ui,sans-serif;',
      'font-size:13px;line-height:1.45;box-shadow:0 10px 30px rgba(0,0,0,.5);',
      'display:flex;gap:12px;align-items:flex-start}',
      '.tkc-ios-hint strong{color:#e8c87b;display:block;margin-bottom:2px;font-family:"Space Grotesk",sans-serif}',
      '.tkc-ios-hint button{margin-left:auto;background:transparent;border:0;color:#fff;',
      'font-size:20px;cursor:pointer;opacity:.7}'
    ].join('');
    document.head.appendChild(s);
  }

  function createButton() {
    if (document.querySelector('.tkc-install-banner')) return null;
    var bar = document.createElement('div');
    bar.className = 'tkc-install-banner';
    bar.setAttribute('role', 'region');
    bar.setAttribute('aria-label', 'Install TKC Talent app');
    bar.innerHTML =
      '<div class="tkc-ib-text">' +
        '<span>📱 Get the <strong>TKC Talent</strong> app — faster booking, offline access</span>' +
      '</div>' +
      '<button type="button" class="tkc-ib-cta" aria-label="Install TKC Talent app">' +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12"/><path d="m7 10 5 5 5-5"/><path d="M5 21h14"/></svg>' +
        '<span>Install App</span>' +
      '</button>' +
      '<button type="button" class="tkc-ib-close" aria-label="Dismiss">×</button>';
    document.body.appendChild(bar);
    document.body.classList.add('tkc-has-install-banner');

    bar.querySelector('.tkc-ib-close').addEventListener('click', function () {
      try { localStorage.setItem(STORAGE_KEY, String(Date.now())); } catch (_) {}
      bar.remove();
      document.body.classList.remove('tkc-has-install-banner');
      track('pwa_banner_dismiss', { source: 'banner' });
    });

    bar.querySelector('.tkc-ib-cta').addEventListener('click', function () {
      track('pwa_install_click', { source: 'banner' });
      handleInstallClick('banner', function () {
        bar.remove();
        document.body.classList.remove('tkc-has-install-banner');
      });
    });
    return bar;
  }

  function handleInstallClick(source, onAccepted) {
      if (deferredPrompt) {
        deferredPrompt.prompt();
        deferredPrompt.userChoice.then(function (choice) {
          var outcome = (choice && choice.outcome) ? choice.outcome : 'unknown';
          track('pwa_install_prompt_result', { source: source, outcome: outcome });
          deferredPrompt = null;
          if (typeof onAccepted === 'function') onAccepted();
        });
      } else if (isIOS()) {
        track('pwa_install_fallback', { source: source, fallback: 'ios_hint' });
        showIOSHint();
      } else {
        track('pwa_install_fallback', { source: source, fallback: 'manual_hint' });
        showManualHint();
      }
  }

  function showManualHint() {
    if (document.querySelector('.tkc-ios-hint')) return;
    var hint = document.createElement('div');
    hint.className = 'tkc-ios-hint';
    hint.innerHTML =
      '<div><strong>Install TKC Talent</strong>Open your browser menu (⋮) and tap “Install app” or “Add to Home screen”.</div>' +
      '<button type="button" aria-label="Dismiss">×</button>';
    document.body.appendChild(hint);
    hint.querySelector('button').addEventListener('click', function () { hint.remove(); });
  }

  function showIOSHint() {
    if (document.querySelector('.tkc-ios-hint')) return;
    var hint = document.createElement('div');
    hint.className = 'tkc-ios-hint';
    hint.innerHTML =
      '<div><strong>Install TKC Talent</strong>Tap the Share icon in Safari, then choose “Add to Home Screen”.</div>' +
      '<button type="button" aria-label="Dismiss">×</button>';
    document.body.appendChild(hint);
    hint.querySelector('button').addEventListener('click', function () {
      try { localStorage.setItem(STORAGE_KEY, String(Date.now())); } catch (_) {}
      hint.remove();
    });
  }

  function wasDismissedRecently() {
    try {
      var t = parseInt(localStorage.getItem(STORAGE_KEY) || '0', 10);
      // Re-show after 7 days
      return t && Date.now() - t < 7 * 24 * 60 * 60 * 1000;
    } catch (_) { return false; }
  }

  function init() {
    if (isStandalone()) return;
    injectStyles();

    window.addEventListener('beforeinstallprompt', function (e) {
      e.preventDefault();
      deferredPrompt = e;
      track('pwa_prompt_available');
    });

    window.addEventListener('appinstalled', function () {
      track('pwa_app_installed');
      deferredPrompt = null;
      var b = document.querySelector('.tkc-install-banner');
      if (b) b.remove();
      var p = document.querySelector('.tkc-install-pill');
      if (p) p.remove();
      document.body.classList.remove('tkc-has-install-banner');
    });

    // Persistent floating pill — always available even after banner dismiss.
    createPill();

    // Prominent top banner on fresh visits (respects 7-day dismiss).
    if (wasDismissedRecently()) return;
    setTimeout(function () {
      var bar = createButton();
      if (bar) {
        requestAnimationFrame(function () { bar.classList.add('is-visible'); });
        if (!bannerImpressionSent) {
          bannerImpressionSent = true;
          track('pwa_banner_impression', { source: 'banner' });
        }
      }
    }, 600);
  }

  function createPill() {
    if (document.querySelector('.tkc-install-pill')) return null;
    var pill = document.createElement('button');
    pill.type = 'button';
    pill.className = 'tkc-install-pill';
    pill.setAttribute('aria-label', 'Install TKC Talent app');
    pill.innerHTML =
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12"/><path d="m7 10 5 5 5-5"/><path d="M5 21h14"/></svg>' +
      '<span>Install App</span>';
    document.body.appendChild(pill);

    var closeBtn = document.createElement('button');
    closeBtn.type = 'button';
    closeBtn.className = 'tkc-install-pill-close';
    closeBtn.setAttribute('aria-label', 'Dismiss install app');
    closeBtn.textContent = '×';
    document.body.appendChild(closeBtn);

    requestAnimationFrame(function () {
      pill.classList.add('is-visible');
      closeBtn.classList.add('is-visible');
    });

    closeBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      try { localStorage.setItem(STORAGE_KEY, String(Date.now())); } catch (_) {}
      pill.remove();
      closeBtn.remove();
      track('pwa_banner_dismiss', { source: 'pill' });
    });

    if (!pillImpressionSent) {
      pillImpressionSent = true;
      track('pwa_pill_impression', { source: 'pill' });
    }

    pill.addEventListener('click', function () {
      track('pwa_install_click', { source: 'pill' });
      handleInstallClick('pill', function () {
        pill.remove();
        closeBtn.remove();
      });
    });
    return pill;
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();