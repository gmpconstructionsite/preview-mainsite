"""Rebuild the editable static pages with Python 3. No dependencies."""
from pathlib import Path
import json
from html import escape as e
from urllib.parse import quote

ROOT = Path(__file__).parent
SITE = ROOT
public_urls = []
data = json.loads((ROOT/'content.json').read_text())
services = data['services']
projects = data['projects']
nav = [('Home','index'),('Services','services'),('Projects','projects'),('About','about'),('Contact','contact')]
domain = 'https://gmpconstruction.site'
area = 'Cainta, Rizal, Pasig and Metro Manila'
phone = '+63 935 393 8879'
email = 'contact@gmpconstruction.site'
address = 'Lot 4 Blk 16 Talavera Street, Vista Verde Executive Village, Cainta, Rizal'
facebook = 'https://www.facebook.com/gmpconstructionph'
company_intro = '<p>GMP Construction is a general contractor established in 2019. The company has been able to provide quality service in all its projects through its team composed of experienced employees and workers with valuable knowledge and expertise in the construction industry.</p>\n<p>We provide end-to-end solutions from conceptual planning, designing, project implementation, and project management up to preventive maintenance service. With each project, we ensure efficient and quality service through excellence, integrity, reliability, resilience, and safety.</p>'

# Shared, decorative line icons. Labels appear in the surrounding text.
icon_paths = {
    'integrity': '<path d="M12 22s7-3 7-10V5l-7-3-7 3v7c0 7 7 10 7 10Z"/><path d="m9 12 2 2 4-4"/>',
    'reliability': '<rect x="4" y="5" width="16" height="16" rx="2"/><path d="M8 3v4m8-4v4M4 10h16m-11 5 2 2 4-4"/>',
    'resilience': '<path d="M20 7v5h-5M4 17v-5h5M5 8a8 8 0 0 1 14-2l1 2M4 16l1 2a8 8 0 0 0 14-2"/>',
    'safety': '<path d="M3 16h18v3H3zM5 16v-3a7 7 0 0 1 14 0v3M10 6v5m4-5v5"/>',
    'excellence': '<path d="m12 3 2.7 5.6 6.2.9-4.5 4.4 1.1 6.2-5.5-2.9-5.5 2.9 1.1-6.2-4.5-4.4 6.2-.9Z"/>',
    'contract': '<path d="M6 3h8l4 4v14H6zM14 3v5h4M9 12h6m-6 4h6"/>',
    'services': '<path d="M14 6a4 4 0 0 0-5-4l2.5 2.5-3 3L6 5a4 4 0 0 0 4 5l8 8a2 2 0 0 0 3-3l-8-8Z"/><path d="m9 14-5 5a1.4 1.4 0 0 0 2 2l5-5"/>',
    'projects': '<path d="M3 21h18M5 21V9l7-5v17m0-12h7v12M8 13h1m-1 4h1m6-4h1m-1 4h1"/>',
    'area': '<path d="M20 10c0 5-8 11-8 11s-8-6-8-11a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.5"/>',
}

def icon(name):
    return f'<span class="brand-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{icon_paths[name]}</svg></span>'

def image(name,alt,priority=False):
    return f'<img src="assets/images/{e(name)}" alt="{e(alt)}" {"fetchpriority=\"high\"" if priority else "loading=\"lazy\""} decoding="async">'
def button(text,href,kind=''):
    return f'<a class="button {kind}" href="{href}">{text} <span class="button-arrow" aria-hidden="true"></span></a>'
def links(active):
    return ''.join(f'<a href="{slug}.html"'+(' aria-current="page"' if slug==active else '')+f'>{title}</a>' for title,slug in nav)
