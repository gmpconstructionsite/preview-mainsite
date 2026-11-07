/* Progressive enhancement. All navigation and project descriptions work without JavaScript. */
document.documentElement.classList.add('js');
console.info('GMP Construction showcase v1.6');

const menu = document.querySelector('.menu-toggle');
const drawer = document.querySelector('.mobile-drawer');
menu.addEventListener('click', () => {
  drawer.showModal();
  menu.setAttribute('aria-expanded', 'true');
});
drawer.querySelector('[data-menu-close]').addEventListener('click', () => drawer.close());
drawer.addEventListener('click', event => {
  if (event.target === drawer || event.target.closest('a')) drawer.close();
});
drawer.addEventListener('close', () => menu.setAttribute('aria-expanded', 'false'));
matchMedia('(max-width: 740px)').addEventListener('change', event => {
  if (!event.matches && drawer.open) drawer.close();
});

/* Quote links can preselect a service by its exact published name. */
const serviceSelect = document.querySelector('#quote-service');
const requestedService = new URLSearchParams(location.search).get('service');
if (serviceSelect && [...serviceSelect.options].some(option => option.value === requestedService)) {
  serviceSelect.value = requestedService;
}

/* Portfolio filters preserve all project content in the HTML for accessibility and SEO. */
const filters = document.querySelector('.filters');
if (filters) {
  const cards = [...document.querySelectorAll('.project-column[data-category]')];
  const buttons = [...filters.querySelectorAll('button')];
  filters.hidden = false;
  buttons.forEach(button => button.addEventListener('click', () => {
    const category = button.dataset.filter;
    let visibleCount = 0;
    buttons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    cards.forEach(card => {
      card.hidden = category !== 'all' && card.dataset.category !== category;
      if (!card.hidden) visibleCount += 1;
    });
    document.querySelector('.results').textContent = visibleCount + (visibleCount === 1 ? ' project' : ' projects');
  }));
}

/* PREVIEW ONLY. Wire the live handler to your server endpoint after launch approval.
   Suggested contract: POST JSON to /api/inquiries or /api/newsletter.
   Keep credentials server-side and show success only when the endpoint confirms acceptance. */
document.querySelectorAll('[data-preview-form]').forEach(form => {
  form.addEventListener('submit', event => {
    event.preventDefault();
    form.querySelector('[role="status"]').textContent = 'Preview complete. Your details were not sent or stored.';
  });
  form.querySelector('[type="submit"]').disabled = false;
});

/* The banner rotates on a five-second cadence when motion is allowed. */
const motion = matchMedia('(prefers-reduced-motion: reduce)');
const slides = [...document.querySelectorAll('.hero-slide')];
if (slides.length > 1) {
  let index = 0;
  let timer;
  function updateRotation() {
    clearInterval(timer);
    if (motion.matches || document.hidden) return;
    timer = setInterval(() => {
      if (slides[index].contains(document.activeElement)) return;
      slides[index].hidden = true;
      index = (index + 1) % slides.length;
      slides[index].hidden = false;
    }, 5000);
  }
  document.addEventListener('visibilitychange', updateRotation);
  motion.addEventListener('change', updateRotation);
  updateRotation();
}

/* Animate a few sections once as they enter view. Content stays visible without JavaScript. */
if (!motion.matches && 'IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('reveal-enter');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: .12 });
  document.querySelectorAll('[data-reveal]').forEach(section => observer.observe(section));
}

/* Start the counters once the stats enter view. The HTML contains the final values. */
const stats = document.querySelector('.credibility-grid');
if (stats && !motion.matches && 'IntersectionObserver' in window) {
  const counts = [...stats.querySelectorAll('[data-stat-count]')].map(element => {
    const currency = element.dataset.statFormat === 'currency';
    return {
      element,
      target: Number(element.dataset.statCount),
      finalText: element.textContent,
      format: new Intl.NumberFormat('en-PH', currency ? {
        style: 'currency', currency: 'PHP', minimumFractionDigits: 2, maximumFractionDigits: 2
      } : { maximumFractionDigits: 0 })
    };
  });
  const statsObserver = new IntersectionObserver(([entry]) => {
    if (!entry.isIntersecting) return;
    statsObserver.disconnect();
    if (motion.matches) return;
    const start = performance.now();
    function render(now) {
      const progress = Math.min((now - start) / 1050, 1);
      const eased = 1 - (1 - progress) ** 3;
      counts.forEach(({element, target, finalText, format}) => {
        element.textContent = progress === 1 || motion.matches ? finalText : format.format(target * eased);
      });
      if (progress < 1 && !motion.matches) requestAnimationFrame(render);
    }
    render(start);
  }, { threshold: .2 });
  statsObserver.observe(stats);
}

