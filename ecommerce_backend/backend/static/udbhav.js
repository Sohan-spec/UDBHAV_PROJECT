/* UDBHAV shared frontend module  auth, cart, search, menu, toast */
window.UDBHAV = (function () {
    const FALLBACK = "https://images.unsplash.com/photo-1556228578-8c89e6adf883?auto=format&fit=crop&w=800&q=80";
    const token = () => localStorage.getItem("token");

    function inr(v) {
        return Number(v || 0).toLocaleString("en-IN", { style: "currency", currency: "INR", minimumFractionDigits: 2 });
    }
    function slugify(v) {
        return String(v || "").toLowerCase().trim().replace(/[^a-z0-9\s-]/g, "").replace(/\s+/g, "-").replace(/-+/g, "-");
    }

    function showToast(msg, isError) {
        const t = document.getElementById("toast");
        if (!t) return;
        t.textContent = msg;
        t.classList.toggle("error", !!isError);
        t.classList.add("is-show");
        clearTimeout(t._tm);
        t._tm = setTimeout(() => t.classList.remove("is-show"), 2600);
    }

    async function addToCart(productId, qty) {
        if (!token()) {
            showToast("Please sign in to add items.", true);
            setTimeout(() => location.href = "/login/", 700);
            return false;
        }
        try {
            const res = await fetch("/api/cart/", {
                method: "POST",
                headers: { "Content-Type": "application/json", "Authorization": "Bearer " + token() },
                body: JSON.stringify({ product_id: Number(productId), quantity: Number(qty || 1) })
            });
            const data = await res.json();
            if (!res.ok) { showToast(data.error || "Unable to add item.", true); return false; }
            showToast("Added to bag");
            updateCartCount();
            return true;
        } catch (e) { showToast("Network error.", true); return false; }
    }

    async function updateCartCount() {
        const badge = document.getElementById("nav-bag-count");
        if (!badge) return;
        if (!token()) { badge.classList.remove("is-visible"); return; }
        try {
            const res = await fetch("/api/cart/", { headers: { "Authorization": "Bearer " + token() } });
            if (!res.ok) { badge.classList.remove("is-visible"); return; }
            const data = await res.json();
            const n = (data.items || []).reduce((s, i) => s + Number(i.qty || 0), 0);
            if (n > 0) { badge.textContent = n > 99 ? "99+" : String(n); badge.classList.add("is-visible"); }
            else { badge.classList.remove("is-visible"); }
        } catch (e) { badge.classList.remove("is-visible"); }
    }

    const cart = {
        open() {
            document.getElementById("cart-drawer").classList.add("is-open");
            document.getElementById("drawer-overlay").classList.add("is-open");
            loadDrawer();
        },
        close() {
            document.getElementById("cart-drawer").classList.remove("is-open");
            document.getElementById("drawer-overlay").classList.remove("is-open");
        }
    };

    async function loadDrawer() {
        const msg = document.getElementById("cart-drawer-msg");
        const wrap = document.getElementById("cart-drawer-items");
        if (!wrap) return;
        msg.textContent = "";
        if (!token()) {
            wrap.innerHTML = emptyBag();
            document.getElementById("cart-drawer-title").textContent = "Bag";
            setTotals(0);
            return;
        }
        try {
            const res = await fetch("/api/cart/", { headers: { "Authorization": "Bearer " + token() } });
            const data = await res.json();
            if (!res.ok) { msg.textContent = data.error || "Failed to load bag"; return; }
            renderDrawer(data.items || [], data.total || 0);
        } catch (e) { msg.textContent = "Request failed"; }
    }

    function emptyBag() {
        return `<div class="cart-empty"><svg viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.2"><path d="M6 7h12l-1 13H7L6 7ZM9 7a3 3 0 0 1 6 0"/></svg><p>Your bag is empty.</p><a href="/" class="btn btn-outline mt-2" style="display:inline-flex">Continue shopping</a></div>`;
    }

    function renderDrawer(items, total) {
        const wrap = document.getElementById("cart-drawer-items");
        document.getElementById("cart-drawer-title").textContent = `Bag (${items.length})`;
        if (!items.length) { wrap.innerHTML = emptyBag(); setTotals(0); return; }
        wrap.innerHTML = items.map(i => `
            <div class="cart-item">
                <div class="cart-item-media"><img src="${i.image || FALLBACK}" alt="${i.name}" style="width:56px;height:56px;object-fit:cover;border-radius:6px" onerror="this.onerror=null;this.src=UDBHAV.FALLBACK;"></div>
                <div class="cart-item-body">
                    <div class="cart-item-name">${i.name}</div>
                    <div class="cart-item-meta">Qty ${i.qty}</div>
                    <div class="cart-item-row">
                        <span class="cart-item-price">${inr(i.price)}</span>
                        <button class="cart-item-remove" onclick="UDBHAV.cart.remove(${i.product_id})">Remove</button>
                    </div>
                </div>
            </div>`).join("");
        setTotals(total);
    }

    function setTotals(total) {
        const t = inr(total);
        const s = document.getElementById("cart-drawer-subtotal"); if (s) s.textContent = t;
        const g = document.getElementById("cart-drawer-total"); if (g) g.textContent = t;
    }

    cart.remove = async function (productId) {
        try {
            await fetch("/api/cart/", {
                method: "DELETE",
                headers: { "Content-Type": "application/json", "Authorization": "Bearer " + token() },
                body: JSON.stringify({ product_id: Number(productId) })
            });
            loadDrawer(); updateCartCount();
        } catch (e) { showToast("Remove failed", true); }
    };

    const forcedSlugByName = {
        "Algae Bloom Revitalizer": "algae-bloom-revitalizer",
        "Ocean Mist Body Oil": "ocean-mist-body-oil",
        "The Gift Set": "the-gift-set",
        "Estee Lauder Pure Color Explicit Slick Shine Lipstick - Call 555": "estee-lauder-call-555-lipstick",
        "Sea Kelp Vitalizing Shampoo": "sea-kelp-vitalizing-shampoo",
        "Coastal Breeze Cooling Mist": "coastal-breeze-cooling-mist",
        "Dead Sea Mud & Mint Mask": "dead-sea-mud-and-mint-mask",
        "Dead Sea Mud and Mint Mask": "dead-sea-mud-and-mint-mask",
        "iPhone 15": "iphone-15",
        "iPhone 14": "iphone-14",
        "Galaxy S24": "galaxy-s24",
        "Galaxy S23": "galaxy-s23",
        "ROG Zephyrus": "rog-zephyrus",
        "ZenBook": "zenbook",
        "MacBook Pro": "macbook-pro",
        "MacBook Air": "macbook-air",
        "Polo T-Shirt": "polo-t-shirt",
        "Casual Graphic T-Shirt": "casual-graphic-t-shirt",
        "Jeans": "jeans",
        "Chinos": "chinos",
        "3-Seater Recliner": "3-seater-recliner",
        "L-Shaped Sofa": "l-shaped-sofa",
        "Spoons": "spoons",
        "Plates": "plates",
        "Forks": "forks",
        "Rice": "rice",
        "Wheat": "wheat",
        "Vegetables": "vegetables"
    };

    function productSlug(p) {
        return forcedSlugByName[p.name] || p.slug || slugify(p.name);
    }

    const catalogCache = { products: null, loading: null, at: 0 };

    async function loadCatalog() {
        const fresh = Date.now() - catalogCache.at < 60000;
        if (catalogCache.products && fresh) return catalogCache.products;
        if (catalogCache.loading) return catalogCache.loading;
        catalogCache.loading = fetch("/api/products/?page=1&size=200")
            .then(r => r.json())
            .then(d => {
                catalogCache.products = (d.products || []).map(p => ({
                    ...p,
                    slug: productSlug(p),
                    _q: `${p.name || ""} ${p.category || ""} ${p.description || ""}`.toLowerCase()
                }));
                catalogCache.at = Date.now();
                catalogCache.loading = null;
                return catalogCache.products;
            })
            .catch(err => {
                catalogCache.loading = null;
                throw err;
            });
        return catalogCache.loading;
    }

    function escapeHtml(s) {
        return String(s || "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
    }

    function highlightMatch(text, query) {
        const safe = escapeHtml(text);
        const q = String(query || "").trim();
        if (!q) return safe;
        const lower = safe.toLowerCase();
        const idx = lower.indexOf(q.toLowerCase());
        if (idx < 0) return safe;
        return safe.slice(0, idx) + "<mark>" + safe.slice(idx, idx + q.length) + "</mark>" + safe.slice(idx + q.length);
    }

    function filterCatalog(products, query) {
        const tokens = String(query || "").toLowerCase().trim().split(/\s+/).filter(Boolean);
        if (!tokens.length) return [];
        return products
            .map(p => {
                let score = 0;
                const name = (p.name || "").toLowerCase();
                for (const t of tokens) {
                    if (!p._q.includes(t)) return null;
                    if (name.startsWith(t)) score += 40;
                    else if (name.includes(t)) score += 20;
                    else score += 5;
                }
                if (name === tokens.join(" ")) score += 50;
                return { p, score };
            })
            .filter(Boolean)
            .sort((a, b) => b.score - a.score || String(a.p.name).localeCompare(String(b.p.name)))
            .map(x => x.p);
    }

    let searchActiveIndex = -1;
    let searchDebounce = null;
    let searchBound = false;

    function renderSearchResults(query, matches) {
        const wrap = document.getElementById("search-results");
        const hint = document.getElementById("search-hint");
        const input = document.getElementById("search-input");
        if (!wrap) return;
        searchActiveIndex = -1;
        if (input) input.setAttribute("aria-expanded", matches.length ? "true" : "false");

        if (!query.trim()) {
            wrap.innerHTML = "";
            if (hint) hint.textContent = "Start typing to search the catalogue.";
            return;
        }

        if (!matches.length) {
            wrap.innerHTML = `<div class="search-empty">No products match “${escapeHtml(query)}”.</div>`;
            if (hint) hint.textContent = "Try another word  we match names and categories.";
            return;
        }

        const shown = matches.slice(0, 8);
        if (hint) hint.innerHTML = `Showing <span>${shown.length}</span> of <span>${matches.length}</span> match${matches.length === 1 ? "" : "es"}`;
        wrap.innerHTML = shown.map((p, i) => {
            const price = Number(p.price || 0);
            const priceLabel = price === 0 ? "Free gift" : inr(price);
            return `
                <a class="search-result" role="option" id="search-opt-${i}" href="/product/${escapeHtml(p.slug)}/" data-index="${i}">
                    <div class="search-result-media">
                        <img src="${escapeHtml(p.image || FALLBACK)}" alt="" loading="lazy" onerror="this.onerror=null;this.src=UDBHAV.FALLBACK;">
                    </div>
                    <div class="search-result-body">
                        <div class="search-result-cat">${escapeHtml(p.category || "")}</div>
                        <div class="search-result-name">${highlightMatch(p.name, query)}</div>
                    </div>
                    <div class="search-result-price">${priceLabel}</div>
                </a>`;
        }).join("") + `
            <div class="search-footer">
                <span>${matches.length} result${matches.length === 1 ? "" : "s"}</span>
                <a href="/shop/?search=${encodeURIComponent(query.trim())}">View all in shop →</a>
            </div>`;
    }

    async function runLiveSearch() {
        const input = document.getElementById("search-input");
        const wrap = document.getElementById("search-results");
        const hint = document.getElementById("search-hint");
        if (!input || !wrap) return;
        const query = input.value;
        if (!query.trim()) {
            renderSearchResults("", []);
            return;
        }
        try {
            if (hint) hint.textContent = "Searching…";
            const products = await loadCatalog();
            const matches = filterCatalog(products, query);
            if (input.value !== query) return;
            renderSearchResults(query, matches);
        } catch (e) {
            wrap.innerHTML = `<div class="search-empty">Couldn't load catalogue. Try again.</div>`;
            if (hint) hint.textContent = "Search temporarily unavailable.";
        }
    }

    function setActiveResult(next) {
        const items = [...document.querySelectorAll("#search-results .search-result")];
        if (!items.length) return;
        items.forEach(el => el.classList.remove("is-active"));
        searchActiveIndex = (next + items.length) % items.length;
        items[searchActiveIndex].classList.add("is-active");
        items[searchActiveIndex].scrollIntoView({ block: "nearest" });
    }

    function bindSearchUI() {
        if (searchBound) return;
        const input = document.getElementById("search-input");
        if (!input) return;
        searchBound = true;

        input.addEventListener("input", () => {
            clearTimeout(searchDebounce);
            searchDebounce = setTimeout(runLiveSearch, 60);
        });

        input.addEventListener("keydown", (e) => {
            const items = document.querySelectorAll("#search-results .search-result");
            if (e.key === "ArrowDown") {
                e.preventDefault();
                setActiveResult(searchActiveIndex + 1);
            } else if (e.key === "ArrowUp") {
                e.preventDefault();
                setActiveResult(searchActiveIndex <= 0 ? items.length - 1 : searchActiveIndex - 1);
            } else if (e.key === "Enter" && searchActiveIndex >= 0 && items[searchActiveIndex]) {
                e.preventDefault();
                location.href = items[searchActiveIndex].getAttribute("href");
            }
        });
    }

    const search = {
        open() {
            const o = document.getElementById("search-overlay");
            if (!o) return;
            bindSearchUI();
            o.classList.add("is-open");
            document.body.style.overflow = "hidden";
            loadCatalog().catch(() => {});
            setTimeout(() => {
                const input = document.getElementById("search-input");
                if (input) {
                    input.focus();
                    if (input.value.trim()) runLiveSearch();
                }
            }, 40);
        },
        close() {
            const o = document.getElementById("search-overlay");
            if (o) o.classList.remove("is-open");
            document.body.style.overflow = "";
            searchActiveIndex = -1;
        },
        submit(e) {
            e.preventDefault();
            const q = (document.getElementById("search-input").value || "").trim();
            search.close();
            location.href = q ? `/shop/?search=${encodeURIComponent(q)}` : "/shop/";
        }
    };

    const menu = {
        open() { document.getElementById("mobile-menu").classList.add("is-open"); document.body.style.overflow = "hidden"; },
        close() { document.getElementById("mobile-menu").classList.remove("is-open"); document.body.style.overflow = ""; }
    };

    const auth = {
        logout(e) { if (e) e.preventDefault(); localStorage.removeItem("token"); localStorage.removeItem("role"); location.href = "/"; },
        updateUI() {
            const t = token();
            const mmLogin = document.getElementById("mm-login");
            const mmLogout = document.getElementById("mm-logout");
            const mmSignup = document.getElementById("mm-signup");
            if (t) {
                if (mmLogin) mmLogin.style.display = "none";
                if (mmSignup) mmSignup.style.display = "none";
                if (mmLogout) mmLogout.style.display = "inline-block";
            } else {
                if (mmLogin) mmLogin.style.display = "inline-block";
                if (mmSignup) mmSignup.style.display = "inline-block";
                if (mmLogout) mmLogout.style.display = "none";
            }
        }
    };

    function init() {
        auth.updateUI();
        updateCartCount();
        bindSearchUI();
        document.addEventListener("keydown", (e) => {
            if (e.key === "Escape") { search.close(); cart.close(); menu.close(); }
        });
        // Warm the catalogue cache in the background for instant search.
        loadCatalog().catch(() => {});
    }

    if (document.readyState !== "loading") init();
    else document.addEventListener("DOMContentLoaded", init);

    return { inr, slugify, addToCart, updateCartCount, cart, search, menu, auth, showToast, FALLBACK, token };
})();
