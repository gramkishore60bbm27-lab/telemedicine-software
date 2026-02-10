# Telemedicine Software

A web-based telemedicine platform with video calling capabilities for secure remote medical consultations.

## 🎯 Overview

This telemedicine platform enables healthcare professionals to conduct secure video consultations with patients from anywhere. Built with Flask (Python backend) and Jitsi Meet (video technology), it provides a complete solution for remote healthcare delivery.

## ✨ Features

### Core Features
- 🎥 **One-on-one Video Consultations** - High-quality video calls with HD support
- 🎤 **Audio/Video Controls** - Easy mute/unmute and camera on/off controls
- 🖥️ **Screen Sharing** - Share medical reports, test results, and documents
- 💬 **Text Chat** - Real-time messaging during video calls
- 👥 **Participant Management** - View and manage call participants
- 🔗 **Easy Room Sharing** - Simple link sharing to join consultations

### Additional Features
- 📱 **Mobile Responsive** - Works on desktop, tablet, and mobile devices
- 📋 **Consultation History** - Track all consultations with timestamps
- 📊 **Active Consultations List** - View all scheduled and ongoing consultations
- 📋 **Copy Room Link** - One-click link copying for easy sharing
- 🎨 **Professional UI** - Medical-themed, user-friendly interface
- ⚠️ **Error Handling** - Comprehensive error messages and notifications
- 🔒 **Secure Room IDs** - UUID-based room identification for security

## 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3 (Responsive Design)
- JavaScript (ES6+)
- Jitsi Meet External API

### Backend
- Python 3.8+
- Flask 3.0.0
- Flask-SQLAlchemy (Database ORM)
- Flask-CORS (Cross-Origin Resource Sharing)
- SQLite (Development Database)

### Video Technology
- Jitsi Meet (meet.jit.si for development)

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Safari, or Edge)
- Internet connection (for Jitsi Meet)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/gramkishore60bbm27-lab/telemedicine-software.git
cd telemedicine-software
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your preferred settings (optional for development)
# The defaults will work fine for testing
```

### 5. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## 📖 Usage Guide

### For Doctors: Creating a Consultation

1. Navigate to the **Consultations** page
2. Fill in the "Create New Consultation" form:
   - Enter your name (Doctor Name)
   - Enter the patient's name
3. Click **"Create Consultation Room"**
4. Copy the generated room link
5. Share the link with your patient via email, SMS, or messaging
6. Click **"Join Room Now"** to enter the consultation

### For Patients: Joining a Consultation

#### Option 1: Using the Room Link
1. Click on the link provided by your doctor
2. You'll be taken directly to the video call interface
3. Allow camera and microphone permissions when prompted
4. Join the consultation

#### Option 2: Using Room ID
1. Go to the **Consultations** page
2. In the "Join Consultation" section, enter the Room ID provided by your doctor
3. Click **"Join Consultation"**
4. Allow camera and microphone permissions
5. Join the consultation

### During the Consultation

- **Mute/Unmute**: Click the microphone icon
- **Video On/Off**: Click the camera icon
- **Screen Share**: Click the screen share icon
- **Chat**: Click the chat icon to open text messaging
- **End Call**: Click the red "End Call" button in the header

### Viewing Active Consultations

- On the Consultations page, scroll to the "Active Consultations" section
- See all scheduled and ongoing consultations
- Click "Join Room" to enter any active consultation
- Click "🔄 Refresh List" to update the list

## 🔌 API Endpoints

### Create Consultation
```http
POST /api/consultation/create
Content-Type: application/json

{
  "doctor_name": "Dr. John Smith",
  "patient_name": "Jane Doe",
  "scheduled_time": "2024-01-01T10:00:00" (optional)
}

Response:
{
  "success": true,
  "consultation": {
    "id": 1,
    "room_id": "uuid-room-id",
    "doctor_name": "Dr. John Smith",
    "patient_name": "Jane Doe",
    "scheduled_time": "2024-01-01T10:00:00",
    "status": "scheduled",
    "created_at": "2024-01-01T09:00:00"
  }
}
```

### Get Consultation Details
```http
GET /api/consultation/<room_id>

Response:
{
  "success": true,
  "consultation": {
    "id": 1,
    "room_id": "uuid-room-id",
    "doctor_name": "Dr. John Smith",
    "patient_name": "Jane Doe",
    "status": "active",
    ...
  }
}
```

### Join Consultation
```http
POST /api/consultation/join
Content-Type: application/json

{
  "room_id": "uuid-room-id"
}

Response:
{
  "success": true,
  "consultation": { ... }
}
```

### Get Active Consultations
```http
GET /api/consultation/active

Response:
{
  "success": true,
  "consultations": [
    { ... },
    { ... }
  ]
}
```

### End Consultation
```http
POST /api/consultation/end
Content-Type: application/json

{
  "room_id": "uuid-room-id"
}

