// checkout.js
(function () {
  const pageBody = document.body;
  const pageCheckout = pageBody.classList.contains("page-checkout");

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

  function initCheckoutPage() {
    const orderItemsEl = document.getElementById("order-items");
    const subtotalEl = document.getElementById("checkout-subtotal");
    const totalEl = document.getElementById("checkout-total");
    const shippingEl = document.getElementById("checkout-shipping");
    const paymentOptions = document.querySelectorAll('input[name="payment-method"]');
    const paymentDetails = document.getElementById("payment-details");
    const codDetails = document.getElementById("cod-details");
    const upiDetails = document.getElementById("upi-details");
    const cardDetails = document.getElementById("card-details");
    const placeOrderBtn = document.getElementById("place-order-btn");
    const modal = document.getElementById("confirmation-modal");
    const modalClose = document.getElementById("modal-close");
    const continueShopping = document.getElementById("continue-shopping");
    const orderIdEl = document.getElementById("order-id");

    if (!orderItemsEl) return;

    const shippingFlat = 15;

    function renderOrderSummary() {
      const items = getCartWithProductData();
      if (!items.length) {
        window.location.href = "cart.html"; // Redirect if no items
        return;
      }

      orderItemsEl.innerHTML = items
        .map(
          (item) => `
        <div class="order-item">
          <img src="${item.image}" alt="${item.name}" />
          <div class="order-item-info">
            <div class="order-item-name">${item.name}</div>
            <div class="order-item-meta">
              <span class="stars">${createStars(item.rating)}</span>
              <span>Qty: ${item.quantity}</span>
            </div>
          </div>
          <div class="order-item-price">${formatPrice(item.price * item.quantity)}</div>
        </div>
      `
        )
        .join("");

      const subtotal = items.reduce(
        (sum, item) => sum + item.price * item.quantity,
        0
      );
      if (subtotalEl) subtotalEl.textContent = formatPrice(subtotal);
      if (shippingEl) shippingEl.textContent = formatPrice(shippingFlat);
      if (totalEl) totalEl.textContent = formatPrice(subtotal + shippingFlat);
    }

    function showPaymentDetails(method) {
      paymentDetails.style.display = "block";
      codDetails.style.display = method === "cod" ? "block" : "none";
      upiDetails.style.display = method === "upi" ? "block" : "none";
      cardDetails.style.display = method === "card" ? "block" : "none";
      placeOrderBtn.disabled = false;
    }

    function validatePaymentDetails(method) {
      if (method === "cod") return true;
      if (method === "upi") {
        const upiId = document.getElementById("upi-id").value.trim();
        return upiId.length > 0;
      }
      if (method === "card") {
        const cardNumber = document.getElementById("card-number").value.trim();
        const expiry = document.getElementById("expiry").value.trim();
        const cvv = document.getElementById("cvv").value.trim();
        const cardName = document.getElementById("card-name").value.trim();
        return cardNumber && expiry && cvv && cardName;
      }
      return false;
    }

    paymentOptions.forEach((option) => {
      option.addEventListener("change", (e) => {
        if (e.target.checked) {
          showPaymentDetails(e.target.value);
        }
      });
    });

    placeOrderBtn.addEventListener("click", () => {
      const selectedMethod = document.querySelector('input[name="payment-method"]:checked');
      if (!selectedMethod) {
        alert("Please select a payment method.");
        return;
      }
      if (!validatePaymentDetails(selectedMethod.value)) {
        alert("Please fill in all required payment details.");
        return;
      }

      // Simulate payment processing
      placeOrderBtn.textContent = "Processing...";
      placeOrderBtn.disabled = true;

      setTimeout(() => {
        // Generate order ID
        const orderId = "ORD" + Date.now();
        orderIdEl.textContent = orderId;

        // Clear cart
        localStorage.removeItem(CART_STORAGE_KEY);

        // Show modal
        modal.style.display = "flex";
        placeOrderBtn.textContent = "Place Order";
      }, 2000);
    });

    modalClose.addEventListener("click", () => {
      modal.style.display = "none";
      window.location.href = "index.html";
    });

    continueShopping.addEventListener("click", () => {
      modal.style.display = "none";
      window.location.href = "index.html";
    });

    // Close modal on outside click
    modal.addEventListener("click", (e) => {
      if (e.target === modal) {
        modal.style.display = "none";
        window.location.href = "index.html";
      }
    });

    renderOrderSummary();
  }

  document.addEventListener("DOMContentLoaded", () => {
    if (pageCheckout) initCheckoutPage();
  });
})();