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