const API_BASE_URL = "http://127.0.0.1:5000/api";
const ORDER_STATUSES = ["Pending", "Completed"];

document.addEventListener("DOMContentLoaded", () => {
    checkAdminAuth();
    refreshAdminData();

    document.getElementById("foodImageFile").addEventListener("change", handleImageUpload);
    document.getElementById("foodImageUrl").addEventListener("input", function() {
        if (document.getElementById("imageType").value === "url" && this.value) {
            document.getElementById("imagePreview").src = this.value;
            document.getElementById("imagePreview").style.display = "block";
        }
    });
});

let base64Image = null;

async function apiRequest(endpoint, method = "GET", data = null, requireAuth = true) {
    const headers = { "Content-Type": "application/json" };
    if (requireAuth) headers.Authorization = `Bearer ${localStorage.getItem("access_token")}`;
    const options = { method, headers };
    if (data && method !== "GET") options.body = JSON.stringify(data);

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        return await response.json();
    } catch (error) {
        return { success: false, message: "Backend is not running. Start Flask on port 5000." };
    }
}

function checkAdminAuth() {
    const currentUser = JSON.parse(localStorage.getItem("currentUser"));
    if (!localStorage.getItem("access_token") || !currentUser || currentUser.user_type !== "admin") {
        window.location.href = "admin-login.html";
    }
}

async function logoutAdmin() {
    await apiRequest("/auth/logout", "POST", {});
    localStorage.removeItem("access_token");
    localStorage.removeItem("currentUser");
    window.location.href = "admin-login.html";
}

function switchTab(tabId) {
    document.querySelectorAll(".tab-content").forEach(tab => tab.classList.remove("active"));
    document.querySelectorAll(".nav-menu li").forEach(li => li.classList.remove("active"));
    document.getElementById(tabId).classList.add("active");
    event.target.classList.add("active");
}

function refreshAdminData() {
    renderDashboard();
    renderFoodList();
    renderOrders();
}

function toggleImageInput() {
    const type = document.getElementById("imageType").value;
    document.getElementById("urlInputGroup").style.display = type === "url" ? "block" : "none";
    document.getElementById("uploadInputGroup").style.display = type === "upload" ? "block" : "none";
    document.getElementById("imagePreview").style.display = "none";
    document.getElementById("foodImageUrl").value = "";
    document.getElementById("foodImageFile").value = "";
    base64Image = null;
}

function handleImageUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = function(e) {
        const img = new Image();
        img.src = e.target.result;
        img.onload = function() {
            const canvas = document.getElementById("imageCanvas");
            const ctx = canvas.getContext("2d");
            const maxWidth = 400;
            const scaleSize = maxWidth / img.width;
            canvas.width = maxWidth;
            canvas.height = img.height * scaleSize;
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            base64Image = canvas.toDataURL("image/jpeg", 0.7);
            document.getElementById("imagePreview").src = base64Image;
            document.getElementById("imagePreview").style.display = "block";
        };
    };
}

async function addFood(e) {
    e.preventDefault();
    const imageType = document.getElementById("imageType").value;
    const image = imageType === "url" ? document.getElementById("foodImageUrl").value : base64Image;
    if (!image) {
        alert("Please provide an image.");
        return;
    }

    const result = await apiRequest("/meals/", "POST", {
        meal_name: document.getElementById("foodName").value,
        price: Number(document.getElementById("foodPrice").value),
        category: document.getElementById("foodCategory").value,
        image
    });

    if (!result.success) {
        alert(result.message);
        return;
    }

    document.getElementById("addFoodForm").reset();
    document.getElementById("imagePreview").style.display = "none";
    base64Image = null;
    alert("Food added successfully!");
    renderFoodList();
    renderDashboard();
}

async function renderFoodList() {
    const tbody = document.getElementById("foodTableBody");
    const filter = document.getElementById("filterCategory").value;
    const query = filter === "all" ? "?include_unavailable=1" : `?category=${filter}&include_unavailable=1`;
    const result = await apiRequest(`/meals/${query}`, "GET", null, false);

    tbody.innerHTML = "";
    if (!result.success || result.data.length === 0) {
        tbody.innerHTML = "<tr><td colspan='6' style='text-align:center;'>No menu items found.</td></tr>";
        return;
    }

    result.data.forEach(food => {
        tbody.innerHTML += `
            <tr>
                <td><img src="${food.image || "static/images/food.jpg"}" alt="food"></td>
                <td>${food.meal_name}</td>
                <td>${food.category}</td>
                <td>Rs.${food.price}</td>
                <td><span class="status-pill ${food.is_available ? "ok" : "muted"}">${food.is_available ? "Available" : "Hidden"}</span></td>
                <td>
                    <div class="action-row">
                        <button class="small-btn" onclick="editFood(${food.id}, '${escapeText(food.meal_name)}', ${food.price})">Edit</button>
                        <button class="small-btn" onclick="toggleFood(${food.id}, ${!food.is_available})">${food.is_available ? "Hide" : "Show"}</button>
                        <button class="delete-btn" onclick="deleteFood(${food.id})">Delete</button>
                    </div>
                </td>
            </tr>
        `;
    });
}

