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
      '.tkc-block{position:relative;overflow:hidden;color:#f5f1e8;background:#0a0a0a;padding:88px 24px;font-family:Inter,system-ui,sans-serif}',
      '.tkc-block .tkc-wrap{max-width:1180px;margin:0 auto;position:relative;z-index:2}',
      '.tkc-block .tkc-eyebrow{display:inline-flex;align-items:center;gap:10px;font-size:12px;letter-spacing:.22em;text-transform:uppercase;color:#c9a84c;font-weight:600;margin-bottom:18px}',
      '.tkc-block .tkc-eyebrow:before{content:"";width:28px;height:1px;background:linear-gradient(90deg,transparent,#c9a84c)}',
      '.tkc-block h2{font-family:"Space Grotesk",Inter,sans-serif;font-weight:700;font-size:clamp(28px,4vw,46px);line-height:1.08;letter-spacing:-.02em;margin:0 0 22px;color:#fff}',
      '.tkc-block h2 .accent{background:linear-gradient(90deg,#e8c97a,#c9a84c 55%,#8a6a26);-webkit-background-clip:text;background-clip:text;color:transparent}',
      '.tkc-block p{font-size:17px;line-height:1.65;color:#cfc9bf;margin:0 0 16px;max-width:780px}',
      '.tkc-block .tkc-cta-row{display:flex;flex-wrap:wrap;gap:14px;margin-top:28px}',
      '.tkc-block .tkc-cta{position:relative;display:inline-flex;align-items:center;gap:10px;padding:14px 26px;border-radius:999px;font-weight:600;font-size:15px;text-decoration:none;transition:transform .25s cubic-bezier(.2,.8,.2,1),box-shadow .25s;will-change:transform}',
      '.tkc-block .tkc-cta.primary{background:linear-gradient(135deg,#e8c97a,#c9a84c);color:#1a1407;box-shadow:0 10px 30px -10px rgba(201,168,76,.55)}',
      '.tkc-block .tkc-cta.primary:hover{box-shadow:0 18px 50px -12px rgba(201,168,76,.7)}',
      '.tkc-block .tkc-cta.ghost{background:rgba(255,255,255,.06);color:#f5f1e8;border:1px solid rgba(255,255,255,.14)}',
      '.tkc-block .tkc-cta.ghost:hover{background:rgba(255,255,255,.1)}',
      /* AI hero specifics */
      '.tkc-ai{background:radial-gradient(1200px 600px at 20% -10%,#1a1a2e 0%,#0a0a0a 55%) , #0a0a0a}',
      '.tkc-ai:before{content:"";position:absolute;inset:0;background-image:radial-gradient(rgba(201,168,76,.18) 1px,transparent 1px);background-size:32px 32px;mask-image:radial-gradient(ellipse at 30% 0%,#000 30%,transparent 70%);opacity:.6;z-index:1}',
      '.tkc-ai .tkc-glow{position:absolute;width:520px;height:520px;border-radius:50%;filter:blur(80px);opacity:.35;pointer-events:none;z-index:0}',
      '.tkc-ai .tkc-glow.g1{background:#3b3a8a;top:-160px;right:-120px}',
      '.tkc-ai .tkc-glow.g2{background:#c9a84c;bottom:-200px;left:-120px;opacity:.18}',
      '.tkc-ai .tkc-grid{display:grid;grid-template-columns:1.4fr 1fr;gap:48px;align-items:center}',
      '@media (max-width:900px){.tkc-ai .tkc-grid{grid-template-columns:1fr;gap:32px}}',
      '.tkc-ai .tkc-stats{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}',
      '.tkc-ai .tkc-stat{padding:18px 18px;border:1px solid rgba(255,255,255,.1);border-radius:14px;background:linear-gradient(180deg,rgba(255,255,255,.04),rgba(255,255,255,.01));transition:transform .35s cubic-bezier(.2,.8,.2,1),border-color .35s}',
      '.tkc-ai .tkc-stat:hover{transform:translateY(-4px);border-color:rgba(201,168,76,.45)}',
      '.tkc-ai .tkc-stat .num{font-family:"Space Grotesk",sans-serif;font-size:32px;font-weight:700;color:#fff;letter-spacing:-.02em}',
      '.tkc-ai .tkc-stat .lbl{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:#a89e8a;margin-top:6px}',
      /* Legacy band */
      '.tkc-legacy{background:linear-gradient(180deg,#0a0a0a 0%,#0f0d08 100%);border-top:1px solid rgba(201,168,76,.18);border-bottom:1px solid rgba(201,168,76,.18)}',
      '.tkc-legacy:before{content:"";position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,#c9a84c 50%,transparent);animation:tkcShine 6s ease-in-out infinite}',
      '@keyframes tkcShine{0%,100%{opacity:.3}50%{opacity:1}}',
      '.tkc-legacy .tkc-grid{display:grid;grid-template-columns:1.5fr 1fr;gap:48px;align-items:center}',
      '@media (max-width:900px){.tkc-legacy .tkc-grid{grid-template-columns:1fr}}',
      '.tkc-legacy .tkc-pillars{display:grid;grid-template-columns:1fr;gap:12px}',
      '.tkc-legacy .tkc-pillar{display:flex;align-items:baseline;gap:16px;padding:18px 22px;border-left:2px solid #c9a84c;background:linear-gradient(90deg,rgba(201,168,76,.06),transparent);border-radius:0 12px 12px 0;transition:transform .3s,background .3s}',
      '.tkc-legacy .tkc-pillar:hover{transform:translateX(6px);background:linear-gradient(90deg,rgba(201,168,76,.12),transparent)}',
      '.tkc-legacy .tkc-pillar .k{font-family:"Space Grotesk",sans-serif;font-size:26px;font-weight:700;color:#e8c97a;min-width:90px}',
      '.tkc-legacy .tkc-pillar .v{font-size:14px;color:#cfc9bf;letter-spacing:.04em}',
      /* Reveal anim */
      '.tkc-reveal{opacity:0;transform:translateY(24px);transition:opacity .9s cubic-bezier(.2,.8,.2,1),transform .9s cubic-bezier(.2,.8,.2,1)}',
      '.tkc-reveal.in{opacity:1;transform:none}',
      '.tkc-reveal[data-delay="1"]{transition-delay:.08s}.tkc-reveal[data-delay="2"]{transition-delay:.16s}.tkc-reveal[data-delay="3"]{transition-delay:.24s}.tkc-reveal[data-delay="4"]{transition-delay:.32s}',
      '@media (prefers-reduced-motion:reduce){.tkc-reveal{opacity:1;transform:none;transition:none}.tkc-legacy:before{animation:none}}'
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
      '<div class="tkc-wrap"><div class="tkc-grid">'+
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
    }, {threshold:0.18});
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
