/**
 * 拜茨清洁 — 全局脚本
 * www.biocce.cn
 */

(function() {
  'use strict';

  /* ── 1. Header Scroll Effect ── */
  const header = document.querySelector('.header');
  let lastScroll = 0;

  window.addEventListener('scroll', function() {
    const scrollY = window.scrollY;
    if (scrollY > 50) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
    lastScroll = scrollY;
  }, { passive: true });

  /* ── 2. Mobile Menu Toggle ── */
  const menuToggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.nav');

  if (menuToggle && nav) {
    menuToggle.addEventListener('click', function() {
      nav.classList.toggle('open');
      menuToggle.classList.toggle('open');
    });

    // Close menu on link click
    nav.querySelectorAll('a').forEach(function(link) {
      link.addEventListener('click', function() {
        nav.classList.remove('open');
        menuToggle.classList.remove('open');
      });
    });
  }

  /* ── 3. Fade-in on Scroll ── */
  const fadeElements = document.querySelectorAll('.fade-in');

  if (fadeElements.length && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.1,
      rootMargin: '0px 0px -40px 0px'
    });

    fadeElements.forEach(function(el) {
      observer.observe(el);
    });
  } else {
    // Fallback: show all
    fadeElements.forEach(function(el) {
      el.classList.add('visible');
    });
  }

  /* ── 4. Category Sidebar Toggle ── */
  document.querySelectorAll('.cat-item.has-sub').forEach(function(item) {
    item.addEventListener('click', function(e) {
      e.stopPropagation();
      this.classList.toggle('open');
    });
  });

  /* ── 5. Category Filter Tabs (Products Page) ── */
  document.querySelectorAll('.cat-tab').forEach(function(tab) {
    tab.addEventListener('click', function() {
      const cat = this.dataset.cat;
      // Update active tab
      document.querySelectorAll('.cat-tab').forEach(function(t) {
        t.style.background = 'var(--card)';
        t.style.color = 'var(--text)';
      });
      this.style.background = 'var(--primary)';
      this.style.color = '#fff';

      // Show/hide sections
      document.querySelectorAll('[data-cat-group]').forEach(function(group) {
        if (cat === 'all' || group.dataset.catGroup === cat) {
          group.style.display = '';
        } else {
          group.style.display = 'none';
        }
      });
    });
  });

  /* ── 6. Brand Page Pagination ── */
  document.querySelectorAll('.pg-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
      if (this.disabled) return;
      const page = this.dataset.page;
      if (page) {
        document.querySelectorAll('.brand-block').forEach(function(b) {
          b.style.display = 'none';
        });
        document.querySelectorAll('.brand-block[data-page="' + page + '"]').forEach(function(b) {
          b.style.display = '';
        });
        document.querySelectorAll('.pg-btn').forEach(function(p) {
          p.classList.remove('on');
        });
        this.classList.add('on');
      }
    });
  });

  /* ── 7. Solution Page Pagination ── */
  document.querySelectorAll('.sol-pages .pg-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
      if (this.disabled) return;
      const page = this.dataset.page;
      if (page) {
        document.querySelectorAll('.sol-grid .sol-card').forEach(function(c) {
          c.style.display = 'none';
        });
        document.querySelectorAll('.sol-grid .sol-card[data-page="' + page + '"]').forEach(function(c) {
          c.style.display = '';
        });
        document.querySelectorAll('.sol-pages .pg-btn').forEach(function(p) {
          p.classList.remove('on');
        });
        this.classList.add('on');
      }
    });
  });

})();