def page(slug,title,desc,body):
    canonical = domain + ('/' if slug=='index' else f'/{slug}.html')
    schema={'@context':'https://schema.org','@type':'GeneralContractor','name':'GMP Construction','url':domain,'image':domain+'/assets/images/paranaque-house.webp','telephone':'+639353938879','email':email,'foundingDate':'2019','address':{'@type':'PostalAddress','streetAddress':'Lot 4 Blk 16 Talavera Street, Vista Verde Executive Village','addressLocality':'Cainta','addressRegion':'Rizal','addressCountry':'PH'},'areaServed':['Cainta','Rizal','Pasig','Metro Manila'],'sameAs':[facebook]}
    public_urls.append(canonical)
    html=f'''<!doctype html>
<html lang="en-PH">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="index, follow">
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="en_PH">
  <meta property="og:site_name" content="GMP Construction">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(desc)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{domain}/assets/images/gmp-social-card-v1.8.2.jpg">
  <meta property="og:image:secure_url" content="{domain}/assets/images/gmp-social-card-v1.8.2.jpg">
  <meta property="og:image:type" content="image/jpeg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="GMP Construction — General contracting in Rizal and Metro Manila, with a completed Parañaque house project">
  <meta name="twitter:image" content="{domain}/assets/images/gmp-social-card-v1.8.2.jpg">
  <meta name="twitter:image:alt" content="GMP Construction — General contracting in Rizal and Metro Manila">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" type="image/png" href="assets/images/gmp-logo-color.png">
  <link rel="stylesheet" href="assets/css/bootstrap-grid.min.css">
  <link rel="stylesheet" href="assets/css/site.css">
  <!-- ANALYTICS: Insert the approved GA4 or GTM head snippet here after launch approval. -->
  <script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script>
  <script src="assets/js/site.js" defer></script>
  {'<script src="assets/js/inquiry.js" defer></script>' if slug == "quote" else ""}
  {'<script src="assets/js/newsletter.js" defer></script>' if slug == "contact" else ""}
</head>
<body>
  <!-- GTM: Insert the approved noscript fallback here if using GTM. -->
  <a class="skip" href="#main">Skip to content</a>
  <div class="utility"><div class="shell"><span>GENERAL CONTRACTOR <i></i> BASED IN CAINTA, RIZAL</span><a href="tel:+639353938879">{phone}</a></div></div>
  <header class="header"><div class="shell nav">
    <a href="index.html" class="logo">{image('gmp-logo-color.png','GMP Construction home',True)}</a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="mobile-nav" aria-label="Open menu"><span class="burger" aria-hidden="true"></span></button>
    <nav id="nav" aria-label="Main navigation">{links(slug)}{button('Request a quote','quote.html#quote')}</nav>
  </div></header>
  <dialog class="mobile-drawer" id="mobile-nav" aria-label="Mobile navigation">
    <div class="drawer-head"><strong>GMP Construction</strong><button type="button" data-menu-close aria-label="Close menu">×</button></div>
    <nav aria-label="Mobile navigation">{links(slug)}{button('Request a quote','quote.html#quote')}</nav>
  </dialog>
  <main id="main">{body}</main>
  <footer>
    <div class="shell footer-grid">
      <div><a class="logo" href="index.html">{image('gmp-logo-white.png','GMP Construction home')}</a><p>Based in Cainta, GMP handles construction and specialist works across Rizal, Pasig, Metro Manila, and nearby communities.</p><div class="social-links">
      <a href="viber://chat?number=%2B639353938879" aria-label="Chat with GMP on Viber" title="Viber"><svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M20 11.5a8 8 0 0 1-8 8h-2l-4 2v-4.5a8 8 0 1 1 14-5.5Z"/><path d="M9 8c-1 0-2 1-1 3 1 2 3 4 5 4 1 0 2-1 2-2l-2-1-1 1c-1-.5-2-1.5-2-2.5l.8-1L10 8Z"/></svg></a>
      <a href="https://m.me/gmpconstructionph" aria-label="Chat with GMP on Messenger" title="Messenger"><svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M12 2a10 10 0 0 0-7.3 16.8V22l3.3-1.8c1.2.5 2.6.8 4 .8a9.5 9.5 0 1 0 0-19Zm-5 12.6 4.3-4.7 2.3 2.4 3.4-2.4-4.2 4.8-2.4-2.4Z"/></svg></a>
      <a href="https://wa.me/639353938879" target="_blank" rel="noopener noreferrer" aria-label="Chat with GMP on WhatsApp (opens a new tab)" title="WhatsApp"><svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M20.5 11.5a8.5 8.5 0 0 1-12.6 7.4L3 20.5l1.5-4.8A8.5 8.5 0 1 1 20.5 11.5Z"/><path d="m8 7 1.5-.2 1 2.6-1 1c.7 1.5 1.7 2.5 3.3 3.2l1-1 2.5 1.1-.2 1.5c-.1.8-1.2 1.4-2.2 1.2-3.6-.6-6.7-3.7-7.1-7.1C6.7 8.3 7.2 7.2 8 7Z"/></svg></a></div></div>
      <div><h2>Get in touch</h2><p><a href="tel:+639353938879">{phone}</a><br><a href="mailto:{email}">{email}</a></p></div>
    </div>
    <div class="shell footer-bottom"><span>© 2026 GMP Construction</span></div>
  </footer>
  <!-- Shared native dialog. Project content is copied from the accessible HTML disclosure. -->
  <dialog class="project-dialog" aria-labelledby="project-dialog-title">
    <div class="dialog-head"><h2 id="project-dialog-title"></h2><button type="button" data-close aria-label="Close project">×</button></div>
    <div class="dialog-body">
      <p class="dialog-description"></p>
      <div class="photo-stage"><div class="photo-window" tabindex="0" aria-label="Project photo. Scroll to pan when zoomed."><img alt=""></div>
        <div class="photo-tools"><button type="button" data-photo-prev aria-label="Previous photo">‹</button><span data-photo-count aria-live="polite"></span><button type="button" data-photo-next aria-label="Next photo">›</button><button type="button" data-zoom aria-label="Magnify photo" aria-pressed="false"><svg viewBox="0 0 24 24" width="19" height="19" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2"><circle cx="10" cy="10" r="6"/><path d="m15 15 6 6M7 10h6m-3-3v6"/></svg><span>Zoom in</span></button></div></div>
      <p class="photo-caption"></p>
      <a class="button dialog-quote" href="quote.html#quote">I want to avail this service</a>
    </div>
  </dialog>
  <!-- MESSENGER: Shared floating chat launcher. Update this URL if the page username changes. -->
  <a class="messenger-float" href="https://m.me/gmpconstructionph" target="_blank" rel="noopener noreferrer" aria-label="Chat with GMP Construction on Messenger (opens a new tab)" title="Chat on Messenger">
    <svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M12 2a10 10 0 0 0-7.3 16.8V22l3.3-1.8c1.2.5 2.6.8 4 .8a9.5 9.5 0 1 0 0-19Zm-5 12.6 4.3-4.7 2.3 2.4 3.4-2.4-4.2 4.8-2.4-2.4Z"/></svg>
  </a>
</body>
</html>
'''
    (SITE/f'{slug}.html').write_text(html,encoding='utf-8')

