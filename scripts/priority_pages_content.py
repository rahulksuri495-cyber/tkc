"""Unique content for the priority keyword pages. Facts are limited to data already
published on the site or supplied by the client (no invented prices)."""
from priority_pages_lib import sec, p, ul, ol, cards, table, e

REL_EVENTS = [
    ("Event management company (India)", "/event-management-company/"),
    ("Event management company in Delhi NCR", "/event-management-delhi/"),
    ("Event planners in Delhi", "/event-planners-delhi/"),
    ("Event management company in Gurgaon", "/event-management-gurgaon/"),
    ("Wedding planner in Delhi", "/wedding-planner-delhi/"),
    ("Corporate event management company", "/corporate-event-management/"),
    ("Event management company in Mumbai", "/event-management-mumbai/"),
    ("Book a celebrity for your wedding", "/book-celebrity-for-wedding/"),
    ("Celebrity booking in India", "/celebrity-booking-india/"),
    ("Best event management companies in India (guide)", "/blog/event-management-company-india/"),
    ("Durga Puja 2026 stalls & sponsorship", "/durga-puja-2026/"),
    ("Contact / get a quote", "/contact-us/"),
]


KEEP = {
    "/event-management-company/": ["/event-management-delhi/", "/corporate-event-management/", "/event-management-mumbai/", "/blog/event-management-company-india/", "/celebrity-booking-india/"],
    "/event-management-delhi/": ["/event-planners-delhi/", "/event-management-gurgaon/", "/wedding-planner-delhi/", "/event-management-company/", "/celebrity-booking-delhi/"],
    "/event-planners-delhi/": ["/event-management-delhi/", "/corporate-event-management/", "/wedding-planner-delhi/", "/contact-us/"],
    "/event-management-gurgaon/": ["/event-management-delhi/", "/celebrity-booking-gurgaon/", "/durga-puja-2026/", "/corporate-event-management/"],
    "/wedding-planner-delhi/": ["/book-celebrity-for-wedding/", "/event-management-delhi/", "/bollywood-celebrity-charges/", "/contact-us/"],
}
EXTRA = {"/celebrity-booking-delhi/": "Celebrity booking in Delhi", "/celebrity-booking-gurgaon/": "Celebrity booking in Gurgaon",
         "/bollywood-celebrity-charges/": "Bollywood celebrity charges 2026"}


def rel(page):
    names = {u: t for t, u in REL_EVENTS}
    names.update(EXTRA)
    return [(names[u], u) for u in KEEP[page]]


PAGES = {}

