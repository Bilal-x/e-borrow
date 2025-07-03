# E-Borrow - Peer-to-Peer Rental Platform

A modern, responsive web application for peer-to-peer item rentals. Users can list their items for rent and browse/rent items from others in their community.

## 🎨 Design Features

- **Modern UI/UX**: Clean, minimalist design with rounded corners and subtle shadows
- **Brand Colors**: 
  - Primary: Indigo (#4B5FB5)
  - Secondary: Sky Blue (#8FCBF2)
  - Accent: Lemon Yellow (#FFD166)
  - Text: Charcoal (#2F2F2F)
  - Background: Soft White (#F9F9F9)
- **Typography**: Inter font family for modern, readable text
- **Mobile-First**: Fully responsive design that works on all devices
- **Accessibility**: Proper contrast ratios and semantic HTML

## 🚀 Features

### Homepage
- Hero section with clear value proposition
- How It Works (3-step process)
- Popular categories with icons
- Featured listings carousel
- Trust-building section
- Comprehensive footer

### User Authentication
- Login/Register forms
- Google Sign-In integration (simulated)
- Form validation
- Responsive design

### Browse & Search
- Advanced search with filters
- Category, location, and price filtering
- Sort options (price, rating, newest)
- Real-time search results
- Filter tags for active filters

### Item Listing
- Comprehensive item posting form
- Image upload with drag & drop
- Pricing options (daily, weekly, monthly)
- Location and availability settings
- Form validation and preview

### Item Details
- Detailed item information
- Image gallery
- Owner profile section
- Booking calendar with price calculation
- Reviews and ratings
- Contact owner functionality

### User Dashboard
- Overview with statistics
- My listings management
- Rental history
- Booking requests
- Messages (placeholder)
- Account settings

### Admin Dashboard
- Platform analytics
- User management
- Listing moderation
- Transaction monitoring
- Reports and issues handling

## 📱 Pages

1. **Homepage** (`index.html`) - Landing page with hero, features, and listings
2. **Login/Register** (`login.html`) - Authentication forms
3. **Browse Items** (`search.html`) - Search and filter listings
4. **Post Item** (`post-item.html`) - Create new listings
5. **Item Details** (`item-detail.html`) - Detailed item view
6. **User Dashboard** (`dashboard.html`) - User account management
7. **Admin Dashboard** (`admin.html`) - Platform administration

## 🛠 Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Styling**: Custom CSS with CSS Variables
- **Icons**: Font Awesome 6
- **Fonts**: Google Fonts (Inter)
- **Server**: Python HTTP Server (for demo)

## 🎯 Demo Features

- **Dummy Data**: Pre-populated with sample listings and users
- **Local Storage**: Simulated user authentication
- **Interactive Elements**: Working forms, filters, and navigation
- **Responsive Design**: Tested on mobile and desktop
- **Modern Animations**: Smooth transitions and hover effects

## 🚀 Getting Started

1. **Clone or download** the project files
2. **Navigate** to the project directory
3. **Start the server**:
   ```bash
   python server.py
   ```
4. **Open your browser** and visit:
   - Local: `http://localhost:12001`
   - Production: `https://work-2-ktgelzsfqhtmxoqe.prod-runtime.all-hands.dev`

## 📂 File Structure

```
e-borrow/
├── index.html          # Homepage
├── login.html          # Authentication
├── search.html         # Browse items
├── post-item.html      # List new item
├── item-detail.html    # Item details
├── dashboard.html      # User dashboard
├── admin.html          # Admin dashboard
├── styles.css          # Main stylesheet
├── script.js           # JavaScript functionality
├── server.py           # Python server
└── README.md           # Documentation
```

## 🎨 Design Principles

- **Mobile-First**: Designed for mobile devices first, then enhanced for desktop
- **Clean & Minimal**: Uncluttered interface focusing on content
- **Consistent**: Uniform spacing, colors, and typography throughout
- **Accessible**: High contrast ratios and semantic HTML
- **Fast**: Optimized for quick loading and smooth interactions

## 🔧 Customization

The design system uses CSS variables for easy customization:

```css
:root {
    --primary: #4B5FB5;
    --secondary: #8FCBF2;
    --accent: #FFD166;
    --text: #2F2F2F;
    --background: #F9F9F9;
}
```

## 📱 Responsive Breakpoints

- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

## 🚀 Future Enhancements

- Real backend integration
- Payment processing
- Real-time messaging
- Push notifications
- Advanced analytics
- Mobile app versions
- Multi-language support

## 📄 License

This is a demo project created for educational purposes.