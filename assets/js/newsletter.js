/* GMP newsletter signup v1.8.1-step6. PUBLIC configuration only; never put secrets here. */
(() => {
  const form = document.querySelector('[data-newsletter-form]');
  if (!form) return;
  const endpoint = 'https://gmp-website-api.gmpconstructionsite.workers.dev/subscribe';
  const sitekey = '0x4AAAAAAGAhzvzBPhJL3ccN';
  const allowedOrigins = new Set(['https://gmpconstruction.site', 'https://www.gmpconstruction.site']);
  const button = form.querySelector('[type="submit"]');
  const status = form.querySelector('[role="status"]');
  const captcha = form.querySelector('[data-turnstile]');
  let token = '', widget, busy = false, completed = false, pending;
  const show = message => { status.textContent = message; };
  const update = () => { button.disabled = busy || completed || !token; };
  if (!allowedOrigins.has(location.origin)) {
    show('To join the mailing list, visit https://gmpconstruction.site/contact.html. This local copy cannot submit.');
    return;
  }
  if (new URLSearchParams(location.search).get('subscription') === 'confirmed') {
    const notice = document.querySelector('[data-subscription-notice]');
    if (notice) notice.hidden = false;
    // Only display a thank-you message. Never set membership from URL parameters.
  }
  window.gmpNewsletterTurnstileReady = () => {
    try {
      widget = window.turnstile.render(captcha, {
        sitekey, action: 'subscribe', theme: 'light', size: 'flexible',
        callback(value) { token = value; update(); if (!busy && !completed) show(''); },
        'expired-callback'() { token = ''; update(); },
        'error-callback'() { token = ''; update(); if (!busy) show('Verification could not load. Refresh the page or contact us by email.'); },
        'timeout-callback'() { token = ''; update(); }
      });
    } catch (_) { show('Verification is unavailable. Refresh the page or contact us by email.'); }
  };
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (busy || completed || !form.reportValidity()) return;
    if (!token) { show('Please complete verification before sending.'); return; }
    const values = new FormData(form);
    const data = {};
    for (const key of ['name', 'email']) {
      data[key] = String(values.get(key) || '').trim();
    }
    data.email = data.email.toLowerCase();
    data.sourcePage = location.origin + location.pathname;
    data.marketing_opt_in = values.get('marketing_opt_in') !== null;
    const fingerprint = JSON.stringify(data);
    // Keep the same ID for unchanged retries within this page session.
    // No contact details are written to browser storage.
    if (!pending || pending.fingerprint !== fingerprint) {
      if (!crypto.randomUUID) { show('Please use an updated browser to submit this signup.'); return; }
      pending = { fingerprint, submissionId: crypto.randomUUID() };
    }
    const payload = { submissionId: pending.submissionId, turnstileToken: token, data };
    busy = true; token = ''; update(); button.textContent = 'Sending…';
    form.setAttribute('aria-busy', 'true'); show('Requesting your confirmation email. Please keep this page open.');
    const controls = [...form.querySelectorAll('input,select,textarea')].map(element => ({element, disabled:element.disabled}));
    controls.forEach(({element}) => { element.disabled = true; });
    try {
      const response = await fetch(endpoint, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload), credentials: 'omit', signal: AbortSignal.timeout(65000)
      });
      let result;
      try { result = await response.json(); } catch (_) { throw new Error('UNCONFIRMED'); }
      if (response.ok && result.ok === true && result.pending === true) {
        completed = true;
        button.textContent = 'Request received';
        show('If your address is eligible, a confirmation email will arrive shortly. Check your inbox and Spam folder, then click Confirm my subscription. You will only join the mailing list after confirming.');
      } else if (response.status === 429) {
        show('Too many attempts. Wait one minute, complete verification again, and retry. Your entries are still here.');
      } else if (result.error === 'VERIFICATION_FAILED') {
        show('Verification expired or failed. Complete verification again, then retry.');
      } else if (['INVALID_FIELDS','CONSENT_REQUIRED','INVALID_SOURCE'].includes(result.error)) {
        show('Please check your details and consent, then try again.');
      } else if (result.error === 'SUBSCRIPTION_UNCONFIRMED') {
        show('We could not confirm that your signup email was sent. Please contact contact@gmpconstruction.site if no confirmation email arrives.');
      } else if (result.error === 'SUBMISSION_CONFLICT') {
        show('This reference has already been used. Contact contact@gmpconstruction.site for help.');
      } else { throw new Error('UNCONFIRMED'); }
    } catch (_) {
      show('We could not confirm your submission. Your entries are still here. Retry without changing them or reloading the page, or email contact@gmpconstruction.site.');
    } finally {
      busy = false; form.removeAttribute('aria-busy');
      controls.forEach(({element, disabled}) => { element.disabled = disabled; });
      if (!completed) button.textContent = 'Join the mailing list';
      update();
      if (widget !== undefined && window.turnstile) window.turnstile.reset(widget);
    }
  });
  // Load after registering the onload callback, avoiding async script races.
  const script = document.createElement('script');
  script.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js?onload=gmpNewsletterTurnstileReady&render=explicit';
  script.async = true; script.defer = true;
  script.onerror = () => show('Verification could not load. Check your connection or email contact@gmpconstruction.site.');
  document.head.appendChild(script);
})();