# ---------------------------------------------------------------- national hub
PAGES["event-management-company"] = dict(
    title="Event Management Company in India | TKC Talent (Since 2005)",
    desc="TKC Talent is an event management company in India since 2005: corporate events, concerts, brand launches, weddings and celebrity shows, run end-to-end by one in-house team.",
    h1="Event Management Company in India — Corporate Events, Concerts, Launches & Weddings",
    eyebrow="Event Management Company · India",
    crumb="Event Management Company",
    service_name="Event management services in India",
    service_type="Event management",
    area=["India", "Delhi NCR", "Mumbai", "Gurgaon", "Noida", "Jaipur", "Goa"],
    geo_region="IN", geo_place="India",
    llms="llms-event-management.txt",
    img="tkc-stage-view-large-audience",
    img_alt="Large audience in front of a main stage at an event produced by TKC Talent",
    answer=("<strong>TKC Talent (The Kabir Company)</strong> is an <strong>event management company</strong> headquartered in New Delhi and working across India since 2005. "
            "One in-house team plans and runs corporate events, concerts, brand launches, weddings and celebrity shows, covering venue, stage production, artist booking, permits, hospitality and the final account. "
            "Send a brief for an itemised quote."),
    facts=[("Founded", "2005, New Delhi"), ("Head office", "600, CR Park, New Delhi 110019"),
           ("Events delivered", "12,000+ across India"), ("Typical budgets", "from ₹3 lakh to ₹12 crore+"),
           ("Lead time", "14 days (rush) to 6+ months (peak season)"), ("Contact", '<a class="underline" href="/contact-us/">enquiry form</a> or hello@tkctalent.com')],
    sections=[
        sec("What does an event management company do?",
            p("An event management company takes responsibility for an event from the first brief to the final invoice. Instead of hiring a venue, a decorator, a sound company, an artist agent and a travel desk separately, you deal with one team that is accountable for the whole result.")
            + p("At TKC Talent that work runs in five stages:")
            + ol(["<strong>Brief and budget</strong> — audience, objective, date, city and spend.",
                  "<strong>Proposal</strong> — concept, venue shortlist, artist options and an itemised cost sheet.",
                  "<strong>Pre-production</strong> — contracts, design, stage and technical plans, permits, travel and hospitality.",
                  "<strong>Show day</strong> — crew call, rehearsals, artist handling, guest flow and safety.",
                  "<strong>Close-out</strong> — vendor settlement, GST invoicing, photos and a short report."])),
        sec("Event management services we provide",
            cards([("Corporate events", 'Annual days, award nights, town halls, conferences and offsites. See <a class="underline" href="/corporate-event-management/">corporate event management</a>.'),
                   ("Dealer & channel meets", "Large-format meets from 500 to 25,000 guests with awards, keynotes and entertainment."),
                   ("Concerts & music nights", "Stage, sound, lighting, LED, artist riders, crowd barriers and ticketed-entry operations."),
                   ("Brand launches & activations", "Product reveals, mall and campus activations, experiential stalls and press days."),
                   ("Weddings & private events", 'Sangeet, reception and destination weddings. See <a class="underline" href="/wedding-planner-delhi/">wedding planner in Delhi</a>.'),
                   ("Celebrity & artist booking", 'Actors, singers, comedians and DJs, booked and managed in-house. See <a class="underline" href="/celebrity-booking-india/">celebrity booking</a>.'),
                   ("Festivals & cultural events", 'Durga Puja stalls and sponsorship in CR Park and Gurgaon. See <a class="underline" href="/durga-puja-2026/">Durga Puja 2026</a>.'),
                   ("Government & public events", "Functions, trade fairs and summits with the required clearances and empanelment paperwork.")]), wide=True),
        sec("How much does an event management company charge?",
            p("Cost depends on guest count, city, venue, production scale and whether a celebrity is involved. These are the ranges we see most often; every quote is itemised.")
            + table(["Event type", "Typical budget", "Notes"], [
                ["Boutique corporate event", "From ₹3 lakh", "Venue, AV, décor, anchor"],
                ["Annual day / dealer meet", "₹25 lakh – ₹2 crore", "Production, awards, entertainment"],
                ["Large summit / conference", "₹1 – 5 crore", "Multi-hall, delegates, hospitality"],
                ["Premium wedding or concert", "₹35 lakh – ₹8 crore", "Depends on guests, venue and artists"],
                ["Agency fee", "8–15% of budget", "Or a fixed project fee"]], "Indicative 2026 ranges. Final quotes depend on the brief; GST extra.")),
        sec("How to choose an event management company",
            p("Ask every agency on your shortlist the same questions and compare the answers side by side:")
            + table(["Question to ask", "Why it matters", "TKC Talent's answer"], [
                ["Is production in-house or sub-contracted?", "Sub-contracting adds cost and weakens accountability", "One in-house team with a single lead per event"],
                ["Can you show events of my size?", "A 300-guest dinner and a 10,000-guest meet need different skills", "500 to 25,000-guest formats delivered"],
                ["Who handles permits?", "Missing permissions can stop a show", "Permits handled by us (Delhi: NDMC, MCD, DPCC, Delhi Police, Fire)"],
                ["How are artists booked?", "Middlemen inflate fees and risk no-shows", "Artists booked and managed directly by our team"],
                ["Is the quote itemised?", "Lump sums hide margins", "Line-by-line cost sheet with GST shown"]])),
        sec("Cities we cover",
            p('We are based in Delhi and run events across India. City pages: <a class="underline" href="/event-management-delhi/">Delhi NCR</a>, '
              '<a class="underline" href="/event-management-gurgaon/">Gurgaon</a>, <a class="underline" href="/event-management-mumbai/">Mumbai</a>, '
              '<a class="underline" href="/celebrity-booking-jaipur/">Jaipur</a>, <a class="underline" href="/celebrity-booking-goa/">Goa</a> and '
              '<a class="underline" href="/celebrity-booking-noida/">Noida</a>. For a ranked comparison of agencies, read our guide to the '
              '<a class="underline" href="/blog/event-management-company-india/">best event management companies in India</a>.')),
    ],
    gallery=[("tkc-large-live-event-audience-india", "Large live-event audience at a TKC Talent production"),
             ("tkc-concert-lighting-stage-production", "Concert lighting and stage production by TKC Talent"),
             ("tkc-experiential-brand-stall-event", "Experiential brand stall at an event managed by TKC Talent"),
             ("tkc-live-performers-event-stage", "Live performers on an event stage produced by TKC Talent"),
             ("tkc-night-event-crowd-management", "Night event crowd management by the TKC Talent operations team"),
             ("tkc-main-stage-dj-production", "Main-stage DJ production at a TKC Talent event")],
    faqs=[("What is an event management company?", "An event management company plans and runs events for clients from brief to final invoice: venue, design, stage production, artists, permits, hospitality and on-day operations, under one accountable team."),
          ("Which is the best event management company in India?", "Wizcraft, Percept and DNA Networks are among the largest by volume. TKC Talent (The Kabir Company), founded in 2005 in New Delhi, is known for combining full event production with in-house celebrity booking. The right choice depends on your event size, city and budget."),
          ("How much does an event management company charge in India?", "Boutique corporate events start at around ₹3 lakh; annual days and dealer meets commonly cost ₹25 lakh to ₹2 crore; premium weddings and concerts ₹35 lakh to ₹8 crore. Agency fees are usually 8–15% of the budget or a fixed project fee."),
          ("How early should I hire an event management company?", "Six months or more for weddings and large concerts in the October–February season; four to eight weeks for most corporate events. TKC Talent can deliver a corporate event in 14 days when the brief and budget are confirmed."),
          ("Does TKC Talent work outside Delhi?", "Yes. TKC Talent is based in New Delhi and runs events across India, including Gurgaon, Noida, Mumbai, Jaipur and Goa, plus destination events."),
          ("How do I get a quote?", 'Share your date, city, guest count and budget through the <a href="/contact-us/">enquiry form</a> or email hello@tkctalent.com. You will receive an itemised proposal.')],
    related=rel("/event-management-company/"),
    cta_h2="Plan your event with TKC Talent",
    cta_text="Tell us the date, city, guest count and budget. We reply with a concept, venue options and an itemised quote.",
)

