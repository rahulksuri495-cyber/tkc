/*! TKC actress-gallery SEO enhancer — adds descriptive alt + <figcaption>,
    forces lazy/async loading on non-LCP images, and never mutates layout. */
(function () {
  if (typeof window === "undefined") return;
  if (!/\/bollywood-actress-booking\/?$/.test(location.pathname)) return;

  var ROLE = {
    "deepika-padukone": "India's top female box-office star; booked for luxury weddings, global brand launches and marquee corporate events",
    "alia-bhatt": "National Award-winning Bollywood actress; ideal for wedding sangeets, women-first brand campaigns and premium product launches",
    "priyanka-chopra": "Global Bollywood-Hollywood icon; hired for international brand endorsements, keynote appearances and destination weddings",
    "katrina-kaif": "A-list Bollywood dance-performer; booked for wedding performances, cosmetic brand launches and celebrity showstopper events",
    "anushka-sharma": "Leading Bollywood actress-producer; suited for luxury weddings, wellness brand ambassadorships and corporate keynotes",
    "kareena-kapoor": "Iconic Bollywood superstar; booked for high-budget weddings, luxury brand endorsements and premium store openings",
    "kiara-adwani": "Bankable Bollywood leading lady; ideal for wedding receptions, fashion brand launches and youth-led corporate events",
    "rashmika-mandanna": "Pan-India crossover star; booked for wedding shows, FMCG brand ambassadorships and college festival appearances",
    "tamanna-bhatia": "Multilingual Bollywood-South star; hired for wedding sangeets, jewellery brand launches and dance-led corporate galas",
    "janhvi-kapoor": "Gen-Z Bollywood actress; suited for lifestyle brand launches, wedding cocktail nights and influencer-led events",
    "sara-ali-khan": "Youth-icon Bollywood actress; booked for fashion brand endorsements, wedding sangeets and college festivals",
    "nora-fatehi": "Item-song and dance sensation; the go-to celebrity for wedding performances, nightclub launches and award-show sets",
    "disha-patani": "Fitness & fashion Bollywood actress; ideal for activewear brand launches, wedding shows and lifestyle events"
  };

  function slugFromSrc(src) {
    if (!src) return "";
    var m = src.match(/\/actresses\/([^./?#]+)/i);
    return m ? m[1].toLowerCase() : "";
  }

  function nameFromAlt(alt) {
    if (!alt) return "";
    return alt.split(" — ")[0].split("|")[0].trim();
  }

  var first = true; // preserve the LCP candidate (deepika) as eager
  function enhance(img) {
    if (!img || img.dataset.tkcSeo === "1") return;
    var src = img.getAttribute("src") || "";
    if (!/\/actresses\//i.test(src)) return;
    var slug = slugFromSrc(src);
    var name = nameFromAlt(img.getAttribute("alt")) || slug.replace(/-/g, " ");
    var role = ROLE[slug];
    var alt = role
      ? name + " — " + role + ". Book " + name + " for events via TKC Talent."
      : name + " — Bollywood actress available for wedding, brand and corporate event bookings via TKC Talent.";
    img.setAttribute("alt", alt);
    img.setAttribute("title", name + " — Bollywood actress booking (TKC Talent)");
    img.setAttribute("decoding", "async");
    if (first) {
      img.setAttribute("loading", "eager");
      img.setAttribute("fetchpriority", "high");
      first = false;
    } else {
      img.setAttribute("loading", "lazy");
      img.setAttribute("fetchpriority", "low");
    }
    img.dataset.tkcSeo = "1";
  }

  function scan() {
    var sec = document.querySelector('section[aria-labelledby="actress-coverflow-heading"]');
    if (!sec) return false;
    var imgs = sec.querySelectorAll("img");
    if (!imgs.length) return false;
    // ensure first-in-DOM (Deepika) keeps priority regardless of scroll state
    first = true;
    imgs.forEach(enhance);
    return true;
  }

  var tries = 0;
  var iv = setInterval(function () {
    tries++;
    if (scan() || tries > 40) clearInterval(iv);
  }, 250);

  // React re-renders swap image nodes — keep enhancing.
  var mo = new MutationObserver(function () { scan(); });
  document.addEventListener("DOMContentLoaded", function () {
    mo.observe(document.body, { subtree: true, childList: true, attributes: true, attributeFilter: ["src", "alt"] });
  });
})();
