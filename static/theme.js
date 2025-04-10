// Theme switching functionality
document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    if (!themeToggle) return;

    const icon = themeToggle.nextElementSibling.querySelector('i');

    // Check for saved theme preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
        themeToggle.checked = true;
        icon.classList.remove('fa-moon');
        icon.classList.add('fa-sun');
        applyDarkTheme();
    }

    themeToggle.addEventListener('change', () => {
        if (themeToggle.checked) {
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
            applyDarkTheme();
        } else {
            document.documentElement.setAttribute('data-theme', 'light');
            localStorage.setItem('theme', 'light');
            icon.classList.remove('fa-sun');
            icon.classList.add('fa-moon');
            applyLightTheme();
        }
    });
});

function applyDarkTheme() {
    // Apply to body and all elements
    document.body.style.backgroundColor = '#1a1a1a';
    document.body.style.color = '#ffffff';
    
    // Update all text elements
    const textElements = document.querySelectorAll('h1, h2, h3, h4, h5, h6, p, span, div, label, a, li, td, th');
    textElements.forEach(element => {
        element.style.color = '#ffffff';
    });
    
    // Update all cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.style.backgroundColor = '#2d2d2d';
        card.style.borderColor = '#404040';
    });

    // Update dashboard
    const dashboard = document.querySelector('.dashboard');
    if (dashboard) {
        dashboard.style.backgroundColor = '#1a1a1a';
    }

    // Update main content
    const mainContent = document.querySelector('.main-content');
    if (mainContent) {
        mainContent.style.backgroundColor = '#1a1a1a';
    }

    // Update app container
    const appContainer = document.querySelector('.app-container');
    if (appContainer) {
        appContainer.style.backgroundColor = '#1a1a1a';
    }

    // Update all inputs
    const inputs = document.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        input.style.backgroundColor = '#333333';
        input.style.color = '#ffffff';
        input.style.borderColor = '#404040';
    });

    // Update sidebar and navigation
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) {
        sidebar.style.backgroundColor = '#1a1a1a';
    }

    // Update navigation items
    const navItems = document.querySelectorAll('.nav-item, .nav-link');
    navItems.forEach(item => {
        item.style.backgroundColor = '#1a1a1a';
        item.style.color = '#3b82f6';
    });

    // Update active navigation items
    const activeNavItems = document.querySelectorAll('.nav-item.active, .nav-link.active');
    activeNavItems.forEach(item => {
        item.style.backgroundColor = '#2d2d2d';
        item.style.color = '#60a5fa';
    });

    // Update header
    const header = document.querySelector('.top-header');
    if (header) {
        header.style.backgroundColor = '#2d2d2d';
    }

    // Update tables
    const tables = document.querySelectorAll('table');
    tables.forEach(table => {
        table.style.backgroundColor = '#2d2d2d';
        table.style.color = '#ffffff';
        
        // Update table headers
        const headers = table.querySelectorAll('th');
        headers.forEach(header => {
            header.style.backgroundColor = '#1a1a1a';
            header.style.color = '#ffffff';
        });
        
        // Update table cells
        const cells = table.querySelectorAll('td');
        cells.forEach(cell => {
            cell.style.backgroundColor = '#2d2d2d';
            cell.style.color = '#ffffff';
        });
        
        // Add alternating row colors
        const rows = table.querySelectorAll('tr');
        rows.forEach((row, index) => {
            if (index > 0) { // Skip header row
                row.style.backgroundColor = index % 2 === 0 ? '#2d2d2d' : '#333333';
            }
        });
    });

    // Update links
    const links = document.querySelectorAll('a');
    links.forEach(link => {
        link.style.color = '#ffffff';
    });

    // Update buttons
    const buttons = document.querySelectorAll('button, .btn');
    buttons.forEach(button => {
        button.style.backgroundColor = '#333333';
        button.style.color = '#ffffff';
        button.style.borderColor = '#404040';
    });

    // Update alerts
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        alert.style.backgroundColor = '#2d2d2d';
        alert.style.color = '#ffffff';
        alert.style.borderColor = '#404040';
    });

    // Update file input labels
    const fileLabels = document.querySelectorAll('.file-label');
    fileLabels.forEach(label => {
        label.style.backgroundColor = '#333333';
        label.style.color = '#ffffff';
        label.style.borderColor = '#404040';
    });

    // Update file names
    const fileNames = document.querySelectorAll('.file-name');
    fileNames.forEach(name => {
        name.style.color = '#ffffff';
    });

    // Update dashboard header
    const dashboardHeader = document.querySelector('.dashboard-header');
    if (dashboardHeader) {
        dashboardHeader.style.color = '#ffffff';
    }

    // Update upload icon
    const uploadIcon = document.querySelector('.upload-icon');
    if (uploadIcon) {
        uploadIcon.style.backgroundColor = '#333333';
    }

    // Update upload icon color
    const uploadIconI = document.querySelector('.upload-icon i');
    if (uploadIconI) {
        uploadIconI.style.color = '#ffffff';
    }

    // Update selection color and navigation styles
    const style = document.createElement('style');
    style.textContent = `
        ::selection {
            background-color: #2d2d2d !important;
            color: #ffffff !important;
        }
        ::-moz-selection {
            background-color: #2d2d2d !important;
            color: #ffffff !important;
        }
        
        /* Navigation hover states */
        .nav-item:hover, .nav-link:hover {
            background-color: #2d2d2d !important;
            color: #60a5fa !important;
        }
        
        /* Selected/active navigation items */
        .nav-item.selected, .nav-link.selected,
        .nav-item.active, .nav-link.active {
            background-color: #2d2d2d !important;
            color: #60a5fa !important;
        }

        /* Left navigation specific styles */
        .sidebar .nav-item {
            background-color: #1a1a1a !important;
        }
        
        .sidebar .nav-item:hover,
        .sidebar .nav-item.active,
        .sidebar .nav-item.selected {
            background-color: #2d2d2d !important;
        }
        
        .sidebar .nav-link {
            background-color: transparent !important;
            color: #3b82f6 !important;
        }

        .sidebar .nav-link:hover,
        .sidebar .nav-link.active {
            color: #60a5fa !important;
        }
        
        /* Text selection in navigation */
        .sidebar ::selection {
            background-color: #2d2d2d !important;
            color: #60a5fa !important;
        }
        
        .sidebar ::-moz-selection {
            background-color: #2d2d2d !important;
            color: #60a5fa !important;
        }
    `;
    document.head.appendChild(style);
}

