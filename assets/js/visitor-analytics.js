/* The website ID is public. Passwords and API keys must never go in this repo. */
(function () {
  'use strict';
  var host = 'munimthahmid.github.io';
  if (window.__visitorAnalyticsLoaded) return;
  window.__visitorAnalyticsLoaded = true;

  function excluded() {
    if (location.hostname !== host || /^\/admin(?:\/|$)/.test(location.pathname)) return true;
    if (navigator.doNotTrack === '1' || navigator.globalPrivacyControl === true) return true;
    try { return localStorage.getItem('umami.disabled') === '1'; }
    catch (_) { return true; }
  }
  if (excluded()) return;

  // Strip arbitrary query strings, fragments and referrer paths before sending.
  window.portfolioAnalyticsBeforeSend = function (type, payload) {
    if (excluded()) return false;
    var clean = Object.assign({}, payload);
    try { clean.url = new URL(payload.url || location.pathname, location.origin).pathname; }
    catch (_) { return false; }
    if (clean.referrer) {
      try { clean.referrer = new URL(clean.referrer).origin; }
      catch (_) { clean.referrer = ''; }
    }
    return clean;
  };

  fetch('/assets/analytics-config.json', { cache: 'no-cache', credentials: 'omit' })
    .then(function (response) {
      if (!response.ok) throw new Error('Analytics configuration unavailable');
      return response.json();
    })
    .then(function (config) {
      if (excluded() || !/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(config.websiteId || '')) return;
      var script = document.createElement('script');
      script.src = 'https://cloud.umami.is/script.js';
      script.async = true;
      script.setAttribute('data-website-id', config.websiteId);
      script.setAttribute('data-domains', host);
      script.setAttribute('data-do-not-track', 'true');
      script.setAttribute('data-exclude-search', 'true');
      script.setAttribute('data-exclude-hash', 'true');
      script.setAttribute('data-before-send', 'portfolioAnalyticsBeforeSend');
      document.head.appendChild(script);

      document.addEventListener('click', function (event) {
        if (excluded() || !window.umami || !event.target.closest) return;
        var anchor = event.target.closest('a[href]');
        if (!anchor) return;
        var url;
        try { url = new URL(anchor.href, location.origin); } catch (_) { return; }
        var name;
        if (url.protocol === 'mailto:') name = 'email-click';
        else if (url.origin === location.origin && /\/Munim_Thahmid_Resume\.pdf$/i.test(url.pathname)) name = 'resume-click';
        else if (url.protocol === 'https:' && url.hostname === 'github.com') name = 'github-click';
        else if (url.protocol === 'https:' && url.hostname === 'www.linkedin.com') name = 'linkedin-click';
        else if (url.origin === location.origin && /\.pdf$/i.test(url.pathname)) name = 'paper-click';
        else if (url.protocol === 'https:' && url.origin !== location.origin) name = 'outbound-click';
        if (name) {
          try { Promise.resolve(window.umami.track(name)).catch(function () {}); }
          catch (_) { /* Analytics must never interrupt navigation. */ }
        }
      });
    })
    .catch(function () { /* The website remains usable when analytics is unavailable. */ });
}());
