(function(){
  var MARK='data-tkc-singers-enhanced';
  var singers=[
    ['Book Altaf Raja','/book-altaf-raja/'],['Book A.R. Rahman','/book-ar-rahman/'],['Book Arijit Singh','/book-arijit-singh/'],['Book Armaan Malik','/book-armaan-malik/'],['Book Asees Kaur','/book-asees-kaur/'],['Book B Praak','/book-b-praak/'],['Book Badshah','/book-badshah/'],['Book Darshan Raval','/book-darshan-raval/'],['Book Diljit Dosanjh','/book-diljit-dosanjh/'],['Book Guru Randhawa','/book-guru-randhawa/'],['Book Hanumankind','/book-hanumankind/'],['Book Jasmine Sandlas','/book-jasmine-sandlas/'],['Book Jonita Gandhi','/book-jonita-gandhi/'],['Book Jubin Nautiyal','/book-jubin-nautiyal/'],['Book Kanika Kapoor','/book-kanika-kapoor/'],['Book Kumar Sanu','/book-kumar-sanu/'],['Book Lucky Ali','/book-lucky-ali/'],['Book Meet Bros','/book-meet-bros/'],['Book Mohit Chauhan','/book-mohit-chauhan/'],['Book Neha Bhasin','/book-neha-bhasin/'],['Book Neha Kakkar','/book-neha-kakkar/'],['Book Palak Muchhal','/book-palak-muchhal/'],['Book Pritam','/book-pritam/'],['Book Sachet-Parampara','/book-sachet-parampara/'],['Book Sachin-Jigar','/book-sachin-jigar/'],['Book Salim-Sulaiman','/book-salim-sulaiman/'],['Book Sara Gurpal','/book-sara-gurpal/'],['Book Shamsher Lehri','/book-shamsher-lehri/'],['Book Shankar Mahadevan','/book-shankar-mahadevan/'],['Book Shreya Ghoshal','/book-shreya-ghoshal/'],['Book Sonu Nigam','/book-sonu-nigam/'],['Book Sunanda Sharma','/book-sunanda-sharma/'],['Book Sunidhi Chauhan','/book-sunidhi-chauhan/'],['Book Tanishk Bagchi','/book-tanishk-bagchi/'],['Book Vishal-Shekhar','/book-vishal-shekhar/']
  ];

  function singerItemHtml(item, cls){
    return '<li><a href="'+item[1]+'" class="'+cls+'">'+item[0]+'</a></li>';
  }

  function chevronRight(){
    return '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-chevron-down h-3.5 w-3.5 -rotate-90" aria-hidden="true"><path d="m6 9 6 6 6-6"></path></svg>';
  }

  function ensureSingerSubmenus(){
    document.querySelectorAll('nav a[href="/singer-booking-india/"]').forEach(function(a){
      if((a.textContent||'').indexOf('Singers')===-1) return;
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

  function scan(){
    ensureSingerSubmenus();
    document.querySelectorAll('ul').forEach(function(ul){
      if(ul.hasAttribute(MARK)) return;
      if(ul.children.length<15) return;
      if(!ul.querySelector('a[href*="/book-"]')) return;
      // confirm this is the singers list (has at least one well-known singer slug)
      if(!ul.querySelector('a[href*="/book-arijit-singh"], a[href*="/book-badshah"], a[href*="/book-shreya-ghoshal"]')) return;
      enhance(ul);
    });
  }

  var mo=new MutationObserver(function(){ scan(); });
  function start(){
    mo.observe(document.body,{childList:true,subtree:true});
    scan();
  }
  if(document.readyState==='loading'){
    document.addEventListener('DOMContentLoaded',start);
  } else { start(); }
})();
