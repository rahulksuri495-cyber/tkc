/* TKC — remove 3-Steps images + inject Corporate Clients scroller (homepage only) */
(function(){
  if (location.pathname !== '/' && location.pathname !== '/index.html') return;

  var LOGOS = [
    ['BMW','bmw.png'],['Mercedes-Benz','mercedes-benz.png'],['Jaguar','jaguar.png'],
    ['Range Rover','range-rover.png'],['Harley-Davidson','harley-davidson.png'],
    ['Royal Enfield','royal-enfield.png'],['Hyundai','hyundai.png'],['Honda','honda.png'],
    ['Skoda','skoda.png'],['Vivo','vivo.png'],['Jio','jio.png'],['Haier','haier.png'],
    ['DLF','dlf.png'],['DLF Cyberhub','dlf-cyberhub.png'],['BPTP','bptp.png'],
    ['Sikka Builders','sikka-builders.png'],['Pacific Golf Estate','pacific-golf-estate.png'],
    ['GAIL','gail.png'],['SAIL','sail.png'],['ArcelorMittal','arcelor-miittal.png'],
    ['Jindal Stainless','jindal-stainless.png'],['Incredible India','incredible-india.png'],
    ['Vanesa','vanesa.png'],['Big Boys Toys','big-boys-toy-logo.png'],
    ['Jindal Stainless','jindal-stainless-2.png']
  ];

  var STYLE_ID = 'tkc-clients-style';
  function injectStyles(){
    if (document.getElementById(STYLE_ID)) return;
    var s = document.createElement('style'); s.id = STYLE_ID;
    s.textContent = [
      '.tkc-clients{position:relative;padding:72px 0 80px;background:#fafaf7;border-top:1px solid rgba(13,13,13,.08);border-bottom:1px solid rgba(13,13,13,.08);overflow:hidden}',
      '.tkc-clients .tkc-clients-head{max-width:1200px;margin:0 auto 40px;padding:0 24px;text-align:center}',
      '.tkc-clients .tkc-eyebrow{display:inline-block;font-family:"Space Grotesk",Inter,sans-serif;font-size:11px;font-weight:700;letter-spacing:.24em;text-transform:uppercase;color:#8a6a26;margin-bottom:14px;padding:6px 14px;border:1px solid rgba(138,106,38,.35);border-radius:999px;background:rgba(201,168,76,.08)}',
      '.tkc-clients h2{font-family:"Space Grotesk",Inter,sans-serif;font-weight:700;font-size:clamp(24px,3.6vw,38px);line-height:1.15;letter-spacing:-.02em;color:#0d0d0d;margin:0 0 10px}',
      '.tkc-clients p.tkc-sub{font-family:Inter,system-ui,sans-serif;font-size:15px;line-height:1.6;color:rgba(13,13,13,.65);margin:0 auto;max-width:640px}',
      '.tkc-clients .tkc-viewport{position:relative;overflow:hidden;mask-image:linear-gradient(to right,transparent,#000 8%,#000 92%,transparent);-webkit-mask-image:linear-gradient(to right,transparent,#000 8%,#000 92%,transparent)}',
      '.tkc-clients .tkc-track{display:flex;gap:56px;align-items:center;width:max-content;animation:tkc-logo-scroll 55s linear infinite;will-change:transform}',
      '.tkc-clients .tkc-track:hover{animation-play-state:paused}',
      '.tkc-clients .tkc-logo{flex:0 0 auto;height:72px;width:170px;display:flex;align-items:center;justify-content:center;padding:10px 14px}',
      '.tkc-clients .tkc-logo img{max-height:100%;max-width:100%;object-fit:contain;filter:grayscale(1) contrast(.9);opacity:.72;transition:filter .3s ease,opacity .3s ease,transform .3s ease}',
      '.tkc-clients .tkc-logo:hover img{filter:none;opacity:1;transform:scale(1.05)}',
      '.tkc-clients .tkc-row + .tkc-row{margin-top:18px}',
      '.tkc-clients .tkc-row.rev .tkc-track{animation-name:tkc-logo-scroll-rev;animation-duration:65s}',
      '@keyframes tkc-logo-scroll{from{transform:translateX(0)}to{transform:translateX(-50%)}}',
      '@keyframes tkc-logo-scroll-rev{from{transform:translateX(-50%)}to{transform:translateX(0)}}',
      '@media (prefers-reduced-motion:reduce){.tkc-clients .tkc-track{animation:none}}',
      '@media (max-width:640px){.tkc-clients{padding:56px 0 60px}.tkc-clients .tkc-logo{height:56px;width:130px;padding:8px 10px}.tkc-clients .tkc-track{gap:36px}}'
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
        img.src = '/assets/clients/' + l[1];
        img.alt = l[0] + ' — TKC Talent corporate client';
        img.loading = 'lazy'; img.decoding = 'async';
        img.width = 170; img.height = 72;
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
      '<h2>Corporate clients who trust The Kabir Company</h2>' +
      '<p class="tkc-sub">Two decades of celebrity bookings, brand activations and live-event delivery for automotive, luxury real-estate, PSU and lifestyle leaders across India.</p>';
    sec.appendChild(head);
    // Split for two rows
    var mid = Math.ceil(LOGOS.length/2);
    sec.appendChild(makeRow(LOGOS.slice(0,mid), false));
    sec.appendChild(makeRow(LOGOS.slice(mid), true));
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
