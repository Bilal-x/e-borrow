// Mobile Navigation Toggle
document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });

        // Close menu when clicking on a link
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('active');
            });
        });
    }

    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add scroll effect to navbar
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.style.backgroundColor = 'rgba(255, 255, 255, 0.95)';
            navbar.style.backdropFilter = 'blur(10px)';
        } else {
            navbar.style.backgroundColor = '#FFFFFF';
            navbar.style.backdropFilter = 'none';
        }
    });
});

// Form validation and handling
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;

    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;

    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.style.borderColor = '#ff3b30';
            isValid = false;
        } else {
            input.style.borderColor = '#E5E5E5';
        }
    });

    return isValid;
}

// Search functionality
function performSearch() {
    const searchInput = document.getElementById('search-input');
    const categoryFilter = document.getElementById('category-filter');
    const locationFilter = document.getElementById('location-filter');
    const priceFilter = document.getElementById('price-filter');

    if (searchInput) {
        const searchTerm = searchInput.value.toLowerCase();
        const category = categoryFilter ? categoryFilter.value : '';
        const location = locationFilter ? locationFilter.value : '';
        const price = priceFilter ? priceFilter.value : '';

        // Filter listings based on search criteria
        filterListings(searchTerm, category, location, price);
    }
}

function filterListings(searchTerm, category, location, price) {
    const listings = document.querySelectorAll('.listing-card');
    
    listings.forEach(listing => {
        const title = listing.querySelector('h3').textContent.toLowerCase();
        const listingLocation = listing.querySelector('.listing-location').textContent.toLowerCase();
        const listingPrice = listing.querySelector('.listing-price').textContent;
        
        let showListing = true;

        // Search term filter
        if (searchTerm && !title.includes(searchTerm)) {
            showListing = false;
        }

        // Location filter
        if (location && !listingLocation.includes(location.toLowerCase())) {
            showListing = false;
        }

        // Price filter (simplified)
        if (price) {
            const priceValue = parseInt(listingPrice.replace(/[^0-9]/g, ''));
            const [minPrice, maxPrice] = price.split('-').map(p => parseInt(p));
            if (priceValue < minPrice || (maxPrice && priceValue > maxPrice)) {
                showListing = false;
            }
        }

        listing.style.display = showListing ? 'block' : 'none';
    });
}

// Image upload preview
function previewImages(input) {
    const preview = document.getElementById('image-preview');
    if (!preview) return;

    preview.innerHTML = '';

    if (input.files) {
        Array.from(input.files).forEach(file => {
            const reader = new FileReader();
            reader.onload = function(e) {
                const img = document.createElement('img');
                img.src = e.target.result;
                img.style.width = '100px';
                img.style.height = '100px';
                img.style.objectFit = 'cover';
                img.style.borderRadius = '8px';
                img.style.margin = '5px';
                preview.appendChild(img);
            };
            reader.readAsDataURL(file);
        });
    }
}