Response:
{
  "success": true,
  "consultation": {
    "status": "completed",
    "ended_at": "2024-01-01T10:30:00",
    "duration": 30,
    ...
  }
}
```

## 📁 Project Structure

```
telemedicine-software/
├── static/
│   ├── css/
│   │   └── video-call.css          # Styling for all pages
│   └── js/
│       └── video-call.js           # Frontend JavaScript logic
├── templates/
│   ├── index.html                  # Landing page
│   ├── consultation.html           # Create/join consultations
│   └── video-call.html             # Video call interface
├── models/
│   ├── __init__.py                 # Database initialization
│   └── consultation.py             # Consultation data model
├── routes/
│   ├── __init__.py
│   └── consultation_routes.py      # API endpoints
├── services/
│   ├── __init__.py
│   └── video_service.py            # Business logic for consultations
├── app.py                          # Flask application entry point
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

## ⚙️ Configuration

### Environment Variables (.env)

```bash
# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=True

# Database Configuration
DATABASE_URL=sqlite:///telemedicine.db

# Jitsi Meet Configuration
JITSI_SERVER_URL=https://meet.jit.si

# Application Settings
HOST=0.0.0.0
PORT=5000
```

### Configuration Options

- **SECRET_KEY**: Secret key for Flask sessions (change in production!)
- **FLASK_ENV**: Environment mode (`development` or `production`)
- **FLASK_DEBUG**: Enable/disable debug mode
- **DATABASE_URL**: Database connection string
- **JITSI_SERVER_URL**: Jitsi Meet server URL
- **HOST**: Server host address
- **PORT**: Server port number

## 🔒 Security & HIPAA Compliance

### Current Security Features
- ✅ Secure UUID-based room IDs
- ✅ Room access validation
- ✅ CORS configuration
- ✅ Environment-based configuration
- ✅ Session management

### HIPAA Compliance Notes

⚠️ **Important**: This application uses the public Jitsi Meet server (meet.jit.si) which is **NOT HIPAA compliant** for production use with real patient data.

For HIPAA-compliant telemedicine in production, you **MUST**:

1. **Self-host Jitsi Meet** on your own secure servers
2. **Implement user authentication** with role-based access control
3. **Use SSL/TLS** encryption (HTTPS) for all communications
4. **Implement end-to-end encryption** for video calls
5. **Add audit logging** for all access and actions
6. **Implement data retention policies** and secure deletion
7. **Use a HIPAA-compliant database** (PostgreSQL/MySQL with encryption)
8. **Sign Business Associate Agreements** (BAAs) with service providers
9. **Implement access controls** and authentication
10. **Add patient consent** mechanisms

## 🚀 Production Deployment Recommendations

### Infrastructure
- Deploy on HIPAA-compliant cloud provider (AWS, Azure, Google Cloud)
- Use managed database service (RDS, Cloud SQL)
- Implement load balancing for scalability
- Set up automated backups

### Security Enhancements
- Implement JWT-based authentication
- Add role-based access control (RBAC)
- Enable rate limiting to prevent abuse
- Implement API key authentication
- Add IP whitelisting for admin access
- Use environment-specific configuration
- Implement comprehensive logging and monitoring

### Database
- Migrate from SQLite to PostgreSQL or MySQL
- Enable database encryption at rest
- Implement regular automated backups
- Set up database replication for high availability

### Monitoring & Logging
- Implement application performance monitoring (APM)
- Set up error tracking (Sentry, Rollbar)
- Configure server monitoring (Datadog, New Relic)
- Implement audit trail logging

### Additional Features for Production
- User registration and authentication
- Email notifications for consultations
- SMS reminders for appointments
- Consultation notes and medical records
- File upload for medical documents
- Payment processing integration
- Multi-language support
- Prescription generation

## 🐛 Troubleshooting

### Application won't start
- Ensure Python 3.8+ is installed: `python --version`
- Check if all dependencies are installed: `pip list`
- Verify virtual environment is activated
- Check for port conflicts (default: 5000)

### Database errors
- Delete `telemedicine.db` and restart the application
- Ensure SQLite is available on your system
- Check file permissions in the project directory

### Video call not loading
- Ensure you have a stable internet connection
- Check browser console for JavaScript errors
- Allow camera and microphone permissions
- Try a different browser
- Check if Jitsi Meet is accessible: https://meet.jit.si

### Room not found errors
- Ensure the room ID is correct
- Check if the consultation is still active
- Refresh the active consultations list

## 🧪 Testing

### Manual Testing Checklist
- [ ] Create a new consultation
- [ ] Copy room link
- [ ] Join consultation as patient
- [ ] Test video/audio controls
- [ ] Test screen sharing
- [ ] Test chat functionality
- [ ] Test end call functionality
- [ ] View active consultations
- [ ] Test on mobile device
- [ ] Test on different browsers

### Browser Compatibility
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ Mobile browsers (iOS Safari, Chrome Android)

## 📝 License

This project is open source and available for educational and development purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## 📧 Support

For questions or support, please open an issue on the GitHub repository.

## 🙏 Acknowledgments

- **Jitsi Meet** - Open-source video conferencing solution
- **Flask** - Python web framework
- **SQLAlchemy** - Database ORM

## 📚 Additional Resources

- [Jitsi Meet Documentation](https://jitsi.github.io/handbook/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [HIPAA Compliance Guide](https://www.hhs.gov/hipaa/index.html)
- [Telemedicine Best Practices](https://www.ama-assn.org/practice-management/digital/telemedicine-toolkit)

---

**Note**: This is a development/demonstration application. For production use with real patient data, ensure full HIPAA compliance and security measures are implemented.