// ── NAVBAR SCROLL ──
const navbar = document.querySelector('.navbar');
window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 50);
});

// ── HAMBURGER MENU ──
const hamburger = document.querySelector('.hamburger');
const navLinks = document.querySelector('.nav-links');
if (hamburger) {
  hamburger.addEventListener('click', () => {
    navLinks.classList.toggle('open');
    hamburger.classList.toggle('active');
  });
}

// ── ACTIVE NAV LINK ──
const currentPath = window.location.pathname;
document.querySelectorAll('.nav-links a').forEach(link => {
  const href = link.getAttribute('href');
  if (href === currentPath || (currentPath === '/' && href === '/') || 
      (href !== '/' && currentPath.startsWith(href))) {
    link.classList.add('active');
  }
});

// ── FADE UP OBSERVER ──
const fadeEls = document.querySelectorAll('.fade-up');
const observer = new IntersectionObserver((entries) => {
  entries.forEach((e, i) => {
    if (e.isIntersecting) {
      setTimeout(() => e.target.classList.add('visible'), i * 80);
      observer.unobserve(e.target);
    }
  });
}, { threshold: 0.12 });
fadeEls.forEach(el => observer.observe(el));

// ── SKILL BAR ANIMATION ──
const skillFills = document.querySelectorAll('.skill-fill');
if (skillFills.length) {
  const skillObs = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const fill = entry.target;
        fill.style.width = fill.dataset.width + '%';
        skillObs.unobserve(fill);
      }
    });
  }, { threshold: 0.2 });
  skillFills.forEach(fill => skillObs.observe(fill));
}

// ── CURSOR GLOW (desktop) ──
if (window.matchMedia('(pointer: fine)').matches) {
  const glow = document.createElement('div');
  glow.style.cssText = `
    position: fixed; width: 300px; height: 300px; border-radius: 50%;
    background: radial-gradient(circle, rgba(255,230,0,0.06) 0%, transparent 70%);
    pointer-events: none; z-index: 9999; transform: translate(-50%, -50%);
    transition: left 0.12s, top 0.12s; left: -999px; top: -999px;
  `;
  document.body.appendChild(glow);
  document.addEventListener('mousemove', e => {
    glow.style.left = e.clientX + 'px';
    glow.style.top = e.clientY + 'px';
  });
}
