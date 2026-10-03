# Private visitor analytics

## Activation (required)

The integration is installed but **does not collect data until a real website ID is configured**.

1. Create an account you own at https://cloud.umami.is/signup (or use your existing account).
2. Add a website named `Munim Thahmid`, domain `munimthahmid.github.io`.
3. Copy its public `data-website-id` from the tracking snippet into `websiteId` in `assets/analytics-config.json`. Never commit a password, API key, or share URL.
4. Keep website/board sharing disabled and do not add other users. Enable account two-factor authentication if available.
5. Publish the configuration, open the homepage with tracking allowed, and confirm a pageview arrives in Umami. Click Resume and check for a `resume-click` event. Local tests do not establish that the external account is receiving data.
6. Bookmark https://munimthahmid.github.io/admin/analytics/ and use its sign-in link.

The Hobby tier is free, but check current usage and history-retention limits at https://umami.is/pricing before relying on lifetime history. Export data before your plan's retention boundary or choose a plan/deployment that retains the history you need. No paid subscription is created by this integration.

## Access boundary

GitHub Pages cannot run a private database or authenticate a dashboard server-side. `/admin/analytics/` is a public, unlisted entry page, with no visitor records or credentials. The actual dashboard and server-side authentication are hosted by Umami. `noindex` discourages indexing; it is not an access control. Do not embed a shared dashboard or put analytics exports in this public repository.

## Collection

The homepage, publications, experience, and legacy Jekyll layout load the same tracker once per page. The tracker runs only on the production domain. Admin pages are excluded. Missing/invalid configuration and provider outages leave the website usable.

Umami provides pageviews, estimated visitors, visits, referrers, approximate geography, browser/device/OS, and language. Availability depends on the provider and plan. Visits are not a reliable count of named people or persistent cross-device identities. No historical visits can be reconstructed from this integration.

Events: `resume-click`, `paper-click`, `email-click`, `github-click`, `linkedin-click`, `outbound-click`. A click does not prove a completed download or sent email. Events carry no custom recipient, destination, name, or email data. Query strings/fragments and referrer paths are stripped; campaign parameters are consequently not collected. Direct PDF loads do not execute JavaScript and are not counted. Clicks before the tracker loads or during navigation may be missed.

Do Not Track, Global Privacy Control, and the owner/browser exclusion preference are respected. Blocking storage also disables collection. No session replay, fingerprinting code, form contents, GPS requests, or identity enrichment is added. The external analytics provider processes ordinary network requests; consult its current privacy/data-processing terms before activation and maintain appropriate visitor disclosures.

## Verify / maintain

Run `node --test tests/visitor-analytics.test.cjs` (no dependency installation required). Clear `websiteId` to disable collection on subsequent loads. The entry page deliberately says “ID configured” rather than claiming successful data collection. Browser exclusion is stored under `umami.disabled` and is not an authentication mechanism.

References: https://docs.umami.is/docs/collect-data, https://docs.umami.is/docs/tracker-configuration, https://docs.umami.is/docs/tracker-functions
