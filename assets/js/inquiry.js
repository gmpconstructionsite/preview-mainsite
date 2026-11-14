/* GMP live inquiries v1.8-step3. PUBLIC configuration only; never put secrets here. */
(() => {
  const form = document.querySelector('[data-inquiry-form]');
  if (!form) return;
  const endpoint = 'https://gmp-website-api.gmpconstructionsite.workers.dev/inquiry';
  const sitekey = '0x4AAAAAAGAhzvzBPhJL3ccN';
  const allowedOrigins = new Set(['https://gmpconstruction.site', 'https://www.gmpconstruction.site']);
  const button = form.querySelector('[type="submit"]');
  const status = form.querySelector('[role="status"]');
  const captcha = form.querySelector('[data-turnstile]');
  let token = '', widget, busy = false, completed = false, pending;
  const show = message => { status.textContent = message; };
  const update = () => { button.disabled = busy || completed || !token; };
  if (!allowedOrigins.has(location.origin)) {
    show('To send an inquiry, visit https://gmpconstruction.site/quote.html. This local copy cannot submit.');
    return;
  }
  window.gmpTurnstileReady = () => {
    try {
      widget = window.turnstile.render(captcha, {
        sitekey, action: 'inquiry', theme: 'light', size: 'flexible',
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
    for (const key of ['name', 'company', 'email', 'phone', 'service', 'location', 'message']) {
      data[key] = String(values.get(key) || '').trim();
    }
    data.email = data.email.toLowerCase();
    data.project = (new URLSearchParams(location.search).get('project') || '').slice(0, 200).trim();
    data.sourcePage = location.origin + location.pathname;
    data.contact_consent = values.get('contact_consent') !== null;
    const fingerprint = JSON.stringify(data);
    // Keep the same ID for unchanged retries within this page session.
    // No contact details are written to browser storage.
    if (!pending || pending.fingerprint !== fingerprint) {
      if (!crypto.randomUUID) { show('Please use an updated browser to submit this inquiry.'); return; }
      pending = { fingerprint, submissionId: crypto.randomUUID() };
    }
    const payload = { submissionId: pending.submissionId, turnstileToken: token, data };
    busy = true; token = ''; update(); button.textContent = 'Sending…';
    form.setAttribute('aria-busy', 'true'); show('Sending your inquiry. Please keep this page open.');
    const controls = [...form.querySelectorAll('input,select,textarea')].map(element => ({element, disabled:element.disabled}));
    controls.forEach(({element}) => { element.disabled = true; });
    try {
      const response = await fetch(endpoint, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload), credentials: 'omit', signal: AbortSignal.timeout(65000)
      });
      let result;
      try { result = await response.json(); } catch (_) { throw new Error('UNCONFIRMED'); }
      if (response.ok && result.ok === true && result.saved === true &&
          result.inquiryId === 'GMP-' + pending.submissionId.toLowerCase()) {
        completed = true;
        button.textContent = 'Inquiry received';
        show('Thank you. Your inquiry has been recorded. Reference: ' + result.inquiryId +
          '. Our team will review your requirements. Keep this reference if you contact us.');
      } else if (response.status === 429) {
        show('Too many attempts. Wait one minute, complete verification again, and retry. Your entries are still here.');
      } else if (result.error === 'VERIFICATION_FAILED') {
        show('Verification expired or failed. Complete verification again, then retry.');
      } else if (['INVALID_FIELDS','CONSENT_REQUIRED','INVALID_SOURCE'].includes(result.error)) {
        show('Please check your details and consent, then try again.');
      } else if (result.error === 'SUBMISSION_CONFLICT') {
        show('This reference has already been used. Contact contact@gmpconstruction.site for help.');
      } else { throw new Error('UNCONFIRMED'); }
    } catch (_) {
      show('We could not confirm your submission. Your entries are still here. Retry without changing them or reloading the page, or email contact@gmpconstruction.site.');
    } finally {
      busy = false; form.removeAttribute('aria-busy');
      controls.forEach(({element, disabled}) => { element.disabled = disabled; });
      if (!completed) button.textContent = 'Send inquiry';
      update();
      if (widget !== undefined && window.turnstile) window.turnstile.reset(widget);
    }
  });
  // Load after registering the onload callback, avoiding async script races.
  const script = document.createElement('script');
  script.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js?onload=gmpTurnstileReady&render=explicit';
  script.async = true; script.defer = true;
  script.onerror = () => show('Verification could not load. Check your connection or email contact@gmpconstruction.site.');
  document.head.appendChild(script);
})();