function applyLightTheme() {
    // Reset body and all elements
    document.body.style.backgroundColor = '#ffffff';
    document.body.style.color = '#333333';
    
    // Reset all text elements
    const textElements = document.querySelectorAll('h1, h2, h3, h4, h5, h6, p, span, div, label, a, li, td, th');
    textElements.forEach(element => {
        element.style.color = '#333333';
    });
    
    // Reset all cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.style.backgroundColor = '#ffffff';
        card.style.borderColor = '#ddd';
    });

    // Reset dashboard
    const dashboard = document.querySelector('.dashboard');
    if (dashboard) {
        dashboard.style.backgroundColor = '#ffffff';
    }

    // Reset main content
    const mainContent = document.querySelector('.main-content');
    if (mainContent) {
        mainContent.style.backgroundColor = '#ffffff';
    }

    // Reset app container
    const appContainer = document.querySelector('.app-container');
    if (appContainer) {
        appContainer.style.backgroundColor = '#ffffff';
    }

    // Reset all inputs
    const inputs = document.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        input.style.backgroundColor = '#ffffff';
        input.style.color = '#333333';
        input.style.borderColor = '#ddd';
    });

    // Reset sidebar
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) {
        sidebar.style.backgroundColor = '#f8f9fa';
    }

    // Reset header
    const header = document.querySelector('.top-header');
    if (header) {
        header.style.backgroundColor = '#ffffff';
    }

    // Reset tables
    const tables = document.querySelectorAll('table');
    tables.forEach(table => {
        table.style.backgroundColor = '#ffffff';
        table.style.color = '#333333';
        
        // Reset table headers
        const headers = table.querySelectorAll('th');
        headers.forEach(header => {
            header.style.backgroundColor = '#f4f4f4';
            header.style.color = '#333333';
        });
        
        // Reset table cells
        const cells = table.querySelectorAll('td');
        cells.forEach(cell => {
            cell.style.backgroundColor = '#ffffff';
            cell.style.color = '#333333';
        });
        
        // Reset alternating row colors
        const rows = table.querySelectorAll('tr');
        rows.forEach((row, index) => {
            if (index > 0) { // Skip header row
                row.style.backgroundColor = index % 2 === 0 ? '#ffffff' : '#f9f9f9';
            }
        });
    });

    // Reset links
    const links = document.querySelectorAll('a');
    links.forEach(link => {
        link.style.color = '#333333';
    });

    // Reset buttons
    const buttons = document.querySelectorAll('button, .btn');
    buttons.forEach(button => {
        button.style.backgroundColor = '#ffffff';
        button.style.color = '#333333';
        button.style.borderColor = '#ddd';
    });

    // Reset alerts
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        alert.style.backgroundColor = '#ffffff';
        alert.style.color = '#333333';
        alert.style.borderColor = '#ddd';
    });

    // Reset file input labels
    const fileLabels = document.querySelectorAll('.file-label');
    fileLabels.forEach(label => {
        label.style.backgroundColor = '#ffffff';
        label.style.color = '#333333';
        label.style.borderColor = '#ddd';
    });

    // Reset file names
    const fileNames = document.querySelectorAll('.file-name');
    fileNames.forEach(name => {
        name.style.color = '#333333';
    });

    // Reset dashboard header
    const dashboardHeader = document.querySelector('.dashboard-header');
    if (dashboardHeader) {
        dashboardHeader.style.color = '#333333';
    }

    // Reset upload icon
    const uploadIcon = document.querySelector('.upload-icon');
    if (uploadIcon) {
        uploadIcon.style.backgroundColor = '#eff6ff';
    }

    // Reset upload icon color
    const uploadIconI = document.querySelector('.upload-icon i');
    if (uploadIconI) {
        uploadIconI.style.color = '#3b82f6';
    }

    // Reset selection color
    const style = document.createElement('style');
    style.textContent = `
        ::selection {
            background-color: #b3d4fc;
            color: #000000;
        }
        ::-moz-selection {
            background-color: #b3d4fc;
            color: #000000;
        }
    `;
    document.head.appendChild(style);
} 