def intro(label,title,description):
    return f'<section class="intro"><div class="shell"><p class="eyebrow">{label}</p><h1>{title}</h1><p>{description}</p></div></section>'

def project_card(p):
    pictures=''.join(f'<figure>{image(pic["file"],pic["alt"])}<figcaption>{e(pic["alt"])}</figcaption></figure>' for pic in p['images'])
    return f'''<div class="project-column col d-flex" data-category="{p['category']}"><article class="project">
      <a class="project-cover" href="#{p['slug']}" aria-label="View project: {e(p['title'])}">{image(p['images'][0]['file'],p['images'][0]['alt'])}</a>
      <div class="project-content"><p class="eyebrow">{e(p['location'])} <span> / </span> {p['date'][:4]}</p>
      <h3>{e(p['title'])}</h3><p>{e(p['description'])}</p>
      <details class="project-evidence" id="{p['slug']}"><summary>View project</summary>{pictures}
      {button('I want to avail this service', 'quote.html?service='+quote(p['quote_service'])+'&amp;project='+quote(p['title'])+'#quote')}</details></div>
    </article></div>'''

# Gallery examples mix GMP photos and clearly labeled illustrative stock.
stock = {
    'roofing': [],
    'construction': [('8961065', 'Construction crew reviewing work at a structural site'), ('1216589', 'Construction workers reviewing drawings')],
    'finishes': [('6474471', 'Worker painting an interior wall'), ('5691622', 'Applying a smooth wall finish')],
    'utilities': [],
}
def gallery(group):
    examples = [(pic['file'], pic['alt'].split(' shown in the GMP company profile')[0], False) for pic in group['gallery']]
    examples += [(f'service-pexels-{number}.jpg', caption, True) for number, caption in stock[group['id']]]
    return ''.join(f'<figure>{image(file, caption)}{"<span class=stock-label>Illustrative photo</span>" if illustrative else ""}</figure>' for file, caption, illustrative in examples)