// Dummy data for demo purposes
const dummyListings = [
    {
        id: 1,
        title: "Canon EOS R5",
        category: "Photography",
        location: "San Francisco, CA",
        price: 35,
        rating: 4.9,
        reviews: 23,
        owner: "John Doe",
        description: "Professional mirrorless camera perfect for photography and videography. Features 45MP full-frame sensor, 8K video recording, and advanced autofocus system."
    },
    {
        id: 2,
        title: "Tesla Model 3",
        category: "Vehicles",
        location: "Los Angeles, CA",
        price: 89,
        rating: 4.8,
        reviews: 45,
        owner: "Jane Smith",
        description: "Electric vehicle with autopilot features and long range. Perfect for city driving and road trips."
    },
    {
        id: 3,
        title: "DeWalt Drill Set",
        category: "Tools",
        location: "New York, NY",
        price: 15,
        rating: 4.7,
        reviews: 12,
        owner: "Mike Johnson",
        description: "Complete drill set with various bits and accessories. Includes cordless drill, impact driver, and carrying case."
    },
    {
        id: 4,
        title: "MacBook Pro 16\"",
        category: "Electronics",
        location: "Seattle, WA",
        price: 45,
        rating: 4.9,
        reviews: 31,
        owner: "Sarah Wilson",
        description: "High-performance laptop for creative professionals. M1 Pro chip, 32GB RAM, 1TB SSD."
    },
    {
        id: 5,
        title: "Mountain Bike",
        category: "Sports",
        location: "Denver, CO",
        price: 25,
        rating: 4.6,
        reviews: 18,
        owner: "Tom Brown",
        description: "Full suspension mountain bike perfect for trails. 29-inch wheels, 21-speed transmission."
    },
    {
        id: 6,
        title: "Dining Table Set",
        category: "Furniture",
        location: "Chicago, IL",
        price: 30,
        rating: 4.8,
        reviews: 9,
        owner: "Lisa Davis",
        description: "Beautiful wooden dining table with 6 chairs. Perfect for dinner parties and events."
    },
    {
        id: 7,
        title: "Sony A7 III",
        category: "Photography",
        location: "San Francisco, CA",
        price: 28,
        rating: 4.8,
        reviews: 15,
        owner: "Alex Chen",
        description: "Full-frame mirrorless camera with excellent low-light performance."
    },
    {
        id: 8,
        title: "BMW X3",
        category: "Vehicles",
        location: "Los Angeles, CA",
        price: 75,
        rating: 4.7,
        reviews: 22,
        owner: "Maria Garcia",
        description: "Luxury SUV perfect for weekend getaways and family trips."
    },
    {
        id: 9,
        title: "Gaming Setup",
        category: "Electronics",
        location: "Austin, TX",
        price: 40,
        rating: 4.9,
        reviews: 28,
        owner: "David Kim",
        description: "Complete gaming setup with high-end PC, monitor, and peripherals."
    },
    {
        id: 10,
        title: "Kayak",
        category: "Sports",
        location: "Portland, OR",
        price: 20,
        rating: 4.6,
        reviews: 11,
        owner: "Emma Johnson",
        description: "Single-person kayak perfect for lake and river adventures."
    }
];

// Load dummy data into listings
function loadDummyListings() {
    const listingsContainer = document.querySelector('.listings-grid, .listings-carousel');
    if (!listingsContainer) return;

    listingsContainer.innerHTML = '';

    dummyListings.forEach(listing => {
        const listingCard = createListingCard(listing);
        listingsContainer.appendChild(listingCard);
    });
}

function createListingCard(listing) {
    const card = document.createElement('div');
    card.className = 'listing-card';
    card.onclick = () => viewListing(listing.id);

    const categoryIcons = {
        'Photography': 'fas fa-camera',
        'Vehicles': 'fas fa-car',
        'Tools': 'fas fa-tools',
        'Electronics': 'fas fa-laptop',
        'Sports': 'fas fa-dumbbell',
        'Furniture': 'fas fa-couch'
    };

    card.innerHTML = `
        <div class="listing-image">
            <div class="placeholder-image">
                <i class="${categoryIcons[listing.category] || 'fas fa-box'}"></i>
            </div>
        </div>
        <div class="listing-content">
            <h3>${listing.title}</h3>
            <p class="listing-location"><i class="fas fa-map-marker-alt"></i> ${listing.location}</p>
            <p class="listing-price">$${listing.price}/day</p>
            <div class="listing-rating">
                <i class="fas fa-star"></i>
                <span>${listing.rating} (${listing.reviews} reviews)</span>
            </div>
        </div>
    `;

    return card;
}

function viewListing(id) {
    // Store listing ID and redirect to detail page
    localStorage.setItem('selectedListingId', id);
    window.location.href = 'item-detail.html';
}

// Initialize dummy data on page load
document.addEventListener('DOMContentLoaded', function() {
    loadDummyListings();
});

// Google Sign-In simulation
function signInWithGoogle() {
    alert('Google Sign-In would be implemented here with actual Google OAuth');
    // Simulate successful login
    localStorage.setItem('user', JSON.stringify({
        name: 'Demo User',
        email: 'demo@example.com',
        avatar: 'https://via.placeholder.com/40'
    }));
    window.location.href = 'dashboard.html';
}

