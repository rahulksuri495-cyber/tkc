(function(){
  var MARK='data-tkc-singers-enhanced';

  // ===== Responsive header breakpoint shim =====
  // The header desktop nav is gated on Tailwind's `md` breakpoint (768px),
  // but between 768–1023px the nav links collide with the logo and the
  // "Book Now" pill wraps onto two lines — the perceived result is that the
  // navigation disappears or looks broken. Shift the breakpoint to `lg`
  // (1024px) via a single injected stylesheet so the mobile drawer covers
  // the tablet range cleanly.
  try{
    if(!document.getElementById('tkc-nav-breakpoint-shim')){
      var s=document.createElement('style');
      s.id='tkc-nav-breakpoint-shim';
      s.textContent=[
        '@media (max-width:1023.98px){',
        '  nav > ul.md\\:flex{display:none !important;}',
        '  nav > a.md\\:inline-flex,',
        '  nav > .md\\:inline-flex,',
        '  nav > .md\\:flex:not(ul){display:none !important;}',
        '  button[aria-controls="mobile-nav-drawer"].md\\:hidden{display:inline-flex !important;}',
        '  aside#mobile-nav-drawer.md\\:hidden{display:flex !important;}',
        '  div[aria-hidden="true"].md\\:hidden[class*="backdrop-blur"]{display:block !important;}',
        '  /* Always show the Home > IITEO submenu inline on small screens, since',
        '     the hover flyout that desktop uses is unreachable on touch. */',
        '  ul[data-tkc-home-sub]{position:static !important;visibility:visible !important;',
        '    opacity:1 !important;display:block !important;box-shadow:none !important;',
        '    border:0 !important;background:transparent !important;color:inherit !important;',
        '    margin:4px 0 0 12px !important;padding:0 !important;max-height:none !important;',
        '    min-width:0 !important;ring-width:0 !important;}',
        '  ul[data-tkc-home-sub] a{padding-left:0 !important;}',
        '}'
      ].join('');
      (document.head||document.documentElement).appendChild(s);
    }
  }catch(e){}

  // ===== Image visibility safety net =====
  // Static export sometimes ships <img class="... opacity-0"> expecting React
  // to flip it on load. On the deployed static HTML that handler never runs,
  // so we force-paint every <img> as visible regardless of load events.
  function forceImgVisible(img){
    try{
      img.classList.remove('opacity-0');
      img.style.opacity='1';
      img.style.visibility='visible';
    }catch(e){}
  }
  function sweepImages(root){
    (root||document).querySelectorAll('img').forEach(forceImgVisible);
  }
  document.addEventListener('load',function(e){
    if(e.target && e.target.tagName==='IMG') forceImgVisible(e.target);
  },true);
  document.addEventListener('error',function(e){
    if(e.target && e.target.tagName==='IMG') forceImgVisible(e.target);
  },true);

  // ===== Nested submenu reachability =====
  // The right-side flyouts use `left-full ml-1`, which (a) leaves a 4px hover
  // gap that drops the menu on mouse-out and (b) overflows the viewport on
  // narrower screens. Add an invisible hover bridge and flip to the left side
  // when there isn't room on the right.
  function fixSubmenu(ul){
    if(ul.__tkcSubFixed) return;
    ul.__tkcSubFixed=true;
    var li=ul.parentElement;
    if(!li) return;
    // close the hover gap so the cursor never crosses dead space
    ul.classList.remove('ml-1');
    ul.style.marginLeft='0';
    ul.style.paddingLeft='4px';
    // make sure it scrolls within the viewport on every screen
    ul.style.maxHeight='min(75vh, calc(100vh - 96px))';
    ul.style.overflowY='auto';
    ul.style.overscrollBehavior='contain';
    // flip to the opposite side if it would overflow the viewport
    function reposition(){
      ul.classList.remove('left-full','right-full');
      ul.style.left=''; ul.style.right='';
      var probeLeft=true;
      var r=li.getBoundingClientRect();
      var w=ul.offsetWidth||260;
      if(r.right+w+8 > window.innerWidth && r.left-w-8 > 0) probeLeft=false;
      if(probeLeft){ ul.classList.add('left-full'); }
      else { ul.classList.add('right-full'); ul.style.paddingLeft='0'; ul.style.paddingRight='4px'; }
    }
    li.addEventListener('mouseenter',reposition);
    li.addEventListener('focusin',reposition);
  }
  function fixAllSubmenus(){
    document.querySelectorAll('li.group\\/sub > ul').forEach(fixSubmenu);
  }

  var singers=[
    ['Book Altaf Raja','/book-altaf-raja/'],['Book A.R. Rahman','/book-ar-rahman/'],['Book Arijit Singh','/book-arijit-singh/'],['Book Armaan Malik','/book-armaan-malik/'],['Book Asees Kaur','/book-asees-kaur/'],['Book B Praak','/book-b-praak/'],['Book Badshah','/book-badshah/'],['Book Darshan Raval','/book-darshan-raval/'],['Book Diljit Dosanjh','/book-diljit-dosanjh/'],['Book Guru Randhawa','/book-guru-randhawa/'],['Book Hanumankind','/book-hanumankind/'],['Book Jasmine Sandlas','/book-jasmine-sandlas/'],['Book Jonita Gandhi','/book-jonita-gandhi/'],['Book Jubin Nautiyal','/book-jubin-nautiyal/'],['Book Kanika Kapoor','/book-kanika-kapoor/'],['Book Kumar Sanu','/book-kumar-sanu/'],['Book Lucky Ali','/book-lucky-ali/'],['Book Meet Bros','/book-meet-bros/'],['Book Mohit Chauhan','/book-mohit-chauhan/'],['Book Neha Bhasin','/book-neha-bhasin/'],['Book Neha Kakkar','/book-neha-kakkar/'],['Book Palak Muchhal','/book-palak-muchhal/'],['Book Pritam','/book-pritam/'],['Book Sachet-Parampara','/book-sachet-parampara/'],['Book Sachin-Jigar','/book-sachin-jigar/'],['Book Salim-Sulaiman','/book-salim-sulaiman/'],['Book Sara Gurpal','/book-sara-gurpal/'],['Book Shamsher Lehri','/book-shamsher-lehri/'],['Book Shankar Mahadevan','/book-shankar-mahadevan/'],['Book Shreya Ghoshal','/book-shreya-ghoshal/'],['Book Sonu Nigam','/book-sonu-nigam/'],['Book Sunanda Sharma','/book-sunanda-sharma/'],['Book Sunidhi Chauhan','/book-sunidhi-chauhan/'],['Book Tanishk Bagchi','/book-tanishk-bagchi/'],['Book Vishal-Shekhar','/book-vishal-shekhar/']
  ];

  function singerItemHtml(item, cls){
    return '<li><a href="'+item[1]+'" class="'+cls+'">'+item[0]+'</a></li>';
  }

  function chevronRight(){
    return '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-chevron-down h-3.5 w-3.5 -rotate-90" aria-hidden="true"><path d="m6 9 6 6 6-6"></path></svg>';
  }

  function normHref(href){
    if(!href) return '';
    try{ href=new URL(href, location.origin).pathname; }catch(e){}
    href=String(href).split('?')[0].split('#')[0];
    if(href.length>1) href=href.replace(/\/+$/,'');
    return href;
  }

  function samePath(a, path){
    return normHref(a && a.getAttribute('href'))===normHref(path);
  }

  function textHas(a, words){
    var txt=(a.textContent||'').toLowerCase();
    return words.every(function(w){ return txt.indexOf(w)!==-1; });
  }

  function navLinks(){
    return Array.prototype.slice.call(document.querySelectorAll('nav a'));
  }

  function categoryItemHtml(label, href, cls){
    return '<li class="relative group/sub"><a href="'+href+'" class="'+cls+'">'+label+chevronRight()+'</a></li>';
  }

  function ensureCelebrityBookingMenu(){
    // Desktop: append Durga Puja link to the existing Celebrity Booking dropdown
    navLinks().forEach(function(a){
      if(!textHas(a,['celebrity','booking','india'])) return;
      if(a.closest('#mobile-nav-drawer')) return;
      var li=a.parentElement;
      if(!li || li.tagName!=='LI') return;
      var ul=li.querySelector(':scope > ul');
      if(!ul) return;
      if(ul.querySelector('a[href="/durga-puja-2026/"]')) return;
      ul.insertAdjacentHTML('beforeend','<li><a href="/durga-puja-2026/" class="block rounded-md px-3 py-2 text-sm font-medium text-foreground/80 transition-colors hover:bg-foreground hover:text-background">Durga Puja 2026 &mdash; CR Park</a></li>');
    });

    // Mobile drawer: append to existing Celebrity Booking sub-menu
    var drawer=document.getElementById('mobile-nav-drawer');
    if(!drawer) return;
    Array.prototype.slice.call(drawer.querySelectorAll('a,button')).forEach(function(a){
      if(!textHas(a,['celebrity','booking','india'])) return;
      var li=a.parentElement;
      if(!li || li.tagName!=='LI') return;
      var ul=li.querySelector(':scope > ul');
      if(!ul) return;
      if(ul.querySelector('a[href="/durga-puja-2026/"]')) return;
      ul.insertAdjacentHTML('beforeend','<li><a href="/durga-puja-2026/" class="flex min-h-9 items-center rounded-lg px-3 py-2 text-xs text-foreground/80 transition hover:bg-foreground/5">Durga Puja 2026 &mdash; CR Park</a></li>');
    });
  }

  function ensureSingerSubmenus(){
    navLinks().forEach(function(a){
      if(!samePath(a,'/singer-booking-india/') && !textHas(a,['singer'])) return;
      if(a.closest('#mobile-nav-drawer')) return;
      var li=a.parentElement;
      if(!li || li.tagName!=='LI') return;
      if(li.querySelector('ul a[href="/book-arijit-singh/"]')) return;
      li.classList.add('relative','group/sub');
      a.classList.remove('block');
      a.classList.add('flex','items-center','justify-between','gap-2','group-hover/sub:bg-foreground','group-hover/sub:text-background');
      if(!a.querySelector('svg')) a.insertAdjacentHTML('beforeend',chevronRight());
      a.insertAdjacentHTML('afterend','<ul class="invisible absolute left-full top-0 z-50 ml-1 max-h-[75vh] min-w-60 overflow-y-auto overscroll-contain rounded-xl border border-foreground/10 bg-background p-2 text-foreground opacity-0 shadow-2xl ring-1 ring-foreground/5 transition-all duration-150 group-hover/sub:visible group-hover/sub:opacity-100 group-focus-within/sub:visible group-focus-within/sub:opacity-100">'+singers.map(function(item){return singerItemHtml(item,'block rounded-md px-3 py-2 text-sm font-medium text-foreground/80 transition-colors hover:bg-foreground hover:text-background');}).join('')+'</ul>');
    });

    var drawer=document.getElementById('mobile-nav-drawer');
    if(!drawer) return;
    drawer.querySelectorAll('a[href="/singer-booking-india/"]').forEach(function(a){
      if((a.textContent||'').indexOf('Singers')===-1) return;
      var li=a.parentElement;
      if(!li || li.tagName!=='LI' || li.querySelector('ul a[href="/book-arijit-singh/"]')) return;
      li.insertAdjacentHTML('beforeend','<ul class="ml-3 mt-1 flex max-h-64 flex-col gap-1 overflow-y-auto overscroll-contain border-l border-foreground/10 pl-3">'+singers.map(function(item){return singerItemHtml(item,'flex min-h-9 items-center rounded-lg px-3 py-2 text-xs text-foreground/80 transition hover:bg-foreground/5');}).join('')+'</ul>');
    });
  }


  // ===== Actresses enhancement =====
  var ACT_MARK='data-tkc-actresses-enhanced';
  var actresses=[["Book Adah Sharma","/book-adah-sharma/"],["Book Aditi Rao Hydari","/book-aditi-rao-hydari/"],["Book Akanksha Puri","/book-akanksha-puri/"],["Book Alia Bhatt","/book-alia-bhatt/"],["Book Ananya Panday","/book-ananya-panday/"],["Book Aneet Padda","/book-aneet-padda/"],["Book Anjali Arora","/book-anjali-arora/"],["Book Anushka Sharma","/book-anushka-sharma/"],["Book Chitrangada Singh","/book-chitrangada-singh/"],["Book Deepika Padukone","/book-deepika-padukone/"],["Book Dia Mirza","/book-dia-mirza/"],["Book Disha Patani","/book-disha-patani/"],["Book Esha Gupta","/book-esha-gupta/"],["Book Fatima Sana Shaikh","/book-fatima-sana-shaikh/"],["Book Huma Qureshi","/book-huma-qureshi/"],["Book Jacqueline Fernandez","/book-jacqueline-fernandez/"],["Book Janhvi Kapoor","/book-janhvi-kapoor/"],["Book Jennifer Winget","/book-jennifer-winget/"],["Book Kajol","/book-kajol/"],["Book Kangana Ranaut","/book-kangana-ranaut/"],["Book Kareena Kapoor Khan","/book-kareena-kapoor/"],["Book Karishma Tanna","/book-karishma-tanna/"],["Book Katrina Kaif","/book-katrina-kaif/"],["Book Kiara Advani","/book-kiara-advani/"],["Book Konkona Sen Sharma","/book-konkona-sen-sharma/"],["Book Kriti Sanon","/book-kriti-sanon/"],["Book Lara Dutta","/book-lara-dutta/"],["Book Mandira Bedi","/book-mandira-bedi/"],["Book Mrunal Thakur","/book-mrunal-thakur/"],["Book Nikita Dutta","/book-nikita-dutta/"],["Book Nimrat Kaur","/book-nimrat-kaur/"],["Book Nora Fatehi","/book-nora-fatehi/"],["Book Nushrratt Bharuccha","/book-nushrratt-bharuccha/"],["Book Palak Tiwari","/book-palak-tiwari/"],["Book Pooja Hegde","/book-pooja-hegde/"],["Book Priyanka Chopra","/book-priyanka-chopra/"],["Book Rakul Preet","/book-rakul-preet/"],["Book Rani Mukerji","/book-rani-mukerji/"],["Book Rashmika Mandanna","/book-rashmika-mandanna/"],["Book Rhea Chakraborty","/book-rhea-chakraborty/"],["Book Sanya Malhotra","/book-sanya-malhotra/"],["Book Sara Ali Khan","/book-sara-ali-khan/"],["Book Saumya Tandon","/book-saumya-tandon/"],["Book Shanaya Kapoor","/book-shanaya-kapoor/"],["Book Sharvari Wagh","/book-sharvari-wagh/"],["Book Shehnaaz Gill","/book-shehnaaz-gill/"],["Book Shilpa Shetty","/book-shilpa-shetty/"],["Book Shraddha Kapoor","/book-shraddha-kapoor/"],["Book Shruti Haasan","/book-shruti-haasan/"],["Book Shweta Tiwari","/book-shweta-tiwari/"],["Book Sonakshi Sinha","/book-sonakshi-sinha/"],["Book Sonam Bajwa","/book-sonam-bajwa/"],["Book Sreeleela","/book-sreeleela/"],["Book Sunny Leone","/book-sunny-leone/"],["Book Taapsee Pannu","/book-taapsee-pannu/"],["Book Tamannaah Bhatia","/book-tamannaah-bhatia/"],["Book Tara Sutaria","/book-tara-sutaria/"],["Book Urvashi Rautela","/book-urvashi-rautela/"],["Book Vaani Kapoor","/book-vaani-kapoor/"],["Book Vidya Balan","/book-vidya-balan/"],["Book Wamiqa Gabbi","/book-wamiqa-gabbi/"],["Book Yami Gautam","/book-yami-gautam/"]];
  var actressNameMap={"Adah Sharma":"/book-adah-sharma/","Aditi Rao Hydari":"/book-aditi-rao-hydari/","Akanksha Puri":"/book-akanksha-puri/","Alia Bhatt":"/book-alia-bhatt/","Ananya Panday":"/book-ananya-panday/","Aneet Padda":"/book-aneet-padda/","Anjali Arora":"/book-anjali-arora/","Anushka Sharma":"/book-anushka-sharma/","Chitrangada Singh":"/book-chitrangada-singh/","Deepika Padukone":"/book-deepika-padukone/","Dia Mirza":"/book-dia-mirza/","Disha Patani":"/book-disha-patani/","Esha Gupta":"/book-esha-gupta/","Fatima Sana Shaikh":"/book-fatima-sana-shaikh/","Huma Qureshi":"/book-huma-qureshi/","Jacqueline Fernandez":"/book-jacqueline-fernandez/","Janhvi Kapoor":"/book-janhvi-kapoor/","Jennifer Winget":"/book-jennifer-winget/","Kajol":"/book-kajol/","Kangana Ranaut":"/book-kangana-ranaut/","Kareena Kapoor Khan":"/book-kareena-kapoor/","Karishma Tanna":"/book-karishma-tanna/","Katrina Kaif":"/book-katrina-kaif/","Kiara Advani":"/book-kiara-advani/","Konkona Sen Sharma":"/book-konkona-sen-sharma/","Kriti Sanon":"/book-kriti-sanon/","Lara Dutta":"/book-lara-dutta/","Mandira Bedi":"/book-mandira-bedi/","Mrunal Thakur":"/book-mrunal-thakur/","Nikita Dutta":"/book-nikita-dutta/","Nimrat Kaur":"/book-nimrat-kaur/","Nora Fatehi":"/book-nora-fatehi/","Nushrratt Bharuccha":"/book-nushrratt-bharuccha/","Palak Tiwari":"/book-palak-tiwari/","Pooja Hegde":"/book-pooja-hegde/","Priyanka Chopra":"/book-priyanka-chopra/","Rakul Preet":"/book-rakul-preet/","Rani Mukerji":"/book-rani-mukerji/","Rashmika Mandanna":"/book-rashmika-mandanna/","Rhea Chakraborty":"/book-rhea-chakraborty/","Sanya Malhotra":"/book-sanya-malhotra/","Sara Ali Khan":"/book-sara-ali-khan/","Saumya Tandon":"/book-saumya-tandon/","Shanaya Kapoor":"/book-shanaya-kapoor/","Sharvari Wagh":"/book-sharvari-wagh/","Shehnaaz Gill":"/book-shehnaaz-gill/","Shilpa Shetty":"/book-shilpa-shetty/","Shraddha Kapoor":"/book-shraddha-kapoor/","Shruti Haasan":"/book-shruti-haasan/","Shweta Tiwari":"/book-shweta-tiwari/","Sonakshi Sinha":"/book-sonakshi-sinha/","Sonam Bajwa":"/book-sonam-bajwa/","Sreeleela":"/book-sreeleela/","Sunny Leone":"/book-sunny-leone/","Taapsee Pannu":"/book-taapsee-pannu/","Tamannaah Bhatia":"/book-tamannaah-bhatia/","Tara Sutaria":"/book-tara-sutaria/","Urvashi Rautela":"/book-urvashi-rautela/","Vaani Kapoor":"/book-vaani-kapoor/","Vidya Balan":"/book-vidya-balan/","Wamiqa Gabbi":"/book-wamiqa-gabbi/","Yami Gautam":"/book-yami-gautam/"};

  function actressItemHtml(item, cls){
    return '<li><a href="'+item[1]+'" class="'+cls+'">'+item[0]+'</a></li>';
  }

  function ensureActressSubmenus(){
    navLinks().forEach(function(a){
      if(!samePath(a,'/bollywood-actress-booking/') && !textHas(a,['actress'])) return;
      if(a.closest('#mobile-nav-drawer')) return;
      var li=a.parentElement;
      if(!li || li.tagName!=='LI') return;
      if(li.querySelector('ul a[href="/book-alia-bhatt/"]')) return;
      li.classList.add('relative','group/sub');
      a.classList.remove('block');
      a.classList.add('flex','items-center','justify-between','gap-2','group-hover/sub:bg-foreground','group-hover/sub:text-background');
      if(!a.querySelector('svg')) a.insertAdjacentHTML('beforeend',chevronRight());
      a.insertAdjacentHTML('afterend','<ul style="max-height:calc(100vh - 120px)" class="invisible absolute left-full top-0 z-50 ml-0 pl-3 -ml-2 min-w-60 overflow-y-auto overscroll-contain rounded-xl border border-foreground/10 bg-background p-2 text-foreground opacity-0 shadow-2xl ring-1 ring-foreground/5 transition-all duration-150 group-hover/sub:visible group-hover/sub:opacity-100 group-focus-within/sub:visible group-focus-within/sub:opacity-100">'+actresses.map(function(item){return actressItemHtml(item,'block rounded-md px-3 py-2 text-sm font-medium text-foreground/80 transition-colors hover:bg-foreground hover:text-background');}).join('')+'</ul>');
    });

    var drawer=document.getElementById('mobile-nav-drawer');
    if(!drawer) return;
    Array.prototype.slice.call(drawer.querySelectorAll('a')).forEach(function(a){
      if(!samePath(a,'/bollywood-actress-booking/') && !textHas(a,['actress'])) return;
      var li=a.parentElement;
      if(!li || li.tagName!=='LI' || li.querySelector('ul a[href="/book-alia-bhatt/"]')) return;
      li.insertAdjacentHTML('beforeend','<ul class="ml-3 mt-1 flex max-h-64 flex-col gap-1 overflow-y-auto overscroll-contain border-l border-foreground/10 pl-3">'+actresses.map(function(item){return actressItemHtml(item,'flex min-h-9 items-center rounded-lg px-3 py-2 text-xs text-foreground/80 transition hover:bg-foreground/5');}).join('')+'</ul>');
    });
  }

  // ===== Actors enhancement (Bollywood Actor dropdown) =====
  var actors=[["Book Aamir Khan","/book-aamir-khan/"],["Book Aditya Roy Kapur","/book-aditya-roy-kapur/"],["Book Ajay Devgn","/book-ajay-devgn/"],["Book Akshay Kumar","/book-akshay-kumar/"],["Book Anil Kapoor","/book-anil-kapoor/"],["Book Arjun Kapoor","/book-arjun-kapoor/"],["Book Ayushmann Khurrana","/book-ayushmann-khurrana/"],["Book Bobby Deol","/book-bobby-deol/"],["Book Hrithik Roshan","/book-hrithik-roshan/"],["Book Kartik Aaryan","/book-kartik-aaryan/"],["Book Manoj Bajpayee","/book-manoj-bajpayee/"],["Book Nawazuddin Siddiqui","/book-nawazuddin-siddiqui/"],["Book Pankaj Tripathi","/book-pankaj-tripathi/"],["Book Rajkummar Rao","/book-rajkummar-rao/"],["Book Ranbir Kapoor","/book-ranbir-kapoor/"],["Book Ranveer Singh","/book-ranveer-singh/"],["Book Salman Khan","/book-salman-khan/"],["Book Shah Rukh Khan","/book-shah-rukh-khan/"],["Book Shahid Kapoor","/book-shahid-kapoor/"],["Book Sidharth Malhotra","/book-sidharth-malhotra/"],["Book Sunny Deol","/book-sunny-deol/"],["Book Tiger Shroff","/book-tiger-shroff/"],["Book Varun Dhawan","/book-varun-dhawan/"],["Book Vicky Kaushal","/book-vicky-kaushal/"],["Book Vijay Varma","/book-vijay-varma/"]];

  function actorItemHtml(item, cls){
    return '<li><a href="'+item[1]+'" class="'+cls+'">'+item[0]+'</a></li>';
  }

  function ensureActorSubmenus(){
    navLinks().forEach(function(a){
      var txt=(a.textContent||'').toLowerCase();
      // Match "Actor" / "Bollywood Actor" labels but NOT "Actress".
      if(!samePath(a,'/bollywood-celebrity-booking/') && txt.indexOf('actor')===-1 && txt.indexOf('bollywood')===-1) return;
      if(txt.indexOf('actress')!==-1) return;
      if(a.closest('#mobile-nav-drawer')) return;
      var li=a.parentElement;
      if(!li || li.tagName!=='LI') return;
      if(li.querySelector('ul a[href="/book-salman-khan/"]')) return;
      li.classList.add('relative','group/sub');
      a.classList.remove('block');
      a.classList.add('flex','items-center','justify-between','gap-2','group-hover/sub:bg-foreground','group-hover/sub:text-background');
      if(!a.querySelector('svg')) a.insertAdjacentHTML('beforeend',chevronRight());
      a.insertAdjacentHTML('afterend','<ul style="max-height:calc(100vh - 120px)" class="invisible absolute left-full top-0 z-50 ml-0 pl-3 -ml-2 min-w-60 overflow-y-auto overscroll-contain rounded-xl border border-foreground/10 bg-background p-2 text-foreground opacity-0 shadow-2xl ring-1 ring-foreground/5 transition-all duration-150 group-hover/sub:visible group-hover/sub:opacity-100 group-focus-within/sub:visible group-focus-within/sub:opacity-100">'+actors.map(function(item){return actorItemHtml(item,'block rounded-md px-3 py-2 text-sm font-medium text-foreground/80 transition-colors hover:bg-foreground hover:text-background');}).join('')+'</ul>');
    });

    var drawer=document.getElementById('mobile-nav-drawer');
    if(!drawer) return;
    Array.prototype.slice.call(drawer.querySelectorAll('a')).forEach(function(a){
      var txt=(a.textContent||'').toLowerCase();
      if(!samePath(a,'/bollywood-celebrity-booking/') && txt.indexOf('actor')===-1 && txt.indexOf('bollywood')===-1) return;
      if(txt.indexOf('actress')!==-1) return;
      var li=a.parentElement;
      if(!li || li.tagName!=='LI' || li.querySelector('ul a[href="/book-salman-khan/"]')) return;
      li.insertAdjacentHTML('beforeend','<ul class="ml-3 mt-1 flex max-h-64 flex-col gap-1 overflow-y-auto overscroll-contain border-l border-foreground/10 pl-3">'+actors.map(function(item){return actorItemHtml(item,'flex min-h-9 items-center rounded-lg px-3 py-2 text-xs text-foreground/80 transition hover:bg-foreground/5');}).join('')+'</ul>');
    });
  }

  function linkActressCards(){
    if(location.pathname.replace(/\/$/,'')!=='/bollywood-actress-booking') return;
    document.querySelectorAll('h3').forEach(function(h){
      var name=(h.textContent||'').trim();
      var href=actressNameMap[name];
      if(!href) return;
      var card=h.closest('li, article, div');
      if(!card) return;
      // Find the outer card container (first ancestor that looks like a card)
      var outer=card;
      while(outer && outer.parentElement && !(outer.className||'').toString().match(/rounded-2xl|rounded-xl/)){
        outer=outer.parentElement;
        if(outer===document.body) return;
      }
      // Guard on the element we actually append to — checking only the inner
      // card caused an infinite append loop via the MutationObserver.
      if(!outer || outer.querySelector('a[data-tkc-card-link]')) return;
      var a=document.createElement('a');
      a.href=href; a.setAttribute('data-tkc-card-link','1');
      a.setAttribute('aria-label','Book '+name);
      a.className='absolute inset-0 z-10';
      a.style.cssText='position:absolute;inset:0;z-index:10;';
      var pos=getComputedStyle(outer).position;
      if(pos==='static') outer.style.position='relative';
      outer.appendChild(a);
    });
  }

  // Some static exports accidentally persisted a dynamically injected actress
  // submenu as a direct child of <nav>. It has no owning <li>, can become
  // visible on mobile, and appears as a black block over the header.
  function removeOrphanNavMenus(){
    document.querySelectorAll('nav > ul').forEach(function(ul){
      // The legitimate desktop navigation is also a direct child of <nav> and
      // contains deeply nested artist links. Only remove a direct artist list;
      // never remove the primary menu that contains top-level site sections.
      var directArtistLinks=ul.querySelectorAll(':scope > li > a[href^="/book-"]');
      var hasPrimaryLinks=ul.querySelector(':scope > li > a[href="/"], :scope > li > a[href="/celebrity-booking-india/"]');
      if(directArtistLinks.length>=15 && !hasPrimaryLinks) ul.remove();
    });
  }

  function bgOf(el){
    var n=el;
    while(n && n!==document.body){
      var c=getComputedStyle(n).backgroundColor;
      if(c && c!=='rgba(0, 0, 0, 0)' && c!=='transparent') return c;
      n=n.parentElement;
    }
    return '#ffffff';
  }

  function enhance(ul){
    if(ul.hasAttribute(MARK)) return;
    var links=ul.querySelectorAll(':scope > li > a[href*="/book-"]');
    if(links.length<15) return;
    ul.setAttribute(MARK,'1');

    var cls=ul.className||'';
    var isMobile=cls.indexOf('max-h-64')!==-1;
    if(isMobile){
      ul.classList.remove('max-h-64');
      ul.style.maxHeight='65vh';
      ul.style.paddingBottom='env(safe-area-inset-bottom)';
    } else {
      ul.style.maxHeight='75vh';
      ul.style.overflowY='auto';
      ul.style.overscrollBehavior='contain';
    }

    var bg=bgOf(ul);
    var wrap=document.createElement('li');
    wrap.style.cssText='position:sticky;top:0;z-index:5;list-style:none;margin:0 0 6px;padding:'+(isMobile?'6px 4px':'4px')+';background:'+bg+';';
    var input=document.createElement('input');
    input.type='search';
    input.placeholder='Search singers…';
    input.setAttribute('aria-label','Search singers');
    input.style.cssText='width:100%;padding:9px 12px;border-radius:9px;border:1px solid rgba(120,120,120,.25);background:rgba(120,120,120,.08);font-size:14px;outline:none;color:inherit;font-family:inherit;-webkit-appearance:none;';
    wrap.appendChild(input);

    ['click','mousedown','touchstart','keydown','keyup','keypress','input','focus'].forEach(function(ev){
      input.addEventListener(ev,function(e){e.stopPropagation();},true);
    });
    input.addEventListener('focus',function(){
      input.style.borderColor='rgba(201,168,76,.7)';
      input.style.background='rgba(255,255,255,.06)';
    });
    input.addEventListener('blur',function(){
      input.style.borderColor='rgba(120,120,120,.25)';
      input.style.background='rgba(120,120,120,.08)';
    });
    input.addEventListener('input',function(){
      var q=input.value.trim().toLowerCase();
      var any=false;
      ul.querySelectorAll(':scope > li').forEach(function(li){
        if(li===wrap) return;
        if(!q){ li.style.display=''; any=true; return; }
        var ok=li.textContent.toLowerCase().indexOf(q)!==-1;
        li.style.display=ok?'':'none';
        if(ok) any=true;
      });
      empty.style.display=any?'none':'block';
    });

    var empty=document.createElement('li');
    empty.textContent='No singers match';
    empty.style.cssText='display:none;padding:10px 12px;font-size:13px;opacity:.6;list-style:none;';
    ul.insertBefore(wrap, ul.firstChild);
    ul.appendChild(empty);
  }

  // ===== Home submenu (IITEO under Home) =====
  function ensureHomeSubmenu(){
    navLinks().forEach(function(a){
      var txt=(a.textContent||'').trim();
      if(txt!=='Home') return;
      var li=a.parentElement;
      if(!li || li.tagName!=='LI') return;
      var inDrawer=!!a.closest('#mobile-nav-drawer');
      if(li.querySelector(':scope > ul a[href="/iiteo/"]')) return;
      if(inDrawer){
        li.insertAdjacentHTML('beforeend','<ul class="ml-3 mt-1 flex flex-col gap-1 border-l border-foreground/10 pl-3"><li><a href="/iiteo/" class="flex min-h-9 items-center rounded-lg px-3 py-2 text-xs text-foreground/80 transition hover:bg-foreground/5">IITEO Legacy</a></li></ul>');
      } else {
        li.classList.add('relative','group/sub');
        a.classList.remove('block');
        a.classList.add('flex','items-center','justify-between','gap-2','group-hover/sub:bg-foreground','group-hover/sub:text-background');
        if(!a.querySelector('svg')) a.insertAdjacentHTML('beforeend',chevronRight());
        a.insertAdjacentHTML('afterend','<ul data-tkc-home-sub="1" class="invisible absolute left-full top-0 z-50 ml-1 min-w-56 rounded-xl border border-foreground/10 bg-background p-2 text-foreground opacity-0 shadow-2xl ring-1 ring-foreground/5 transition-all duration-150 group-hover/sub:visible group-hover/sub:opacity-100 group-focus-within/sub:visible group-focus-within/sub:opacity-100"><li><a href="/iiteo/" class="block rounded-md px-3 py-2 text-sm font-medium text-foreground/80 transition-colors hover:bg-foreground hover:text-background">IITEO Legacy</a></li></ul>');
      }
    });
  }

  // ===== Global page search (floating) =====
  var SEARCH_INDEX=null;
  function buildSearchIndex(){
    if(SEARCH_INDEX) return SEARCH_INDEX;
    var sections=[
      ['Home','/'],
      ['IITEO Legacy','/iiteo/'],
      ['Our Services','/ourservice/'],
      ['Celebrity Booking India','/celebrity-booking-india/'],
      ['Pan India Celebrity Booking','/pan-india-celebrity-booking/'],
      ['Bollywood Celebrity Booking','/bollywood-celebrity-booking/'],
      ['Bollywood Actress Booking','/bollywood-actress-booking/'],
      ['Singer Booking India','/singer-booking-india/'],
      ['Comedian Booking India','/comedian-booking-india/'],
      ['Celebrity DJ Booking','/celebrity-dj-booking/'],
      ['Influencer Booking India','/influencer-booking-india/'],
      ['Billing Support','/support/billing/']
    ];
    var extras=[
      ['Book Aakash Gupta','/book-aakash-gupta/'],['Book Abish Mathew','/book-abish-mathew/'],['Book Anubhav Singh Bassi','/book-anubhav-singh-bassi/'],['Book Biswa Kalyan Rath','/book-biswa-kalyan-rath/'],['Book Bharti Singh','/book-bharti-singh/'],['Book Gaurav Kapoor','/book-gaurav-kapoor/'],['Book Kanan Gill','/book-kanan-gill/'],['Book Kapil Sharma','/book-kapil-sharma/'],['Book Kenny Sebastian','/book-kenny-sebastian/'],['Book Krushna Abhishek','/book-krushna-abhishek/'],['Book Munawar Faruqui','/book-munawar-faruqui/'],['Book Nishant Tanwar','/book-nishant-tanwar/'],['Book Rahul Subramanian','/book-rahul-subramanian/'],['Book Samay Raina','/book-samay-raina/'],['Book Zakir Khan','/book-zakir-khan/']
    ];
    SEARCH_INDEX=sections.concat(singers).concat(actresses).concat(actors).concat(extras);
    // de-dup by url
    var seen={}, out=[];
    SEARCH_INDEX.forEach(function(it){ if(seen[it[1]]) return; seen[it[1]]=1; out.push(it); });
    SEARCH_INDEX=out;
    return SEARCH_INDEX;
  }

  function ensureGlobalSearch(){
    if(document.getElementById('tkc-global-search')) return;
    var wrap=document.createElement('div');
    wrap.id='tkc-global-search';
    wrap.style.cssText='position:fixed;left:50%;bottom:18px;transform:translateX(-50%);z-index:9998;width:min(420px,calc(100vw - 96px));font-family:Inter,system-ui,sans-serif;';
    wrap.innerHTML=''
      +'<div style="position:relative;">'
      +'  <input id="tkc-gs-input" type="search" placeholder="Search any page…" aria-label="Search the site" autocomplete="off" '
      +'    style="width:100%;height:46px;padding:0 44px 0 18px;border-radius:999px;border:1px solid rgba(255,255,255,.18);'
      +'    background:rgba(15,15,15,.85);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);color:#fff;'
      +'    font:500 14px/1 Inter,system-ui,sans-serif;outline:none;box-shadow:0 14px 36px rgba(0,0,0,.4);" />'
      +'  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
      +'    style="position:absolute;right:16px;top:14px;color:rgba(255,255,255,.6);pointer-events:none;"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>'
      +'  <ul id="tkc-gs-results" role="listbox" '
      +'    style="display:none;list-style:none;margin:8px 0 0;padding:6px;max-height:50vh;overflow-y:auto;overscroll-behavior:contain;'
      +'    border-radius:14px;border:1px solid rgba(255,255,255,.12);background:rgba(15,15,15,.95);backdrop-filter:blur(10px);'
      +'    -webkit-backdrop-filter:blur(10px);box-shadow:0 18px 40px rgba(0,0,0,.45);"></ul>'
      +'</div>';
    document.body.appendChild(wrap);

    var input=wrap.querySelector('#tkc-gs-input');
    var list=wrap.querySelector('#tkc-gs-results');

    function render(items, q){
      if(!items.length){
        list.innerHTML='<li style="padding:10px 14px;font-size:13px;color:rgba(255,255,255,.6);">No pages match</li>';
        list.style.display='block';
        return;
      }
      list.innerHTML=items.slice(0,40).map(function(it){
        return '<li><a href="'+it[1]+'" style="display:block;padding:9px 14px;border-radius:10px;color:#f5f1e8;text-decoration:none;font-size:13px;line-height:1.3;">'+it[0]+'<span style="display:block;font-size:11px;color:rgba(255,255,255,.45);margin-top:2px;">'+it[1]+'</span></a></li>';
      }).join('');
      list.style.display='block';
    }

    input.addEventListener('input',function(){
      var q=input.value.trim().toLowerCase();
      if(!q){ list.style.display='none'; list.innerHTML=''; return; }
      var idx=buildSearchIndex();
      var matches=idx.filter(function(it){ return it[0].toLowerCase().indexOf(q)!==-1 || it[1].toLowerCase().indexOf(q)!==-1; });
      render(matches,q);
    });
    input.addEventListener('focus',buildSearchIndex);
    list.addEventListener('mouseover',function(e){
      var a=e.target.closest('a'); if(!a) return; a.style.background='rgba(255,255,255,.08)';
    });
    list.addEventListener('mouseout',function(e){
      var a=e.target.closest('a'); if(!a) return; a.style.background='';
    });
    document.addEventListener('click',function(e){
      if(!wrap.contains(e.target)){ list.style.display='none'; }
    });
    input.addEventListener('keydown',function(e){
      if(e.key==='Escape'){ input.value=''; list.style.display='none'; input.blur(); }
    });
  }

  function scan(){
    removeOrphanNavMenus();
    ensureHomeSubmenu();
    ensureCelebrityBookingMenu();
    ensureSingerSubmenus();
    ensureActressSubmenus();
    ensureActorSubmenus();
    linkActressCards();
    fixAllSubmenus();
    sweepImages();
    ensureGlobalSearch();

  }

  // Debounce + re-entrancy guard so our own DOM writes never re-trigger an
  // immediate synchronous re-scan (previously caused an infinite loop).
  var scanScheduled=false, scanning=false;
  function safeScan(){
    if(scanning) return;
    scanning=true;
    try{ scan(); } finally { scanning=false; }
  }
  var mo=new MutationObserver(function(){
    if(scanScheduled||scanning) return;
    scanScheduled=true;
    requestAnimationFrame(function(){
      scanScheduled=false;
      safeScan();
    });
  });
  function start(){
    mo.observe(document.body,{childList:true,subtree:true});
    safeScan();
  }
  if(document.readyState==='loading'){
    document.addEventListener('DOMContentLoaded',start);
  } else { start(); }
})();
