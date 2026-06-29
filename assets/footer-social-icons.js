/* TKC Footer social icons enhancer v1
 * Replaces the footer "Follow" link list with brand-colored SVG icon tiles.
 * Idempotent: safe to run multiple times.
 */
(function () {
  if (window.__tkcFooterSocialV1) return;
  window.__tkcFooterSocialV1 = true;

  var ICONS = {
    facebook: {
      bg: '#1877F2', label: 'Facebook',
      svg: '<svg viewBox="0 0 24 24" width="20" height="20" fill="#fff" aria-hidden="true"><path d="M13.5 21v-7.5h2.6l.4-3h-3V8.6c0-.9.3-1.5 1.6-1.5H17V4.4c-.3 0-1.3-.1-2.4-.1-2.4 0-4.1 1.5-4.1 4.1v2.1H8v3h2.5V21h3z"/></svg>'
    },
    twitter: {
      bg: '#000000', label: 'X',
      svg: '<svg viewBox="0 0 24 24" width="18" height="18" fill="#fff" aria-hidden="true"><path d="M17.5 3h3l-6.6 7.5L22 21h-6.2l-4.9-6.4L5.3 21H2.3l7-8L1.7 3H8l4.4 5.8L17.5 3zm-1.1 16h1.7L7.7 5H5.9l10.5 14z"/></svg>'
    },
    youtube: {
      bg: '#FF0000', label: 'YouTube',
      svg: '<svg viewBox="0 0 24 24" width="22" height="22" fill="#fff" aria-hidden="true"><path d="M23.5 7.3a3 3 0 0 0-2.1-2.1C19.5 4.7 12 4.7 12 4.7s-7.5 0-9.4.5A3 3 0 0 0 .5 7.3 31 31 0 0 0 0 12a31 31 0 0 0 .5 4.7 3 3 0 0 0 2.1 2.1c1.9.5 9.4.5 9.4.5s7.5 0 9.4-.5a3 3 0 0 0 2.1-2.1A31 31 0 0 0 24 12a31 31 0 0 0-.5-4.7zM9.6 15.5v-7l6.3 3.5-6.3 3.5z"/></svg>'
    },
    instagram: {
      bg: 'radial-gradient(circle at 30% 110%,#fdf497 0%,#fdf497 5%,#fd5949 45%,#d6249f 60%,#285AEB 90%)',
      label: 'Instagram',
      svg: '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#fff" stroke-width="2" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="#fff" stroke="none"/></svg>'
    },
    pinterest: {
      bg: '#E60023', label: 'Pinterest',
      svg: '<svg viewBox="0 0 24 24" width="20" height="20" fill="#fff" aria-hidden="true"><path d="M12 2a10 10 0 0 0-3.6 19.3c-.1-.8-.2-2 0-2.9l1.3-5.5s-.3-.7-.3-1.7c0-1.6.9-2.8 2.1-2.8 1 0 1.5.7 1.5 1.6 0 1-.6 2.5-1 3.9-.3 1.2.6 2.1 1.7 2.1 2 0 3.6-2.1 3.6-5.2 0-2.7-2-4.6-4.7-4.6-3.2 0-5.1 2.4-5.1 4.9 0 1 .4 2 .9 2.6.1.1.1.2.1.3l-.3 1.3c-.1.2-.2.3-.4.2-1.5-.7-2.4-2.8-2.4-4.6 0-3.7 2.7-7.2 7.8-7.2 4.1 0 7.3 2.9 7.3 6.8 0 4.1-2.6 7.4-6.2 7.4-1.2 0-2.3-.6-2.7-1.4l-.7 2.8c-.3 1-1 2.3-1.4 3.1A10 10 0 1 0 12 2z"/></svg>'
    },
    linkedin: {
      bg: '#0A66C2', label: 'LinkedIn',
      svg: '<svg viewBox="0 0 24 24" width="20" height="20" fill="#fff" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9h4v12H3V9zm7 0h3.8v1.7h.1c.5-.9 1.8-1.9 3.7-1.9 4 0 4.7 2.6 4.7 6V21h-4v-5.6c0-1.3 0-3-1.9-3s-2.2 1.5-2.2 3V21h-4V9z"/></svg>'
    },
    imdb: {
      bg: '#F5C518', label: 'IMDb', color: '#000',
      svg: '<svg viewBox="0 0 32 16" width="28" height="14" fill="#000" aria-hidden="true"><path d="M2 1h2v14H2zM5.5 1h2.7l1.4 6.5L11 1h2.7v14h-2V5l-1.6 10H8.6L7 5.2V15H5.5zM15 1h3c1.7 0 2.9.5 3.3 1.5.2.6.3 1.6.3 3.2v4c0 1.8-.1 2.8-.4 3.4-.5 1.2-1.7 1.9-3.6 1.9H15V1zm2.3 2v10h.5c.8 0 1.2-.2 1.4-.6.1-.3.2-1.2.2-2.7V5.6c0-1.3-.1-2.1-.2-2.3-.2-.4-.6-.6-1.4-.6h-.5zM22.7 1H25v4.2c.4-.5 1.1-.8 1.9-.8 1.5 0 2.4.9 2.4 2.8v5.6c0 1.9-.9 2.8-2.4 2.8-.8 0-1.5-.3-2-.9V15h-2.2V1zm2.4 5.6v6c0 .5.2.7.6.7s.6-.2.6-.7v-6c0-.5-.2-.7-.6-.7s-.6.2-.6.7z"/></svg>'
    },
    medium: {
      bg: '#000000', label: 'Medium',
      svg: '<svg viewBox="0 0 24 24" width="22" height="22" fill="#fff" aria-hidden="true"><path d="M2.4 5.5c0-.2-.1-.4-.2-.5L.6 3v-.3H5l3.5 7.6L11.6 2.7h4.3V3l-1.3 1.2c-.1.1-.2.2-.2.4v9c0 .1.1.3.2.4l1.2 1.2v.2h-6.3v-.2l1.3-1.2c.1-.1.1-.2.1-.4V6.4l-3.6 9h-.5l-4.2-9v6c0 .2.1.5.2.7L4.7 15v.2H.1V15l1.8-2c.2-.2.2-.4.2-.7V5.5zM18 14.7l1.8-2c.1-.1.1-.4.1-.5V5.2c0-.2 0-.4-.1-.5L18 2.8v-.2h4.6L26 11l3-8.4H33v.2l-1.5 1.5c-.1.1-.2.3-.2.4v10c0 .2.1.3.2.4l1.4 1.4v.2H26v-.2l1.5-1.5c.1-.1.1-.3.1-.5V5.5l-4.1 9.6h-.4l-4.7-9.6v6.7c0 .3.1.6.2.8l1.9 2.4v.2H18v-.2z"/></svg>'
    },
    threads: {
      bg: '#000000', label: 'Threads',
      svg: '<svg viewBox="0 0 24 24" width="20" height="20" fill="#fff" aria-hidden="true"><path d="M12.2 22h-.1C8.4 22 5.6 20.8 4 18.4 2.5 16.3 1.8 13.4 1.8 10s.7-6.3 2.2-8.4C5.6.2 8.3-1 12 -1h.1c2.8 0 5.1.9 6.8 2.5 1.5 1.4 2.6 3.5 3.1 6L20 7.9c-.7-3.4-2.9-5.1-6.8-5.1H13c-2.5 0-4.4.8-5.6 2.4C6.3 6.6 5.7 8.7 5.7 12s.6 5.4 1.7 6.8c1.2 1.6 3.1 2.4 5.6 2.4h.1c2.3 0 3.8-.5 5.1-1.8 1.4-1.4 1.4-3.2.9-4.3-.3-.6-.8-1.2-1.6-1.6-.2 1.4-.6 2.5-1.3 3.3-.9 1.1-2.3 1.7-4 1.7-1.3 0-2.5-.3-3.4-1-1.1-.7-1.7-1.9-1.7-3.3 0-2.7 2.2-4.5 5.4-4.5.9 0 1.7.1 2.5.2 0-.6-.2-1.1-.5-1.5-.4-.5-1-.8-1.9-.8h0c-.7 0-1.7.2-2.3 1.2L9.5 8.5c.7-1 2-2.4 4.2-2.4.1 0 .3 0 .4.1 2 .1 3.6 1.3 4.2 3.2 2 .8 3.2 2 3.8 3.4.8 2 .2 4.7-1.7 6.6-1.7 1.7-3.7 2.5-6.6 2.5zm.7-9.5c-1.7 0-3.3.7-3.3 2.4 0 .5.2 2.2 3 2.2 2.7 0 3.1-1.8 3.2-3.4-.4-.1-.9-.2-1.5-.2-.5-.1-1-.1-1.4-.1z"/></svg>'
    },
    tumblr: {
      bg: '#36465D', label: 'Tumblr',
      svg: '<svg viewBox="0 0 24 24" width="20" height="20" fill="#fff" aria-hidden="true"><path d="M14 21c-3.6 0-6.2-1.8-6.2-6.2v-6H5.5V6.1c2.9-.8 4.2-3.2 4.4-5.1h2.7v4.7h4.2v3.1h-4.2v5.4c0 1.8.9 2.4 2.4 2.4h2v4.4h-3z"/></svg>'
    },
    quora: {
      bg: '#B92B27', label: 'Quora',
      svg: '<svg viewBox="0 0 24 24" width="20" height="20" fill="#fff" aria-hidden="true"><path d="M12.7 18.1c-.7-1.4-1.5-2.9-3.3-2.9-.4 0-.7.1-1.1.2l-.4-.8c.5-.5 1.7-1.4 3.5-1.4 2.9 0 4.4 1.4 5.6 3.2 .7-1.4 1-3.3 1-5.1 0-4.7-1.5-7.1-4.9-7.1S8.2 6.6 8.2 11.4c0 4.7 1.5 7.1 4.9 7.1 0-.1-.4-.1-.4-.4zM14.6 19.7c-.7.2-1.4.3-2.2.3-4.5 0-9-3.6-9-8.6S8 2.8 12.4 2.8s8.9 3.6 8.9 8.6c0 2.8-1.4 5.2-3.5 6.7.7 1 1.4 1.7 2.4 1.7 1.1 0 1.5-.8 1.6-1.5h1c.1.7-.1 4.1-4.2 4.1-2.5 0-3.6-1.4-4-2.7z"/></svg>'
    }
  };

  function detect(href, label) {
    var h = (href || '').toLowerCase();
    var l = (label || '').toLowerCase();
    if (h.indexOf('facebook.com') > -1) return 'facebook';
    if (h.indexOf('x.com') > -1 || h.indexOf('twitter.com') > -1 || l.indexOf('twitter') > -1) return 'twitter';
    if (h.indexOf('youtube.com') > -1 || h.indexOf('youtu.be') > -1) return 'youtube';
    if (h.indexOf('instagram.com') > -1) return 'instagram';
    if (h.indexOf('pinterest.') > -1) return 'pinterest';
    if (h.indexOf('linkedin.com') > -1) return 'linkedin';
    if (h.indexOf('imdb.com') > -1) return 'imdb';
    if (h.indexOf('medium.com') > -1) return 'medium';
    if (h.indexOf('threads.net') > -1) return 'threads';
    if (h.indexOf('tumblr.com') > -1) return 'tumblr';
    if (h.indexOf('quora.com') > -1) return 'quora';
    return null;
  }

  function injectStyles() {
    if (document.getElementById('tkc-footer-social-style')) return;
    var s = document.createElement('style');
    s.id = 'tkc-footer-social-style';
    s.textContent = [
      '.tkc-social-row{display:flex;flex-wrap:wrap;gap:10px;list-style:none;padding:0;margin:0}',
      '.tkc-social-row li{margin:0}',
      '.tkc-social-row a{display:inline-flex;align-items:center;justify-content:center;width:40px;height:40px;border-radius:10px;background:#222;color:#fff;text-decoration:none;transition:transform .18s ease,box-shadow .18s ease,filter .18s ease;box-shadow:0 1px 2px rgba(0,0,0,.25)}',
      '.tkc-social-row a:hover{transform:translateY(-2px) scale(1.06);box-shadow:0 6px 18px rgba(0,0,0,.25);filter:brightness(1.08)}',
      '.tkc-social-row a:focus-visible{outline:2px solid #fff;outline-offset:2px}',
      '.tkc-social-row svg{display:block}'
    ].join('');
    document.head.appendChild(s);
  }

  function enhance() {
    injectStyles();
    var footers = document.querySelectorAll('footer');
    footers.forEach(function (footer) {
      // Find the "Follow" list — heuristic: a UL whose links go to known social domains.
      var lists = footer.querySelectorAll('ul');
      lists.forEach(function (ul) {
        if (ul.dataset.tkcSocial === '1') return;
        var links = ul.querySelectorAll('a[href]');
        if (!links.length) return;
        var socialLinks = [];
        for (var i = 0; i < links.length; i++) {
          var key = detect(links[i].getAttribute('href'), links[i].textContent);
          if (key) socialLinks.push({ key: key, href: links[i].getAttribute('href'), label: links[i].textContent.trim() });
        }
        // Only convert if list is predominantly social
        if (socialLinks.length < 2 || socialLinks.length < links.length * 0.6) return;

        ul.className = 'tkc-social-row';
        ul.dataset.tkcSocial = '1';
        ul.innerHTML = socialLinks.map(function (s) {
          var ico = ICONS[s.key];
          var bgStyle = ico.bg.indexOf('gradient') > -1 ? 'background:' + ico.bg : 'background-color:' + ico.bg;
          return '<li><a href="' + s.href + '" target="_blank" rel="noopener" aria-label="' + ico.label + '" title="' + ico.label + '" style="' + bgStyle + '">' + ico.svg + '</a></li>';
        }).join('');
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', enhance);
  } else {
    enhance();
  }
  // Re-run after SPA-ish updates
  setTimeout(enhance, 800);
})();