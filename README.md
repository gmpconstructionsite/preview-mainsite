# GMP Construction website showcase v1.6

Open `index.html` in a browser after extracting the ZIP. All six pages
work locally. The extracted folder is the GitHub Pages publishing root.

## Edit and rebuild

- `content.json` holds all service and project copy, photo references and source pages.
- `build.py` holds shared navigation, footer, contact details, SEO tags and page templates.
- `assets/css/site.css` holds the layout and brand colors.
- `assets/js/site.js` holds the menu, portfolio filters and preview form handlers.
- `assets/images/` holds the supplied logos and company-profile photography.

Run `python3 build.py` using Python 3.12 or later after editing a template or the
content file. The generated HTML can also be edited directly for a quick
review, but those edits will be overwritten by the next build.

The 17 projects are documented in the 2025 profile (PDF pages 5–9). The review
copy shows only the aggregate portfolio contract value. Dates are the dates printed in the profile.
Content and project claims must be verified and approved by GMP Construction.

## Integration handoff

Search `build.py` for ANALYTICS, GTM, MESSENGER, CALENDLY, INQUIRY and NEWSLETTER.
The markup has separate inquiry and mailing list forms. The JavaScript
demonstrates validation and feedback without retaining or transmitting entries.

1. Confirm the approved content, privacy notice, business email and final domain.
2. Add a server endpoint for inquiries. Validate input, check for spam, record the
   lead in a private Google Sheet, and send an internal alert and a client
   acknowledgment through the selected email service. Keep provider credentials
   outside the site files. Use a separate opt-in flow and unsubscribe handling
   for the newsletter.
3. Connect and test Calendly, Google Calendar and Zoom. Add the approved
   analytics and messaging snippets only after the relevant setup is ready.
4. Test the forms and confirmation delivery before launch. Confirm the canonical URLs, sharing image and discovery files on the final domain.

Example launch endpoint contract (illustrative, no live endpoint in this draft):

```text
POST /api/inquiries
Content-Type: application/json

{ "name": "...", "company": "", "phone": "...", "email": "...",
  "service": "...", "location": "...", "message": "...", "contact_consent": true }

POST /api/newsletter
Content-Type: application/json

{ "name": "", "email": "...", "marketing_opt_in": true }
```

## Service photo credits

Illustrative images are bundled for offline viewing under the [Pexels license](https://www.pexels.com/license/). GMP project photos remain identified separately.

- [Construction site review](https://www.pexels.com/photo/8961065/)
- [Reviewing drawings](https://www.pexels.com/photo/1216589/)
- [Interior painting](https://www.pexels.com/photo/6474471/)
- [Wall finishing](https://www.pexels.com/photo/5691622/)

## GitHub Pages deployment

Upload the contents of the extracted folder to the repository root. In Settings
→ Pages, select Deploy from a branch, choose the publishing branch and /(root).
The CNAME file names the intended custom domain, gmpconstruction.site. Configure
that domain in Pages and point its DNS to GitHub Pages for the actual repository
owner. Verify HTTPS once DNS and the certificate are ready.

The root contains robots.txt, sitemap.xml and llms.txt. Canonical URLs and the
sitemap target https://gmpconstruction.site. The HTML permits indexing. The
quote and newsletter forms and booking are still previews.

The homepage contract value is the sum of the distinct projects listed in the
2025 company profile (pages 5–9), saved as an aggregate in content.json. The Dasmariñas fit-out is counted
once despite appearing in two photo panels. The map uses the published office
address and requires internet access. Confirm the map pin before launch.

## Version history

- **v1.6 (2026-11-07):** Simplified the homepage statistics to an alternating red and white 2×2 grid, with a one-time count-up animation for the three numeric figures.

- **v1.5 (2026-11-07):** Added portfolio statistics and an embedded office map. Simplified service cards and galleries, and added branded icons to GMP values.

- **v1.4 (2026-11-07):** Moved all pages and assets to the publishing root. Added crawler discovery files and a GitHub Pages custom domain configuration.

- **v1.3 (2026-11-07):** Simplified the homepage and About page, added automatic banner rotation and a mobile navigation drawer, moved project gallery controls over the image, and rebuilt the Services page as photo galleries. Version reporting moved to the browser console.

- **v1.2 (2026-11-07):** Standardized spacing, photo crops, and corner radii. Used the locally bundled Bootstrap 5.3.3 grid and flex display utilities to align service and project cards within each row. The package works offline without Bootstrap JavaScript.

- **v1.1 (2026-11-07):** Added the homepage slideshow, company introduction, service galleries, project modal with zoom, expanded About page, and a dedicated Quotes and Bookings page. Moved the newsletter form to Contact and simplified the footer.
- **v1.0 (2026-11-07):** Initial five-page showcase with 13 services and 17 projects.

Use the version in the ZIP filename or browser console when giving feedback.
