/* site.js — Too Apps minimal usability helpers */

(function () {
  'use strict';

  /* ── Language Toggle ─────────────────────────────────────── */
  const html = document.documentElement;

  function getLang() {
    return localStorage.getItem('lang') || html.getAttribute('data-lang') || 'zh';
  }

  function setLang(lang) {
    html.setAttribute('data-lang', lang);
    html.setAttribute('lang', lang === 'zh' ? 'zh-Hans' : 'en');
    localStorage.setItem('lang', lang);
    updateTextNodes(lang);
  }

  function updateTextNodes(lang) {
    const key = 'data-' + lang;
    document.querySelectorAll('[data-zh][data-en]').forEach(function (el) {
      const text = el.getAttribute(key);
      if (text !== null) el.innerHTML = text;
    });
  }

  const toggleBtn = document.querySelector('.lang-toggle');
  if (toggleBtn) {
    toggleBtn.addEventListener('click', function () {
      const next = getLang() === 'zh' ? 'en' : 'zh';
      setLang(next);
    });
  }

  // Apply persisted language on load
  const persisted = localStorage.getItem('lang');
  if (persisted && persisted !== html.getAttribute('data-lang')) {
    setLang(persisted);
  }

  /* ── FAQ Accordion ───────────────────────────────────────── */
  document.querySelectorAll('.faq-question').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const expanded = btn.getAttribute('aria-expanded') === 'true';
      const answer = btn.closest('.faq-item').querySelector('.faq-answer');

      btn.setAttribute('aria-expanded', String(!expanded));
      answer.hidden = expanded;
    });
  });

  /* ── Smooth-scroll for anchor links (fallback for older Safari) ── */
  document.querySelectorAll('a[href^="#"]').forEach(function (link) {
    link.addEventListener('click', function (e) {
      const target = document.querySelector(link.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

}());
