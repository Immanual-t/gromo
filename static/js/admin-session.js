// File location: static/js/admin-session.js

/**
 * Handle admin session checking and management
 * This script helps ensure separate admin and frontend sessions
 */
document.addEventListener('DOMContentLoaded', function() {
    // Only run this script on admin pages
    if (window.location.pathname.startsWith('/admin/')) {
        checkAdminSession();
    }
});

/**
 * Check if there's a valid admin session
 */
function checkAdminSession() {
    // Check for admin session cookie
    const hasAdminSession = getCookie('finarva_admin_sessionid') !== null;
    const hasAdminAuth = getCookie('finarva_admin_auth') === 'true';

    // If on admin login page, don't redirect
    if (window.location.pathname === '/admin/login/') {
        return;
    }

    // If no admin session, redirect to login
    if (!hasAdminSession || !hasAdminAuth) {
        window.location.href = '/admin/login/?next=' + encodeURIComponent(window.location.pathname);
    }
}

/**
 * Get a cookie by name
 */
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        return parts.pop().split(';').shift();
    }
    return null;
}

/**
 * Clear admin session cookies on logout
 */
function clearAdminSession() {
    // Delete admin cookies by setting expiration in the past
    document.cookie = 'finarva_admin_sessionid=; path=/admin/; expires=Thu, 01 Jan 1970 00:00:00 GMT';
    document.cookie = 'finarva_admin_csrftoken=; path=/admin/; expires=Thu, 01 Jan 1970 00:00:00 GMT';
    document.cookie = 'finarva_admin_auth=; path=/admin/; expires=Thu, 01 Jan 1970 00:00:00 GMT';
    document.cookie = 'admin_logged_in=; path=/admin/; expires=Thu, 01 Jan 1970 00:00:00 GMT';

    // Redirect to login page
    window.location.href = '/admin/login/';
}

// Add event listener to logout links/buttons in admin
document.addEventListener('DOMContentLoaded', function() {
    const logoutLinks = document.querySelectorAll('a[href*="logout"]');
    logoutLinks.forEach(link => {
        if (window.location.pathname.startsWith('/admin/')) {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                clearAdminSession();
            });
        }
    });
});