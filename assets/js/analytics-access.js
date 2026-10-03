(function () {
  'use strict';
  var status = document.getElementById('tracking-status');
  fetch('/assets/analytics-config.json', { cache: 'no-cache', credentials: 'omit' })
    .then(function (response) { if (!response.ok) throw new Error(); return response.json(); })
    .then(function (config) {
      var configured = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(config.websiteId || '');
      status.textContent = configured
        ? 'Tracking ID configured. Open the dashboard to verify incoming visits.'
        : 'Tracking is not active yet. The owner’s Umami website ID still needs to be connected.';
    })
    .catch(function () { status.textContent = 'Could not check tracking configuration. Try refreshing this page.'; });

  var button = document.getElementById('exclude-visits');
  var note = document.getElementById('exclusion-status');
  function render() {
    try {
      var excluded = localStorage.getItem('umami.disabled') === '1';
      button.disabled = false;
      button.textContent = excluded ? 'Include this browser’s visits' : 'Exclude this browser’s visits';
      button.setAttribute('aria-pressed', String(excluded));
      note.textContent = excluded ? 'Visits from this browser are excluded.' : 'Visits from this browser are eligible to be counted when tracking is active and privacy settings allow it.';
    } catch (_) {
      button.disabled = true;
      button.textContent = 'Browser storage is unavailable';
      note.textContent = 'Tracking is disabled when this browser’s storage cannot be read.';
    }
  }
  button.addEventListener('click', function () {
    try {
      if (localStorage.getItem('umami.disabled') === '1') localStorage.removeItem('umami.disabled');
      else localStorage.setItem('umami.disabled', '1');
      render();
    } catch (_) { note.textContent = 'Could not save this preference. Check your browser’s storage settings.'; }
  });
  render();
}());
