// General functionality for the application

document.addEventListener('DOMContentLoaded', function() {
    // Check if user is logged in
    checkLoginStatus();
    
    // Add event listeners
    setupEventListeners();
});

function checkLoginStatus() {
    // This would typically check with the server if the user is logged in
    // For now, we'll just simulate this behavior
    
    // In a real application, you would make an API call to check the session
    fetch('/api/check-auth')
        .then(response => response.json())
        .then(data => {
            if (data.authenticated) {
                // User is logged in
                document.getElementById('loginLink').textContent = 'Logout';
                document.getElementById('loginLink').href = 'logout.html';
            } else {
                // User is not logged in
                document.getElementById('loginLink').textContent = 'Login';
                document.getElementById('loginLink').href = 'login.html';
            }
        })
        .catch(error => {
            console.error('Error checking authentication status:', error);
            // Default to not logged in if there's an error
            document.getElementById('loginLink').textContent = 'Login';
            document.getElementById('loginLink').href = 'login.html';
        });
}

function setupEventListeners() {
    // Add event listener for search input (Enter key)
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                document.getElementById('searchButton').click();
            }
        });
    }
    
    // Add event listeners for table sorting
    const tables = document.querySelectorAll('table.sortable');
    tables.forEach(table => {
        const headers = table.querySelectorAll('th');
        headers.forEach(header => {
            header.addEventListener('click', function() {
                sortTable(table, Array.from(headers).indexOf(header));
            });
        });
    });
}

function sortTable(table, columnIndex) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    // Get the current sort direction
    const th = table.querySelectorAll('th')[columnIndex];
    const currentDirection = th.getAttribute('data-sort') || 'asc';
    const newDirection = currentDirection === 'asc' ? 'desc' : 'asc';
    
    // Update the sort direction
    table.querySelectorAll('th').forEach(header => {
        header.removeAttribute('data-sort');
    });
    th.setAttribute('data-sort', newDirection);
    
    // Sort the rows
    rows.sort((a, b) => {
        const aValue = a.querySelectorAll('td')[columnIndex].textContent.trim();
        const bValue = b.querySelectorAll('td')[columnIndex].textContent.trim();
        
        // Check if the values are numbers
        const aNum = parseFloat(aValue);
        const bNum = parseFloat(bValue);
        
        if (!isNaN(aNum) && !isNaN(bNum)) {
            return newDirection === 'asc' ? aNum - bNum : bNum - aNum;
        } else {
            return newDirection === 'asc' 
                ? aValue.localeCompare(bValue, 'de') 
                : bValue.localeCompare(aValue, 'de');
        }
    });
    
    // Reorder the rows
    rows.forEach(row => {
        tbody.appendChild(row);
    });
}

// Function to get URL parameters
function getUrlParameter(name) {
    name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    const regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
    const results = regex.exec(location.search);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
}

// Function to format date
function formatDate(dateString) {
    if (!dateString) return '';
    
    const date = new Date(dateString);
    return date.toLocaleDateString('de-DE', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    });
}

// Function to show a notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Show the notification
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    // Hide and remove the notification after 3 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
} 