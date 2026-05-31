/**
 * Smart Canteen Pre-ordering System - API Client
 * 
 * Include this script in your HTML: <script src="frontend_api.js"></script>
 * Make sure to call these functions from your other JavaScript files when needed.
 */

const API_BASE_URL = 'http://127.0.0.1:5000/api';

// Utility function to handle API requests
async function apiRequest(endpoint, method = 'GET', data = null, requireAuth = false) {
    const headers = {
        'Content-Type': 'application/json'
    };

    if (requireAuth) {
        const token = localStorage.getItem('access_token');
        if (!token) {
            console.error("No access token found. Please login.");
            return { success: false, message: "Authentication required." };
        }
        headers['Authorization'] = `Bearer ${token}`;
    }

    const options = {
        method,
        headers
    };

    if (data && (method === 'POST' || method === 'PUT')) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        return await response.json();
    } catch (error) {
        console.error(`API Request Error (${endpoint}):`, error);
        return { success: false, message: 'Network error occurred. Is the backend running?' };
    }
}

// ----------------------------------------
// 1. Authentication APIs
// ----------------------------------------

async function registerUser(fullName, email, phone, password, userType = 'user') {
    return await apiRequest('/auth/register', 'POST', {
        full_name: fullName,
        email,
        phone,
        password,
        user_type: userType
    });
}

async function loginUser(email, password) {
    const response = await apiRequest('/auth/login', 'POST', { email, password });
    if (response.success && response.data) {
        localStorage.setItem('access_token', response.data.access_token);
        localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response;
}

function logoutUser() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    console.log("Logged out successfully");
}

async function forgotPassword(email) {
    return await apiRequest('/auth/forgot-password', 'POST', { email });
}

async function resetPassword(email, resetToken, newPassword) {
    return await apiRequest('/auth/reset-password', 'POST', {
        email,
        reset_token: resetToken,
        new_password: newPassword
    });
}

// ----------------------------------------
// 2. User Profile APIs
// ----------------------------------------

async function getUserProfile() {
    return await apiRequest('/users/profile', 'GET', null, true);
}

async function updateProfile(fullName, phone) {
    return await apiRequest('/users/profile', 'PUT', { full_name: fullName, phone }, true);
}

// ----------------------------------------
// 3. Meal Plan APIs
// ----------------------------------------

async function getMeals(category = null, search = null) {
    let url = '/meals/';
    const params = new URLSearchParams();
    if (category) params.append('category', category);
    if (search) params.append('search', search);
    
    if (params.toString()) {
        url += `?${params.toString()}`;
    }
    return await apiRequest(url, 'GET');
}

// Admin only
async function addMeal(mealData) {
    return await apiRequest('/meals/', 'POST', mealData, true);
}

// ----------------------------------------
// 4. Weekly Order APIs
// ----------------------------------------

/**
 * items format: [{ meal_id: 1, day_of_week: 'Monday', quantity: 1 }]
 */
async function createWeeklyOrder(weekStartDate, items) {
    return await apiRequest('/orders/', 'POST', {
        week_start_date: weekStartDate, // Format: YYYY-MM-DD
        items: items
    }, true);
}

async function getMyOrders() {
    return await apiRequest('/orders/', 'GET', null, true);
}

async function getOrderDetails(orderId) {
    return await apiRequest(`/orders/${orderId}`, 'GET', null, true);
}

async function cancelOrder(orderId) {
    return await apiRequest(`/orders/${orderId}/cancel`, 'PUT', null, true);
}

// ----------------------------------------
// 5. Payment APIs
// ----------------------------------------

async function createPayment(orderId, paymentMethod = 'Cash on Delivery') {
    return await apiRequest('/payments/create', 'POST', {
        order_id: orderId,
        payment_method: paymentMethod
    }, true);
}

// ----------------------------------------
// 6. Delivery Time Slot APIs
// ----------------------------------------

async function getTimeSlots() {
    return await apiRequest('/delivery/slots', 'GET');
}

// ----------------------------------------
// 7. Admin Dashboard APIs
// ----------------------------------------

async function getDashboardStats() {
    return await apiRequest('/admin/dashboard', 'GET', null, true);
}

// ----------------------------------------
// Usage Example (Commented out)
// ----------------------------------------
/*
// Put this in your frontend JS file:

document.getElementById('loginBtn').addEventListener('click', async () => {
    const res = await loginUser('john@example.com', 'user123');
    if (res.success) {
        alert("Logged in successfully!");
        
        // Fetch meals after login
        const mealsRes = await getMeals();
        console.log("Available Meals:", mealsRes.data);
    } else {
        alert("Login failed: " + res.message);
    }
});
*/