# ---------------------------------------------------------------- Delhi NCR
PAGES["event-management-delhi"] = dict(
    title="Event Management Company in Delhi NCR | TKC Talent, CR Park",
    desc="Event management company in Delhi NCR since 2005. Corporate events, launches, concerts and weddings across Delhi, Gurgaon, Noida and Faridabad. Itemised quotes.",
    h1="Event Management Company in Delhi NCR",
    eyebrow="Event Management · Delhi NCR",
    crumb="Event Management Delhi NCR",
    crumbs=[("Event Management Company", "https://tkctalent.com/event-management-company/")],
    service_name="Event management in Delhi NCR",
    service_type="Event management",
    area=["Delhi NCR", "New Delhi", "Gurgaon", "Noida", "Greater Noida", "Faridabad", "Ghaziabad"],
    llms="llms-delhi.txt",
    img="tkc-live-concert-crowd-energy",
    img_alt="Concert crowd at a Delhi NCR event managed by TKC Talent",
    answer=("<strong>TKC Talent (The Kabir Company)</strong> is an <strong>event management company in Delhi NCR</strong>, based at 600 CR Park, New Delhi, since 2005. "
            "It manages corporate events, dealer meets, brand launches, concerts and weddings across Delhi, Gurgaon, Noida, Greater Noida and Faridabad, with venue, production, artists and Delhi permits handled by one in-house team."),
    facts=[("Office", "600, CR Park, New Delhi 110019"), ("Since", "2005 (20+ years in NCR)"),
           ("Covers", "Delhi, Gurgaon, Noida, Greater Noida, Faridabad, Ghaziabad"), ("Budgets", "₹3 lakh to ₹12 crore+"),
           ("Clients include", "DS Group, DLF, BPTP, M3M, Omaxe"), ("Contact", '<a class="underline" href="/contact-us/">enquiry form</a> or hello@tkctalent.com')],
    sections=[
        sec("Best event management company in Delhi NCR: how to decide",
            p("There is no single \"best\" agency for every event. The best event management company in Delhi NCR for you is the one that has delivered events of your size, in your part of NCR, and does the core work itself. Other established Delhi names include E-Factor Experiences, Encompass, 70 EMG, Pegasus and Cogent E-services. Use these checks to compare them with TKC Talent:")
            + table(["What to check", "Good sign", "TKC Talent"], [
                ["Local base", "An NCR office and crew, not a fly-in team", "Head office in CR Park, South Delhi"],
                ["Venue experience", "Has worked at your venue or similar", "Bharat Mandapam, Yashobhoomi, Pragati Maidan, Aerocity hotels, Chattarpur farms"],
                ["Permits", "Handles Delhi and Haryana approvals", "Delhi Police, Fire, MCD/NDMC, DPCC; MCG for Gurgaon"],
                ["Talent", "Books artists directly", "Celebrities, singers, comedians and DJs booked in-house"],
                ["Transparency", "Itemised quote with GST", "Line-by-line proposal"]])),
        sec("Where we work across Delhi NCR",
            table(["Area", "Typical events", "Venues we use"], [
                ["Central & New Delhi", "Government functions, summits, award nights", "Bharat Mandapam, Pragati Maidan, The Ashok, Vigyan Bhawan"],
                ["Aerocity & Dwarka", "Conferences, launches, delegate events", "Yashobhoomi, JW Marriott Aerocity, Aerocity hotels"],
                ["South Delhi", "Weddings, private parties, Durga Puja", "Chattarpur farms, CR Park, Taj, Leela, ITC Maurya"],
                ["Gurgaon", "Corporate offsites, launches, weddings", 'Cyber Hub, Leela Ambience, Oberoi — see <a class="underline" href="/event-management-gurgaon/">Gurgaon</a>'],
                ["Noida & Greater Noida", "Dealer meets, expos, concerts", "India Expo Mart, Buddh International Circuit"],
                ["Faridabad", "Corporate and community events", "Hotels, banquet halls and open grounds"]])),
        sec("Event calendar in Delhi NCR",
            ul(["<strong>October–February:</strong> wedding season, Diwali corporate events and Durga Puja; book venues and artists 4–6 months ahead.",
                "<strong>February–March:</strong> financial-year-end annual days, dealer meets and award nights.",
                "<strong>April–June:</strong> heat moves events indoors; good rates on hotel ballrooms.",
                "<strong>July–September:</strong> monsoon; launches, conferences and indoor concerts."])),
        sec("What we manage for Delhi NCR events",
            cards([("Corporate events", 'Annual days, town halls and award nights. More on <a class="underline" href="/corporate-event-management/">corporate event management</a>.'),
                   ("Real-estate events", "Tower launches, channel-partner meets and possession ceremonies for NCR developers."),
                   ("Concerts", "Indoor and open-air shows with stage, sound, LED, barricading and artist hospitality."),
                   ("Weddings", 'Planning, décor and entertainment. See our <a class="underline" href="/wedding-planner-delhi/">wedding planner in Delhi</a> page.'),
                   ("Celebrity appearances", 'Bollywood actors, singers and comedians. See <a class="underline" href="/celebrity-booking-delhi/">celebrity booking in Delhi</a>.'),
                   ("Festivals", 'Durga Puja stalls and sponsorship in CR Park and Gurgaon — <a class="underline" href="/durga-puja-2026/">Durga Puja 2026</a>.')]), wide=True),
    ],
    gallery=[("tkc-live-concert-event-management-india", "Live concert managed by TKC Talent"),
             ("tkc-outdoor-event-crowd-management", "Outdoor event crowd management by TKC Talent in NCR"),
             ("tkc-night-concert-audience-operations", "Night concert audience operations by TKC Talent"),
             ("tkc-outdoor-food-stalls-event", "Outdoor food stalls at an event managed by TKC Talent"),
             ("tkc-dj-stage-performance-production", "DJ stage performance production by TKC Talent"),
             ("tkc-concert-crowd-barrier-management", "Concert crowd barrier management by TKC Talent")],
    faqs=[("Which is the best event management company in Delhi NCR?", "Established Delhi NCR agencies include TKC Talent (The Kabir Company), E-Factor Experiences, Encompass, 70 EMG, Pegasus and Cogent E-services. TKC Talent is based in CR Park, has worked in NCR since 2005 and handles production, permits and celebrity booking in-house. Compare agencies on local experience, venue history and itemised quotes."),
          ("How much does event management cost in Delhi NCR?", "Small corporate events start at about ₹3 lakh. Annual days and dealer meets usually cost ₹25 lakh to ₹2 crore, and premium weddings or concerts ₹35 lakh to ₹8 crore. GST is extra."),
          ("Do you cover Gurgaon, Noida and Faridabad?", "Yes. Gurgaon, Noida, Greater Noida, Faridabad and Ghaziabad are all covered by the same NCR team."),
          ("Which permissions are needed for an event in Delhi?", "Depending on the venue and format: Delhi Police, Fire, MCD or NDMC, and DPCC for sound. TKC Talent applies for and tracks these as part of the job."),
          ("How quickly can you deliver an event in Delhi?", "A corporate event can be delivered in about 14 days once the brief and budget are confirmed. Weddings and concerts in peak season need 4–6 months."),
          ("Where is your Delhi office?", "600, CR Park, New Delhi 110019. Contact us through the enquiry form or at hello@tkctalent.com.")],
    related=rel("/event-management-delhi/"),
    cta_h2="Planning an event in Delhi NCR?",
    cta_text="Share the date, area and guest count. We reply with venue options and an itemised quote.",
)