group_tiles=''.join(f'<div class="col d-flex"><a href="services.html#{g["id"]}" class="group-tile">{image(g["gallery"][0]["file"],"")}<div><h3>{e(g["name"])}</h3><p>{e(g["summary"])}</p><span class="service-link">Explore services <span aria-hidden="true">›</span></span></div></a></div>' for g in services)
featured=[projects[i] for i in (0,1,2,5)]
slides=''.join(f'<div class="hero-slide" {"hidden" if i else ""}>{image(p["images"][0]["file"],p["images"][0]["alt"],not i)}<a href="projects.html#{p["slug"]}" class="hero-caption">PROJECT SPOTLIGHT <strong>{e(p["title"])} · {e(p["location"])}</strong></a></div>' for i,p in enumerate(featured))
home=f'''<section class="hero" aria-label="Featured project slideshow">
  {slides}
  <div class="shell hero-inner"><p class="eyebrow">GENERAL CONTRACTING IN RIZAL &amp; METRO MANILA</p>
  <h1>From foundation<br>to finishing.</h1><p>GMP Construction handles new builds, roof and waterproofing works, and the specialist trades that bring a space together.</p>
  <div class="actions">{button('Request a quote','quote.html#quote')}{button('Explore our projects','projects.html','ghost')}</div></div>
</section>
<section class="shell section about-layout home-intro" data-reveal>{image('team.webp','GMP crew working on a building exterior')}<div><p class="eyebrow">MEET GMP CONSTRUCTION</p><h2>A general contractor based in Cainta</h2>{company_intro}{button('About GMP','about.html','outline')}</div></section>
<section class="section shell"><p class="eyebrow">WHAT WE DO</p><h2>Find the right service</h2><div class="group-grid row row-cols-1 row-cols-sm-2 row-cols-xl-4 g-4">{group_tiles}</div></section>
<section class="section tinted"><div class="shell"><p class="eyebrow">PROJECT PORTFOLIO</p><div class="section-head"><h2>See the work for yourself</h2>{button('View all projects','projects.html','outline')}</div>
<div class="project-grid row row-cols-1 row-cols-sm-2 row-cols-lg-3 g-4">{''.join(project_card(p) for p in projects[:3])}</div></div></section>'''
page('index','GMP Construction | General Contractor in Cainta, Rizal', 'GMP Construction provides house construction, roofing, waterproofing and specialist trades in Cainta, Rizal, Pasig and Metro Manila. Explore documented projects.',home)

service_sections=[]
for group in services:
    items=''.join(f'<article class="service-description"><div><h3>{e(name)}</h3><p>{e(desc)}</p></div></article>' for name,desc in group['items'])
    service_sections.append(f'<section class="service-section" data-reveal id="{group["id"]}"><h2>{e(group["name"])}</h2><div class="service-gallery">{gallery(group)}</div><div class="service-descriptions">{items}</div></section>')
page('services','Construction Services in Rizal & Metro Manila | GMP Construction','Explore GMP’s roofing, waterproofing, house construction, interiors, masonry, plumbing, electrical and land development services.',intro('CONSTRUCTION SERVICES','One contractor. A range of trades.','From new construction to focused repairs and installations, explore the work GMP can take on in Cainta, Rizal, Pasig and Metro Manila.')+f'<div class="shell section service-layout gallery-layout"><aside aria-label="Service categories"><h2>Browse services</h2>{"".join(f"<a href=\"#{g['id']}\">{e(g['name'])}</a>" for g in services)}</aside><div>{"".join(service_sections)}</div></div>')

filters=[('all','All projects'),('residential','Residential'),('institutional','Institutional'),('interiors','Interiors'),('roofing','Roofing & waterproofing'),('specialty','Specialty works')]
filter_html=''.join(f'<button type="button" data-filter="{key}" aria-pressed="{str(key=="all").lower()}">{e(label)}</button>' for key,label in filters)
page('projects','Project Portfolio | GMP Construction','Browse GMP’s documented construction projects in Rizal, Pasig, Quezon City, Manila, Parañaque and nearby areas, with photos and project details.',intro('PROJECT PORTFOLIO','Documented work across the region','Explore residential builds, institutional projects, interior renovations and specialty works. Open a project to see its photos.')+f'<section class="shell section"><h2>Browse {len(projects)} projects</h2><div class="filters" aria-label="Filter projects" hidden>{filter_html}</div><p class="results" aria-live="polite">{len(projects)} projects</p><div class="project-grid row row-cols-1 row-cols-sm-2 row-cols-lg-3 g-4">{"".join(project_card(p) for p in projects)}</div></section>')

