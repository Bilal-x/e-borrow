// API Service for E-Borrow
const API_URL = '/api';

// Helper function to handle API responses
const handleResponse = async (response) => {
    const data = await response.json();
    
    if (!response.ok) {
        const error = data.error || response.statusText;
        return Promise.reject(error);
    }
    
    return data;
};

// Helper function to get auth header
const getAuthHeader = () => {
    const token = localStorage.getItem('e-borrow-token');
    return token ? { 'Authorization': `Bearer ${token}` } : {};
};

// Authentication API
const authAPI = {
    // Register a new user
    register: async (userData) => {
        const response = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });
        
        const data = await handleResponse(response);
        
        // Store token and user data
        if (data.access_token) {
            localStorage.setItem('e-borrow-token', data.access_token);
            localStorage.setItem('e-borrow-user', JSON.stringify(data.user));
        }
        
        return data;
    },
    
    // Login user
    login: async (credentials) => {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(credentials)
        });
        
        const data = await handleResponse(response);
        
        // Store token and user data
        if (data.access_token) {
            localStorage.setItem('e-borrow-token', data.access_token);
            localStorage.setItem('e-borrow-user', JSON.stringify(data.user));
        }
        
        return data;
    },
    
    // Admin login
    adminLogin: async (credentials) => {
        const response = await fetch(`${API_URL}/auth/admin-login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(credentials)
        });
        
        const data = await handleResponse(response);
        
        // Store token and user data
        if (data.access_token) {
            localStorage.setItem('e-borrow-token', data.access_token);
            localStorage.setItem('e-borrow-user', JSON.stringify(data.user));
            localStorage.setItem('e-borrow-admin', data.is_admin);
        }
        
        return data;
    },
    
    // Get current user
    getCurrentUser: async () => {
        const response = await fetch(`${API_URL}/auth/me`, {
            method: 'GET',
            headers: {
                ...getAuthHeader(),
                'Content-Type': 'application/json'
            }
        });
        
        return handleResponse(response);
    },
    
    // Logout user
    logout: () => {
        localStorage.removeItem('e-borrow-token');
        localStorage.removeItem('e-borrow-user');
        localStorage.removeItem('e-borrow-admin');
    },
    
    // Check if user is logged in
    isLoggedIn: () => {
        return !!localStorage.getItem('e-borrow-token');
    },
    
    // Check if user is admin
    isAdmin: () => {
        return localStorage.getItem('e-borrow-admin') === 'true';
    }
};

// Users API
const usersAPI = {
    // Get all users (admin only)
    getUsers: async (page = 1, perPage = 10) => {
        const response = await fetch(`${API_URL}/users?page=${page}&per_page=${perPage}`, {
            method: 'GET',
            headers: {
                ...getAuthHeader(),
                'Content-Type': 'application/json'
            }
        });
        
        return handleResponse(response);
    },
    
    // Get user by ID
    getUser: async (userId) => {
        const response = await fetch(`${API_URL}/users/${userId}`, {
            method: 'GET',
            headers: {
                ...getAuthHeader(),
                'Content-Type': 'application/json'
            }
        });
        
        return handleResponse(response);
    },
    
    // Update user
    updateUser: async (userId, userData) => {
        const response = await fetch(`${API_URL}/users/${userId}`, {
            method: 'PUT',
            headers: {
                ...getAuthHeader(),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });
        
        return handleResponse(response);
    },
    
    // Delete user
    deleteUser: async (userId) => {
        const response = await fetch(`${API_URL}/users/${userId}`, {
            method: 'DELETE',
            headers: {
                ...getAuthHeader(),
                'Content-Type': 'application/json'
            }
        });
        
        return handleResponse(response);
    }
};

// Listings API
const listingsAPI = {
    // Get all listings with filters
    getListings: async (filters = {}) => {
        // Build query string from filters
        const queryParams = new URLSearchParams();
        
        if (filters.page) queryParams.append('page', filters.page);
        if (filters.perPage) queryParams.append('per_page', filters.perPage);
        if (filters.category) queryParams.append('category', filters.category);
        if (filters.location) queryParams.append('location', filters.location);
        if (filters.minPrice) queryParams.append('min_price', filters.minPrice);
        if (filters.maxPrice) queryParams.append('max_price', filters.maxPrice);
        if (filters.search) queryParams.append('search', filters.search);
        if (filters.sortBy) queryParams.append('sort_by', filters.sortBy);
        if (filters.sortOrder) queryParams.append('sort_order', filters.sortOrder);
        
        const response = await fetch(`${API_URL}/listings?${queryParams.toString()}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        return handleResponse(response);
    },
    
    // Get listing by ID
    getListing: async (listingId) => {
        const response = await fetch(`${API_URL}/listings/${listingId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        return handleResponse(response);
    },
    
    // Create new listing
    createListing: async (listingData) => {
        const response = await fetch(`${API_URL}/listings`, {
            method: 'POST',
            headers: {
                ...getAuthHeader(),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(listingData)
        });
        
        return handleResponse(response);
    },
    
    // Update listing
    updateListing: async (listingId, listingData) => {
        const response = await fetch(`${API_URL}/listings/${listingId}`, {
            method: 'PUT',
            headers: {
                ...getAuthHeader(),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(listingData)
        });
        
        return handleResponse(response);
    },
    
    // Delete listing
    deleteListing: async (listingId) => {
        const response = await fetch(`${API_URL}/listings/${listingId}`, {
            method: 'DELETE',
            headers: {
                ...getAuthHeader(),
                'Content-Type': 'application/json'
            }
        });
        
        return handleResponse(response);
    },
    
    // Get all categories
    getCategories: async () => {
        const response = await fetch(`${API_URL}/listings/categories`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        return handleResponse(response);
    },
    
    // Get all locations
    getLocations: async () => {
        const response = await fetch(`${API_URL}/listings/locations`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        return handleResponse(response);
    },
    
    // Get listings by user ID
    getUserListings: async (userId, page = 1, perPage = 12) => {
        const response = await fetch(`${API_URL}/users/${userId}/listings?page=${page}&per_page=${perPage}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        return handleResponse(response);
    }
};

// Bookings API
const bookingsAPI = {
    // Get all bookings
    getBookings: async (filters = {}) => {
        // Build query string from filters
        const queryParams = new URLSearchParams();
        
        if (filters.page) queryParams.append('page', filters.page);
        if (filters.perPage) queryParams.append('per_page', filters.perPage);
        if (filters.status) queryParams.append('status', filters.status);
        
        const response = await fetch(`${API_URL}/bookings?${queryParams.toString()}`, {
            method: 'GET',
            headers: {
                ...getAuthHeader(),
                'Content-Type': 'application/json'
            }
        });
        
        return handleResponse(response);
    },
    
    // Get booking by ID
    getBooking: async (bookingId) => {
        const response = await fetch(`${API_URL}/bookings/${bookingId}`, {
            method: 'GET',
            headers: {
                ...getAuthHeader(),
                'Content-Type': 'application/json'
            }
        });
        
        return handleResponse(response);
    },
    
    // Create new booking
    createBooking: async (bookingData) => {
        const response = await fetch(`${API_URL}/bookings`, {
            method: 'POST',
            headers: {
                ...getAuthHeader(),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(bookingData)
        });
        
        return handleResponse(response);
    },
    
    // Update booking status
    updateBookingStatus: async (bookingId, statusData) => {
        const response = await fetch(`${API_URL}/bookings/${bookingId}`, {
            method: 'PUT',
            headers: {
                ...getAuthHeader(),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(statusData)
        });
        
        return handleResponse(response);
    },
    
    // Delete booking
    deleteBooking: async (bookingId) => {
        const response = await fetch(`${API_URL}/bookings/${bookingId}`, {
            method: 'DELETE',
            headers: {
                ...getAuthHeader(),
                'Content-Type': 'application/json'
            }
        });
        
        return handleResponse(response);
    },
    
    // Get bookings by user ID
    getUserBookings: async (userId, filters = {}) => {
        // Build query string from filters
        const queryParams = new URLSearchParams();
        
        if (filters.page) queryParams.append('page', filters.page);
        if (filters.perPage) queryParams.append('per_page', filters.perPage);
        if (filters.status) queryParams.append('status', filters.status);
        
        const response = await fetch(`${API_URL}/users/${userId}/bookings?${queryParams.toString()}`, {
            method: 'GET',
            headers: {
                ...getAuthHeader(),
                'Content-Type': 'application/json'
            }
        });
        
        return handleResponse(response);
    },
    
    // Get bookings by listing ID
    getListingBookings: async (listingId, filters = {}) => {
        // Build query string from filters
        const queryParams = new URLSearchParams();
        
        if (filters.page) queryParams.append('page', filters.page);
        if (filters.perPage) queryParams.append('per_page', filters.perPage);
        if (filters.status) queryParams.append('status', filters.status);
        
        const response = await fetch(`${API_URL}/listings/${listingId}/bookings?${queryParams.toString()}`, {
            method: 'GET',
            headers: {
                ...getAuthHeader(),
                'Content-Type': 'application/json'
            }
        });
        
        return handleResponse(response);
    }
};

// Reviews API
const reviewsAPI = {
    // Get all reviews with filters
    getReviews: async (filters = {}) => {
        // Build query string from filters
        const queryParams = new URLSearchParams();
        
        if (filters.page) queryParams.append('page', filters.page);
        if (filters.perPage) queryParams.append('per_page', filters.perPage);
        if (filters.listingId) queryParams.append('listing_id', filters.listingId);
        if (filters.reviewerId) queryParams.append('reviewer_id', filters.reviewerId);
        if (filters.revieweeId) queryParams.append('reviewee_id', filters.revieweeId);
        
        const response = await fetch(`${API_URL}/reviews?${queryParams.toString()}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        return handleResponse(response);
    },
    
    // Get review by ID
    getReview: async (reviewId) => {
        const response = await fetch(`${API_URL}/reviews/${reviewId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        return handleResponse(response);
    },
    
    // Create new review
    createReview: async (reviewData) => {
        const response = await fetch(`${API_URL}/reviews`, {
            method: 'POST',
            headers: {
                ...getAuthHeader(),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(reviewData)
        });
        
        return handleResponse(response);
    },
    
    // Update review
    updateReview: async (reviewId, reviewData) => {
        const response = await fetch(`${API_URL}/reviews/${reviewId}`, {
            method: 'PUT',
            headers: {
                ...getAuthHeader(),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(reviewData)
        });
        
        return handleResponse(response);
    },
    
    // Delete review
    deleteReview: async (reviewId) => {
        const response = await fetch(`${API_URL}/reviews/${reviewId}`, {
            method: 'DELETE',
            headers: {
                ...getAuthHeader(),
                'Content-Type': 'application/json'
            }
        });
        
        return handleResponse(response);
    },
    
    // Get reviews by listing ID
    getListingReviews: async (listingId, page = 1, perPage = 10) => {
        const response = await fetch(`${API_URL}/listings/${listingId}/reviews?page=${page}&per_page=${perPage}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        return handleResponse(response);
    },
    
    // Get reviews by user ID
    getUserReviews: async (userId, type = 'received', page = 1, perPage = 10) => {
        const response = await fetch(`${API_URL}/users/${userId}/reviews?type=${type}&page=${page}&per_page=${perPage}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        return handleResponse(response);
    }
};

// Export all APIs
const api = {
    auth: authAPI,
    users: usersAPI,
    listings: listingsAPI,
    bookings: bookingsAPI,
    reviews: reviewsAPI
};

// Make API available globally
window.api = api;