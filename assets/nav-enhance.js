(function(){
  var MARK='data-tkc-singers-enhanced';

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
