// main.js
(function () {
  const pageBody = document.body;
  const pageProducts = pageBody.classList.contains("page-products");
  const pageProductDetail = pageBody.classList.contains("page-product");
  const pageCart = pageBody.classList.contains("page-cart");
  const pageWishlist = pageBody.classList.contains("page-wishlist");

  /* Shared helpers */
function formatPrice(value) {
  return value.toLocaleString("en-IN", {
    style: "currency",
    currency: "INR",
    minimumFractionDigits: 2
  });
}

  function createStars(rating) {
    const fullStars = Math.floor(rating);
    const halfStar = rating - fullStars >= 0.5;
    let stars = "";
    for (let i = 0; i < 5; i++) {
      if (i < fullStars) stars += "★";
      else if (i === fullStars && halfStar) stars += "☆";
      else stars += "☆";
    }
    return stars;
  }

  function goToProduct(id) {
    window.location.href = `product.html?id=${encodeURIComponent(id)}`;
  }

  function updateNavbarCounts() {
    const cartCountEl = document.getElementById("cart-count");
    const wishlistCountEl = document.getElementById("wishlist-count");
    if (cartCountEl) cartCountEl.textContent = countCartItems();
    if (wishlistCountEl) wishlistCountEl.textContent = countWishlistItems();
  }

  function attachCardWishlistButtons(container) {
    if (!container) return;
    container.addEventListener("click", (e) => {
      const btn = e.target.closest("[data-wishlist-toggle]");
      if (!btn) return;
      e.stopPropagation();
      const id = Number(btn.dataset.productId);
      toggleWishlist(id);
      const inWishlist = isInWishlist(id);
      btn.classList.toggle("active", inWishlist);
      updateNavbarCounts();
    });
  }

  function productCardHTML(product, { showActions = true } = {}) {
    const inWishlist = isInWishlist(product.id);
    return `
      <article class="product-card" data-product-id="${product.id}">
        <div class="product-card-image-wrapper" data-product-link>
          <img src="${product.image}" alt="${product.name}" loading="lazy" />
          <div class="product-card-badge">${product.category}</div>
          <button type="button"
            class="icon-button product-card-wishlist ${inWishlist ? "active" : ""}"
            data-wishlist-toggle
            data-product-id="${product.id}"
            aria-label="Wishlist">
            <span class="icon-heart"></span>
          </button>
        </div>
        <div class="product-card-body">
          <div class="product-card-category">${product.category}</div>
          <h3 class="product-card-name" data-product-link>${product.name}</h3>
          <div class="product-card-meta">
            <div class="price">${formatPrice(product.price)}</div>
            <div class="rating">
              <span class="stars">${createStars(product.rating)}</span>
              <span>${product.rating.toFixed(1)}</span>
            </div>
          </div>
          ${
            showActions
              ? `<div class="product-card-actions">
                  <button type="button" class="btn-primary" data-add-to-cart data-product-id="${product.id}">
                    Add to Cart
                  </button>
                </div>`
              : ""
          }
        </div>
      </article>
    `;
  }

  function attachCardInteractions(container) {
    if (!container) return;

    // Navigate to product on image/title click
    container.addEventListener("click", (e) => {
      const linkTarget = e.target.closest("[data-product-link]");
      if (!linkTarget) return;
      const card = linkTarget.closest(".product-card");
      if (!card) return;
      const id = Number(card.dataset.productId);
      goToProduct(id);
    });

    // Add to cart from listing / related / wishlist
    container.addEventListener("click", (e) => {
      const btn = e.target.closest("[data-add-to-cart]");
      if (!btn) return;
      const id = Number(btn.dataset.productId);
      addToCart(id, 1);
      updateNavbarCounts();
    });

    // Wishlist toggle
    attachCardWishlistButtons(container);
  }

  /* Listing page */
  function initListingPage() {
    const grid = document.querySelector(".product-grid[data-page='listing']");
    const noResultsEl = document.getElementById("no-results");
    if (!grid) return;

    let filters = {
      category: "all",
      maxPrice: 1000,
      rating: 0,
      search: "",
      sort: "newest"
    };

    // Price slider
    const priceRange = document.getElementById("price-range");
    const priceRangeValue = document.getElementById("price-range-value");
    if (priceRange && priceRangeValue) {
      const maxPriceInData = Math.max(...PRODUCTS.map((p) => p.price));
      priceRange.max = Math.ceil(maxPriceInData / 10) * 10;
      priceRange.value = priceRange.max;
      filters.maxPrice = Number(priceRange.value);
      priceRangeValue.textContent = formatPrice(filters.maxPrice);

      priceRange.addEventListener("input", () => {
        filters.maxPrice = Number(priceRange.value);
        priceRangeValue.textContent = formatPrice(filters.maxPrice);
        render();
      });
    }

    // Category chips
    const categoryFilters = document.getElementById("category-filters");
    if (categoryFilters) {
      categoryFilters.addEventListener("click", (e) => {
        const chip = e.target.closest(".chip");
        if (!chip) return;
        categoryFilters.querySelectorAll(".chip").forEach((c) => c.classList.remove("active"));
        chip.classList.add("active");
        filters.category = chip.dataset.category;
        render();
      });
    }

    // Rating chips
    const ratingFilter = document.getElementById("rating-filter");
    if (ratingFilter) {
      ratingFilter.addEventListener("click", (e) => {
        const chip = e.target.closest(".chip");
        if (!chip) return;
        ratingFilter.querySelectorAll(".chip").forEach((c) => c.classList.remove("active"));
        chip.classList.add("active");
        filters.rating = Number(chip.dataset.rating);
        render();
      });
    }

    // Sort
    const sortSelect = document.getElementById("sort-select");
    if (sortSelect) {
      sortSelect.addEventListener("change", () => {
        filters.sort = sortSelect.value;
        render();
      });
    }

    // Search
    const searchForm = document.getElementById("search-form");
    const searchInput = document.getElementById("search-input");
    if (searchForm && searchInput) {
      searchForm.addEventListener("submit", (e) => {
        e.preventDefault();
        filters.search = searchInput.value.trim().toLowerCase();
        render();
      });
      searchInput.addEventListener("input", () => {
        filters.search = searchInput.value.trim().toLowerCase();
        render();
      });
    }

    // Clear filters
    const clearFiltersBtn = document.getElementById("clear-filters-btn");
    if (clearFiltersBtn) {
      clearFiltersBtn.addEventListener("click", () => {
        filters = {
          category: "all",
          maxPrice: Number(priceRange ? priceRange.max : 1000),
          rating: 0,
          search: "",
          sort: "newest"
        };
        if (priceRange && priceRangeValue) {
          priceRange.value = priceRange.max;
          priceRangeValue.textContent = formatPrice(filters.maxPrice);
        }
        if (categoryFilters) {
          categoryFilters
            .querySelectorAll(".chip")
            .forEach((c) => c.classList.toggle("active", c.dataset.category === "all"));
        }
        if (ratingFilter) {
          ratingFilter
            .querySelectorAll(".chip")
            .forEach((c) => c.classList.toggle("active", c.dataset.rating === "0"));
        }
        if (sortSelect) sortSelect.value = "newest";
        if (searchInput) searchInput.value = "";
        render();
      });
    }

    function applyFiltersAndSort(products) {
      return products
        .filter((p) => {
          if (filters.category !== "all" && p.category !== filters.category) return false;
          if (p.price > filters.maxPrice) return false;
          if (p.rating < filters.rating) return false;
          if (filters.search) {
            const q = filters.search;
            const text = `${p.name} ${p.category} ${p.description}`.toLowerCase();
            if (!text.includes(q)) return false;
          }
          return true;
        })
        .sort((a, b) => {
          switch (filters.sort) {
            case "price-asc":
              return a.price - b.price;
            case "price-desc":
              return b.price - a.price;
            case "rating-desc":
              return b.rating - a.rating;
            case "newest":
            default:
              return b.id - a.id;
          }
        });
    }

    function render() {
      const filtered = applyFiltersAndSort(PRODUCTS);
      if (!filtered.length) {
        grid.innerHTML = "";
        if (noResultsEl) noResultsEl.hidden = false;
        return;
      }
      if (noResultsEl) noResultsEl.hidden = true;
      grid.innerHTML = filtered.map((p) => productCardHTML(p)).join("");
      attachCardInteractions(grid);
      updateNavbarCounts();
    }

    render();
  }

  /* Product detail page */
  function initProductDetailPage() {
    const params = new URLSearchParams(window.location.search);
    const id = Number(params.get("id"));
    const product = PRODUCTS.find((p) => p.id === id) || PRODUCTS[0];

    const imgMain = document.getElementById("product-image-main");
    const thumbs = document.getElementById("product-thumbnails");
    const nameEl = document.getElementById("product-name");
    const priceEl = document.getElementById("product-price");
    const ratingEl = document.getElementById("product-rating");
    const catEl = document.getElementById("product-category");
    const shortDescEl = document.getElementById("product-short-description");
    const longDescEl = document.getElementById("product-long-description");
    const reviewsList = document.getElementById("reviews-list");
    const qtyInput = document.getElementById("quantity-input");
    const addToCartBtn = document.getElementById("add-to-cart-detail");
    const wishlistBtn = document.getElementById("toggle-wishlist-detail");
    const relatedGrid = document.getElementById("related-products");

    if (!product) return;

    imgMain.src = product.image;
    imgMain.alt = product.name;

    // Simple thumbnail gallery (same image variations)
    if (thumbs) {
      const thumbSources = [
        product.image,
        product.image + "?v=2",
        product.image + "?v=3"
      ];
      thumbs.innerHTML = thumbSources
        .map(
          (src, index) =>
            `<img src="${src}" alt="${product.name}" data-thumb-index="${index}" class="${
              index === 0 ? "active" : ""
            }"/>`
        )
        .join("");
      thumbs.addEventListener("click", (e) => {
        const img = e.target.closest("img[data-thumb-index]");
        if (!img) return;
        thumbs.querySelectorAll("img").forEach((el) => el.classList.remove("active"));
        img.classList.add("active");
        imgMain.src = img.src;
      });
    }

    if (nameEl) nameEl.textContent = product.name;
    if (priceEl) priceEl.textContent = formatPrice(product.price);
    if (ratingEl)
      ratingEl.innerHTML = `<span class="stars">${createStars(
        product.rating
      )}</span><span>${product.rating.toFixed(1)}</span>`;
    if (catEl) catEl.textContent = product.category;
    if (shortDescEl) shortDescEl.textContent = product.description;
    if (longDescEl) longDescEl.textContent = product.longDescription;

    // Reviews
    if (reviewsList) {
      reviewsList.innerHTML = product.reviews
        .map(
          (r) => `
        <div class="review">
          <div class="review-user">
            <span class="review-user-name">${r.user}</span>
            <div class="rating">
              <span class="stars">${createStars(r.rating)}</span>
              <span>${r.rating.toFixed(1)}</span>
            </div>
          </div>
          <p class="review-comment">${r.comment}</p>
        </div>
      `
        )
        .join("");
    }

    // Tabs
    const tabs = document.querySelectorAll(".tab");
    const panels = document.querySelectorAll(".tab-panel");
    tabs.forEach((tab) => {
      tab.addEventListener("click", () => {
        const target = tab.dataset.tab;
        tabs.forEach((t) => t.classList.remove("active"));
        panels.forEach((p) => p.classList.remove("active"));
        tab.classList.add("active");
        document.getElementById(`tab-${target}`).classList.add("active");
      });
    });

    // Quantity
    document.querySelectorAll(".qty-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        const change = Number(btn.dataset.change);
        const current = Number(qtyInput.value) || 1;
        const next = Math.max(1, current + change);
        qtyInput.value = next;
      });
    });

    qtyInput.addEventListener("change", () => {
      const value = Number(qtyInput.value) || 1;
      qtyInput.value = Math.max(1, value);
    });

    // Wishlist state
    const inWishlist = isInWishlist(product.id);
    wishlistBtn.classList.toggle("active", inWishlist);

    wishlistBtn.addEventListener("click", () => {
      toggleWishlist(product.id);
      wishlistBtn.classList.toggle("active", isInWishlist(product.id));
      updateNavbarCounts();
    });

    // Add to cart
    addToCartBtn.addEventListener("click", () => {
      const quantity = Math.max(1, Number(qtyInput.value) || 1);
      addToCart(product.id, quantity);
      updateNavbarCounts();
    });

    // Related
    if (relatedGrid) {
      const related = PRODUCTS.filter(
        (p) => p.category === product.category && p.id !== product.id
      ).slice(0, 4);
      relatedGrid.innerHTML = related.map((p) => productCardHTML(p)).join("");
      attachCardInteractions(relatedGrid);
    }
  }

  /* Cart page */
  function initCartPage() {
    const container = document.getElementById("cart-items");
    const emptyMessage = document.getElementById("empty-cart-message");
    const subtotalEl = document.getElementById("cart-subtotal");
    const totalEl = document.getElementById("cart-total");
    const shippingEl = document.getElementById("cart-shipping");
    const checkoutBtn = document.getElementById("checkout-btn");

    if (!container) return;

    const shippingFlat = 15;

    function recalcTotals() {
      const items = getCartWithProductData();
      const subtotal = items.reduce(
        (sum, item) => sum + item.price * item.quantity,
        0
      );
      if (subtotalEl) subtotalEl.textContent = formatPrice(subtotal);
      if (shippingEl) shippingEl.textContent = subtotal ? formatPrice(shippingFlat) : "₹0.00";
      if (totalEl)
        totalEl.textContent = subtotal
          ? formatPrice(subtotal + shippingFlat)
          : "₹0.00";
    }

    function render() {
      const items = getCartWithProductData();
      if (!items.length) {
        container.innerHTML = "";
        if (emptyMessage) emptyMessage.hidden = false;
        recalcTotals();
        updateNavbarCounts();
        return;
      }
      if (emptyMessage) emptyMessage.hidden = true;

      container.innerHTML = items
        .map(
          (item) => `
        <article class="cart-item" data-product-id="${item.id}">
          <img src="${item.image}" alt="${item.name}" />
          <div class="cart-item-info">
            <div class="cart-item-name">${item.name}</div>
            <div class="cart-item-meta">
              <span class="price">${formatPrice(item.price)}</span>
              <div class="rating">
                <span class="stars">${createStars(item.rating)}</span>
                <span>${item.rating.toFixed(1)}</span>
              </div>
            </div>
            <div class="quantity-control">
              <button type="button" class="qty-btn" data-change="-1">-</button>
              <input type="number" class="cart-qty-input" value="${item.quantity}" min="1" />
              <button type="button" class="qty-btn" data-change="1">+</button>
            </div>
          </div>
          <div class="cart-item-actions">
            <div class="price">${formatPrice(item.price * item.quantity)}</div>
            <button type="button" class="btn-link" data-remove>Remove</button>
          </div>
        </article>
      `
        )
        .join("");

      recalcTotals();
      updateNavbarCounts();
    }

    container.addEventListener("click", (e) => {
      const removeBtn = e.target.closest("[data-remove]");
      if (removeBtn) {
        const itemEl = removeBtn.closest(".cart-item");
        const id = Number(itemEl.dataset.productId);
        removeFromCart(id);
        render();
        return;
      }

      const qtyBtn = e.target.closest(".qty-btn");
      if (!qtyBtn) return;
      const change = Number(qtyBtn.dataset.change);
      const itemEl = qtyBtn.closest(".cart-item");
      const input = itemEl.querySelector(".cart-qty-input");
      const current = Number(input.value) || 1;
      const next = Math.max(1, current + change);
      input.value = next;
      const id = Number(itemEl.dataset.productId);
      updateCartQuantity(id, next);
      render();
    });

    container.addEventListener("change", (e) => {
      const input = e.target.closest(".cart-qty-input");
      if (!input) return;
      const itemEl = input.closest(".cart-item");
      const id = Number(itemEl.dataset.productId);
      const value = Math.max(1, Number(input.value) || 1);
      input.value = value;
      updateCartQuantity(id, value);
      render();
    });

    if (checkoutBtn) {
      checkoutBtn.addEventListener("click", () => {
        alert("Checkout flow is not implemented in this demo. Connect your backend here.");
      });
    }

    render();
  }

  /* Wishlist page */
  function initWishlistPage() {
    const grid = document.getElementById("wishlist-grid");
    const emptyMessage = document.getElementById("empty-wishlist-message");
    if (!grid) return;

    function render() {
      const ids = getWishlist();
      if (!ids.length) {
        grid.innerHTML = "";
        if (emptyMessage) emptyMessage.hidden = false;
        updateNavbarCounts();
        return;
      }
      if (emptyMessage) emptyMessage.hidden = true;

      const products = ids
        .map((id) => PRODUCTS.find((p) => p.id === id))
        .filter(Boolean);

      grid.innerHTML = products
        .map((p) =>
          productCardHTML(p, { showActions: false }).replace(
            "</div></article>",
            `
              <div class="product-card-actions">
                <button type="button" class="btn-primary" data-move-to-cart data-product-id="${p.id}">
                  Move to Cart
                </button>
                <button type="button" class="btn-ghost" data-remove-wishlist data-product-id="${p.id}">
                  Remove
                </button>
              </div>
            </div></article>`
          )
        )
        .join("");

      attachCardInteractions(grid);
      updateNavbarCounts();
    }

    grid.addEventListener("click", (e) => {
      const moveBtn = e.target.closest("[data-move-to-cart]");
      if (moveBtn) {
        const id = Number(moveBtn.dataset.productId);
        addToCart(id, 1);
        removeFromWishlist(id);
        render();
        return;
      }

      const removeBtn = e.target.closest("[data-remove-wishlist]");
      if (removeBtn) {
        const id = Number(removeBtn.dataset.productId);
        removeFromWishlist(id);
        render();
      }
    });

    render();
  }

  /* Shared footer year */
  const yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear().toString();

  /* Init by page */
  document.addEventListener("DOMContentLoaded", () => {
    updateNavbarCounts();
    if (pageProducts) initListingPage();
    if (pageProductDetail) initProductDetailPage();
    if (pageCart) initCartPage();
    if (pageWishlist) initWishlistPage();
  });
})();