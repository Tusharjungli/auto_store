document.addEventListener("DOMContentLoaded", function () {
    console.log("Cart.js loaded!");

    // ✅ Handle "Add to Cart" buttons
    document.querySelectorAll(".add-to-cart-btn").forEach(button => {
        button.addEventListener("click", async function (event) {
            event.preventDefault();
            const productId = this.dataset.productId;
            await addToCart(productId);
        });
    });

    // ✅ Function to add item to cart via AJAX
    async function addToCart(productId) {
        try {
            const response = await fetch(`/cart/add/${productId}/`, {
                method: "GET",
                headers: { "X-Requested-With": "XMLHttpRequest" }
            });
            const data = await response.json();
            if (data.success) {
                alert("Item added to cart!");
                updateCartCount(data.cart_count);
            } else {
                alert("Failed to add item to cart.");
            }
        } catch (error) {
            console.error("Error adding to cart:", error);
        }
    }

    // ✅ Update cart count in UI
    function updateCartCount(count) {
        const cartCountElement = document.querySelector("#cart-count");
        if (cartCountElement) cartCountElement.textContent = count;
    }

    // ✅ Handle quantity update
    document.querySelectorAll(".update-cart-btn").forEach(button => {
        button.addEventListener("click", async function () {
            const productId = this.dataset.productId;
            const quantityInput = document.querySelector(`#quantity-${productId}`);
            await updateCart(productId, quantityInput.value);
        });
    });

    // ✅ Function to update cart item quantity
    async function updateCart(productId, quantity) {
        try {
            const response = await fetch(`/cart/update/${productId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken(),
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: `quantity=${quantity}`
            });
            const data = await response.json();
            if (data.success) {
                document.querySelector(`#cart-total`).textContent = data.cart_total;
                document.querySelector(`tr[data-product-id='${productId}'] .product-total`).textContent = `₹${data.item_total}`;
            } else {
                alert("Failed to update cart.");
            }
        } catch (error) {
            console.error("Error updating cart:", error);
        }
    }

    // ✅ Handle "Remove from Cart" buttons
    document.querySelectorAll(".remove-btn").forEach(button => {
        button.addEventListener("click", async function (event) {
            event.preventDefault();
            const productId = this.dataset.productId;
            await removeFromCart(productId);
        });
    });

    // ✅ Function to remove item from cart
    async function removeFromCart(productId) {
        try {
            const response = await fetch(`/cart/remove/${productId}/`, {
                method: "POST",
                headers: { "X-CSRFToken": getCSRFToken() }
            });
            const data = await response.json();
            if (data.success) {
                document.querySelector(`tr[data-product-id='${productId}']`).remove();
                document.querySelector("#cart-total").textContent = data.cart_total;
            } else {
                alert("Failed to remove item from cart.");
            }
        } catch (error) {
            console.error("Error removing from cart:", error);
        }
    }

    // ✅ Function to get CSRF token for POST requests
    function getCSRFToken() {
        return document.querySelector("[name=csrfmiddlewaretoken]")?.value || "";
    }
});