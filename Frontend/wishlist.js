// wishlist.js
const WISHLIST_STORAGE_KEY = "aurora_wishlist";

function getWishlist() {
  const raw = localStorage.getItem(WISHLIST_STORAGE_KEY);
  if (!raw) return [];
  try {
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function saveWishlist(list) {
  localStorage.setItem(WISHLIST_STORAGE_KEY, JSON.stringify(list));
}

function isInWishlist(productId) {
  return getWishlist().includes(productId);
}

function toggleWishlist(productId) {
  const list = getWishlist();
  const index = list.indexOf(productId);
  if (index >= 0) {
    list.splice(index, 1);
  } else {
    list.push(productId);
  }
  saveWishlist(list);
  return list;
}

function removeFromWishlist(productId) {
  const list = getWishlist().filter((id) => id !== productId);
  saveWishlist(list);
  return list;
}

function countWishlistItems() {
  return getWishlist().length;
}