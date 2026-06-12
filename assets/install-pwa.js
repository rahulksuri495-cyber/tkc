(function () {
  if (window.__tkcInstallInit) return;
  window.__tkcInstallInit = true;

  var STORAGE_KEY = 'tkc-install-dismissed-v1';
  var deferredPrompt = null;

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
      '.tkc-install-btn{position:fixed;right:16px;bottom:16px;z-index:9999;',
      'display:inline-flex;align-items:center;gap:8px;padding:12px 18px;',
      'border-radius:999px;border:1px solid rgba(255,255,255,.15);',
      'background:linear-gradient(135deg,#c9a14a,#e8c87b);color:#0a0a0a;',
      'font-family:"Space Grotesk",ui-sans-serif,system-ui,sans-serif;',
      'font-weight:700;font-size:14px;letter-spacing:.01em;cursor:pointer;',
      'box-shadow:0 10px 30px rgba(0,0,0,.35);transition:transform .15s ease,opacity .2s ease;',
      'opacity:0;transform:translateY(8px);pointer-events:none}',
      '.tkc-install-btn.is-visible{opacity:1;transform:none;pointer-events:auto}',
      '.tkc-install-btn:hover{transform:translateY(-1px) scale(1.02)}',
      '.tkc-install-btn svg{width:18px;height:18px}',
      '.tkc-install-close{margin-left:4px;background:transparent;border:0;color:#0a0a0a;',
      'font-size:18px;line-height:1;cursor:pointer;padding:0 2px;opacity:.7}',
      '.tkc-install-close:hover{opacity:1}',
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
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'tkc-install-btn';
    btn.setAttribute('aria-label', 'Install TKC Talent app');
    btn.innerHTML =
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12"/><path d="m7 10 5 5 5-5"/><path d="M5 21h14"/></svg>' +
      '<span>Install App</span>' +
      '<span class="tkc-install-close" aria-label="Dismiss">×</span>';
    document.body.appendChild(btn);

    btn.addEventListener('click', function (e) {
      if (e.target && e.target.classList && e.target.classList.contains('tkc-install-close')) {
        e.stopPropagation();
        try { localStorage.setItem(STORAGE_KEY, String(Date.now())); } catch (_) {}
        btn.remove();
        return;
      }
      if (!deferredPrompt) return;
      deferredPrompt.prompt();
      deferredPrompt.userChoice.then(function () {
        deferredPrompt = null;
        btn.remove();
      });
    });
    return btn;
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
    if (isStandalone() || wasDismissedRecently()) return;
    injectStyles();

    window.addEventListener('beforeinstallprompt', function (e) {
      e.preventDefault();
      deferredPrompt = e;
      var btn = createButton();
      requestAnimationFrame(function () { btn.classList.add('is-visible'); });
    });

    window.addEventListener('appinstalled', function () {
      deferredPrompt = null;
      var b = document.querySelector('.tkc-install-btn');
      if (b) b.remove();
    });

    if (isIOS()) {
      setTimeout(showIOSHint, 2500);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();