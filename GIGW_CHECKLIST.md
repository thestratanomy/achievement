Guidelines for Indian Government Websites (GIGW) — checklist and how to apply

Key items to implement for compliance and accessibility:

- Accessibility (WCAG 2.1 AA / GIGW):
  - Provide semantic HTML, headings, labels and ARIA where necessary.
  - Include a visible skip link (done in `layouts/_default/baseof.html`).
  - Ensure color contrast, keyboard focus styles, and text-scaling support.

- Multilingual support:
  - Serve language-specific pages (set `lang` attribute and provide translations).
  - Provide language switcher in header.

- Metadata and legal:
  - Include contact details, privacy policy, terms, and last updated timestamps.
  - Add structured data where appropriate for press releases and reports.

- Performance & Security:
  - Use static builds (Hugo/Jekyll) and host via CDN.
  - Serve assets with correct caching headers; enable HTTPS.

- Content / Media:
  - Provide downloadable reports as accessible PDFs (tagged PDFs preferred).
  - Provide transcripts for videos and descriptive alt text for images.

- Testing & validation:
  - Run automated accessibility tests (axe, pa11y) and manual assistive-technology checks.
  - Validate HTML and run Lighthouse audits.

How to adapt a third-party theme for GIGW:
- Replace theme header/footer with GIGW-required elements (skip link, contact, language selector).
- Add accessible focus styles and ensure color contrast meets WCAG.
- Ensure all forms and interactive widgets have labels and error messaging.
- Add robots/privacy metadata and a `/.well-known/security.txt` if required.