// Logout function
function logout() {
    localStorage.removeItem('user');
    window.location.href = 'index.html';
}

// Check if user is logged in
function checkAuth() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
}

// Update navigation based on auth status
function updateNavigation() {
    const user = checkAuth();
    const loginLink = document.querySelector('a[href="login.html"]');
    
    if (user && loginLink) {
        loginLink.textContent = user.name;
        loginLink.href = 'dashboard.html';
    }
}

// ===== ENHANCED UI/UX JAVASCRIPT ===== 

// Enhanced Mobile Navigation with Animation
function initEnhancedNavigation() {
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');
    
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navToggle.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', function(event) {
            if (!navMenu.contains(event.target) && !navToggle.contains(event.target) && navMenu.classList.contains('active')) {
                navToggle.classList.remove('active');
                navMenu.classList.remove('active');
            }
        });
    }
}

// Button Microinteractions
function initMicrointeractions() {
    // Add ripple effect to buttons
    const buttons = document.querySelectorAll('.btn');
    
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const rect = button.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const ripple = document.createElement('span');
            ripple.classList.add('ripple');
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.style.position = 'absolute';
            ripple.style.width = '20px';
            ripple.style.height = '20px';
            ripple.style.borderRadius = '50%';
            ripple.style.background = 'rgba(255, 255, 255, 0.6)';
            ripple.style.transform = 'scale(0)';
            ripple.style.animation = 'ripple 0.6s linear';
            ripple.style.pointerEvents = 'none';
            
            button.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
    
    // Simulate loading state on form submissions
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('[type="submit"]');
            
            if (submitBtn && !submitBtn.classList.contains('btn-loading')) {
                e.preventDefault();
                
                // Add loading state
                submitBtn.classList.add('btn-loading');
                const btnText = submitBtn.textContent;
                submitBtn.innerHTML = '<span class="spinner"></span><span>' + btnText + '</span>';
                
                // Simulate form submission
                setTimeout(() => {
                    // Remove loading state
                    submitBtn.classList.remove('btn-loading');
                    submitBtn.innerHTML = btnText;
                    
                    // Proceed with form submission or show success
                    if (form.id === 'login-form') {
                        simulateLogin();
                    } else if (form.id === 'register-form') {
                        simulateRegistration();
                    } else if (form.id === 'post-item-form') {
                        simulateItemPosting();
                    } else {
                        form.submit();
                    }
                }, 1500);
            }
        });
    });
}

// Enhanced Search and Filter Functionality
function initSearchFilters() {
    // Filter chips functionality
    const filterChips = document.querySelectorAll('.filter-chip');
    
    filterChips.forEach(chip => {
        const closeIcon = chip.querySelector('i');
        
        if (closeIcon) {
            closeIcon.addEventListener('click', function(e) {
                e.stopPropagation();
                chip.remove();
                updateSearchResults();
            });
        }
        
        if (chip.classList.contains('clear-all')) {
            chip.addEventListener('click', function() {
                document.querySelectorAll('.filter-chip:not(.clear-all)').forEach(c => c.remove());
                updateSearchResults();
            });
        }
    });
    
    // Price range slider
    const priceSlider = document.getElementById('price-range');
    const priceValue = document.getElementById('price-value');
    
    if (priceSlider && priceValue) {
        priceSlider.addEventListener('input', function() {
            priceValue.textContent = '₹' + this.value;
        });
    }
    
    // Sort dropdown
    const sortDropdown = document.getElementById('sort-options');
    
    if (sortDropdown) {
        sortDropdown.addEventListener('change', function() {
            updateSearchResults();
        });
    }
    
    // Apply filters button
    const applyFiltersBtn = document.querySelector('.apply-filters');
    
    if (applyFiltersBtn) {
        applyFiltersBtn.addEventListener('click', function() {
            // Simulate filter application
            const loadingSpinner = document.createElement('span');
            loadingSpinner.classList.add('spinner');
            this.prepend(loadingSpinner);
            
            setTimeout(() => {
                loadingSpinner.remove();
                updateSearchResults();
            }, 800);
        });
    }
}

