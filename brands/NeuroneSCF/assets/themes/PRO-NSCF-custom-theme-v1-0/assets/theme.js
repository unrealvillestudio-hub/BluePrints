/* ═══════════════════════════════════════════════════════════════
   NEURONE COSMÉTICA — THEME.JS v1.0
   Unreal>ille Studio
   ═══════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  // ── HEADER SCROLL ────────────────────────────────────────────
  const header = document.querySelector('.nc-header');
  if (header) {
    const onScroll = () => {
      header.classList.toggle('scrolled', window.scrollY > 40);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // ── MOBILE MENU ──────────────────────────────────────────────
  const mobileToggle = document.querySelector('.nc-mobile-toggle');
  const mobileMenu = document.querySelector('.nc-mobile-menu');
  if (mobileToggle && mobileMenu) {
    mobileToggle.addEventListener('click', () => {
      mobileMenu.classList.toggle('open');
      mobileToggle.setAttribute(
        'aria-expanded',
        mobileMenu.classList.contains('open')
      );
    });
    document.addEventListener('click', (e) => {
      if (!mobileToggle.contains(e.target) && !mobileMenu.contains(e.target)) {
        mobileMenu.classList.remove('open');
      }
    });
  }

  // ── CART DRAWER ──────────────────────────────────────────────
  const cartOverlay = document.querySelector('.nc-cart-overlay');
  const cartDrawer = document.querySelector('.nc-cart-drawer');
  const cartClose = document.querySelector('.nc-cart-close');
  const cartTriggers = document.querySelectorAll('[data-cart-toggle]');

  function openCart() {
    if (!cartOverlay || !cartDrawer) return;
    cartOverlay.classList.add('open');
    cartDrawer.classList.add('open');
    document.body.style.overflow = 'hidden';
    refreshCart();
  }

  function closeCart() {
    if (!cartOverlay || !cartDrawer) return;
    cartOverlay.classList.remove('open');
    cartDrawer.classList.remove('open');
    document.body.style.overflow = '';
  }

  cartTriggers.forEach(t => t.addEventListener('click', openCart));
  if (cartClose) cartClose.addEventListener('click', closeCart);
  if (cartOverlay) cartOverlay.addEventListener('click', closeCart);

  function refreshCart() {
    fetch('/cart.js')
      .then(r => r.json())
      .then(cart => {
        // Update badge
        document.querySelectorAll('.nc-cart-count').forEach(b => {
          b.textContent = cart.item_count;
          b.style.display = cart.item_count > 0 ? 'flex' : 'none';
        });

        // Update items list
        const itemsList = document.querySelector('.nc-cart-items');
        const totalPrice = document.querySelector('.nc-cart-total-price');
        if (!itemsList) return;

        if (cart.items.length === 0) {
          itemsList.innerHTML = '<p style="text-align:center;padding:32px 0;color:var(--nc-text-muted);font-size:.85rem;">Tu carrito está vacío</p>';
        } else {
          itemsList.innerHTML = cart.items.map(item => `
            <div class="nc-cart-item">
              <div class="nc-cart-item-img">
                <img src="${item.featured_image?.url || ''}" alt="${item.title}" loading="lazy">
              </div>
              <div class="nc-cart-item-info">
                <div class="nc-cart-item-name">${item.product_title}</div>
                <div style="font-size:.78rem;color:var(--nc-text-muted);margin:3px 0;">${item.variant_title !== 'Default Title' ? item.variant_title : ''}</div>
                <div style="display:flex;justify-content:space-between;align-items:center;margin-top:8px;">
                  <div class="nc-cart-item-price">${formatMoney(item.final_line_price)}</div>
                  <div style="display:flex;align-items:center;gap:8px;">
                    <button onclick="updateCart(${item.key},${item.quantity - 1})" style="width:24px;height:24px;display:flex;align-items:center;justify-content:center;border:1px solid var(--nc-border);border-radius:3px;color:var(--nc-text-muted);cursor:pointer;background:transparent;font-size:1rem;transition:var(--nc-transition-fast)" onmouseover="this.style.color='white'" onmouseout="this.style.color='var(--nc-text-muted)'">−</button>
                    <span style="font-size:.85rem;color:var(--nc-white);min-width:20px;text-align:center">${item.quantity}</span>
                    <button onclick="updateCart(${item.key},${item.quantity + 1})" style="width:24px;height:24px;display:flex;align-items:center;justify-content:center;border:1px solid var(--nc-border);border-radius:3px;color:var(--nc-text-muted);cursor:pointer;background:transparent;font-size:1rem;transition:var(--nc-transition-fast)" onmouseover="this.style.color='white'" onmouseout="this.style.color='var(--nc-text-muted)'">+</button>
                  </div>
                </div>
              </div>
            </div>
          `).join('');
        }

        if (totalPrice) {
          totalPrice.textContent = formatMoney(cart.total_price);
        }
      });
  }

  window.updateCart = function (key, quantity) {
    fetch('/cart/change.js', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id: key, quantity })
    })
      .then(r => r.json())
      .then(() => refreshCart());
  };

  function formatMoney(cents) {
    return '$' + (cents / 100).toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  }

  // ── ADD TO CART ──────────────────────────────────────────────
  const addToCartForms = document.querySelectorAll('[data-product-form]');
  addToCartForms.forEach(form => {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const btn = form.querySelector('[data-add-to-cart-btn]');
      const variantId = form.querySelector('[name="id"]')?.value;
      const qty = form.querySelector('[name="quantity"]')?.value || 1;
      if (!variantId) return;

      if (btn) {
        btn.disabled = true;
        btn.textContent = 'Agregando...';
      }

      try {
        await fetch('/cart/add.js', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ id: variantId, quantity: parseInt(qty) })
        });
        openCart();
      } catch (err) {
        console.error('Error adding to cart:', err);
      } finally {
        if (btn) {
          btn.disabled = false;
          btn.textContent = 'Agregar al Carrito';
        }
      }
    });
  });

  // ── QUICK ADD (product cards) ────────────────────────────────
  document.querySelectorAll('[data-quick-add]').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      const variantId = btn.dataset.quickAdd;
      if (!variantId) return;
      btn.textContent = '✓';
      btn.disabled = true;
      try {
        await fetch('/cart/add.js', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ id: variantId, quantity: 1 })
        });
        openCart();
      } catch (_) {}
      setTimeout(() => {
        btn.textContent = 'Agregar';
        btn.disabled = false;
      }, 1800);
    });
  });

  // ── PRODUCT GALLERY ──────────────────────────────────────────
  const galleryMain = document.querySelector('.nc-gallery-main img');
  const galleryThumbs = document.querySelectorAll('.nc-gallery-thumb');
  galleryThumbs.forEach(thumb => {
    thumb.addEventListener('click', () => {
      const src = thumb.dataset.src;
      const alt = thumb.dataset.alt || '';
      if (galleryMain && src) {
        galleryMain.src = src;
        galleryMain.alt = alt;
      }
      galleryThumbs.forEach(t => t.classList.remove('active'));
      thumb.classList.add('active');
    });
  });

  // ── PRODUCT TABS ─────────────────────────────────────────────
  const tabBtns = document.querySelectorAll('.nc-tab-btn');
  const tabPanels = document.querySelectorAll('.nc-tab-panel');
  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const target = btn.dataset.tab;
      tabBtns.forEach(b => b.classList.remove('active'));
      tabPanels.forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById(target)?.classList.add('active');
    });
  });

  // ── VARIANT SELECTION ────────────────────────────────────────
  const variantBtns = document.querySelectorAll('.nc-variant-btn');
  const variantInput = document.querySelector('[name="id"]');
  const priceEl = document.querySelector('.nc-product-price');

  variantBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      variantBtns.forEach(b => b.classList.remove('selected'));
      btn.classList.add('selected');
      if (variantInput) variantInput.value = btn.dataset.variantId;
      if (priceEl && btn.dataset.price) {
        priceEl.textContent = formatMoney(parseInt(btn.dataset.price));
      }
    });
  });

  // ── QUANTITY CONTROLS ────────────────────────────────────────
  const qtyInput = document.querySelector('.nc-qty-input');
  document.querySelector('[data-qty-minus]')?.addEventListener('click', () => {
    if (qtyInput && parseInt(qtyInput.value) > 1) qtyInput.value = parseInt(qtyInput.value) - 1;
  });
  document.querySelector('[data-qty-plus]')?.addEventListener('click', () => {
    if (qtyInput) qtyInput.value = parseInt(qtyInput.value) + 1;
  });

  // ── SCROLL REVEAL ────────────────────────────────────────────
  const revealEls = document.querySelectorAll('.nc-reveal');
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
    revealEls.forEach(el => observer.observe(el));
  } else {
    revealEls.forEach(el => el.classList.add('visible'));
  }

  // ── NEWSLETTER FORM ──────────────────────────────────────────
  const newsletterForms = document.querySelectorAll('[data-newsletter-form]');
  newsletterForms.forEach(form => {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const input = form.querySelector('input[type="email"]');
      const btn = form.querySelector('[type="submit"]');
      if (!input?.value) return;
      if (btn) {
        btn.textContent = '✓';
        btn.disabled = true;
        btn.style.background = '#2a7a3a';
      }
      // Shopify newsletter via form action
      const data = new FormData(form);
      try {
        await fetch(form.action || '/contact', { method: 'POST', body: data });
      } catch (_) {}
      setTimeout(() => {
        if (btn) { btn.textContent = 'Enviar'; btn.disabled = false; btn.style.background = ''; }
        input.value = '';
      }, 3000);
    });
  });

  // ── ANNOUNCEMENT BAR HEIGHT OFFSET ───────────────────────────
  const announcement = document.querySelector('.nc-announcement');
  if (announcement) {
    const h = announcement.offsetHeight;
    document.documentElement.style.setProperty('--nc-header-h', `${68 + h}px`);
    document.querySelectorAll('.nc-mobile-menu').forEach(m => {
      m.style.top = `${68 + h}px`;
    });
  }

})();
