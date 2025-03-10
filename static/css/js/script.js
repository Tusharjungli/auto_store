document.addEventListener("DOMContentLoaded", function () {
  console.log("script.js loaded!");

  // ✅ Toggle Mobile Navigation Menu
  const menuToggle = document.querySelector("#menu-toggle");
  const navMenu = document.querySelector(".nav-menu");

  if (menuToggle && navMenu) {
      menuToggle.addEventListener("click", function () {
          navMenu.classList.toggle("active");
      });
  }

  // ✅ Close Menu on Click (Mobile)
  document.querySelectorAll(".nav-menu a").forEach(link => {
      link.addEventListener("click", function () {
          navMenu.classList.remove("active");
      });
  });

  // ✅ Handle "Shop Now" Button Scroll
  const shopNowButton = document.querySelector("#shop-now");
  if (shopNowButton) {
      shopNowButton.addEventListener("click", function (event) {
          event.preventDefault();
          const productSection = document.querySelector("#featured-products");
          if (productSection) {
              productSection.scrollIntoView({ behavior: "smooth" });
          }
      });
  }

  // ✅ Sticky Header on Scroll
  window.addEventListener("scroll", function () {
      const header = document.querySelector(".header");
      if (window.scrollY > 50) {
          header.classList.add("sticky");
      } else {
          header.classList.remove("sticky");
      }
  });

  // ✅ Fade-in Animation for Sections
  const fadeElements = document.querySelectorAll(".fade-in");
  const fadeObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => {
          if (entry.isIntersecting) {
              entry.target.classList.add("visible");
          }
      });
  });

  fadeElements.forEach(el => fadeObserver.observe(el));
});
