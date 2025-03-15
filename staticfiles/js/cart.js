document.addEventListener("DOMContentLoaded", function () {
    fetchCartCount(); // ✅ Ensure the cart count loads on page load

    // ✅ Add to Cart (AJAX)
    document.querySelectorAll(".add-to-cart-btn").forEach(button => {
        button.addEventListener("click", function () {
            const productId = this.dataset.productId;

            fetch(`/cart/add/${productId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken(),
                    "X-Requested-With": "XMLHttpRequest",
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    updateCartCount(data.cart_count);
                    alert("Item added to cart!");
                }
            });
        });
    });

    // ✅ Increase & Decrease Quantity (AJAX)
    document.querySelectorAll(".increase-btn, .decrease-btn").forEach(button => {
        button.addEventListener("click", function () {
            const parent = this.closest("tr");
            const productId = parent.dataset.productId;
            const quantityInput = parent.querySelector(".cart-item-quantity");
            let newQuantity = parseInt(quantityInput.value);

            if (this.classList.contains("increase-btn")) {
                newQuantity++;
            } else if (this.classList.contains("decrease-btn") && newQuantity > 1) {
                newQuantity--;
            }

            quantityInput.value = newQuantity;
            updateCart(productId, newQuantity, parent);
        });
    });

    // ✅ Update Cart on Manual Input Change (AJAX)
    document.querySelectorAll(".cart-item-quantity").forEach(input => {
        input.addEventListener("change", function () {
            const parent = this.closest("tr");
            const productId = parent.dataset.productId;
            let newQuantity = parseInt(this.value);

            if (newQuantity > 0) {
                updateCart(productId, newQuantity, parent);
            }
        });
    });

    // ✅ Remove from Cart (AJAX)
    document.querySelectorAll(".remove-from-cart-btn").forEach(button => {
        button.addEventListener("click", function () {
            const parent = this.closest("tr");
            const productId = parent.dataset.productId;

            fetch(`/cart/remove/${productId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken(),
                    "X-Requested-With": "XMLHttpRequest",
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    parent.remove();
                    document.querySelector("#cart-total").textContent = `Total: ₹${data.cart_total}`;
                    updateCartCount(data.cart_count);
                }
            });
        });
    });

    // ✅ Function to Update Cart Quantity & Prices
    function updateCart(productId, quantity, parent) {
        fetch(`/cart/update/${productId}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "X-Requested-With": "XMLHttpRequest",
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: new URLSearchParams({ quantity: quantity }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                parent.querySelector(".item-total").textContent = `₹${data.item_total}`;
                document.querySelector("#cart-total").textContent = `Total: ₹${data.cart_total}`;
                updateCartCount(data.cart_count);
            }
        })
        .catch(error => console.error("Error updating cart:", error));
    }

    // ✅ Function to Fetch Initial Cart Count
    function fetchCartCount() {
        fetch(`/cart/count/`) // 🔹 This API should return {"cart_count": X}
            .then(response => response.json())
            .then(data => {
                if (data.cart_count !== undefined) {
                    updateCartCount(data.cart_count);
                }
            })
            .catch(error => console.error("Error fetching cart count:", error));
    }

    // ✅ Function to Get CSRF Token
    function getCSRFToken() {
        return document.querySelector("input[name=csrfmiddlewaretoken]").value;
    }

    // ✅ Function to Update Cart Count in Navbar
    function updateCartCount(count) {
        let cartCountElement = document.querySelector("#cart-count");

        if (cartCountElement) {
            cartCountElement.textContent = count;
        } else {
            console.error("Cart count element not found!");
        }
    }
});
