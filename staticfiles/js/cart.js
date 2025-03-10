document.addEventListener("DOMContentLoaded", function () {
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

    // ✅ Update Cart (AJAX)
    document.querySelectorAll(".cart-item-quantity").forEach(input => {
        input.addEventListener("change", function () {
            const productId = this.dataset.productId;
            const newQuantity = this.value;

            fetch(`/cart/update/${productId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken(),
                    "X-Requested-With": "XMLHttpRequest",
                },
                body: new URLSearchParams({ quantity: newQuantity }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.querySelector(`#item-total-${productId}`).innerText = `₹${data.item_total}`;
                    document.querySelector("#cart-total").innerText = `Total: ₹${data.cart_total}`;
                }
            });
        });
    });

    // ✅ Remove from Cart (AJAX)
    document.querySelectorAll(".remove-from-cart-btn").forEach(button => {
        button.addEventListener("click", function () {
            const productId = this.dataset.productId;

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
                    document.querySelector(`#cart-item-${productId}`).remove();
                    document.querySelector("#cart-total").innerText = `Total: ₹${data.cart_total}`;
                }
            });
        });
    });

    // ✅ Function to Get CSRF Token
    function getCSRFToken() {
        return document.querySelector("input[name=csrfmiddlewaretoken]").value;
    }

    // ✅ Function to Update Cart Count
    function updateCartCount(count) {
        document.querySelector("#cart-count").innerText = count;
    }
});
