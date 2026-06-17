/* TKC Talent homepage content injector — AI hero + Legacy band
   Inserts two sections around the pricing block on the homepage with premium effects. */
(function(){
  if (location.pathname !== '/' && location.pathname !== '/index.html') return;
  var INSERTED = false;
  var STYLE_ID = 'tkc-blocks-style';

  function injectStyles(){
    if (document.getElementById(STYLE_ID)) return;
    var s = document.createElement('style');
    s.id = STYLE_ID;
    s.textContent = [
      /* Shared */
      '.tkc-block{position:relative;padding:72px 22px;font-family:Inter,system-ui,sans-serif}',
      '.tkc-block .tkc-wrap{max-width:1180px;margin:0 auto;position:relative;z-index:2}',
      '.tkc-block .tkc-eyebrow{display:inline-flex;align-items:center;gap:10px;font-size:11px;letter-spacing:.22em;text-transform:uppercase;font-weight:700;margin-bottom:18px;padding:7px 14px;border-radius:999px}',
      '.tkc-block h2{font-family:"Space Grotesk",Inter,sans-serif;font-weight:700;font-size:clamp(26px,4.2vw,44px);line-height:1.1;letter-spacing:-.02em;margin:0 0 18px}',
      '.tkc-block p{font-size:16px;line-height:1.65;margin:0 0 14px;max-width:780px}',
      '.tkc-block .tkc-cta-row{display:flex;flex-wrap:wrap;gap:12px;margin-top:24px}',
      '.tkc-block .tkc-cta{position:relative;display:inline-flex;align-items:center;gap:10px;padding:14px 24px;border-radius:12px;font-weight:600;font-size:15px;text-decoration:none;transition:transform .2s ease,box-shadow .2s ease;will-change:transform}',
      /* Sticky label tabs */
      '.tkc-sticky-label{position:sticky;top:0;display:inline-flex;align-items:center;gap:8px;padding:8px 18px;font-size:11px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;border-radius:0 0 14px 0;z-index:100;backdrop-filter:blur(8px);margin-bottom:-34px}',
      '.tkc-ai .tkc-sticky-label{background:rgba(99,102,241,.92);color:#fff;border-right:1px solid rgba(255,255,255,.2);border-bottom:1px solid rgba(255,255,255,.2)}',
      '.tkc-legacy .tkc-sticky-label{background:rgba(201,168,76,.95);color:#1a1407;border-right:1px solid rgba(26,20,7,.15);border-bottom:1px solid rgba(26,20,7,.15)}',
      /* AI hero — clean dark with vivid blue accent */
      '.tkc-ai{color:#e8efff;background:#0b1020;background:linear-gradient(180deg,#0b1020 0%,#0e1530 100%)}',
      '.tkc-ai:before{content:"";position:absolute;inset:0;background:radial-gradient(900px 500px at 85% 10%,rgba(99,102,241,.28),transparent 60%),radial-gradient(700px 400px at 10% 100%,rgba(56,189,248,.18),transparent 60%);z-index:0}',
      '.tkc-ai .tkc-eyebrow{background:rgba(99,102,241,.15);color:#a5b4fc;border:1px solid rgba(99,102,241,.35)}',
      '.tkc-ai h2{color:#fff}',
      '.tkc-ai h2 .accent{background:linear-gradient(90deg,#818cf8,#38bdf8);-webkit-background-clip:text;background-clip:text;color:transparent}',
      '.tkc-ai p{color:#c7d0e6}',
      '.tkc-ai .tkc-cta.primary{background:linear-gradient(135deg,#6366f1,#3b82f6);color:#fff;box-shadow:0 14px 40px -12px rgba(99,102,241,.7)}',
      '.tkc-ai .tkc-cta.primary:hover{transform:translateY(-2px);box-shadow:0 20px 55px -12px rgba(99,102,241,.85)}',
      '.tkc-ai .tkc-cta.ghost{background:rgba(255,255,255,.06);color:#e8efff;border:1px solid rgba(255,255,255,.18)}',
      '.tkc-ai .tkc-cta.ghost:hover{background:rgba(255,255,255,.12)}',
      '.tkc-ai .tkc-grid{display:grid;grid-template-columns:1.35fr 1fr;gap:44px;align-items:center}',
      '@media (max-width:900px){.tkc-ai .tkc-grid{grid-template-columns:1fr;gap:28px}}',
      '.tkc-ai .tkc-stats{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}',
      '.tkc-ai .tkc-stat{padding:18px;border:1px solid rgba(255,255,255,.14);border-radius:14px;background:linear-gradient(180deg,rgba(255,255,255,.06),rgba(255,255,255,.02));backdrop-filter:blur(6px);transition:transform .3s ease,border-color .3s ease}',
      '.tkc-ai .tkc-stat:hover{transform:translateY(-3px);border-color:rgba(129,140,248,.6)}',
      '.tkc-ai .tkc-stat .num{font-family:"Space Grotesk",sans-serif;font-size:30px;font-weight:700;color:#fff;letter-spacing:-.02em;line-height:1}',
      '.tkc-ai .tkc-stat .lbl{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#a5b4fc;margin-top:8px;font-weight:600}',
      /* Legacy band — light cream for clear contrast against the dark page */
      '.tkc-legacy{color:#1a1407;background:linear-gradient(180deg,#fdfaf2 0%,#f5ecd6 100%);border-top:3px solid #c9a84c;border-bottom:3px solid #c9a84c}',
      '.tkc-legacy:before{content:"";position:absolute;inset:0;background:radial-gradient(600px 300px at 90% 0%,rgba(201,168,76,.25),transparent 60%);z-index:0}',
      '.tkc-legacy .tkc-eyebrow{background:#1a1407;color:#e8c97a;border:1px solid #1a1407}',
      '.tkc-legacy h2{color:#1a1407}',
      '.tkc-legacy h2 .accent{background:linear-gradient(90deg,#8a6a26,#c9a84c);-webkit-background-clip:text;background-clip:text;color:transparent}',
      '.tkc-legacy p{color:#3d3424}',
      '.tkc-legacy .tkc-grid{display:grid;grid-template-columns:1.5fr 1fr;gap:44px;align-items:center}',
      '@media (max-width:900px){.tkc-legacy .tkc-grid{grid-template-columns:1fr}}',
      '.tkc-legacy .tkc-pillars{display:grid;grid-template-columns:1fr;gap:12px}',
      '.tkc-legacy .tkc-pillar{display:flex;align-items:baseline;gap:16px;padding:18px 22px;border-left:3px solid #c9a84c;background:#fff;border-radius:0 12px 12px 0;box-shadow:0 4px 18px -10px rgba(26,20,7,.25);transition:transform .15s ease,box-shadow .15s ease}',
      '.tkc-legacy .tkc-pillar:hover{transform:translateX(6px);box-shadow:0 10px 30px -12px rgba(26,20,7,.35)}',
      '.tkc-legacy .tkc-pillar .k{font-family:"Space Grotesk",sans-serif;font-size:22px;font-weight:700;color:#1a1407;min-width:100px}',
      '.tkc-legacy .tkc-pillar .v{font-size:14px;color:#5a4d34;letter-spacing:.02em;line-height:1.5}',
      /* Reveal anim — snappier, earlier trigger */
      '.tkc-reveal{opacity:0;transform:translateY(12px);transition:opacity .5s ease-out,transform .5s ease-out}',
      '.tkc-reveal.in{opacity:1;transform:none}',
      '.tkc-legacy .tkc-reveal{transition-duration:.35s;transform:translateY(8px)}',
      '.tkc-reveal[data-delay="1"]{transition-delay:.06s}.tkc-reveal[data-delay="2"]{transition-delay:.12s}.tkc-reveal[data-delay="3"]{transition-delay:.18s}.tkc-reveal[data-delay="4"]{transition-delay:.24s}',
      '@media (prefers-reduced-motion:reduce){.tkc-reveal{opacity:1;transform:none;transition:none}}'
    ].join('');
    document.head.appendChild(s);
  }

  function buildAI(){
    var el = document.createElement('section');
    el.className = 'tkc-block tkc-ai';
    el.id = 'tkc-ai-platform';
    el.setAttribute('aria-label','AI-first celebrity booking platform');
    el.innerHTML = ''+
      '<div class="tkc-glow g1"></div><div class="tkc-glow g2"></div>'+
      '<span class="tkc-sticky-label">AI-Powered Booking</span>'+
      '<div class="tkc-wrap"><div class="tkc-grid">'+
        '<div>'+
          '<span class="tkc-eyebrow tkc-reveal">India\u2019s First AI-First Booking Platform</span>'+
          '<h2 class="tkc-reveal" data-delay="1">Brief us in plain words. <span class="accent">Get bookable shortlists in seconds.</span></h2>'+
          '<p class="tkc-reveal" data-delay="2">TKC Talent is India\u2019s first celebrity booking platform built for an AI-first world. Our vertical event-and-entertainment LLM turns vague briefs into precise, bookable options\u2014matching your date, city, budget, and campaign goals with the right Bollywood stars, singers, and creators in seconds.</p>'+
          '<p class="tkc-reveal" data-delay="3">Instead of guessing market rates or chasing multiple coordinators, planners see transparent, category-based fee bands and availability signals, then work directly with The Kabir Company\u2019s on-ground team to lock contracts, logistics, and performance flow. Human relationships plus AI intelligence mean faster shortlists, sharper negotiations, and reliably delivered celebrity experiences for weddings, brands, and corporate events across India.</p>'+
          '<div class="tkc-cta-row tkc-reveal" data-delay="4">'+
            '<a class="tkc-cta primary tkc-magnetic" href="https://forms.gle/HbfLkzyVTMDywsFM8?utm_source=tkctalent&utm_medium=cta&utm_campaign=ai_hero&utm_content=homepage" target="_blank" rel="noopener">Start an AI-assisted brief \u2192</a>'+
            '<a class="tkc-cta ghost" href="https://wa.me/919599599699?text=Hi%20TKC%20Talent%2C%20I%27d%20like%20a%20celebrity%20shortlist." target="_blank" rel="noopener">Chat on WhatsApp</a>'+
          '</div>'+
        '</div>'+
        '<div class="tkc-stats">'+
          '<div class="tkc-stat tkc-reveal" data-delay="1"><div class="num" data-count="500" data-suffix="+">0</div><div class="lbl">Artists in roster</div></div>'+
          '<div class="tkc-stat tkc-reveal" data-delay="2"><div class="num" data-count="60" data-suffix="s">0</div><div class="lbl">From brief to shortlist</div></div>'+
          '<div class="tkc-stat tkc-reveal" data-delay="3"><div class="num" data-count="12000" data-suffix="+">0</div><div class="lbl">Clients served</div></div>'+
          '<div class="tkc-stat tkc-reveal" data-delay="4"><div class="num" data-count="20" data-suffix="+">0</div><div class="lbl">Years of operations DNA</div></div>'+
        '</div>'+
      '</div></div>';
    return el;
  }

  function buildLegacy(){
    var el = document.createElement('section');
    el.className = 'tkc-block tkc-legacy';
    el.id = 'tkc-legacy';
    el.setAttribute('aria-label','TKC and IITEO legacy');
    el.innerHTML = ''+
      '<span class="tkc-sticky-label">TKC Legacy</span>'+
      '<div class="tkc-wrap"><div class="tk,grid">'+
        '<div>'+
          '<span class="tkc-eyebrow tkc-reveal">Two-Decade Legacy \u00B7 TKC \u00D7 IITEO</span>'+
          '<h2 class="tkc-reveal" data-delay="1">A <span class="accent">live-events operations DNA</span> behind every booking.</h2>'+
          '<p class="tkc-reveal" data-delay="2">TKC Talent is backed by The Kabir Company\u2019s two-decade legacy in India\u2019s exhibition and live events ecosystem, including experience shaped through IITEO-style trade fairs and large public shows. What began as meticulous planning for high-footfall exhibitions evolved into precision-led celebrity bookings, concerts, and premium brand experiences across India.</p>'+
          '<p class="tkc-reveal" data-delay="3">So when you explore artists on TKC Talent, you\u2019re not browsing a listing platform alone\u2014you\u2019re accessing the same event operations DNA that has powered concerts, corporate events, exhibitions, and wedding entertainment nationwide.</p>'+
        '</div>'+
        '<div class="tkc-pillars">'+
          '<div class="tkc-pillar tkc-reveal" data-delay="1"><div class="k">20+ Yrs</div><div class="v">Live events, exhibitions &amp; celebrity execution</div></div>'+
          '<div class="tkc-pillar tkc-reveal" data-delay="2"><div class="k">New Delhi</div><div class="v">HQ \u00B7 Pan-India delivery network</div></div>'+
          '<div class="tkc-pillar tkc-reveal" data-delay="3"><div class="k">Events + Talent</div><div class="v">Concerts, weddings, brand &amp; corporate</div></div>'+
        '</div>'+
      '</div></div>';
    return el;
  }

  function findPricingSection(){
    // Priority: explicit id=pricing, then any section containing 'Price Guide' / 'Charges' / 'Pricing' heading
    var el = document.getElementById('pricing');
    if (el) return el.closest('section') || el;
    var headings = document.querySelectorAll('h1,h2,h3');
    for (var i=0;i<headings.length;i++){
      var t = (headings[i].textContent||'').toLowerCase();
      if (/price guide|pricing|celebrity charges|fee guide|fee band/.test(t)){
        var s = headings[i].closest('section'); if (s) return s;
      }
    }
    return null;
  }

  function countUp(el){
    var target = parseInt(el.getAttribute('data-count')||'0',10);
    var suffix = el.getAttribute('data-suffix')||'';
    var dur = 1400, start = performance.now();
    function fmt(n){ return n>=1000 ? n.toLocaleString('en-IN') : String(n); }
    function tick(now){
      var p = Math.min(1,(now-start)/dur);
      var v = Math.floor(target * (1 - Math.pow(1-p, 3)));
      el.textContent = fmt(v) + suffix;
      if (p<1) requestAnimationFrame(tick); else el.textContent = fmt(target) + suffix;
    }
    requestAnimationFrame(tick);
  }

  function wireEffects(scope){
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if (e.isIntersecting){
          e.target.classList.add('in');
          if (e.target.matches('.tkc-stat')){
            var n = e.target.querySelector('[data-count]');
            if (n && !n.dataset.done){ n.dataset.done='1'; countUp(n); }
          }
          io.unobserve(e.target);
        }
      });
    }, {threshold:0.05, rootMargin:'0px 0px 60px 0px'});
    scope.querySelectorAll('.tkc-reveal').forEach(function(n){io.observe(n);});

    // Magnetic CTA
    scope.querySelectorAll('.tkc-magnetic').forEach(function(btn){
      btn.addEventListener('pointermove', function(e){
        var r = btn.getBoundingClientRect();
        var x = e.clientX - r.left - r.width/2;
        var y = e.clientY - r.top - r.height/2;
        btn.style.transform = 'translate('+(x*.18)+'px,'+(y*.25)+'px)';
      });
      btn.addEventListener('pointerleave', function(){ btn.style.transform = ''; });
    });
  }

  function insert(){
    if (INSERTED) return true;
    var pricing = findPricingSection();
    if (!pricing) return false;
    injectStyles();
    var legacy = buildLegacy();
    var ai = buildAI();
    // Block 1 (AI hero) — near top, before pricing
    pricing.parentNode.insertBefore(ai, pricing);
    // Block 2 (Legacy) — after pricing, before roster
    pricing.parentNode.insertBefore(legacy, pricing.nextSibling);
    wireEffects(ai); wireEffects(legacy);
    INSERTED = true;
    return true;
  }

  function start(){
    if (insert()) return;
    var tries = 0;
    var mo = new MutationObserver(function(){
      if (insert() || ++tries>60) mo.disconnect();
    });
    mo.observe(document.body, {childList:true, subtree:true});
    setTimeout(function(){ try{ mo.disconnect(); }catch(_){ } }, 15000);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
