/**
 * contact.js
 * Lightweight modal contact handler for this site.
 *
 * What it does
 * ------------
 * - Opens/closes the contact modal (with overlay)
 * - Focus management for accessibility (focus goes into the modal on open and
 *   returns to the trigger on close; ESC closes the modal)
 * - Sends a prefilled email via `mailto:` using the textarea content
 *
 * Assumptions
 * -----------
 * - The page contains elements with the following IDs:
 *     #contact-button, #contact-modal, #modal-overlay, #close-button, #send-button
 *   and a <textarea> inside #contact-modal.
 * - This script is loaded at the end of <body> so the DOM is ready.
 *
 * Notes
 * -----
 * - If any required element is missing, the script fails gracefully (no errors).
 * - The code aims to be readable and "human"—practical comments explain the why,
 *   not just the what.
 */

// Cache DOM references up front
const contactButton = document.getElementById('contact-button');
const contactModal  = document.getElementById('contact-modal');
const modalOverlay  = document.getElementById('modal-overlay');

// These live inside the modal
const closeButton   = contactModal ? contactModal.querySelector('#close-button') : null;
const sendButton    = contactModal ? contactModal.querySelector('#send-button')  : null;
const messageField  = contactModal ? contactModal.querySelector('textarea')      : null;

// If core pieces are missing, exit quietly (prevents console errors on pages without a modal)
if (!contactButton || !contactModal || !modalOverlay || !closeButton || !sendButton || !messageField) {
  // Optional: surface a small hint for developers in the console
  // console.warn('[contact.js] Modal markup not found. Skipping contact modal wiring.');
} else {
  // --- Accessibility setup (done once) --------------------------------------

  // Give the modal proper dialog semantics so screen readers understand the context
  contactModal.setAttribute('role', 'dialog');
  contactModal.setAttribute('aria-modal', 'true');

  // Point aria-labelledby to the modal title if it exists; create an ID if needed
  const modalTitle = contactModal.querySelector('h2');
  if (modalTitle) {
    if (!modalTitle.id) modalTitle.id = 'contact-modal-title';
    contactModal.setAttribute('aria-labelledby', modalTitle.id);
  }

  // Track the element that opened the modal so we can restore focus later
  let lastFocusedElement = null;

  // Keep a list of focusable elements inside the modal for a lightweight focus trap
  const getFocusable = () => {
    // This selector covers common interactive elements
    return contactModal.querySelectorAll(
      'a[href], button:not([disabled]), textarea, input, select, [tabindex]:not([tabindex="-1"])'
    );
  };

  // We'll also remember and restore the page's scroll state
  let previousBodyOverflow = '';

  // Toggle helpers ------------------------------------------------------------

  const openModal = () => {
    // Save current focus to restore it when closing
    lastFocusedElement = document.activeElement;

    // Show modal & overlay
    contactModal.style.display = 'block';
    modalOverlay.style.display = 'block';

    // Prevent body scroll while the modal is open (no CSS class required)
    previousBodyOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';

    // Move focus into the modal (textarea is a sensible default)
    messageField.focus();

    // Listen for keydown to support ESC close and focus trap
    document.addEventListener('keydown', handleKeydown);
  };

  const closeModal = () => {
    // Hide modal & overlay
    contactModal.style.display = 'none';
    modalOverlay.style.display = 'none';

    // Re-enable body scroll
    document.body.style.overflow = previousBodyOverflow;

    // Remove keydown listener
    document.removeEventListener('keydown', handleKeydown);

    // Clear the message (optional—feels tidy after sending/cancelling)
    // Comment out if you'd like to persist the draft between opens.
    // messageField.value = '';

    // Return focus to the button that opened the modal (if it still exists)
    if (lastFocusedElement && typeof lastFocusedElement.focus === 'function') {
      lastFocusedElement.focus();
    }
  };

  // Key handling: ESC to close, TAB to loop focus inside the modal
  const handleKeydown = (e) => {
    if (e.key === 'Escape') {
      e.preventDefault();
      closeModal();
      return;
    }

    if (e.key === 'Tab') {
      const focusable = getFocusable();
      if (!focusable.length) return;

      const first = focusable[0];
      const last  = focusable[focusable.length - 1];

      // If Shift+Tab on first, wrap to last; if Tab on last, wrap to first
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    }
  };

  // Mail helper: build a clean mailto URL (in English)
  const buildMailtoHref = (to, subject, body) => {
    const parts = [
      `mailto:${encodeURIComponent(to)}`,
      `subject=${encodeURIComponent(subject)}`,
      `body=${encodeURIComponent(body)}`
    ];
    // Use '?' for the first param and '&' for the rest
    return `${parts.shift()}?${parts.join('&')}`;
  };

  // Send action: basic validation + open the user's mail client
  const handleSend = () => {
    const text = messageField.value.trim();

    if (!text) {
      alert('Please type a short message before sending.');
      messageField.focus();
      return;
    }

    // It helps to include where the message was sent from (page URL)
    const contextLine = `\n\n— Sent from: ${window.location.href}`;
    const body = `${text}${contextLine}`;

    // Update these if you ever change your contact address or want a different subject line
    const recipient = 'stevenkemendics@gmail.com';
    const subject   = 'Message from portfolio website';

    // Trigger the user’s email client
    window.location.href = buildMailtoHref(recipient, subject, body);

    // Wipe the textarea and close the modal (feels complete)
    messageField.value = '';
    closeModal();
  };

  // Event wiring --------------------------------------------------------------

  // Open via the fixed "Contact Me" button
  contactButton.addEventListener('click', openModal);

  // Close via the “Close” button
  closeButton.addEventListener('click', closeModal);

  // Close by clicking the shaded overlay
  modalOverlay.addEventListener('click', closeModal);

  // Send via the “Send” button
  sendButton.addEventListener('click', handleSend);
}