# ---------------------------------------------------------------- Event planners Delhi
PAGES["event-planners-delhi"] = dict(
    title="Event Planners in Delhi | Planning Timeline, Permits & Cost – TKC",
    desc="Event planners in Delhi since 2005: planning timelines, Delhi permits, budgets and a single planner for corporate events, parties and weddings. TKC Talent, CR Park.",
    h1="Event Planners in Delhi",
    eyebrow="Event Planners · Delhi",
    crumb="Event Planners Delhi",
    crumbs=[("Event Management Delhi NCR", "https://tkctalent.com/event-management-delhi/")],
    service_name="Event planning in Delhi",
    service_type="Event planning",
    area=["New Delhi", "Delhi NCR"],
    llms="llms-delhi.txt",
    img="tkc-live-event-audience-engagement",
    img_alt="Audience engagement at a Delhi event planned by TKC Talent",
    answer=("<strong>TKC Talent</strong> is a team of <strong>event planners in Delhi</strong>, based in CR Park since 2005. "
            "One named planner takes your event from brief to settlement: budget, venue, timeline, vendors, permits, artists and show-day running. "
            "Corporate events can be planned in 14 days; weddings and large shows need 4–6 months."),
    facts=[("Planner model", "One accountable planner per event"), ("Fastest turnaround", "14 days (corporate)"),
           ("Agency fee", "8–15% of budget or fixed fee"), ("Smallest projects", "From ₹3 lakh"),
           ("Permits handled", "Delhi Police, Fire, MCD/NDMC, DPCC"), ("Office", "600, CR Park, New Delhi")],
    sections=[
        sec("How Delhi event planning works, week by week",
            table(["When", "Corporate event (8 weeks)", "Wedding or concert (6 months)"], [
                ["Start", "Brief, budget, date hold", "Brief, budget, guest estimate"],
                ["Weeks 1–2 / Month 1", "Venue visits and proposal", "Venue booking and concept"],
                ["Weeks 3–4 / Months 2–3", "Contracts, design, artist confirmation", "Décor design, artists, travel blocks"],
                ["Weeks 5–6 / Months 4–5", "Permits, run-of-show, rehearsals plan", "Permits, vendor contracts, guest logistics"],
                ["Final week", "Technical rehearsal, guest comms", "Final walkthroughs and rehearsals"],
                ["After", "Settlement and report", "Settlement, photos and report"]],
                "Rush timeline: with a confirmed budget, a corporate event can be compressed to 14 days.")),
        sec("Permits for events in Delhi",
            p("Missing approvals are one of the most common reasons Delhi events get delayed. Our planners file and track them for you:")
            + table(["Approval", "Usually needed for"], [
                ["Delhi Police", "Public gatherings, traffic and late-night events"],
                ["Delhi Fire Service", "Temporary structures, large indoor gatherings"],
                ["MCD / NDMC", "Use of public land, hoardings and temporary structures"],
                ["DPCC", "Amplified sound and generators"],
                ["Venue approvals", "Load-in times, fire plans and insurance at hotels and halls"]])),
        sec("What an event planner does — and what you do",
            ul(["<strong>We do:</strong> budget plan, venue shortlist, vendor contracts, design, stage and sound, artist booking, permits, guest logistics, run-of-show and settlement.",
                "<strong>You do:</strong> approve the brief and budget, choose from shortlisted options, share guest lists and sign off final designs.",
                "<strong>On the day:</strong> your planner runs the show; you host."])),
        sec("What a Delhi event budget usually covers",
            p("When you compare quotes from event planners, check that each one includes the same line items:")
            + table(["Line item", "Includes"], [
                ["Venue", "Hall or lawn hire, F&amp;B minimums, overtime charges"],
                ["Production", "Stage, sound, lighting, LED screens, power back-up"],
                ["Design", "Décor, branding, signage, printed material"],
                ["Talent", "Anchor, performers, celebrity fee and riders"],
                ["Logistics", "Guest transport, travel, rooms, crew meals"],
                ["Compliance", "Permit fees, insurance, security staff"],
                ["Planner fee &amp; GST", "Fee as a percentage or fixed amount, plus 18% GST"]])),
        sec("Questions to ask any event planner in Delhi",
            ol(["Who exactly will be my planner, and will they be there on the day?",
                "Which Delhi venues have you worked at in the last year?",
                "Which permits will my event need, and who files them?",
                "Is stage, sound and lighting your own or rented through someone else?",
                "Can I see an itemised quote with GST shown separately?"])),
        sec("Events our Delhi planners handle",
            p('Corporate annual days and town halls (see <a class="underline" href="/corporate-event-management/">corporate event management</a>), product launches, dealer meets, private parties, '
              '<a class="underline" href="/wedding-planner-delhi/">weddings</a>, concerts and festivals such as <a class="underline" href="/durga-puja-2026/">Durga Puja in CR Park</a>. '
              'For full-scale production across NCR, see our <a class="underline" href="/event-management-delhi/">event management company in Delhi NCR</a> page.')),
    ],
    gallery=[("tkc-live-stage-performance-production", "Live stage performance planned by TKC Talent"),
             ("tkc-experiential-brand-stall-event", "Brand stall at a Delhi event planned by TKC Talent"),
             ("tkc-female-dj-live-event-india", "DJ performance at a Delhi event planned by TKC Talent")],
    faqs=[("How much do event planners in Delhi charge?", "Most charge 8–15% of the event budget or a fixed project fee. TKC Talent's smallest corporate projects start at around ₹3 lakh in total budget."),
          ("How far in advance should I book an event planner in Delhi?", "Four to eight weeks for most corporate events, and four to six months for weddings and concerts in the October–February season. A rush corporate event can be done in 14 days."),
          ("Do event planners in Delhi handle police and fire permissions?", "Good planners do. TKC Talent files and tracks Delhi Police, Fire, MCD/NDMC and DPCC approvals where the event needs them."),
          ("Can I hire a planner only for the event day?", "Yes, as day-of coordination, but most of the value is in planning: venue, contracts and permits. We recommend involving a planner from the brief."),
          ("Do you plan small events?", "Yes. Boutique corporate events, private parties and intimate functions are planned by the same team."),
          ("How do I contact TKC Talent's planners?", 'Use the <a href="/contact-us/">enquiry form</a> or email hello@tkctalent.com with your date, guest count and budget.')],
    related=rel("/event-planners-delhi/"),
    cta_h2="Get a Delhi event planner assigned",
    cta_text="Send your date, guest count and budget. A planner will reply with a timeline and cost plan.",
)

