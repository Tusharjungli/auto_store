document.addEventListener("DOMContentLoaded", function () {
  console.log("Cart.js loaded!");

  // ✅ Handle "Add to Cart" buttons
  const addToCartButtons = document.querySelectorAll(".add-to-cart-btn");
  addToCartButtons.forEach(button => {
      button.addEventListener("click", function (event) {
          event.preventDefault();
          const productId = this.dataset.productId;
          addToCart(productId);
      });
  });

  // ✅ Function to add item to cart via AJAX
  function addToCart(productId) {
      fetch(`/cart/add/${productId}/`, {
          method: "GET",
          headers: {
              "X-Requested-With": "XMLHttpRequest"
          }
      })
      .then(response => response.json())
      .then(data => {
          if (data.success) {
              alert("Item added to cart!");
              updateCartCount(data.cart_count);
          } else {
              alert("Failed to add item to cart.");
          }
      })
      .catch(error => console.error("Error:", error));
  }

  // ✅ Update cart count in UI
  function updateCartCount(count) {
      const cartCountElement = document.querySelector("#cart-count");
      if (cartCountElement) {
          cartCountElement.textContent = count;
      }
  }

  // ✅ Handle quantity update
  const updateButtons = document.querySelectorAll(".update-cart-btn");
  updateButtons.forEach(button => {
      button.addEventListener("click", function () {
          const productId = this.dataset.productId;
          const quantityInput = document.querySelector(`#quantity-${productId}`);
          updateCart(productId, quantityInput.value);
      });
  });

  // ✅ Function to update cart item quantity
  function updateCart(productId, quantity) {
      fetch(`/cart/update/${productId}/`, {
          method: "POST",
          headers: {
              "X-CSRFToken": getCSRFToken(),
              "Content-Type": "application/x-www-form-urlencoded"
          },
          body: `quantity=${quantity}`
      })
      .then(response => response.json())
      .then(data => {
          if (data.success) {
              location.reload();
          } else {
              alert("Failed to update cart.");
          }
      })
      .catch(error => console.error("Error:", error));
  }

  // ✅ Handle "Remove from Cart" buttons
  const removeButtons = document.querySelectorAll(".remove-btn");
  removeButtons.forEach(button => {
      button.addEventListener("click", function (event) {
          event.preventDefault();
          const productId = this.dataset.productId;
          removeFromCart(productId);
      });
  });

  // ✅ Function to remove item from cart
  function removeFromCart(productId) {
      fetch(`/cart/remove/${productId}/`, {
          method: "GET"
      })
      .then(response => response.json())
      .then(data => {
          if (data.success) {
              location.reload();
          } else {
              alert("Failed to remove item from cart.");
          }
      })
      .catch(error => console.error("Error:", error));
  }

  // ✅ Function to get CSRF token for POST requests
  function getCSRFToken() {
      return document.querySelector("[name=csrfmiddlewaretoken]").value;
  }
});
