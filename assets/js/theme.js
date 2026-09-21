(() => {
  const root = document.documentElement;
  const preference = window.matchMedia('(prefers-color-scheme: dark)');
  let saved;
  try { saved = localStorage.getItem('munim-theme'); } catch (_) { /* System theme remains available. */ }
  if (saved === 'light' || saved === 'dark') root.dataset.theme = saved;

  const isDark = () => root.dataset.theme ? root.dataset.theme === 'dark' : preference.matches;

  document.addEventListener('DOMContentLoaded', () => {
    const button = document.querySelector('.theme-toggle');
    if (!button) return;
    const update = () => {
      const label = isDark() ? 'Switch to light mode' : 'Switch to dark mode';
      button.setAttribute('aria-label', label);
      button.title = label;
      document.querySelector('meta[name="theme-color"]').content = isDark() ? '#111a23' : '#ffffff';
    };
    button.style.display = 'inline-flex';
    button.addEventListener('click', () => {
      root.dataset.theme = isDark() ? 'light' : 'dark';
      try { localStorage.setItem('munim-theme', root.dataset.theme); } catch (_) { /* Theme still works without storage. */ }
      update();
    });
    preference.addEventListener('change', update);
    update();
  });
})();