# ---------------------------------------------------------------- Gurgaon
PAGES["event-management-gurgaon"] = dict(
    title="Event Management Company in Gurgaon (Gurugram) | TKC Talent",
    desc="Event management company in Gurgaon: corporate offsites, launches, weddings and concerts across Cyber City, Golf Course Road and Sohna Road. Durga Puja stalls in Gurgaon.",
    h1="Event Management Company in Gurgaon (Gurugram)",
    eyebrow="Event Management · Gurgaon",
    crumb="Event Management Gurgaon",
    crumbs=[("Event Management Delhi NCR", "https://tkctalent.com/event-management-delhi/")],
    service_name="Event management in Gurgaon",
    service_type="Event management",
    area=["Gurgaon", "Gurugram", "Manesar", "Sohna"],
    geo_region="IN-HR", geo_place="Gurugram, Haryana, India",
    llms="llms-gurgaon.txt",
    img="tkc-main-stage-dj-production",
    img_alt="Main-stage production at a Gurgaon event managed by TKC Talent",
    answer=("<strong>TKC Talent</strong> is an <strong>event management company in Gurgaon</strong> that runs corporate offsites, annual days, product launches, weddings and concerts across DLF Cyber City, Golf Course Road, Sohna Road and Manesar. "
            "Our NCR team handles venue, production, artists and Haryana permits. For Durga Puja 2026, stalls are available in Gurgaon Sectors 29 and 56 at ₹35,000–₹45,000."),
    facts=[("Areas", "Cyber City, Golf Course Rd, Sohna Rd, Manesar"), ("Venues", "Leela Ambience, Oberoi, ITC Grand Bharat, Karma Lakelands"),
           ("Permits", "MCG, HSPCB, Haryana Fire"), ("Budgets", "₹5 lakh to ₹10 crore+"),
           ("Durga Puja stalls", '<a class="underline" href="/durga-puja-2026/">Sector 29 & 56 · ₹35k–45k</a>'), ("Contact", "hello@tkctalent.com")],
    sections=[
        sec("Gurgaon areas and what we run there",
            table(["Area", "Common events", "Example venues"], [
                ["DLF Cyber City & Cyber Hub", "Town halls, team nights, launches", "Cyber Hub, 32nd Milestone, Cyber City hotels"],
                ["Golf Course Road", "Award nights, leadership dinners, weddings", "Leela Ambience, Oberoi Gurgaon, Trident"],
                ["Sohna Road & Sohna", "Offsites, outdoor weddings, team building", "Karma Lakelands, The Westin Sohna"],
                ["Manesar", "Plant events, dealer meets, family days", "ITC Grand Bharat, factory grounds"],
                ["Sectors 29 & 56", "Durga Puja, community and food events", 'Puja grounds — <a class="underline" href="/durga-puja-2026/">stall booking</a>']])),
        sec("Durga Puja 2026 stalls in Gurgaon",
            p('Stalls are available at Durga Puja pandals in <strong>Gurgaon Sector 29 and Sector 56</strong> for the five days of 16–20 October 2026. '
              'Stall rent is <strong>₹35,000–₹45,000</strong> depending on size and position. Full details, rate cards and sponsorship tiers are on the '
              '<a class="underline" href="/durga-puja-2026/">Durga Puja 2026 stall booking page</a>, with more on <a class="underline" href="/book-stalls-durga-puja/">booking stalls</a> and '
              '<a class="underline" href="/durga-puja-sponsorship/">sponsorship</a>.')),
        sec("Corporate events for Gurgaon offices",
            p("Gurgaon is home to the India offices of many IT, consulting, BFSI and consumer companies. That means weekday town halls, quarterly award nights and leadership offsites, often at short notice. We plan these around Cyber City traffic, building security rules and hotel load-in windows, and can add a celebrity host or performer through our in-house booking team.")
            + p('See also: <a class="underline" href="/corporate-event-management/">corporate event management</a> and <a class="underline" href="/celebrity-booking-gurgaon/">celebrity booking in Gurgaon</a>.')),
        sec("Planning tips for events in Gurgaon",
            ul(["<strong>Traffic:</strong> NH-48, Golf Course Road and Sohna Road jam between 6 and 9 pm on weekdays. Set guest arrival after 8 pm or arrange shuttles from metro stations.",
                "<strong>Office buildings:</strong> Cyber City towers need security passes and fixed load-in slots. Apply a week ahead.",
                "<strong>Monsoon:</strong> for July–August outdoor events, keep a covered or indoor backup, because low-lying roads can flood.",
                "<strong>Weekend weddings:</strong> resorts on Sohna Road and in Manesar book out early in November–February.",
                "<strong>Festivals:</strong> Durga Puja and Diwali weeks bring large crowds to the Sector 29 and 56 grounds. Plan parking and stall logistics early."])),
        sec("Permits for events in Gurgaon",
            table(["Approval", "Used for"], [
                ["MCG (Municipal Corporation of Gurugram)", "Temporary structures and public spaces"],
                ["HSPCB", "Amplified sound and generators"],
                ["Haryana Fire Service", "Temporary structures and large gatherings"],
                ["Gurugram Police", "Traffic, crowd control and late events"]])),
    ],
    gallery=[("tkc-male-dj-concert-performance", "DJ concert performance at a TKC Talent event"),
             ("tkc-outdoor-concert-audience-india", "Outdoor concert audience at a TKC Talent event"),
             ("tkc-female-dj-event-performance", "DJ performance at an event managed by TKC Talent")],
    faqs=[("Which is a good event management company in Gurgaon?", "TKC Talent (The Kabir Company) runs corporate events, launches, weddings and concerts across Gurgaon with its NCR team, handling production, artists and Haryana permits in-house. Compare agencies on Gurgaon venue experience and itemised quotes."),
          ("Are Durga Puja stalls available in Gurgaon in 2026?", "Yes. Stalls are available in Gurgaon Sector 29 and Sector 56 for 16–20 October 2026, at a rent of ₹35,000–₹45,000."),
          ("How much does a corporate event in Gurgaon cost?", "Gurgaon corporate events usually start at about ₹5 lakh; large offsites, dealer meets and award nights can run into crores depending on guests and production."),
          ("Which venues in Gurgaon do you work with?", "Leela Ambience, Oberoi Gurgaon, Trident, ITC Grand Bharat, The Westin Sohna, Karma Lakelands and Cyber Hub, among others."),
          ("Can you bring a celebrity to a Gurgaon event?", 'Yes. Actors, singers, comedians and DJs are booked by our in-house team — see <a href="/celebrity-booking-gurgaon/">celebrity booking in Gurgaon</a>.'),
          ("How do I get a quote?", 'Use the <a href="/contact-us/">enquiry form</a> or email hello@tkctalent.com with date, area and guest count.')],
    related=rel("/event-management-gurgaon/"),
    cta_h2="Planning an event in Gurgaon?",
    cta_text="Tell us the area, date and guest count. We reply with venues and an itemised quote.",
)