page('about','About GMP Construction | Cainta General Contractor','Meet GMP Construction, a general contractor established in 2019 and based in Cainta, Rizal, serving Pasig, Metro Manila and surrounding areas.',intro('ABOUT GMP','A general contractor based in Cainta','Established in 2019, GMP Construction works on residential, institutional and specialty projects across Rizal, Metro Manila and nearby areas.')+f'''
<section class="shell section about-layout">{image('team.webp','GMP crew working on the exterior of a building')}
<div><p class="eyebrow">OUR APPROACH</p><h2>One team through each stage</h2>{company_intro}
{button('Explore the portfolio','projects.html','outline')}</div></section>
<section class="section tinted"><div class="shell about-columns">
  <article><p class="eyebrow">OUR PURPOSE</p><h2>Mission</h2><p>To provide high-quality service by pursuing excellence for our customers and employees.</p></article>
  <article><p class="eyebrow">OUR DIRECTION</p><h2>Vision</h2><p>To become a leading general contractor in the metro, respected for our service and construction expertise.</p></article>
</div></section>
<section class="shell section"><p class="eyebrow">HOW WE WORK</p><h2>GMP values</h2><dl class="value-grid">
<div><dt>{icon('integrity')}Integrity</dt><dd>Work honestly and communicate transparently.</dd></div>
<div><dt>{icon('reliability')}Reliability</dt><dd>Honor commitments and deliver consistent service.</dd></div>
<div><dt>{icon('resilience')}Resilience</dt><dd>Adapt when site conditions or requirements change.</dd></div>
<div><dt>{icon('safety')}Safety</dt><dd>Put safety first throughout operations.</dd></div>
<div><dt>{icon('excellence')}Excellence</dt><dd>Maintain high standards and improve how we work.</dd></div></dl></section>
<section class="section tinted"><div class="shell about-columns"><div><p class="eyebrow">CONTRACTOR DETAILS</p><h2>GMP Construction</h2><dl class="company-facts"><dt>Business</dt><dd>General contractor, established in 2019</dd><dt>Base</dt><dd>{address}</dd><dt>Capabilities</dt><dd>Planning, design, construction and project management. The company profile lists backhoes, dump trucks, scaffolding, compactors and welding equipment.</dd></dl></div>
<div><p class="eyebrow">TEAM HEADS</p><h2>Leadership</h2><figure class="team-profile">{image('gabriel-marco-pangan.webp','Gabriel Marco Pangan, Managing Director of GMP Construction')}<figcaption><strong>Gabriel Marco Pangan</strong><span>Managing Director</span></figcaption></figure></div></div></section>
''')

