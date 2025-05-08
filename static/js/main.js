// Main JavaScript file for FinArva AI

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    const alertList = document.querySelectorAll('.alert-dismissible');
    alertList.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Highlight active nav item based on current URL
    const currentLocation = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentLocation) {
            link.classList.add('active');
        }
    });

    // Add refresh button functionality for dashboard cards
    const refreshButtons = document.querySelectorAll('.refresh-card');
    refreshButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const cardId = this.getAttribute('data-card-id');
            const card = document.getElementById(cardId);

            if (card) {
                // Add loading spinner
                card.querySelector('.card-body').innerHTML = '<div class="text-center"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div></div>';

                // Fetch updated data
                fetch('/dashboard/refresh-card/' + cardId + '/')
                    .then(response => response.json())
                    .then(data => {
                        if (data.html) {
                            card.querySelector('.card-body').innerHTML = data.html;
                        } else {
                            card.querySelector('.card-body').innerHTML = '<div class="alert alert-danger">Failed to load data</div>';
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        card.querySelector('.card-body').innerHTML = '<div class="alert alert-danger">Error loading data</div>';
                    });
            }
        });
    });

    // Initialize any charts on the page
    initializeCharts();

    // Setup AI suggestion notifications
    setupAiNotifications();
});

// Function to initialize charts using Chart.js
function initializeCharts() {
    // Performance chart
    const performanceChart = document.getElementById('performanceChart');
    if (performanceChart) {
        const ctx = performanceChart.getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: performanceChart.getAttribute('data-labels').split(','),
                datasets: [{
                    label: 'Sales Amount (₹)',
                    data: performanceChart.getAttribute('data-values').split(','),
                    backgroundColor: 'rgba(0, 123, 255, 0.2)',
                    borderColor: 'rgba(0, 123, 255, 1)',
                    borderWidth: 2,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '₹' + value;
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                    }
                }
            }
        });
    }

    // Product distribution chart
    const productChart = document.getElementById('productChart');
    if (productChart) {
        const ctx = productChart.getContext('2d');
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: productChart.getAttribute('data-labels').split(','),
                datasets: [{
                    data: productChart.getAttribute('data-values').split(','),
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.7)',
                        'rgba(54, 162, 235, 0.7)',
                        'rgba(255, 206, 86, 0.7)',
                        'rgba(75, 192, 192, 0.7)',
                        'rgba(153, 102, 255, 0.7)',
                        'rgba(255, 159, 64, 0.7)',
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'right',
                    }
                }
            }
        });
    }
}

// Function to set up AI notifications
function setupAiNotifications() {
    // Check for new AI insights every minute
    setInterval(checkForNewInsights, 60000);

    // Initial check
    checkForNewInsights();
}

// Function to check for new AI insights
function checkForNewInsights() {
    // Only run if user is logged in
    if (document.querySelector('.logged-in-user')) {
        fetch('/ai-assistant/check-insights/')
            .then(response => response.json())
            .then(data => {
                if (data.has_new_insights) {
                    showInsightNotification(data.insight);
                }
            })
            .catch(error => console.error('Error checking insights:', error));
    }
}

// Function to show insight notification
function showInsightNotification(insight) {
    const notificationContainer = document.getElementById('notificationContainer');
    if (!notificationContainer) {
        // Create container if it doesn't exist
        const container = document.createElement('div');
        container.id = 'notificationContainer';
        container.className = 'position-fixed bottom-0 end-0 p-3';
        container.style.zIndex = '5';
        document.body.appendChild(container);
    }

    // Create notification HTML
    const notificationId = 'insight-' + Date.now();
    const notificationHtml = `
        <div id="${notificationId}" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header bg-info text-white">
                <i class="fas fa-robot me-2"></i>
                <strong class="me-auto">FinArva AI Insight</strong>
                <small>Just now</small>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                ${insight}
                <div class="mt-2 pt-2 border-top">
                    <a href="/ai-assistant/insights/" class="btn btn-sm btn-primary">View All Insights</a>
                </div>
            </div>
        </div>
    `;

    // Add notification to container
    document.getElementById('notificationContainer').innerHTML += notificationHtml;

    // Initialize and show toast
    const toastEl = document.getElementById(notificationId);
    const toast = new bootstrap.Toast(toastEl, { autohide: true, delay: 10000 });
    toast.show();
}