/* Project gallery. */
const dialog = document.querySelector('.project-dialog');
const photo = dialog.querySelector('.photo-window img');
const viewport = photo.parentElement;
const prev = dialog.querySelector('[data-photo-prev]');
const next = dialog.querySelector('[data-photo-next]');
const zoom = dialog.querySelector('[data-zoom]');
let photos = [];
let currentPhoto = 0;
let trigger;
function setZoom(enabled) {
  viewport.classList.toggle('zoomed', enabled);
  zoom.setAttribute('aria-pressed', String(enabled));
  zoom.querySelector('span').textContent = enabled ? 'Zoom out' : 'Zoom in';
  zoom.setAttribute('aria-label', enabled ? 'Reset photo zoom' : 'Magnify photo');
  viewport.scrollTo(0, 0);
}
function renderPhoto() {
  const item = photos[currentPhoto];
  photo.src = item.src;
  photo.alt = item.alt;
  dialog.querySelector('.photo-caption').textContent = item.alt;
  dialog.querySelector('[data-photo-count]').textContent = (currentPhoto + 1) + ' / ' + photos.length;
  prev.hidden = next.hidden = photos.length < 2;
  setZoom(false);
}
function openProject(details, opener) {
  const card = details.closest('.project');
  trigger = opener;
  photos = [...details.querySelectorAll('figure img')];
  currentPhoto = 0;
  dialog.querySelector('h2').textContent = card.querySelector('h3').textContent;
  dialog.querySelector('.dialog-description').textContent = card.querySelector('.project-content > p:not(.eyebrow)').textContent;
  dialog.querySelector('.dialog-quote').href = details.querySelector('a.button').href;
  renderPhoto();
  if (!dialog.open) dialog.showModal();
}
function movePhoto(offset) {
  if (photos.length < 2) return;
  currentPhoto = (currentPhoto + offset + photos.length) % photos.length;
  renderPhoto();
}
document.querySelectorAll('.project').forEach(card => {
  const details = card.querySelector('.project-evidence');
  [card.querySelector('.project-cover'), details.querySelector('summary')].forEach(opener => {
    opener.addEventListener('click', event => {
      event.preventDefault();
      openProject(details, opener);
    });
  });
});
function openLinkedProject() {
  const details = document.getElementById(location.hash.slice(1));
  if (details?.matches('.project-evidence')) openProject(details, details.querySelector('summary'));
}
window.addEventListener('hashchange', openLinkedProject);
prev.addEventListener('click', () => movePhoto(-1));
next.addEventListener('click', () => movePhoto(1));
zoom.addEventListener('click', () => setZoom(!viewport.classList.contains('zoomed')));
dialog.querySelector('[data-close]').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', event => {
  if (event.target === dialog) dialog.close();
});
dialog.addEventListener('keydown', event => {
  if (viewport.classList.contains('zoomed')) return;
  if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
    event.preventDefault();
    movePhoto(event.key === 'ArrowLeft' ? -1 : 1);
  }
});
dialog.addEventListener('close', () => {
  if (location.hash && document.getElementById(location.hash.slice(1))?.matches('.project-evidence')) {
    history.replaceState(null, '', location.pathname + location.search);
  }
  trigger?.focus();
});
openLinkedProject();

/* Show the originating project while keeping the quote form as the sole inquiry entry point. */
const projectContext = document.querySelector('.project-context');
const originatingProject = new URLSearchParams(location.search).get('project');
if (projectContext && originatingProject) {
  projectContext.textContent = 'Project reference: ' + originatingProject.slice(0, 160);
  projectContext.hidden = false;
}