// Update search results (simulation)
function updateSearchResults() {
    const resultsCount = document.querySelector('.search-results-count');
    const emptyState = document.querySelector('.empty-state');
    const itemsGrid = document.querySelector('.listings-grid');
    
    if (resultsCount && emptyState && itemsGrid) {
        // Simulate loading state
        itemsGrid.style.opacity = '0.5';
        
        setTimeout(() => {
            // Get active filters
            const activeFilters = document.querySelectorAll('.filter-chip:not(.clear-all)');
            
            // Simulate results based on filters
            if (activeFilters.length > 3) {
                // Show empty state if too many filters
                resultsCount.style.display = 'none';
                emptyState.style.display = 'block';
                itemsGrid.style.display = 'none';
            } else {
                // Show results
                const count = Math.max(1, 24 - (activeFilters.length * 5));
                resultsCount.textContent = 'Showing ' + count + ' items near Kasargod';
                resultsCount.style.display = 'block';
                emptyState.style.display = 'none';
                itemsGrid.style.display = 'grid';
            }
            
            itemsGrid.style.opacity = '1';
        }, 800);
    }
}

// Item Gallery and Lightbox
function initItemGallery() {
    // Thumbnail gallery
    const thumbnails = document.querySelectorAll('.thumbnail');
    const mainImage = document.getElementById('featured-image');
    
    if (thumbnails.length && mainImage) {
        thumbnails.forEach(thumb => {
            thumb.addEventListener('click', function() {
                // Update active thumbnail
                thumbnails.forEach(t => t.classList.remove('active'));
                this.classList.add('active');
                
                // Update main image
                const imageUrl = this.getAttribute('data-image');
                mainImage.src = imageUrl;
            });
        });
    }
}

// Show notification
function showNotification(message, type = 'info') {
    // Create notification element if it doesn't exist
    let notification = document.querySelector('.notification');
    
    if (!notification) {
        notification = document.createElement('div');
        notification.classList.add('notification');
        document.body.appendChild(notification);
    }
    
    // Set type class
    notification.className = 'notification';
    notification.classList.add(`notification-${type}`);
    
    // Set message
    notification.textContent = message;
    
    // Show notification
    notification.classList.add('show');
    
    // Hide after 3 seconds
    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}

// Empty States
function initEmptyStates() {
    // Check for empty listings in dashboard
    const listingsContainer = document.querySelector('.listings-container');
    const bookingsContainer = document.querySelector('.bookings-container');
    
    if (listingsContainer && listingsContainer.children.length === 0) {
        showEmptyState(listingsContainer, 'camera', 'No listings yet', 'You haven\'t listed any items for rent. Share your items with the community and start earning!', 'Post Your First Item');
    }
    
    if (bookingsContainer && bookingsContainer.children.length === 0) {
        showEmptyState(bookingsContainer, 'calendar', 'No bookings yet', 'You don\'t have any active bookings. Browse items to rent or promote your listings to get more bookings.', 'Browse Items');
    }
}

// Helper to create empty state
function showEmptyState(container, icon, title, message, buttonText) {
    const emptyState = document.createElement('div');
    emptyState.classList.add('empty-state');
    
    emptyState.innerHTML = `
        <i class="fas fa-${icon}"></i>
        <h3>${title}</h3>
        <p>${message}</p>
        <button class="btn btn-primary">${buttonText}</button>
    `;
    
    container.appendChild(emptyState);
    
    // Add button functionality
    const button = emptyState.querySelector('button');
    
    if (button) {
        button.addEventListener('click', function() {
            if (buttonText === 'Post Your First Item') {
                window.location.href = 'post-item.html';
            } else if (buttonText === 'Browse Items') {
                window.location.href = 'search.html';
            }
        });
    }
}