options=''.join(f'<optgroup label="{e(g["name"])}">'+''.join(f'<option>{e(name)}</option>' for name,_ in g['items'])+'</optgroup>' for g in services)
page('contact','Contact GMP Construction | Cainta, Rizal','Find GMP Construction contact details and service coverage in Rizal and Metro Manila.',intro('GET IN TOUCH','Contact GMP Construction','For project estimates or consultations, use our dedicated quote and booking page.')+f'''
<section class="shell section contact-layout">
<div><h2>Contact our team</h2><dl class="company-facts"><dt>Phone</dt><dd><a href="tel:+639353938879">{phone}</a></dd><dt>Email</dt><dd><a href="mailto:{email}">{email}</a></dd><dt>Office</dt><dd>{address}</dd></dl>
<iframe class="contact-map" title="Google Maps showing the GMP Construction office address in Cainta" src="https://www.google.com/maps?q={quote(address + ', Philippines')}&amp;output=embed" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
<p><a href="https://www.google.com/maps/search/?api=1&amp;query={quote(address)}">Get directions</a> · <a href="https://m.me/gmpconstructionph">Messenger</a></p>
{button('Quotes and bookings','quote.html','outline')}</div>
<div class="quote-panel">      <!-- NEWSLETTER: Live double opt-in through Cloudflare and Brevo. -->
      <h2>Project updates</h2><p>Get occasional news and project updates from GMP.</p>
      <p class="subscription-notice" data-subscription-notice hidden>Thank you for confirming your email. You can now close this page.</p>
      <form method="post" data-newsletter-form>
        <label for="newsletter-name">Name <span>(optional)</span></label><input id="newsletter-name" name="name" autocomplete="name" maxlength="100">
        <label for="newsletter-email">Email address</label><input id="newsletter-email" name="email" type="email" autocomplete="email" maxlength="160" required>
        <label class="check"><input type="checkbox" name="marketing_opt_in" required> I agree to receive GMP project updates by email.</label>
        <div class="inquiry-verification" data-turnstile></div>
        <button class="button" type="submit" disabled>Join the mailing list</button>
        <p class="form-note">We will email a confirmation link. Confirm to join; you can unsubscribe from any future newsletter.</p>
        <noscript><p>Please enable JavaScript to subscribe, or email contact@gmpconstruction.site for assistance.</p></noscript>
        <p class="status" role="status" aria-live="polite"></p>
      </form>
</div></section>''')
page('quote','Request a Quote or Book a Consultation | GMP Construction','Request a quote or explore consultation booking with GMP Construction.',intro('QUOTES AND BOOKINGS','Tell us about your project','Share the location and scope so the GMP team can assess your requirements.')+f'''
<section class="shell section contact-layout quote-layout"><div><h2>Book a consultation</h2><p>Discuss your project scope, site conditions and next steps with the team.</p>
<div class="booking">
<!-- CALENDLY: Auto-resize adjusts each booking step; keep only one resizing embed on this page. -->
<div class="calendly-inline-widget" data-resize="true" data-url="https://calendly.com/gmpconstructionsite/30min?hide_event_type_details=1&amp;hide_gdpr_banner=1&amp;primary_color=991b1b" style="min-width:320px;height:580px;"></div>
<script type="text/javascript" src="https://assets.calendly.com/assets/external/widget.js" async></script>
<p class="booking-fallback"><a href="https://calendly.com/gmpconstructionsite/30min?hide_event_type_details=1&amp;hide_gdpr_banner=1&amp;primary_color=991b1b" target="_blank" rel="noopener noreferrer">Open calendar in a new tab <span aria-hidden="true">↗</span></a></p>
</div></div>
<div class="quote-panel" id="quote"><h2>Request a quote</h2><p>Fields marked * are required.</p>
<!-- INQUIRY: Connected to the Cloudflare Worker; credentials stay server-side. -->
<form method="post" data-inquiry-form>
<p class="project-context" hidden></p><div class="fields">
<label>Full name *<input name="name" autocomplete="name" required maxlength="100"></label>
<label>Company <span>(optional)</span><input name="company" autocomplete="organization" maxlength="120"></label>
<label>Phone number *<input name="phone" type="tel" autocomplete="tel" required maxlength="35"></label>
<label>Email address *<input name="email" type="email" autocomplete="email" required maxlength="160"></label>
<label>Service needed *<select name="service" id="quote-service" required><option value="">Choose a service</option>{options}<option>Other / multiple services</option></select></label>
<label>Project location *<input name="location" placeholder="City or municipality" required maxlength="160"></label>
<label class="full">Project details *<textarea name="message" rows="5" maxlength="3000" required placeholder="Scope of work, site conditions or target schedule"></textarea></label>
</div><label class="check"><input type="checkbox" name="contact_consent" required> I agree to be contacted about this inquiry.</label>
<div class="inquiry-verification" data-turnstile></div>
<button class="button" type="submit" disabled>Send inquiry</button>
<p class="form-note">Your details will be used to respond to this inquiry. Sending an inquiry does not subscribe you to marketing emails.</p>
<noscript><p>Please enable JavaScript to send this form, or email <a href="mailto:contact@gmpconstruction.site">contact@gmpconstruction.site</a>.</p></noscript>
<p class="status" role="status" aria-live="polite"></p>
</form></div></section>''')

# Publish discovery files at the same root as index.html.
sitemap_entries = ''.join(f'  <url><loc>{e(url)}</loc></url>\n' for url in public_urls)
(SITE/'sitemap.xml').write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + sitemap_entries + '</urlset>\n', encoding='utf-8'
)
(SITE/'robots.txt').write_text(
    f'User-agent: *\nAllow: /\n\nSitemap: {domain}/sitemap.xml\n', encoding='utf-8'
)
