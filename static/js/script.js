document.addEventListener("DOMContentLoaded", function () {
    console.log("script.js loaded!");

    // ✅ Toggle Three-Dot Menu Dropdown
    const menuToggle = document.querySelector(".three-dot-menu");
    const dropdownMenu = document.querySelector(".menu-dropdown");

    if (menuToggle && dropdownMenu) {
        menuToggle.addEventListener("click", function (event) {
            event.stopPropagation();
            dropdownMenu.classList.toggle("active");
            menuToggle.classList.toggle("rotated");

            if (dropdownMenu.classList.contains("active")) {
                dropdownMenu.style.display = "block";
                setTimeout(() => (dropdownMenu.style.opacity = "1"), 50);
            } else {
                dropdownMenu.style.opacity = "0";
                setTimeout(() => (dropdownMenu.style.display = "none"), 300);
            }
        });

        // ✅ Close Dropdown When Clicking Outside
        document.addEventListener("click", function (event) {
            if (!menuToggle.contains(event.target) && !dropdownMenu.contains(event.target)) {
                dropdownMenu.classList.remove("active");
                menuToggle.classList.remove("rotated");
                dropdownMenu.style.opacity = "0";
                setTimeout(() => (dropdownMenu.style.display = "none"), 300);
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
        navbar.classList.toggle("scrolled", scrollY > 50);

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

    // ✅ Light/Dark Mode Toggle
    const themeToggle = document.querySelector(".theme-toggle");
    const body = document.body;

    if (themeToggle) {
        if (localStorage.getItem("theme") === "dark") {
            body.classList.add("dark-mode");
        }

        themeToggle.addEventListener("click", function () {
            body.classList.toggle("dark-mode");
            localStorage.setItem("theme", body.classList.contains("dark-mode") ? "dark" : "light");
        });
    }

    // ✅ Load Chat History
    loadChatHistory();

    // ✅ Handle Enter Key Press in Chat Input
    const chatInput = document.getElementById("chatbot-input");
    if (chatInput) {
        chatInput.addEventListener("keypress", function (event) {
            if (event.key === "Enter") {
                event.preventDefault();  // Prevent default form submission
                sendMessage();  // Call sendMessage function
            }
        });
    }
});

// ✅ CSRF Token Retrieval Function
function getCSRFToken() {
    let csrfToken = document.cookie
        .split("; ")
        .find(row => row.startsWith("csrftoken="))
        ?.split("=")[1];
    return csrfToken || "";
}

// ✅ Toggle Chatbot Window
function toggleChatbot() {
    const chatbot = document.getElementById("chatbot");
    chatbot.style.display = chatbot.style.display === "flex" ? "none" : "flex";
}

// ✅ Load Chat History from sessionStorage
function loadChatHistory() {
    const chatbox = document.getElementById("chatbot-messages");
    const history = sessionStorage.getItem("chatHistory");
    if (history) {
        chatbox.innerHTML = history;
        chatbox.scrollTop = chatbox.scrollHeight;
    }
}

// ✅ Save Chat History to sessionStorage
function saveChatHistory() {
    const chatbox = document.getElementById("chatbot-messages");
    sessionStorage.setItem("chatHistory", chatbox.innerHTML);
}

// ✅ Handle User Message
function sendMessage() {
    const inputField = document.getElementById("chatbot-input");
    const message = inputField.value.trim();
    if (message === "") return;

    // ✅ Display User Message Instantly
    displayMessage("You", message);

    // ✅ Show Typing Indicator for Bot
    const botMessage = displayMessage("Bot", "🤖 Typing...");

    // ✅ Retrieve Chat History
    const chatbox = document.getElementById("chatbot-messages");
    const chatHistory = chatbox.innerHTML;

    // ✅ Send Message & Chat History to Backend
    fetch("/chatbot/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({
            message: message,
            chat_history: chatHistory
        }),
    })
    .then(response => response.json())
    .then(data => {
        botMessage.innerHTML = `<strong>Bot:</strong> ${data.response || "⚠️ No response received."}`;
        saveChatHistory();  // ✅ Save updated chat history
    })
    .catch(error => {
        botMessage.innerHTML = `<strong>Bot:</strong> ❌ Error: Could not connect.`;
        console.error("❌ Chatbot Error:", error);
    });

    inputField.value = "";
}

// ✅ Display Message in Chat Window
function displayMessage(sender, message) {
    const chatbox = document.getElementById("chatbot-messages");
    const msgElement = document.createElement("div");
    msgElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatbox.appendChild(msgElement);
    chatbox.scrollTop = chatbox.scrollHeight;
    return msgElement;
}
