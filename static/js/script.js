document.addEventListener("DOMContentLoaded", function () {
    console.log("script.js loaded!");

    // ✅ Toggle Three-Dot Menu Dropdown
    const menuToggle = document.querySelector(".three-dot-menu"); // Selector for the three-dot menu
    const dropdownMenu = document.querySelector(".menu-dropdown"); // Selector for the dropdown menu

    if (menuToggle && dropdownMenu) {
        menuToggle.addEventListener("click", function (event) {
            event.stopPropagation();
            dropdownMenu.classList.toggle("active");
            menuToggle.classList.toggle("rotated");

            if (dropdownMenu.classList.contains("active")) {
                dropdownMenu.style.display = "block";
                setTimeout(() => dropdownMenu.style.opacity = "1", 50);
            } else {
                dropdownMenu.style.opacity = "0";
                setTimeout(() => dropdownMenu.style.display = "none", 300); // Hide smoothly
            }
        });

        // ✅ Close Dropdown When Clicking Outside
        document.addEventListener("click", function (event) {
            if (!menuToggle.contains(event.target) && !dropdownMenu.contains(event.target)) {
                dropdownMenu.classList.remove("active");
                menuToggle.classList.remove("rotated");
                dropdownMenu.style.opacity = "0";
                setTimeout(() => dropdownMenu.style.display = "none", 300);
            }
        });

        // ✅ Prevent Dropdown from Closing When Clicking Inside
        dropdownMenu.addEventListener("click", function (event) {
            event.stopPropagation();
        });
    }

    // ✅ Sticky Navbar with Auto-Hide on Scroll
    const navbar = document.querySelector(".navbar");
    let lastScrollY = window.scrollY;
    let isScrollingDown = false;
    let timeout;

    window.addEventListener("scroll", function () {
        clearTimeout(timeout);
        let scrollY = window.scrollY;

        // Apply background blur on scroll
        if (scrollY > 50) {
            navbar.classList.add("scrolled");
        } else {
            navbar.classList.remove("scrolled");
        }

        // Auto-hide navbar on scroll down, show on scroll up
        if (scrollY > lastScrollY) {
            if (!isScrollingDown) {
                navbar.classList.add("hidden");
                isScrollingDown = true;
            }
        } else {
            if (isScrollingDown) {
                navbar.classList.remove("hidden");
                isScrollingDown = false;
            }
        }
        lastScrollY = scrollY;

        // Prevent flickering with debounce
        timeout = setTimeout(() => navbar.classList.remove("hidden"), 300);
    });

    // ✅ Smooth Fade-in Animation for Sections
    const fadeElements = document.querySelectorAll(".fade-in");
    const fadeObserver = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("visible");
            }
        });
    });

    fadeElements.forEach(el => fadeObserver.observe(el));

    // ✅ Light/Dark Mode Toggle (Ensuring it runs after DOM loads)
    const themeToggle = document.querySelector(".theme-toggle"); // Button for switching themes
    const body = document.body; // Body element to apply theme changes

    if (themeToggle) {
        // Check for saved theme preference in localStorage
        if (localStorage.getItem("theme") === "dark") {
            body.classList.add("dark-mode"); // Apply dark mode
        }

        // Toggle theme when button is clicked
        themeToggle.addEventListener("click", function () {
            body.classList.toggle("dark-mode"); // Add or remove dark-mode class

            // Save preference to localStorage
            if (body.classList.contains("dark-mode")) {
                localStorage.setItem("theme", "dark");
            } else {
                localStorage.setItem("theme", "light");
            }
        });
    }
});
