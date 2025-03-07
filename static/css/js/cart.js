// ✅ Toggle Cart Sidebar
function toggleCart() {
  let cartSidebar = document.getElementById("cart-sidebar");
  if (cartSidebar.style.right === "0px") {
      cartSidebar.style.right = "-300px"; // Hide Cart
  } else {
      cartSidebar.style.right = "0px"; // Show Cart
  }
}

// ✅ Add Item to Cart
function addToCart(productId, name, price) {
  let cartItems = document.getElementById("cart-items");
  let cartCount = document.getElementById("cart-count");

  // Create new item
  let item = document.createElement("div");
  item.classList.add("cart-item");
  item.innerHTML = `<p>${name} - ₹${price}</p>`;

  cartItems.appendChild(item);

  // Update cart count
  cartCount.innerText = cartItems.children.length;
}

// ✅ Checkout (Placeholder)
function checkout() {
  alert("Proceeding to checkout!");
}
