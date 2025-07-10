
# RUN POLLS - Online Voting System

A modern, secure, and user-friendly online voting system built with Django REST Framework backend and vanilla JavaScript frontend. This system enables educational institutions to conduct digital elections with complete transparency and security.

## 🚀 Features

### For Voters
- **Secure Registration**: Student verification with department-based eligibility
- **User-Friendly Interface**: Intuitive voting experience with candidate information
- **Real-time Updates**: Live election status and notifications
- **Vote Tracking**: Confirmation and voting history
- **Mobile Responsive**: Works seamlessly on all devices

### For Administrators
- **Election Management**: Create, configure, and monitor elections
- **Candidate Management**: Approve candidate registrations and manage profiles
- **Voter Management**: Oversee voter registrations and eligibility
- **Results Dashboard**: Real-time results with detailed analytics
- **Notification System**: Send announcements and updates

### Security Features
- Token-based authentication
- One vote per position constraint
- Vote uniqueness validation
- Secure session management
- User role-based access control

## 🏗️ Architecture

```
RUN POLLS/
├── backend/           # Django REST API
│   ├── accounts/      # User management
│   ├── elections/     # Election management
│   ├── voting/        # Vote casting and results
│   └── notifications/ # Notification system
├── js/               # Frontend JavaScript modules
├── images/           # Static assets
└── *.html           # Frontend pages
```

## 🛠️ Technology Stack

**Backend:**
- Django 4.2.7
- Django REST Framework 3.14.0
- SQLite Database
- Token Authentication

**Frontend:**
- HTML5/CSS3
- Vanilla JavaScript
- Bootstrap 5.3.0
- Bootstrap Icons

## 📦 Installation & Setup

### Prerequisites
- Python 3.8+
- Modern web browser

### Quick Start

1. **Clone the repository** (if applicable)
2. **Install backend dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Setup database:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create admin user:**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start the development server:**
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

6. **Access the application:**
   - Frontend: Open `index.html` in your browser
   - Backend API: http://0.0.0.0:8000/api/
   - Admin Panel: http://0.0.0.0:8000/admin/

## 📚 API Documentation

### Authentication Endpoints
```
POST /api/accounts/login/     # User login
POST /api/accounts/register/  # User registration
GET  /api/accounts/profile/   # Get user profile
PUT  /api/accounts/profile/   # Update profile
```

### Election Endpoints
```
GET  /api/elections/                    # List elections
POST /api/elections/                    # Create election (admin)
GET  /api/elections/{id}/               # Election details
GET  /api/elections/{id}/candidates/    # Election candidates
POST /api/elections/register-candidate/ # Register as candidate
```

### Voting Endpoints
```
POST /api/voting/cast-vote/            # Cast votes
GET  /api/voting/my-votes/             # User's voting history
GET  /api/voting/results/{election_id}/ # Election results
GET  /api/voting/eligibility/{election_id}/ # Check eligibility
```

### Notification Endpoints
```
GET /api/notifications/           # Get notifications
PUT /api/notifications/{id}/read/ # Mark as read
GET /api/notifications/unread-count/ # Unread count
```

## 🎨 Frontend Structure

### Pages
- **Public Pages:**
  - `index.html` - Landing page
  - `Login.html` - Authentication
  - `registration.html` - User registration
  - `forgot-password.html` - Password recovery

- **Voter Dashboard:**
  - `Voter-dashboard.html` - Main dashboard
  - `election-page.html` - Election listings
  - `vote.html` - Voting interface
  - `notifications.html` - User notifications
  - `Voter-guidline.html` - Voting guidelines

- **Admin Dashboard:**
  - `admin-dashboard.html` - Admin overview
  - `admin-election.html` - Election management
  - `admin-voters.html` - Voter management
  - `admin-candidate.html` - Candidate management
  - `admin-results.html` - Results viewing

### JavaScript Modules
- `config.js` - API configuration
- `auth.js` - Authentication management
- `api.js` - API communication
- `dashboard.js` - Dashboard functionality
- `elections.js` - Election operations
- `notifications.js` - Notification handling
- `results.js` - Results display

## 🔧 Configuration

### Backend Configuration
The Django settings are configured in `backend/voting_system/settings.py`:
- Database: SQLite (development)
- API Base URL: `http://0.0.0.0:8000/api`
- CORS enabled for frontend integration
- Token authentication enabled

### Frontend Configuration
API configuration in `js/config.js`:
```javascript
const API_CONFIG = {
    BASE_URL: 'http://0.0.0.0:8000/api',
    ENDPOINTS: {
        LOGIN: '/accounts/login/',
        REGISTER: '/accounts/register/',
        ELECTIONS: '/elections/',
        VOTE: '/voting/vote/',
        NOTIFICATIONS: '/notifications/'
    }
};
```

## 🚀 Deployment on Replit

This project is configured to run on Replit:

1. **Click the Run button** to start the Django backend
2. **Open the frontend** by opening `index.html`
3. **Admin access** via the Django admin panel

The Run button executes:
- Database migrations
- Django development server on port 8000

## 👥 User Roles

### Voter
- Register for elections
- Cast votes securely
- View election results
- Receive notifications

### Administrator
- Create and manage elections
- Approve candidates and voters
- Monitor election progress
- Generate reports and analytics

### Candidate
- Register for positions
- Manage campaign information
- View election results

## 🔒 Security Considerations

- **Authentication**: Token-based with secure session management
- **Authorization**: Role-based access control
- **Vote Integrity**: One vote per position enforcement
- **Data Protection**: Secure handling of voter information
- **Audit Trail**: Complete logging of voting activities

## 📱 Mobile Support

The system is fully responsive and works on:
- Desktop browsers
- Tablets
- Mobile phones
- Various screen sizes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is created for educational purposes. Please ensure compliance with your institution's policies when deploying.

## 📞 Support

For technical support or questions:
- Email: isaiahdurojaiye9@gmail.com
- Check the FAQ section on the website
- Review the voter guidelines

## 🎯 Future Enhancements

- Real-time vote counting with WebSockets
- Advanced analytics dashboard
- Multi-language support
- Email notification system
- Blockchain integration for enhanced security
- Mobile app development

---

**RUN POLLS** - Making democracy digital, secure, and accessible! 🗳️
