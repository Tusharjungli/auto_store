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
                    document.querySelector("#cart-total").innerText = `Total: ₹${data.cart_total}`;
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
                parent.querySelector(".item-total").innerText = `₹${data.item_total}`;
                document.querySelector("#cart-total").innerText = `Total: ₹${data.cart_total}`;
            }
        })
        .catch(error => console.error("Error updating cart:", error));
    }

    // ✅ Function to Get CSRF Token
    function getCSRFToken() {
        return document.querySelector("input[name=csrfmiddlewaretoken]").value;
    }

    // ✅ Function to Update Cart Count (if needed)
    function updateCartCount(count) {
        document.querySelector("#cart-count").innerText = count;
    }
});
