
# RUN POLLS - Django Backend

This is the Django REST API backend for the RUN POLLS online voting system.

## Features

- User authentication (Voters and Administrators)
- Election management
- Candidate registration and approval
- Secure voting system
- Real-time results
- Notification system
- Admin dashboard APIs

## Setup Instructions

1. **Install Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

4. **Run Development Server**
   ```bash
   python manage.py runserver 0.0.0.0:5000
   ```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/` - Update user profile

### Elections
- `GET /api/elections/` - List all elections
- `POST /api/elections/` - Create new election (admin only)
- `GET /api/elections/{id}/` - Get election details
- `GET /api/elections/{id}/candidates/` - Get election candidates
- `POST /api/elections/register-candidate/` - Register as candidate
- `GET /api/elections/registrations/` - Get election registrations
- `GET /api/elections/dashboard-stats/` - Get dashboard statistics

### Voting
- `POST /api/voting/cast-vote/` - Cast votes
- `GET /api/voting/my-votes/` - Get user's votes
- `GET /api/voting/results/{election_id}/` - Get election results
- `GET /api/voting/eligibility/{election_id}/` - Check voting eligibility

### Notifications
- `GET /api/notifications/` - Get notifications
- `PUT /api/notifications/{id}/read/` - Mark notification as read
- `GET /api/notifications/unread-count/` - Get unread count
- `GET /api/notifications/announcements/` - Get system announcements

## Database Schema

The system uses SQLite with the following main models:

### User Management
- `User` - Extended Django user model
- `VoterProfile` - Voter-specific information
- `AdminProfile` - Administrator information

### Elections
- `Election` - Election details and settings
- `Position` - Positions within elections
- `Candidate` - Candidate registrations
- `ElectionRegistration` - Voter registrations for elections

### Voting
- `Vote` - Individual vote records
- `VotingSession` - Voting session tracking

### Notifications
- `Notification` - User notifications
- `SystemAnnouncement` - System-wide announcements

## Security Features

- Token-based authentication
- User type validation
- Election status validation
- Vote uniqueness constraints
- IP tracking for voting sessions
- Registration approval workflow

## Usage Examples

### Register a new voter
```python
import requests

data = {
    "email": "student@university.edu",
    "username": "student123",
    "password": "securepassword",
    "confirm_password": "securepassword",
    "first_name": "John",
    "last_name": "Doe",
    "student_id": "2023001",
    "department": "Computer Science"
}

response = requests.post("http://localhost:5000/api/auth/register/", json=data)
```

### Login and get token
```python
login_data = {
    "email": "student@university.edu",
    "password": "securepassword",
    "user_type": "voter"
}

response = requests.post("http://localhost:5000/api/auth/login/", json=login_data)
token = response.json()["token"]
```

### Cast a vote
```python
headers = {"Authorization": f"Token {token}"}
vote_data = {
    "election_id": 1,
    "votes": [
        {"position_id": 1, "candidate_id": 2},
        {"position_id": 2, "candidate_id": 5}
    ]
}

response = requests.post("http://localhost:5000/api/voting/cast-vote/", 
                        json=vote_data, headers=headers)
```

## Admin Panel

Access the Django admin panel at `http://localhost:5000/admin/` to manage:
- Users and profiles
- Elections and positions
- Candidates and registrations
- Votes and sessions
- Notifications and announcements
