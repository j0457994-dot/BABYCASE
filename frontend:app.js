// API Configuration
const API_BASE_URL = window.location.origin.includes('localhost') 
    ? 'http://localhost:8000/api/v1'
    : 'https://your-backend.onrender.com/api/v1';

let apiKey = localStorage.getItem('apiKey');

// Login Handler
document.getElementById('loginForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        
        if (response.ok) {
            const data = await response.json();
            apiKey = data.api_key;
            localStorage.setItem('apiKey', apiKey);
            document.getElementById('loginScreen').style.display = 'none';
            document.getElementById('appContent').style.display = 'block';
            loadDashboard();
        } else {
            alert('Invalid credentials');
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('Connection error');
    }
});

// API Request Helper
async function apiRequest(endpoint, options = {}) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers: {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json',
            ...options.headers
        }
    });
    
    if (response.status === 401) {
        localStorage.removeItem('apiKey');
        location.reload();
    }
    
    return response.json();
}

// Copy API Key
function copyApiKey() {
    navigator.clipboard.writeText(apiKey);
    alert('API Key copied to clipboard!');
}

// Load Dashboard
async function loadDashboard() {
    const content = document.getElementById('pageContent');
    content.innerHTML = `
        <div class="dashboard-grid">
            <div class="stat-card">
                <div class="stat-header">
                    <h3>Active Campaigns</h3>
                    <span>📊</span>
                </div>
                <div class="stat-value">0</div>
            </div>
            <div class="stat-card">
                <div class="stat-header">
                    <h3>Targets Enriched</h3>
                    <span>🎯</span>
                </div>
                <div class="stat-value">0</div>
            </div>
            <div class="stat-card">
                <div class="stat-header">
                    <h3>Success Rate</h3>
                    <span>📈</span>
                </div>
                <div class="stat-value">0%</div>
            </div>
            <div class="stat-card">
                <div class="stat-header">
                    <h3>System Status</h3>
                    <span>🟢</span>
                </div>
                <div class="stat-value">Operational</div>
            </div>
        </div>
    `;
}

// Logout
document.getElementById('logoutBtn')?.addEventListener('click', () => {
    localStorage.removeItem('apiKey');
    location.reload();
});

// Navigation
document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', (e) => {
        e.preventDefault();
        document.querySelectorAll('.nav-item').forEach(nav => nav.classList.remove('active'));
        item.classList.add('active');
        const page = item.dataset.page;
        document.getElementById('pageTitle').innerText = item.querySelector('span').innerText;
        
        if (page === 'dashboard') loadDashboard();
    });
});

// Auto-login check
if (apiKey) {
    document.getElementById('loginScreen').style.display = 'none';
    document.getElementById('appContent').style.display = 'block';
    loadDashboard();
}