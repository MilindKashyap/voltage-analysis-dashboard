// Simplified JavaScript for Voltage Analysis Dashboard

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the dashboard
    initDashboard();
    
    // Add active navigation highlighting
    highlightActiveNav();
    
    // Add chart responsiveness
    addChartResponsiveness();
});

function initDashboard() {
    console.log('Voltage Analysis Dashboard initialized');
    
    // Add any global dashboard functionality here
    addCardAnimations();
}

function highlightActiveNav() {
    // Highlight active navigation item based on current page
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
    
    // Special case for home page
    if (currentPath === '/' || currentPath === '') {
        const homeLink = document.querySelector('.navbar-nav .nav-link[href="/"]');
        if (homeLink) homeLink.classList.add('active');
    }
}

function addChartResponsiveness() {
    // Make Plotly charts responsive
    window.addEventListener('resize', function() {
        const charts = document.querySelectorAll('.plotly-chart');
        charts.forEach(chart => {
            if (chart.data && chart.layout) {
                Plotly.Plots.resize(chart);
            }
        });
    });
}

function addCardAnimations() {
    // Add staggered animation to cards
    const cards = document.querySelectorAll('.content-card, .analysis-card, .stat-card');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                entry.target.style.animationDelay = `${index * 0.1}s`;
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
}

// Enhanced chart rendering with error handling
function renderChart(containerId, chartData, config = {}) {
    try {
        const defaultConfig = {
            responsive: true,
            displayModeBar: true,
            modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
            displaylogo: false,
            toImageButtonOptions: {
                format: 'png',
                filename: 'voltage_chart',
                height: 800,
                width: 1200,
                scale: 1
            }
        };
        
        const finalConfig = { ...defaultConfig, ...config };
        
        // Add loading state
        const container = document.getElementById(containerId);
        if (container) {
            container.innerHTML = '<div class="chart-loading"><div class="loading-spinner"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div><p class="mt-2 text-light">Loading chart...</p></div></div>';
        }
        
        // Render chart
        return Plotly.newPlot(containerId, chartData.data, chartData.layout, finalConfig)
            .then(() => {
                // Remove loading state
                if (container) {
                    container.innerHTML = `<div id="${containerId}" class="plotly-chart"></div>`;
                    Plotly.newPlot(containerId, chartData.data, chartData.layout, finalConfig);
                }
            })
            .catch(error => {
                console.error('Chart rendering error:', error);
                if (container) {
                    container.innerHTML = `
                        <div class="alert alert-danger" role="alert">
                            <i class="fas fa-exclamation-triangle me-2"></i>
                            Error loading chart. Please refresh the page.
                        </div>
                    `;
                }
            });
    } catch (error) {
        console.error('Chart setup error:', error);
        const container = document.getElementById(containerId);
        if (container) {
            container.innerHTML = `
                <div class="alert alert-danger" role="alert">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    Chart setup failed. Please check your data.
                </div>
            `;
        }
    }
}

// Utility functions for data formatting
function formatNumber(num, decimals = 2) {
    return Number(num).toFixed(decimals);
}

function formatTimestamp(timestamp) {
    return new Date(timestamp).toLocaleString();
}

function formatVoltage(voltage) {
    return `${formatNumber(voltage)}V`;
}

// Export functions for charts
function exportChartAsPNG(containerId, filename = 'voltage_chart.png') {
    try {
        Plotly.downloadImage(containerId, {
            format: 'png',
            filename: filename,
            width: 1200,
            height: 800,
            scale: 1
        });
    } catch (error) {
        console.error('Export error:', error);
        alert('Export failed. Please try again.');
    }
}

function exportChartAsSVG(containerId, filename = 'voltage_chart.svg') {
    try {
        Plotly.downloadImage(containerId, {
            format: 'svg',
            filename: filename,
            width: 1200,
            height: 800,
            scale: 1
        });
    } catch (error) {
        console.error('Export error:', error);
        alert('Export failed. Please try again.');
    }
}

// Performance monitoring (only in development)
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    // Monitor chart performance
    const originalRenderChart = renderChart;
    renderChart = function(containerId, chartData, config) {
        const startTime = performance.now();
        return originalRenderChart(containerId, chartData, config).then(() => {
            const endTime = performance.now();
            const renderTime = endTime - startTime;
            if (renderTime > 1000) {
                console.warn(`Chart ${containerId} took ${renderTime.toFixed(2)}ms to render`);
            }
        });
    };
} 