// Enhanced Authentication
function checkUserAuth() {
    const isLoggedIn = localStorage.getItem('e-borrow-user');
    const loginLinks = document.querySelectorAll('a[href="login.html"]');
    const dashboardLinks = document.querySelectorAll('a[href="dashboard.html"]');
    const userMenus = document.querySelectorAll('.user-menu');
    
    if (isLoggedIn) {
        // User is logged in
        const userData = JSON.parse(isLoggedIn);
        
        // Update login links to show user name
        loginLinks.forEach(link => {
            link.innerHTML = `<img src="${userData.avatar || 'https://randomuser.me/api/portraits/men/32.jpg'}" class="user-avatar-small"> ${userData.name}`;
            link.href = 'dashboard.html';
        });
        
        // Show dashboard links
        dashboardLinks.forEach(link => {
            link.style.display = 'block';
        });
        
        // Update user menus
        userMenus.forEach(menu => {
            const nameElement = menu.querySelector('.user-name');
            const avatarElement = menu.querySelector('.user-avatar');
            
            if (nameElement) nameElement.textContent = userData.name;
            if (avatarElement) avatarElement.src = userData.avatar || 'https://randomuser.me/api/portraits/men/32.jpg';
            
            menu.style.display = 'block';
        });
    } else {
        // User is not logged in
        dashboardLinks.forEach(link => {
            link.style.display = 'none';
        });
        
        userMenus.forEach(menu => {
            menu.style.display = 'none';
        });
    }
}

// Simulate login
function simulateLogin() {
    const emailInput = document.querySelector('#login-email');
    const passwordInput = document.querySelector('#login-password');
    
    if (emailInput && passwordInput && emailInput.value && passwordInput.value) {
        // Create user object
        const user = {
            name: emailInput.value.split('@')[0],
            email: emailInput.value,
            avatar: 'https://randomuser.me/api/portraits/men/32.jpg',
            id: 'user_' + Date.now()
        };
        
        // Store in localStorage
        localStorage.setItem('e-borrow-user', JSON.stringify(user));
        
        // Show success message
        showNotification('Login successful! Redirecting to dashboard...', 'success');
        
        // Redirect to dashboard
        setTimeout(() => {
            window.location.href = 'dashboard.html';
        }, 1500);
    } else {
        showNotification('Please enter both email and password', 'error');
    }
}

// Simulate registration
function simulateRegistration() {
    const nameInput = document.querySelector('#register-name');
    const emailInput = document.querySelector('#register-email');
    const passwordInput = document.querySelector('#register-password');
    
    if (nameInput && emailInput && passwordInput && 
        nameInput.value && emailInput.value && passwordInput.value) {
        // Create user object
        const user = {
            name: nameInput.value,
            email: emailInput.value,
            avatar: 'https://randomuser.me/api/portraits/men/32.jpg',
            id: 'user_' + Date.now()
        };
        
        // Store in localStorage
        localStorage.setItem('e-borrow-user', JSON.stringify(user));
        
        // Show success message
        showNotification('Registration successful! Redirecting to dashboard...', 'success');
        
        // Redirect to dashboard
        setTimeout(() => {
            window.location.href = 'dashboard.html';
        }, 1500);
    } else {
        showNotification('Please fill in all fields', 'error');
    }
}

// Simulate item posting
function simulateItemPosting() {
    const titleInput = document.querySelector('#item-title');
    const categorySelect = document.querySelector('#item-category');
    const priceInput = document.querySelector('#item-price');
    
    if (titleInput && categorySelect && priceInput && 
        titleInput.value && categorySelect.value && priceInput.value) {
        // Show success message
        showNotification('Item posted successfully! Redirecting to your listings...', 'success');
        
        // Redirect to dashboard
        setTimeout(() => {
            window.location.href = 'dashboard.html';
        }, 1500);
    } else {
        showNotification('Please fill in all required fields', 'error');
    }
}

// Initialize all enhanced features
document.addEventListener('DOMContentLoaded', function() {
    // Initialize enhanced components
    initEnhancedNavigation();
    initMicrointeractions();
    initSearchFilters();
    initItemGallery();
    initEmptyStates();
    
    // Check if user is logged in (from localStorage)
    checkUserAuth();
    
    // Add CSS for ripple animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
});