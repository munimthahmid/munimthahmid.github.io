(() => {
  const root = document.documentElement;
  const preference = window.matchMedia('(prefers-color-scheme: dark)');
  let saved;
  try { saved = localStorage.getItem('munim-theme'); } catch (_) { /* System theme remains available. */ }
  let explicitTheme = saved === 'light' || saved === 'dark' ? saved : null;
  root.dataset.theme = explicitTheme || (preference.matches ? 'dark' : 'light');

  const isDark = () => root.dataset.theme === 'dark';

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
      explicitTheme = isDark() ? 'light' : 'dark';
      root.dataset.theme = explicitTheme;
      try { localStorage.setItem('munim-theme', explicitTheme); } catch (_) { /* Theme still works without storage. */ }
      update();
    });
    preference.addEventListener('change', () => {
      if (!explicitTheme) root.dataset.theme = preference.matches ? 'dark' : 'light';
      update();
    });
    update();
  });
})();