function escapeText(value) {
    return String(value).replace(/'/g, "\\'");
}

async function editFood(id, currentName, currentPrice) {
    const mealName = prompt("Meal name", currentName);
    if (!mealName) return;
    const price = prompt("Price", currentPrice);
    if (!price || Number(price) <= 0) return;

    const result = await apiRequest(`/meals/${id}`, "PUT", {
        meal_name: mealName,
        price: Number(price)
    });
    if (!result.success) {
        alert(result.message);
        return;
    }
    renderFoodList();
    renderDashboard();
}

async function toggleFood(id, isAvailable) {
    const result = await apiRequest(`/meals/${id}`, "PUT", { is_available: isAvailable });
    if (!result.success) {
        alert(result.message);
        return;
    }
    renderFoodList();
    renderDashboard();
}

async function deleteFood(id) {
    if (!confirm("Are you sure you want to delete this item?")) return;
    const result = await apiRequest(`/meals/${id}`, "DELETE");
    if (!result.success) {
        alert(result.message);
        return;
    }
    renderFoodList();
    renderDashboard();
}

async function renderOrders() {
    const result = await apiRequest("/orders/");
    const tbody = document.getElementById("ordersTableBody");
    tbody.innerHTML = "";

    if (!result.success || result.data.length === 0) {
        tbody.innerHTML = "<tr><td colspan='7' style='text-align:center;'>No orders yet.</td></tr>";
        return;
    }

    result.data.forEach(order => {
        const items = order.items.map(i => `${i.meal_name} (x${i.quantity})`).join(", ");
        const customer = order.user ? `${order.user.full_name}<br><span class="subtle">${order.user.email}</span>` : `User #${order.user_id}`;
        tbody.innerHTML += `
            <tr>
                <td>#${order.id}</td>
                <td>${new Date(order.created_at).toLocaleString()}</td>
                <td>${customer}</td>
                <td>Rs.${order.total_price}</td>
                <td>${items}</td>
                <td><span class="${orderStatusClass(order.status)}">${order.status}</span></td>
                <td>
                    <div class="action-row">
                        <select id="status-${order.id}">
                            ${ORDER_STATUSES.map(status => `<option value="${status}" ${status === order.status ? "selected" : ""}>${status}</option>`).join("")}
                        </select>
                        <button class="small-btn" onclick="updateOrderStatus(${order.id})">Update</button>
                    </div>
                </td>
            </tr>
        `;
    });
}

async function updateOrderStatus(orderId) {
    const status = document.getElementById(`status-${orderId}`).value;
    const result = await apiRequest(`/orders/${orderId}/status`, "PUT", { status });
    if (!result.success) {
        alert(result.message);
        return;
    }
    alert(result.message || "Order status updated successfully");
    renderOrders();
    renderDashboard();
}

function orderStatusClass(status) {
    return status === "Completed" ? "status-pill completed" : "status-pill pending";
}

async function renderDashboard() {
    const result = await apiRequest("/admin/dashboard");
    if (!result.success) return;

    document.getElementById("totalOrdersStat").innerText = result.data.total_orders;
    document.getElementById("totalRevenueStat").innerText = `Rs.${result.data.total_revenue}`;
    document.getElementById("totalFoodsStat").innerText = result.data.total_menu_items;
    document.getElementById("totalUsersStat").innerText = result.data.total_users;
    document.getElementById("pendingDeliveriesStat").innerText = result.data.pending_deliveries;
    document.getElementById("pendingPaymentsStat").innerText = result.data.pending_payments;
    renderMostOrdered(result.data.most_ordered_meals || []);
    renderChart();
}

function renderMostOrdered(meals) {
    const list = document.getElementById("mostOrderedList");
    if (!meals.length) {
        list.innerHTML = '<p class="empty-text">No order data yet.</p>';
        return;
    }

    list.innerHTML = meals.map((meal, index) => `
        <div class="rank-item">
            <span>${index + 1}. ${meal.meal_name}</span>
            <strong>${meal.quantity}</strong>
        </div>
    `).join("");
}

async function renderChart() {
    const canvas = document.getElementById("ordersChart");
    if (typeof Chart === "undefined") {
        canvas.parentElement.innerHTML = '<p style="text-align:center;color:#aaa;padding:40px;">Chart unavailable.</p>';
        return;
    }

    const result = await apiRequest("/admin/analytics/revenue?days=30");
    const labels = result.success ? result.data.map(row => row.date) : [];
    const data = result.success ? result.data.map(row => row.revenue) : [];

    if (window.myChart) window.myChart.destroy();
    window.myChart = new Chart(canvas.getContext("2d"), {
        type: "bar",
        data: {
            labels,
            datasets: [{
                label: "Revenue (Rs.)",
                data,
                backgroundColor: "#ff6a00",
                borderRadius: 5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { beginAtZero: true, grid: { color: "#333" } },
                x: { grid: { display: false } }
            },
            plugins: { legend: { labels: { color: "white" } } }
        }
    });
}
