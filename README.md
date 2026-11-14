# GMP Construction website v1.8.2 — design polish and signup integration test

## Deploy
Copy this folder's contents to the GitHub repository root, commit and push to main.
Cloudflare Pages deploys from GitHub. index.html remains at the root.
The actual domain is https://gmpconstruction.site.

## Edit
- content.json: service/project copy and photo references.
- build.py: shared layouts, metadata, contact details and forms. Run python3 build.py to rebuild.
- assets/css/site.css: GMP styling.
- assets/js/site.js: navigation, slides and project galleries.
- assets/js/inquiry.js: live quote-form submission.
- assets/js/newsletter.js: live mailing-list signup.
- assets/images: logos, profile photos, illustrative stock and 66 uploaded project photos.
- photo-import-index.csv: original filenames mapped to optimized assets.
Direct HTML changes are overwritten by rebuilds. Python 3.12+ is required for rebuilding.

## Integration configuration
The public Worker URL and Turnstile site key are in the two form scripts.
NEVER place Brevo keys, Turnstile secrets or BACKEND_SHARED_SECRET in this repository.
Live forms require the actual domain; local files and pages.dev previews cannot submit.
Inquiry data is sent to /inquiry with Turnstile action inquiry.
Signup data is sent to /subscribe with Turnstile action subscribe.
Apps Script v1.8-step4 and Worker v1.8-step5 must be deployed first.
Brevo list 3 and active DOI template 1 are configured privately in Apps Script properties.
Signup acknowledgment does not mean delivery or an active subscription.
Existing/suppressed addresses receive the same generic acknowledgment to protect privacy.
No marketing opt-in is inferred from an inquiry.

## Test newsletter
1. Hard-refresh /contact.html on the actual domain.
2. Use your own email that is not already on list 3 or suppressed in Brevo.
3. Give marketing consent, complete verification and submit once.
4. Check Subscribers for Pending confirmation and Email Log for Accepted.
5. Open the email and click Confirm my subscription. Brevo should add the contact to list 3.
6. In Apps Script run syncGmpSubscribers to observe the status change to Active.
7. Enable the 15-minute trigger using enableGmpSubscriberSync only when instructed.
The sync visits up to 40 records per run. Larger lists take multiple runs to refresh.
Confirmed At / Unsubscribed At are first observed timestamps, not exact Brevo event times.
The confirmation query parameter only displays a message; it never activates membership.

## Unsubscribe and remaining validation
Send future newsletter campaigns from Brevo with its unsubscribe link intact.
Brevo suppression applies there immediately. Sheets reflects it on a later sync.
A real opt-in / unsubscribe test remains required before calling mailing-list setup complete.
Native Cloudflare rate limiting and recovery for failed inquiry emails remain follow-up work.
The Worker currently has only a best-effort per-instance throttle.
No analytics integration has been added. Calendly and Messenger keep their existing setup.

## Submission retries
Entries and submission IDs are retained in memory only while the current page stays open.
After an uncertain response, retry unchanged entries without reloading to reuse the ID.
Brevo confirmation failures may require administrator review; do not repeatedly resubmit.
No contact details are stored in localStorage or sessionStorage.

## Checks
Local code and mock integration checks cover payloads, consent, challenge actions,
retry IDs, response handling and preservation of the inquiry form. Live delivery,
confirmation and unsubscribe tests must run on the deployed domain.

## v1.8.2 design updates
- Footer WhatsApp: https://wa.me/639353938879 (same number as Viber/phone).
  GMP must have WhatsApp activated for this number; account availability is not verified.
- Calendly uses its supported data-resize=true option, with a 580px starting height
  instead of a fixed 700px. Calendly controls final internal layout; check both
  date selection and booking details after deployment. No content is cropped.
- Added a versioned 1200x630 JPEG social card, explicit OG size/type/secure URL,
  and Twitter image tags on all six pages. SVG source is included alongside it.
- Minor footer, form focus and mobile spacing refinements preserve GMP branding.
- Inquiry and newsletter JavaScript are unchanged from v1.8.1.
After deployment, verify the social image URL returns image/jpeg and use the
Facebook Sharing Debugger to refresh cached previews for shared page URLs.
