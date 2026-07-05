/* TKC — remove 3-Steps images + inject Corporate Clients scroller (homepage only) */
(function(){
  if (location.pathname !== '/' && location.pathname !== '/index.html') return;

  var LOGOS = [
    ['Mercedes-Benz','mercedes-benz.jpg'],['BMW','bmw.jpg'],['Jaguar','jaguar.jpg'],
    ['Range Rover','range-rover.jpg'],['Harley-Davidson','harley-davidson.jpg'],
    ['Royal Enfield','royal-enfield.jpg'],['Hyundai','hyundai.jpg'],['Honda','honda.jpg'],
    ['Toyota','toyota.jpg'],['Skoda','skoda.jpg'],['Samsung','samsung.jpg'],
    ['Jio','jio.jpg'],['Haier','haier.jpg'],['DLF','dlf.jpg'],
    ['DLF Cyberhub','dlf-cyberhub.jpg'],['BPTP','bptp.jpg'],['GAIL','gail.jpg'],
    ['SAIL','sail.jpg'],['SBI','sbi.jpg'],['ArcelorMittal','arcelor-mittal.jpg'],
    ['Jindal Stainless','jindal-stainless.jpg'],['Incredible India','incredible-india.jpg'],
    ['Big Boy Toyz','big-boys-toyz.jpg'],['Royal Enfield Motors','royal-enfield.jpg']
  ];

  var STYLE_ID = 'tkc-clients-style';
  function injectStyles(){
    if (document.getElementById(STYLE_ID)) return;
    var s = document.createElement('style'); s.id = STYLE_ID;
    s.textContent = [
      '.tkc-clients{position:relative;padding:88px 0 96px;background:radial-gradient(ellipse at top,#131313 0%,#0a0a0a 60%,#050505 100%);border-top:1px solid rgba(255,255,255,.06);border-bottom:1px solid rgba(255,255,255,.06);overflow:hidden}',
      '.tkc-clients::before{content:"";position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.05) 1px,transparent 1px);background-size:22px 22px;opacity:.35;pointer-events:none}',
      '.tkc-clients .tkc-clients-head{position:relative;max-width:1200px;margin:0 auto 48px;padding:0 24px;text-align:center}',
      '.tkc-clients .tkc-eyebrow{display:inline-block;font-family:"Space Grotesk",Inter,sans-serif;font-size:11px;font-weight:700;letter-spacing:.32em;text-transform:uppercase;color:#e9c874;margin-bottom:18px;padding:8px 18px;border:1px solid rgba(233,200,116,.35);border-radius:999px;background:rgba(233,200,116,.06)}',
      '.tkc-clients h2{font-family:"Space Grotesk",Inter,sans-serif;font-weight:700;font-size:clamp(26px,3.8vw,42px);line-height:1.12;letter-spacing:-.02em;color:#fafafa;margin:0 0 14px}',
      '.tkc-clients h2 em{font-style:normal;background:linear-gradient(90deg,#e9c874,#f5deb3);-webkit-background-clip:text;background-clip:text;color:transparent}',
      '.tkc-clients p.tkc-sub{font-family:Inter,system-ui,sans-serif;font-size:15px;line-height:1.65;color:rgba(255,255,255,.6);margin:0 auto;max-width:660px}',
      '.tkc-clients .tkc-viewport{position:relative;overflow:hidden;mask-image:linear-gradient(to right,transparent,#000 6%,#000 94%,transparent);-webkit-mask-image:linear-gradient(to right,transparent,#000 6%,#000 94%,transparent)}',
      '.tkc-clients .tkc-track{display:flex;gap:28px;align-items:center;width:max-content;animation:tkc-logo-scroll 60s linear infinite;will-change:transform}',
      '.tkc-clients .tkc-track:hover{animation-play-state:paused}',
      '.tkc-clients .tkc-logo{flex:0 0 auto;height:120px;width:200px;display:flex;align-items:center;justify-content:center;padding:18px 22px;background:linear-gradient(180deg,#111,#080808);border:1px solid rgba(255,255,255,.08);border-radius:14px;box-shadow:0 4px 20px rgba(0,0,0,.4),inset 0 1px 0 rgba(255,255,255,.04);transition:transform .35s ease,border-color .35s ease,box-shadow .35s ease}',
      '.tkc-clients .tkc-logo:hover{transform:translateY(-4px);border-color:rgba(233,200,116,.45);box-shadow:0 10px 30px rgba(0,0,0,.6),0 0 0 1px rgba(233,200,116,.15),inset 0 1px 0 rgba(255,255,255,.06)}',
      '.tkc-clients .tkc-logo img{max-height:100%;max-width:100%;object-fit:contain;transition:transform .35s ease;filter:drop-shadow(0 2px 6px rgba(0,0,0,.4))}',
      '.tkc-clients .tkc-logo:hover img{transform:scale(1.05)}',
      '.tkc-clients .tkc-row + .tkc-row{margin-top:24px}',
      '.tkc-clients .tkc-row.rev .tkc-track{animation-name:tkc-logo-scroll-rev;animation-duration:70s}',
      '.tkc-clients .tkc-stats{position:relative;max-width:1100px;margin:56px auto 0;padding:0 24px;display:grid;grid-template-columns:repeat(3,1fr);gap:24px;text-align:center}',
      '.tkc-clients .tkc-stat{padding:22px 18px;border:1px solid rgba(255,255,255,.08);border-radius:14px;background:rgba(255,255,255,.02)}',
      '.tkc-clients .tkc-stat b{display:block;font-family:"Space Grotesk",sans-serif;font-size:clamp(28px,3.4vw,40px);font-weight:700;color:#e9c874;letter-spacing:-.02em;line-height:1}',
      '.tkc-clients .tkc-stat span{display:block;margin-top:8px;font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:rgba(255,255,255,.55)}',
      '@keyframes tkc-logo-scroll{from{transform:translateX(0)}to{transform:translateX(-50%)}}',
      '@keyframes tkc-logo-scroll-rev{from{transform:translateX(-50%)}to{transform:translateX(0)}}',
      '@media (prefers-reduced-motion:reduce){.tkc-clients .tkc-track{animation:none}}',
      '@media (max-width:640px){.tkc-clients{padding:64px 0 68px}.tkc-clients .tkc-logo{height:88px;width:150px;padding:12px 14px;border-radius:12px}.tkc-clients .tkc-track{gap:18px}.tkc-clients .tkc-stats{grid-template-columns:1fr;gap:12px;margin-top:36px}}'
    ].join('');
    document.head.appendChild(s);
  }

  function makeRow(list, reverse){
    var row = document.createElement('div'); row.className = 'tkc-row' + (reverse?' rev':'');
    var vp = document.createElement('div'); vp.className = 'tkc-viewport';
    var track = document.createElement('div'); track.className = 'tkc-track';
    function fill(){
      list.forEach(function(l){
        var d = document.createElement('div'); d.className = 'tkc-logo';
        var img = document.createElement('img');
        img.src = '/assets/clients-v2/' + l[1];
        img.alt = l[0] + ' — TKC Talent corporate client';
        img.loading = 'lazy'; img.decoding = 'async';
        img.width = 200; img.height = 120;
        d.appendChild(img); track.appendChild(d);
      });
    }
    fill(); fill(); // duplicate for seamless loop
    vp.appendChild(track); row.appendChild(vp);
    return row;
  }

  function buildSection(){
    var sec = document.createElement('section');
    sec.className = 'tkc-clients';
    sec.id = 'tkc-clients';
    sec.setAttribute('aria-label', 'Corporate clients trusted by TKC Talent');
    var head = document.createElement('div'); head.className = 'tkc-clients-head';
    head.innerHTML =
      '<span class="tkc-eyebrow">Trusted by India\u2019s Leading Brands</span>' +
      '<h2>Corporate clients who trust <em>The Kabir Company</em></h2>' +
      '<p class="tkc-sub">Two decades of celebrity bookings, brand activations and live-event delivery for automotive, luxury real-estate, PSU and lifestyle leaders across India.</p>';
    sec.appendChild(head);
    // Split for two rows
    var mid = Math.ceil(LOGOS.length/2);
    sec.appendChild(makeRow(LOGOS.slice(0,mid), false));
    sec.appendChild(makeRow(LOGOS.slice(mid), true));
    var stats = document.createElement('div'); stats.className = 'tkc-stats';
    stats.innerHTML =
      '<div class="tkc-stat"><b>20+</b><span>Years of Execution</span></div>' +
      '<div class="tkc-stat"><b>500+</b><span>Bollywood, Music &amp; OTT Talents</span></div>' +
      '<div class="tkc-stat"><b>1,200+</b><span>Brand Activations Delivered</span></div>';
    sec.appendChild(stats);
    return sec;
  }

  function findStepsSection(){
    var headings = document.querySelectorAll('h2');
    for (var i=0;i<headings.length;i++){
      if (/3 Simple Steps/i.test(headings[i].textContent||'')){
        return headings[i].closest('section');
      }
    }
    return null;
  }

  function stripStepsImages(section){
    // Remove first-child image wrapper in each article inside the steps section
    var articles = section.querySelectorAll('article');
    articles.forEach(function(a){
      // Remove any element whose class contains 'aspect-' (image wrapper)
      a.querySelectorAll('[class*="aspect-"]').forEach(function(el){ el.remove(); });
      // Also remove any leftover <img> or <picture>
      a.querySelectorAll('img,picture,source').forEach(function(el){ el.remove(); });
    });
  }

  var INSERTED = false;
  function run(){
    var sec = findStepsSection();
    if (!sec) return false;
    stripStepsImages(sec);
    if (!INSERTED){
      injectStyles();
      var clients = buildSection();
      sec.parentNode.insertBefore(clients, sec.nextSibling);
      INSERTED = true;
    }
    return true;
  }

  function start(){
    if (run()) { watchForRerender(); return; }
    var tries = 0;
    var mo = new MutationObserver(function(){ if (run() || ++tries > 80) { mo.disconnect(); watchForRerender(); } });
    mo.observe(document.body, {childList:true, subtree:true});
    setTimeout(function(){ try{ mo.disconnect(); }catch(_){}} , 20000);
  }

  // Re-strip images if the React app re-renders them
  function watchForRerender(){
    var mo = new MutationObserver(function(){
      var sec = findStepsSection();
      if (sec && sec.querySelector('img,[class*="aspect-"]')) stripStepsImages(sec);
    });
    mo.observe(document.body, {childList:true, subtree:true});
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
