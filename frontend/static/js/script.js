const API_BASE_URL = "http://127.0.0.1:5000/api";

const categoryMeta = {
    gym: { title: "Gym Lovers Menu", desc: "High-protein meals" },
    elders: { title: "Elders Menu", desc: "Healthy soft meals" },
    kids: { title: "Kids Menu", desc: "Tasty fun meals" }
};

const categoryNames = {
    gym: "gym",
    elders: "elders",
    kids: "kids"
};

async function apiRequest(endpoint, method = "GET", data = null, requireAuth = false) {
    const headers = { "Content-Type": "application/json" };
    if (requireAuth) {
        const token = localStorage.getItem("access_token");
        if (!token) return { success: false, message: "Please login first" };
        headers.Authorization = `Bearer ${token}`;
    }

    const options = { method, headers };
    if (data && method !== "GET") options.body = JSON.stringify(data);

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        return await response.json();
    } catch (error) {
        return { success: false, message: "Backend is not running. Start Flask on port 5000." };
    }
}

function currentUser() {
    const user = localStorage.getItem("currentUser");
    return user ? JSON.parse(user) : null;
}

function setSession(data) {
    localStorage.setItem("access_token", data.access_token);
    localStorage.setItem("currentUser", JSON.stringify({
        id: data.user.id,
        email: data.user.email,
        username: data.user.full_name,
        user_type: data.user.user_type
    }));
}

document.addEventListener("DOMContentLoaded", () => {
    updateNavbar();
    updateCartCount();

    if (window.location.pathname.includes("category.html")) renderCategoryPage();
    if (window.location.pathname.includes("cart.html")) renderCartPage();
    if (window.location.pathname.includes("checkout.html")) renderCheckoutPage();
});

function updateNavbar() {
    const navRight = document.getElementById("navRight");
    if (!navRight) return;

    const user = currentUser();
    if (user) {
        navRight.innerHTML = `
            <div class="profile-container">
                <div class="profile-circle" onclick="toggleProfile()">
                    ${user.username.charAt(0).toUpperCase()}
                </div>
                <div class="profile-dropdown" id="profileDropdown">
                    <p>${user.username}</p>
                    <p style="font-size:12px;color:gray;">${user.email}</p>
                    <a href="#" onclick="logout()" class="logout-btn">Logout</a>
                </div>
            </div>
        `;
    } else {
        navRight.innerHTML = `
            <a href="login.html" class="nav-btn">Login</a>
            <a href="signup.html" class="nav-btn signup">Sign Up</a>
        `;
    }
}

function toggleProfile() {
    document.getElementById("profileDropdown").classList.toggle("show");
}

window.onclick = function(e) {
    if (!e.target.matches(".profile-circle")) {
        const dropdown = document.getElementById("profileDropdown");
        if (dropdown && dropdown.classList.contains("show")) dropdown.classList.remove("show");
    }
};

async function signup(e) {
    e.preventDefault();
    const fullName = document.getElementById("username").value.trim();
    const email = document.getElementById("email").value.trim().toLowerCase();
    const password = document.getElementById("password").value;

    const result = await apiRequest("/auth/register", "POST", {
        full_name: fullName,
        email,
        password,
        user_type: "user"
    });

    if (!result.success) {
        document.getElementById("error-msg").innerText = result.message;
        return;
    }

    const loginResult = await apiRequest("/auth/login", "POST", { email, password });
    if (loginResult.success) {
        setSession(loginResult.data);
        window.location.href = "menu.html";
    }
}

async function login(e) {
    e.preventDefault();
    const email = document.getElementById("email").value.trim().toLowerCase();
    const password = document.getElementById("password").value;

    const result = await apiRequest("/auth/login", "POST", { email, password });
    if (result.success) {
        setSession(result.data);
        window.location.href = result.data.user.user_type === "admin" ? "admin.html" : "menu.html";
    } else {
        document.getElementById("error-msg").innerText = result.message;
    }
}

async function logout() {
    if (localStorage.getItem("access_token")) {
        await apiRequest("/auth/logout", "POST", {}, true);
    }
    localStorage.removeItem("access_token");
    localStorage.removeItem("currentUser");
    localStorage.removeItem("cart");
    window.location.href = "index.html";
}

function getCart() {
    return JSON.parse(localStorage.getItem("cart")) || [];
}

function saveCart(cart) {
    localStorage.setItem("cart", JSON.stringify(cart));
}

function updateCartCount() {
    const cartElement = document.getElementById("cartCount");
    if (cartElement) cartElement.innerText = getCart().length;
}

