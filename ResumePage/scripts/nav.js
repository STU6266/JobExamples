/**
 * nav.js
 * Tiny toggler for the hamburger menu on mobile/tablet.
 * Accessible: updates aria-expanded and closes after a link click.
 */
const navToggle = document.getElementById('nav-toggle');
const navList   = document.getElementById('primary-nav');

if (navToggle && navList) {
  navToggle.addEventListener('click', () => {
    const isOpen = navToggle.getAttribute('aria-expanded') === 'true';
    navToggle.setAttribute('aria-expanded', String(!isOpen));
    navToggle.setAttribute('aria-label', isOpen ? 'Open menu' : 'Close menu');
  });

  // Close menu when a link is clicked (mobile convenience)
  navList.addEventListener('click', (e) => {
    if (e.target.closest('a')) {
      navToggle.setAttribute('aria-expanded', 'false');
      navToggle.setAttribute('aria-label', 'Open menu');
    }
  });

  // Optional: press Escape to close if open
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && navToggle.getAttribute('aria-expanded') === 'true') {
      navToggle.setAttribute('aria-expanded', 'false');
      navToggle.setAttribute('aria-label', 'Open menu');
      navToggle.focus();
    }
  });
}
