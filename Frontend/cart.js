// cart.js
const CART_STORAGE_KEY = "aurora_cart";

function getCart() {
  const raw = localStorage.getItem(CART_STORAGE_KEY);
  if (!raw) return [];
  try {
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function saveCart(cart) {
  localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(cart));
}

function addToCart(productId, quantity = 1) {
  const cart = getCart();
  const existing = cart.find((item) => item.id === productId);
  if (existing) {
    existing.quantity += quantity;
  } else {
    cart.push({ id: productId, quantity });
  }
  saveCart(cart);
  return cart;
}

function removeFromCart(productId) {
  const cart = getCart().filter((item) => item.id !== productId);
  saveCart(cart);
  return cart;
}

function updateCartQuantity(productId, quantity) {
  const cart = getCart();
  const item = cart.find((i) => i.id === productId);
  if (!item) return cart;
  item.quantity = Math.max(1, quantity);
  saveCart(cart);
  return cart;
}

function countCartItems() {
  return getCart().reduce((sum, item) => sum + item.quantity, 0);
}

function getCartWithProductData() {
  return getCart().map((entry) => {
    const product = PRODUCTS.find((p) => p.id === entry.id);
    return product ? { ...product, quantity: entry.quantity } : null;
  }).filter(Boolean);
}