async function renderCategoryPage() {
    const urlParams = new URLSearchParams(window.location.search);
    const cat = urlParams.get("cat");
    const meta = categoryMeta[cat];

    if (!cat || !meta) {
        document.querySelector(".menu-page").innerHTML = "<h2>Category not found</h2>";
        return;
    }

    document.getElementById("catTitle").innerText = meta.title;
    document.getElementById("catDesc").innerText = meta.desc;

    const grid = document.getElementById("foodGrid");
    grid.innerHTML = "<p>Loading meals...</p>";

    const result = await apiRequest(`/meals/?category=${encodeURIComponent(categoryNames[cat])}`);
    if (!result.success) {
        grid.innerHTML = `<p>${result.message}</p>`;
        return;
    }

    grid.innerHTML = "";
    result.data.forEach(food => {
        const imgSrc = food.image || "static/images/food.jpg";
        grid.innerHTML += `
            <div class="food-card">
                <img src="${imgSrc}">
                <div class="food-info">
                    <h3>${food.meal_name}</h3>
                    <div class="price-row">
                        <span class="price">Rs.${food.price}</span>
                        <button class="add-btn" onclick="openModal(${food.id}, '${escapeText(food.meal_name)}', '${food.price}', '${imgSrc}')">Add</button>
                    </div>
                </div>
            </div>
        `;
    });
}

function escapeText(value) {
    return String(value).replace(/'/g, "\\'");
}

function openModal(id, name, price, image) {
    document.getElementById("scheduleModal").style.display = "flex";
    document.getElementById("foodName").value = name;
    document.getElementById("foodPrice").value = price;
    document.getElementById("foodImage").value = image;
    document.getElementById("foodName").dataset.mealId = id;
}

function closeModal() {
    document.getElementById("scheduleModal").style.display = "none";
}

function addToCart(e) {
    e.preventDefault();
    if (!currentUser()) {
        window.location.href = "login.html";
        return;
    }

    const cart = getCart();
    cart.push({
        meal_id: Number(document.getElementById("foodName").dataset.mealId),
        name: document.getElementById("foodName").value,
        price: Number(document.getElementById("foodPrice").value),
        image: document.getElementById("foodImage").value,
        day: document.getElementById("daySelect").value,
        time: document.getElementById("timeSelect").value
    });
    saveCart(cart);

    closeModal();
    updateCartCount();
    alert("Added to cart!");
}

function renderCartPage() {
    const cart = getCart();
    const tableDiv = document.getElementById("cartTableBody");
    let total = 0;
    tableDiv.innerHTML = "";

    if (cart.length === 0) {
        tableDiv.innerHTML = "<p style='padding:20px'>Your cart is empty.</p>";
        document.getElementById("totalItems").innerText = "0";
        document.getElementById("totalAmount").innerText = "Rs.0";
        return;
    }

    cart.forEach((item, index) => {
        total += Number(item.price);
        tableDiv.innerHTML += `
            <div class="table-row">
                <div class="meal">
                    <img src="${item.image}">
                    <p>${item.name}</p>
                </div>
                <span>Rs.${item.price}</span>
                <select><option>${item.day}</option></select>
                <select><option>${item.time}</option></select>
                <button onclick="removeFromCart(${index})" class="delete-btn" style="border:none;background:none;cursor:pointer;font-size:20px;">Delete</button>
            </div>
        `;
    });

    document.getElementById("totalItems").innerText = "Total Meals Added: " + cart.length;
    document.getElementById("totalAmount").innerText = "Rs." + total;
}

function removeFromCart(index) {
    const cart = getCart();
    cart.splice(index, 1);
    saveCart(cart);
    renderCartPage();
    updateCartCount();
}

function renderCheckoutPage() {
    const cart = getCart();
    const total = cart.reduce((sum, item) => sum + Number(item.price), 0);
    document.getElementById("checkoutTotalItems").innerText = cart.length;
    document.getElementById("checkoutTotalAmount").innerText = "Rs." + total;
}

function nextMonday() {
    const date = new Date();
    const day = date.getDay();
    const diff = day === 1 ? 0 : (8 - day) % 7;
    date.setDate(date.getDate() + diff);
    return date.toISOString().slice(0, 10);
}

async function confirmOrder(e) {
    e.preventDefault();
    const user = currentUser();
    if (!user) {
        window.location.href = "login.html";
        return;
    }

    const cart = getCart();
    const selectedDays = new Set(cart.map(item => item.day));
    const requiredDays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
    if (!requiredDays.every(day => selectedDays.has(day))) {
        alert("Please add one meal for each day from Monday to Sunday.");
        return;
    }

    const selected = document.querySelector('input[name="payment"]:checked');
    if (!selected) {
        alert("Please select a payment method");
        return;
    }

    if (selected.value === "Card") {
        const cardNumber = document.querySelector("#card-options input:nth-child(1)").value;
        if (!cardNumber) {
            alert("Enter card details");
            return;
        }
    }

    const orderResult = await apiRequest("/orders/", "POST", {
        week_start_date: nextMonday(),
        delivery_address: document.getElementById("address").value,
        items: cart.map(item => ({
            meal_id: item.meal_id,
            day_of_week: item.day,
            delivery_time: item.time,
            quantity: 1
        }))
    }, true);

    if (!orderResult.success) {
        alert(orderResult.message);
        return;
    }

    const paymentMethod = selected.value === "COD" ? "Cash on Delivery" : selected.value;
    const paymentResult = await apiRequest("/payments/create", "POST", {
        order_id: orderResult.data.id,
        payment_method: paymentMethod,
        provider: selected.value
    }, true);

    if (!paymentResult.success) {
        alert(paymentResult.message);
        return;
    }

    localStorage.removeItem("cart");
    window.location.href = `success.html?orderId=${orderResult.data.id}`;
}
