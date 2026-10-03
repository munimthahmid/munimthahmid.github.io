const { test } = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');
const root = path.join(__dirname, '..');
const source = fs.readFileSync(path.join(root, 'assets/js/visitor-analytics.js'), 'utf8');
const id = '12345678-1234-4234-8234-123456789abc';

async function run(options = {}) {
  const scripts = [], events = [], handlers = {}, requests = [];
  const storage = new Map(options.excluded ? [['umami.disabled', '1']] : []);
  const context = {
    URL, Promise,
    location: { hostname: options.host || 'munimthahmid.github.io', pathname: options.pathname || '/', origin: 'https://munimthahmid.github.io' },
    navigator: { doNotTrack: options.dnt, globalPrivacyControl: options.gpc },
    localStorage: { getItem(key) { if (options.storageError) throw new Error(); return storage.get(key); } },
    document: {
      createElement() { return { attributes: {}, setAttribute(key, value) { this.attributes[key] = value; } }; },
      head: { appendChild(script) { scripts.push(script); } },
      addEventListener(name, handler) { handlers[name] = handler; }
    },
    fetch: async function (url) {
      requests.push(url);
      if (options.networkError) throw new Error();
      return { ok: options.ok !== false, json: async () => ({ websiteId: options.id === undefined ? id : options.id }) };
    },
    umami: { track(name) { events.push(name); return Promise.resolve(); } }
  };
  context.window = context;
  vm.createContext(context);
  vm.runInContext(source, context);
  await new Promise(resolve => setImmediate(resolve));
  return { context, scripts, events, handlers, requests, storage };
}

test('production loads one tracker with privacy configuration; repeated inclusion is idempotent', async () => {
  const r = await run();
  assert.equal(r.scripts.length, 1);
  assert.equal(r.scripts[0].src, 'https://cloud.umami.is/script.js');
  assert.equal(r.scripts[0].attributes['data-website-id'], id);
  assert.equal(r.scripts[0].attributes['data-before-send'], 'portfolioAnalyticsBeforeSend');
  vm.runInContext(source, r.context);
  await new Promise(resolve => setImmediate(resolve));
  assert.equal(r.scripts.length, 1);
});

test('admin, preview, DNT, GPC, owner exclusion, and blocked storage make no requests', async () => {
  for (const options of [{ pathname: '/admin' }, { pathname: '/admin/analytics/' }, { host: 'localhost' }, { dnt: '1' }, { gpc: true }, { excluded: true }, { storageError: true }]) {
    const r = await run(options);
    assert.equal(r.requests.length, 0, JSON.stringify(options));
    assert.equal(r.scripts.length, 0);
  }
});

test('missing or invalid ID and network failures never load the provider', async () => {
  for (const options of [{ id: '' }, { id: 'not-a-website-id' }, { ok: false }, { networkError: true }]) {
    assert.equal((await run(options)).scripts.length, 0);
  }
});

test('query strings, fragments, and referrer paths cannot leave via the tracker', async () => {
  const r = await run();
  const input = { url: '/publications/?email=private@example.com#token', referrer: 'https://example.com/private?secret=1#token', title: 'Publications' };
  const output = r.context.portfolioAnalyticsBeforeSend('event', input);
  assert.equal(output.url, '/publications/');
  assert.equal(output.referrer, 'https://example.com');
  assert.equal(output.title, 'Publications');
  assert.equal(input.url, '/publications/?email=private@example.com#token');
  r.storage.set('umami.disabled', '1');
  assert.equal(r.context.portfolioAnalyticsBeforeSend('event', input), false);
});

test('link events use fixed categories without recipient or destination data', async () => {
  const r = await run();
  const click = href => r.handlers.click({ target: { closest: () => ({ href }) } });
  click('/files/Munim_Thahmid_Resume.pdf?private=1');
  click('mailto:private@example.com?body=secret');
  click('https://github.com/munimthahmid');
  click('https://www.linkedin.com/in/munimthahmid/');
  click('/files/paper.pdf');
  click('https://example.org/private');
  click('/experience/');
  click('javascript:void(0)');
  assert.deepEqual(r.events, ['resume-click', 'email-click', 'github-click', 'linkedin-click', 'paper-click', 'outbound-click']);
  r.storage.set('umami.disabled', '1');
  click('/files/paper.pdf');
  assert.equal(r.events.length, 6);
});

test('provider errors never cancel link navigation', async () => {
  const r = await run();
  r.context.umami.track = () => { throw new Error('blocked'); };
  assert.doesNotThrow(() => r.handlers.click({ target: { closest: () => ({ href: '/files/paper.pdf' }) } }));
});

test('tracking is wired to all active layouts; entry page is untracked and unlisted', () => {
  for (const file of ['index.html', 'publications/index.html', 'experience/index.html', '_includes/scripts.html']) {
    const content = fs.readFileSync(path.join(root, file), 'utf8');
    assert.equal(content.split('/assets/js/visitor-analytics.js').length - 1, 1);
    assert.ok(!content.includes('/admin/analytics/'));
  }
  const entry = fs.readFileSync(path.join(root, 'admin/analytics/index.html'), 'utf8');
  assert.ok(entry.includes('noindex, nofollow, noarchive'));
  assert.ok(entry.includes('https://cloud.umami.is/login'));
  assert.ok(!entry.includes('visitor-analytics.js'));
  assert.ok(!entry.includes('type="password"'));
  const config = JSON.parse(fs.readFileSync(path.join(root, 'assets/analytics-config.json'), 'utf8'));
  assert.deepEqual(Object.keys(config), ['websiteId']);
});

test('entry page distinguishes unconfigured tracking and persists browser exclusion', async () => {
  const storage = new Map();
  const elements = Object.fromEntries(['tracking-status', 'exclude-visits', 'exclusion-status'].map(key => [key, {
    textContent: '', disabled: true, setAttribute() {}, addEventListener(name, callback) { this[name] = callback; }
  }]));
  const context = { document: { getElementById: key => elements[key] }, localStorage: {
    getItem: key => storage.get(key), setItem: (key, value) => storage.set(key, value), removeItem: key => storage.delete(key)
  }, fetch: async () => ({ ok: true, json: async () => ({ websiteId: '' }) }) };
  vm.runInNewContext(fs.readFileSync(path.join(root, 'assets/js/analytics-access.js'), 'utf8'), context);
  await new Promise(resolve => setImmediate(resolve));
  assert.match(elements['tracking-status'].textContent, /not active/);
  elements['exclude-visits'].click();
  assert.equal(storage.get('umami.disabled'), '1');
  assert.match(elements['exclusion-status'].textContent, /are excluded/);
  elements['exclude-visits'].click();
  assert.equal(storage.has('umami.disabled'), false);
});
