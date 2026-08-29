/* TKC Talent — IITEO Legacy homepage section
   Injects a rich dignitary-gallery band summarizing /iiteo/ for E-E-A-T. */
(function(){
  if (location.pathname !== '/' && location.pathname !== '/index.html') return;
  var INSERTED = false;
  var STYLE_ID = 'tkc-iiteo-legacy-style';

  var LEADERS = [
    {file:'pranab-mukherjee-president-india.png', name:'Shri Pranab Mukherjee', role:'13th President of India'},
    {file:'pratibha-patil-president-india.png',   name:'Smt. Pratibha Patil',   role:'12th President of India'},
    {file:'narendra-modi-prime-minister.png',     name:'Shri Narendra Modi',    role:'Prime Minister of India'},
    {file:'rajnath-singh-defence-minister.png',   name:'Shri Rajnath Singh',    role:'Defence Minister of India'},
    {file:'sheila-dikshit-cm-delhi.png',          name:'Smt. Sheila Dikshit',   role:'Former Chief Minister, Delhi'},
    {file:'bhupinder-singh-hooda-cm-haryana.png', name:'Shri Bhupinder Singh Hooda', role:'Former Chief Minister, Haryana'},
    {file:'akhilesh-yadav-cm-uttar-pradesh.png',  name:'Shri Akhilesh Yadav',   role:'Former Chief Minister, Uttar Pradesh'},
    {file:'omar-abdullah-cm-jammu-kashmir.png',   name:'Shri Omar Abdullah',    role:'Chief Minister, Jammu & Kashmir'},
    {file:'arjun-munda-cm-jharkhand.png',         name:'Shri Arjun Munda',      role:'Former Chief Minister, Jharkhand'},
    {file:'ramesh-pokhriyal-cm-uttarakhand.png',  name:'Shri Ramesh Pokhriyal', role:'Former Chief Minister, Uttarakhand'},
    {file:'jagannath-pahadia-governor.png',       name:'Shri Jagannath Pahadia',role:'Former Governor of Haryana'},
    {file:'syed-ahmed-governor.png',              name:'Shri Syed Ahmed',       role:'Former Governor of Jharkhand'}
  ];

  function injectStyles(){
    if (document.getElementById(STYLE_ID)) return;
    var s = document.createElement('style');
    s.id = STYLE_ID;
    s.textContent = [
      '.tkc-iiteo{position:relative;padding:80px 22px;font-family:Inter,system-ui,sans-serif;color:#e9e4d4;background:radial-gradient(1000px 500px at 85% 0%,rgba(201,168,76,.14),transparent 60%),linear-gradient(180deg,#0b0a07 0%,#141008 100%);border-top:3px solid #c9a84c;border-bottom:3px solid #c9a84c;overflow:hidden}',
      '.tkc-iiteo:before{content:"";position:absolute;inset:0;background:radial-gradient(700px 340px at 8% 100%,rgba(201,168,76,.10),transparent 60%);z-index:0}',
      '.tkc-iiteo .tkc-wrap{position:relative;z-index:2;max-width:1200px;margin:0 auto}',
      '.tkc-iiteo .tkc-sticky-label{position:sticky;top:0;display:inline-flex;align-items:center;gap:8px;padding:8px 18px;font-size:11px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;border-radius:0 0 14px 0;z-index:10;background:rgba(201,168,76,.95);color:#1a1407;margin-bottom:-32px}',
      '.tkc-iiteo .eyebrow{display:inline-flex;align-items:center;gap:10px;font-size:11px;letter-spacing:.22em;text-transform:uppercase;font-weight:700;margin-bottom:18px;padding:7px 14px;border-radius:999px;background:rgba(201,168,76,.14);color:#e8c97a;border:1px solid rgba(201,168,76,.4)}',
      '.tkc-iiteo h2{font-family:"Space Grotesk",Inter,sans-serif;font-weight:700;font-size:clamp(28px,4.4vw,46px);line-height:1.08;letter-spacing:-.02em;margin:0 0 18px;color:#fdf6df;max-width:900px}',
      '.tkc-iiteo h2 .accent{background:linear-gradient(90deg,#e8c97a,#c9a84c);-webkit-background-clip:text;background-clip:text;color:transparent}',
      '.tkc-iiteo p{font-size:16px;line-height:1.7;color:#cfc7ad;max-width:820px;margin:0 0 14px}',
      '.tkc-iiteo p a{color:#e8c97a;border-bottom:1px solid rgba(232,201,122,.4);text-decoration:none}',
      '.tkc-iiteo p a:hover{color:#fff;border-color:#fff}',
      '.tkc-iiteo .stats{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:28px 0 40px;max-width:820px}',
      '.tkc-iiteo .stat{padding:18px;border:1px solid rgba(201,168,76,.28);border-radius:14px;background:linear-gradient(180deg,rgba(201,168,76,.08),rgba(201,168,76,.02))}',
      '.tkc-iiteo .stat .n{font-family:"Space Grotesk",sans-serif;font-size:26px;font-weight:700;color:#fdf6df;letter-spacing:-.02em;line-height:1}',
      '.tkc-iiteo .stat .l{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#e8c97a;margin-top:8px;font-weight:600}',
      '@media (max-width:640px){.tkc-iiteo .stats{grid-template-columns:1fr}.tkc-iiteo .stat .n{font-size:22px}}',
      '.tkc-iiteo .gallery{display:grid;grid-template-columns:repeat(6,1fr);gap:16px;margin-top:8px}',
      '@media (max-width:1024px){.tkc-iiteo .gallery{grid-template-columns:repeat(4,1fr)}}',
      '@media (max-width:640px){.tkc-iiteo .gallery{grid-template-columns:repeat(2,1fr);gap:12px}}',
      '.tkc-iiteo .card{position:relative;padding:14px 12px 16px;border-radius:16px;background:linear-gradient(180deg,rgba(255,255,255,.04),rgba(255,255,255,.015));border:1px solid rgba(201,168,76,.22);text-align:center;transition:transform .25s ease,border-color .25s ease,box-shadow .25s ease}',
      '.tkc-iiteo .card:hover{transform:translateY(-4px);border-color:rgba(232,201,122,.65);box-shadow:0 18px 40px -18px rgba(201,168,76,.4)}',
      '.tkc-iiteo .card .ph{width:100%;aspect-ratio:1/1;border-radius:12px;overflow:hidden;background:#1a1407;border:1px solid rgba(201,168,76,.3);margin-bottom:12px}',
      '.tkc-iiteo .card .ph img{width:100%;height:100%;object-fit:cover;object-position:center top;display:block;transition:transform .5s ease}',
      '.tkc-iiteo .card:hover .ph img{transform:scale(1.06)}',
      '.tkc-iiteo .card .nm{font-family:"Space Grotesk",sans-serif;font-size:13px;font-weight:700;color:#fdf6df;line-height:1.25;margin:0 0 4px}',
      '.tkc-iiteo .card .rl{font-size:11px;color:#cfc7ad;line-height:1.35;letter-spacing:.02em}',
      '.tkc-iiteo .cta-row{display:flex;flex-wrap:wrap;gap:12px;margin-top:36px}',
      '.tkc-iiteo .cta{display:inline-flex;align-items:center;gap:10px;padding:14px 24px;border-radius:12px;font-weight:600;font-size:15px;text-decoration:none;transition:transform .2s ease,box-shadow .2s ease}',
      '.tkc-iiteo .cta.primary{background:linear-gradient(135deg,#e8c97a,#c9a84c);color:#1a1407;box-shadow:0 14px 40px -14px rgba(201,168,76,.7)}',
      '.tkc-iiteo .cta.primary:hover{transform:translateY(-2px);box-shadow:0 20px 55px -12px rgba(201,168,76,.9)}',
      '.tkc-iiteo .cta.ghost{background:rgba(255,255,255,.05);color:#fdf6df;border:1px solid rgba(232,201,122,.35)}',
      '.tkc-iiteo .cta.ghost:hover{background:rgba(255,255,255,.1)}',
      '.tkc-iiteo .tkc-reveal{opacity:0;transform:translateY(12px);transition:opacity .5s ease-out,transform .5s ease-out}',
      '.tkc-iiteo .tkc-reveal.in{opacity:1;transform:none}',
      '.tkc-iiteo .tkc-reveal[data-d="1"]{transition-delay:.06s}.tkc-iiteo .tkc-reveal[data-d="2"]{transition-delay:.12s}.tkc-iiteo .tkc-reveal[data-d="3"]{transition-delay:.18s}.tkc-iiteo .tkc-reveal[data-d="4"]{transition-delay:.24s}',
      '@media (prefers-reduced-motion:reduce){.tkc-iiteo .tkc-reveal{opacity:1;transform:none;transition:none}}'
    ].join('');
    document.head.appendChild(s);
  }

  function buildGallery(){
    return LEADERS.map(function(p){
      var alt = p.name + ', ' + p.role + ' — hosted by The Kabir Company / TKC Talent leadership';
      return ''+
        '<figure class="card tkc-reveal">'+
          '<div class="ph"><img src="/assets/iiteo-leaders/'+p.file+'" alt="'+alt+'" loading="lazy" decoding="async" width="240" height="240"/></div>'+
          '<figcaption><div class="nm">'+p.name+'</div><div class="rl">'+p.role+'</div></figcaption>'+
        '</figure>';
    }).join('');
  }

  function buildSection(){
    var el = document.createElement('section');
    el.className = 'tkc-iiteo';
    el.id = 'tkc-iiteo-legacy';
    el.setAttribute('aria-labelledby','tkc-iiteo-heading');
    el.innerHTML = ''+
      '<span class="tkc-sticky-label">IITEO Legacy</span>'+
      '<div class="tkc-wrap">'+
        '<span class="eyebrow tkc-reveal">IITEO \u00D7 The Kabir Company \u2014 Two-Decade Event Legacy</span>'+
        '<h2 id="tkc-iiteo-heading" class="tkc-reveal" data-d="1">From India\u2019s biggest trade fairs to the country\u2019s <span class="accent">most-booked stage.</span></h2>'+
        '<p class="tkc-reveal" data-d="2">TKC Talent is the celebrity-booking vertical of <strong>The Kabir Company</strong>, a New Delhi-headquartered event management group whose legacy was shaped through India\u2019s trade fair and exhibition ecosystem\u2014including long-standing association with <strong>IITEO (India International Trade Event Organisation)</strong>. That operating DNA, forged across large public exhibitions and government-scale programming, is what now powers our concerts, corporate events, luxury weddings and Bollywood celebrity bookings across India.</p>'+
        '<p class="tkc-reveal" data-d="3">Over two decades, the leadership team has hosted and worked alongside Presidents, Prime Ministers, Union Ministers, Governors and Chief Ministers of India\u2014credentials that underline the trust, compliance discipline and on-ground execution capability every TKC Talent booking is built on. <a href="/topleader/">Meet the leaders we\u2019ve hosted \u2192</a></p>'+
        '<div class="stats">'+
          '<div class="stat tkc-reveal" data-d="1"><div class="n">20+ Yrs</div><div class="l">Event legacy</div></div>'+
          '<div class="stat tkc-reveal" data-d="2"><div class="n">10+</div><div class="l">Heads of State &amp; CMs hosted</div></div>'+
          '<div class="stat tkc-reveal" data-d="3"><div class="n">500+</div><div class="l">Talents \u00B7 Pan-India delivery</div></div>'+
        '</div>'+
        '<div class="gallery">'+ buildGallery() +'</div>'+
        '<div class="cta-row">'+
          '<a class="cta primary" href="/topleader/">Read the full IITEO legacy \u2192</a>'+
          '<a class="cta ghost" href="https://wa.me/919599599699?text=Hi%20TKC%20Talent%2C%20I%27d%20like%20to%20discuss%20an%20event." target="_blank" rel="noopener">Talk to our team on WhatsApp</a>'+
        '</div>'+
      '</div>';
    return el;
  }

  function injectSchema(){
    if (document.getElementById('tkc-iiteo-legacy-jsonld')) return;
    var data = {
      "@context":"https://schema.org",
      "@type":"ItemList",
      "@id":"https://tkctalent.com/#iiteo-legacy-dignitaries",
      "name":"Dignitaries hosted by The Kabir Company / TKC Talent leadership",
      "itemListElement": LEADERS.map(function(p,i){
        return {"@type":"ListItem","position":i+1,"item":{"@type":"Person","name":p.name,"jobTitle":p.role}};
      })
    };
    var s = document.createElement('script');
    s.type = 'application/ld+json';
    s.id = 'tkc-iiteo-legacy-jsonld';
    s.textContent = JSON.stringify(data);
    document.head.appendChild(s);
  }

  function findAnchor(){
    // Prefer inserting right after the existing #tkc-legacy band
    var legacy = document.getElementById('tkc-legacy');
    if (legacy) return {parent:legacy.parentNode, before:legacy.nextSibling};
    // Fallback: before the clients scroller
    var clients = document.getElementById('tkc-clients');
    if (clients) return {parent:clients.parentNode, before:clients};
    // Last resort: before footer
    var footer = document.querySelector('footer');
    if (footer) return {parent:footer.parentNode, before:footer};
    return null;
  }

  function wireReveal(scope){
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){ if (e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } });
    }, {threshold:0.05, rootMargin:'0px 0px 60px 0px'});
    scope.querySelectorAll('.tkc-reveal').forEach(function(n){ io.observe(n); });
  }

  function insert(){
    if (INSERTED) return true;
    var anchor = findAnchor();
    if (!anchor) return false;
    injectStyles();
    var sec = buildSection();
    anchor.parent.insertBefore(sec, anchor.before);
    wireReveal(sec);
    injectSchema();
    INSERTED = true;
    return true;
  }

  function start(){
    if (insert()) return;
    var tries = 0;
    var mo = new MutationObserver(function(){
      if (insert() || ++tries > 80) mo.disconnect();
    });
    mo.observe(document.body, {childList:true, subtree:true});
    setTimeout(function(){ try{ mo.disconnect(); }catch(_){} }, 20000);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