# ---------------------------------------------------------------- Wedding planner Delhi
PAGES["wedding-planner-delhi"] = dict(
    title="Wedding Planner in Delhi | Planning, Décor & Entertainment – TKC",
    desc="Wedding planner in Delhi NCR: venue, décor, sangeet entertainment, celebrity performers, guest hospitality and logistics. TKC Talent, CR Park, since 2005.",
    h1="Wedding Planner in Delhi",
    eyebrow="Wedding Planning · Delhi NCR",
    crumb="Wedding Planner Delhi",
    crumbs=[("Event Management Delhi NCR", "https://tkctalent.com/event-management-delhi/")],
    service_name="Wedding planning in Delhi",
    service_type="Wedding planning",
    area=["New Delhi", "Delhi NCR", "Gurgaon", "Noida"],
    llms="llms-delhi.txt",
    img="tkc-live-performers-event-stage",
    img_alt="Live performers on a stage produced by TKC Talent",
    answer=("<strong>TKC Talent</strong> is a <strong>wedding planner in Delhi</strong>, based in CR Park, that plans weddings across Delhi NCR: venue booking, décor, sangeet and reception entertainment, celebrity performers, guest hospitality and logistics. "
            "Each wedding is quoted individually; start planning 6 months ahead for October–February dates."),
    facts=[("Based in", "600, CR Park, New Delhi"), ("Covers", "Delhi, Gurgaon, Noida, farmhouses & hotels"),
           ("Best lead time", "6+ months for Oct–Feb dates"), ("Pricing", "Quoted per wedding"),
           ("Entertainment", 'Singers, DJs, comedians, <a class="underline" href="/book-celebrity-for-wedding/">celebrities</a>'), ("Contact", "hello@tkctalent.com")],
    sections=[
        sec("What our Delhi wedding planning covers",
            cards([("Venue", "Shortlists and bookings at Delhi hotels, Chattarpur farmhouses and Gurgaon resorts."),
                   ("Décor & design", "Theme, mandap, stage, florals and lighting for each function."),
                   ("Sangeet & entertainment", "Choreographers, singers, DJs, bands and comedians."),
                   ("Celebrity performers", 'Bollywood singers and stars for sangeet or reception — see <a class="underline" href="/book-celebrity-for-wedding/">book a celebrity for your wedding</a>.'),
                   ("Guest hospitality", "Room blocks, airport pickups, welcome desks and transport."),
                   ("Wedding-day running", "Run-of-show for every function, vendor coordination and family support.")]), wide=True),
        sec("Wedding planning timeline",
            table(["Time before wedding", "What gets done"], [
                ["9–12 months", "Budget, guest estimate, dates, venue shortlist"],
                ["6–9 months", "Venue booking, planner contract, décor concept"],
                ["4–6 months", "Entertainment and celebrity bookings, room blocks"],
                ["2–3 months", "Invitations, menus, function-wise run-of-show"],
                ["Final month", "Rehearsals, final guest list, transport plan"],
                ["Wedding week", "Planner team on site for every function"]],
                "October–February is peak season in Delhi; popular venues and artists book out early.")),
        sec("Wedding functions we plan",
            table(["Function", "What we arrange"], [
                ["Roka / engagement", "Venue, décor, ring ceremony set-up, photography coordination"],
                ["Mehendi & haldi", "Day décor, seating, live music or dhol, food counters"],
                ["Sangeet", "Stage, sound, LED, choreographer, DJ, live singer or celebrity act"],
                ["Wedding ceremony", "Mandap, baraat logistics, pandit coordination, guest flow"],
                ["Reception", "Stage, entertainment, celebrity appearance, guest hospitality"]])),
        sec("Popular wedding venues in Delhi NCR",
            ul(["<strong>Five-star hotels:</strong> ITC Maurya, The Leela Palace, Taj Mansingh, Roseate House, Oberoi Gurgaon, Leela Ambience.",
                "<strong>Farmhouses:</strong> Chattarpur, Westend Greens and Sultanpur farm venues.",
                "<strong>Resorts near Delhi:</strong> Gurgaon, Sohna and Manesar properties for weekend weddings."])),
        sec("How wedding planning is priced",
            p("We quote each wedding individually after understanding guest count, number of functions, venue and entertainment. "
              "Planning fees are usually a percentage of the budget (commonly 8–15%) or a fixed fee. Luxury multi-day weddings we manage typically range from ₹35 lakh to ₹8 crore all-in; celebrity performers are quoted separately. "
              'For artist fees, see <a class="underline" href="/bollywood-celebrity-charges/">celebrity charges</a> and <a class="underline" href="/celebrity-singer-fees-2026/">singer fees 2026</a>.')),
    ],
    gallery=[("tkc-concert-stage-lighting-production", "Stage lighting production by TKC Talent"),
             ("tkc-female-dj-live-event-india", "DJ performance at an event by TKC Talent"),
             ("tkc-live-stage-performance-production", "Live stage performance produced by TKC Talent")],
    gallery_title="Stage and entertainment production by TKC Talent",
    faqs=[("How much does a wedding planner in Delhi cost?", "Planners usually charge 8–15% of the wedding budget or a fixed fee. TKC Talent quotes each wedding individually; luxury multi-day weddings we manage typically total ₹35 lakh to ₹8 crore including venue, décor and entertainment."),
          ("When should I book a wedding planner in Delhi?", "Six months or more ahead for October–February dates, when venues, décor teams and artists are in highest demand."),
          ("Can the wedding planner book a celebrity for the sangeet?", 'Yes. Singers, actors, comedians and DJs are booked through our in-house team. See <a href="/book-celebrity-for-wedding/">book a celebrity for your wedding</a>.'),
          ("Do you plan weddings in Gurgaon and Noida?", "Yes, across Delhi NCR, including Gurgaon, Noida and farmhouse venues around Delhi."),
          ("Do you handle destination weddings?", "Yes. We plan destination weddings in Jaipur, Goa and other locations with the same team."),
          ("How do I start?", 'Share your dates, city, guest count and budget through the <a href="/contact-us/">enquiry form</a> or email hello@tkctalent.com.')],
    related=rel("/wedding-planner-delhi/"),
    cta_h2="Start planning your Delhi wedding",
    cta_text="Send your dates, guest count and venue ideas. We reply with a plan and an indicative budget.",
)
