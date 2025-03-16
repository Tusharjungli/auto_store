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

    // ✅ Modern Sticky & Auto-Hide Header on Scroll
    let navbar = document.querySelector(".navbar");
    let lastScrollY = window.scrollY;
    let isScrollingDown = false;

    window.addEventListener("scroll", function () {
        let scrollY = window.scrollY;

        if (scrollY > 50) {
            navbar.classList.add("scrolled"); // Adds glass effect
        } else {
            navbar.classList.remove("scrolled"); // Removes glass effect
        }

        if (scrollY > lastScrollY) {
            if (!isScrollingDown) {
                navbar.classList.add("hidden"); // Hide on scroll down
                isScrollingDown = true;
            }
        } else {
            if (isScrollingDown) {
                navbar.classList.remove("hidden"); // Show on scroll up
                isScrollingDown = false;
            }
        }
        lastScrollY = scrollY;
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
