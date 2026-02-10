// API Base URL
const API_BASE = '/api/consultation';

// Jitsi API instance
let jitsiApi = null;

// Utility Functions
function showNotification(message, type = 'info') {
    const notification = document.getElementById('notification');
    if (!notification) return;
    
    notification.textContent = message;
    notification.className = `notification ${type}`;
    notification.classList.add('show');
    
    setTimeout(() => {
        notification.classList.remove('show');
    }, 4000);
}

function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString();
}

// Consultation Page Functions
if (window.location.pathname === '/consultation') {
    document.addEventListener('DOMContentLoaded', () => {
        // Create Consultation Form
        const createForm = document.getElementById('createConsultationForm');
        if (createForm) {
            createForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const doctorName = document.getElementById('doctorName').value.trim();
                const patientName = document.getElementById('patientName').value.trim();
                
                if (!doctorName || !patientName) {
                    showNotification('Please fill in all required fields', 'error');
                    return;
                }
                
                try {
                    const response = await fetch(`${API_BASE}/create`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            doctor_name: doctorName,
                            patient_name: patientName
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        const roomId = data.consultation.room_id;
                        const roomLink = `${window.location.origin}/video-call/${roomId}`;
                        
                        // Show room link section
                        document.getElementById('roomLink').value = roomLink;
                        document.getElementById('roomLinkSection').style.display = 'block';
                        document.getElementById('joinRoomBtn').href = `/video-call/${roomId}`;
                        
                        // Hide form
                        createForm.style.display = 'none';
                        
                        showNotification('Consultation room created successfully!', 'success');
                        
                        // Refresh consultations list
                        loadActiveConsultations();
                    } else {
                        showNotification(`Error: ${data.error}`, 'error');
                    }
                } catch (error) {
                    console.error('Error creating consultation:', error);
                    showNotification('Failed to create consultation. Please try again.', 'error');
                }
            });
        }
        
        // Copy Link Button
        const copyLinkBtn = document.getElementById('copyLinkBtn');
        if (copyLinkBtn) {
            copyLinkBtn.addEventListener('click', async () => {
                const roomLink = document.getElementById('roomLink');
                try {
                    await navigator.clipboard.writeText(roomLink.value);
                    showNotification('Room link copied to clipboard!', 'success');
                } catch (err) {
                    // Fallback for browsers that don't support Clipboard API
                    roomLink.select();
                    document.execCommand('copy');
                    showNotification('Room link copied to clipboard!', 'success');
                }
            });
        }
        
        // Create Another Button
        const createAnotherBtn = document.getElementById('createAnotherBtn');
        if (createAnotherBtn) {
            createAnotherBtn.addEventListener('click', () => {
                document.getElementById('roomLinkSection').style.display = 'none';
                document.getElementById('createConsultationForm').style.display = 'block';
                document.getElementById('createConsultationForm').reset();
            });
        }
        
        // Join Consultation Form
        const joinForm = document.getElementById('joinConsultationForm');
        if (joinForm) {
            joinForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const roomId = document.getElementById('roomId').value.trim();
                
                if (!roomId) {
                    showNotification('Please enter a room ID', 'error');
                    return;
                }
                
                try {
                    const response = await fetch(`${API_BASE}/join`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ room_id: roomId })
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        showNotification('Joining consultation...', 'success');
                        setTimeout(() => {
                            window.location.href = `/video-call/${roomId}`;
                        }, 500);
                    } else {
                        showNotification(`Error: ${data.error}`, 'error');
                    }
                } catch (error) {
                    console.error('Error joining consultation:', error);
                    showNotification('Failed to join consultation. Please check the room ID.', 'error');
                }
            });
        }
        
        // Refresh Consultations Button
        const refreshBtn = document.getElementById('refreshConsultationsBtn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => {
                loadActiveConsultations();
            });
        }
        
        // Load active consultations on page load
        loadActiveConsultations();
    });
}

async function loadActiveConsultations() {
    const loadingSpinner = document.getElementById('loadingSpinner');
    const consultationsList = document.getElementById('consultationsList');
    const noConsultations = document.getElementById('noConsultations');
    
    if (!consultationsList) return;
    
    // Show loading
    if (loadingSpinner) loadingSpinner.style.display = 'flex';
    consultationsList.innerHTML = '';
    if (noConsultations) noConsultations.style.display = 'none';
    
    try {
        const response = await fetch(`${API_BASE}/active`);
        const data = await response.json();
        
        if (loadingSpinner) loadingSpinner.style.display = 'none';
        
        if (data.success && data.consultations.length > 0) {
            consultationsList.innerHTML = data.consultations.map(consultation => `
                <div class="consultation-item">
                    <div class="consultation-info">
                        <h4>👨‍⚕️ ${consultation.doctor_name} → 👤 ${consultation.patient_name}</h4>
                        <p>📅 Scheduled: ${formatDateTime(consultation.scheduled_time)}</p>
                        <p>🆔 Room ID: <code>${consultation.room_id}</code></p>
                        <span class="status-badge status-${consultation.status.toLowerCase()}">
                            ${consultation.status.toUpperCase()}
                        </span>
                    </div>
                    <div class="consultation-actions">
                        <a href="/video-call/${consultation.room_id}" class="btn btn-primary">
                            Join Room
                        </a>
                    </div>
                </div>
            `).join('');
        } else {
            if (noConsultations) noConsultations.style.display = 'block';
        }
    } catch (error) {
        console.error('Error loading consultations:', error);
        if (loadingSpinner) loadingSpinner.style.display = 'none';
        showNotification('Failed to load consultations', 'error');
    }
}

// Video Call Page Functions
if (window.location.pathname.startsWith('/video-call/')) {
    document.addEventListener('DOMContentLoaded', async () => {
        const roomId = ROOM_ID; // Set by template
        
        if (!roomId) {
            showError('Invalid room ID');
            return;
        }
        
        // Validate room exists
        try {
            const response = await fetch(`${API_BASE}/join`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ room_id: roomId })
            });
            
            const data = await response.json();
            
            if (!data.success) {
                showError(data.error || 'Consultation room not found');
                return;
            }
            
            // Initialize Jitsi
            initializeJitsi(roomId, data.consultation);
            
        } catch (error) {
            console.error('Error validating room:', error);
            showError('Failed to connect to consultation room');
        }
        
        // End Call Button
        const endCallBtn = document.getElementById('endCallBtn');
        if (endCallBtn) {
            endCallBtn.addEventListener('click', () => {
                showEndCallModal();
            });
        }
        
        // End Call Modal
        const confirmEndBtn = document.getElementById('confirmEndBtn');
        if (confirmEndBtn) {
            confirmEndBtn.addEventListener('click', async () => {
                await endConsultation(roomId);
            });
        }
        
        const cancelEndBtn = document.getElementById('cancelEndBtn');
        if (cancelEndBtn) {
            cancelEndBtn.addEventListener('click', () => {
                hideEndCallModal();
            });
        }
    });
}

function initializeJitsi(roomId, consultationData) {
    const container = document.getElementById('jitsi-meet-container');
    const loadingScreen = document.getElementById('loadingScreen');
    
    if (!container) {
        console.error('Jitsi container not found');
        return;
    }
    
    const domain = 'meet.jit.si';
    const options = {
        roomName: roomId,
        width: '100%',
        height: '100%',
        parentNode: container,
        configOverwrite: {
            startWithAudioMuted: false,
            startWithVideoMuted: false,
            enableWelcomePage: false,
            prejoinPageEnabled: true,
            disableDeepLinking: true
        },
        interfaceConfigOverwrite: {
            TOOLBAR_BUTTONS: [
                'microphone', 'camera', 'closedcaptions', 'desktop', 'fullscreen',
                'fodeviceselection', 'hangup', 'profile', 'chat', 'recording',
                'livestreaming', 'etherpad', 'sharedvideo', 'settings', 'raisehand',
                'videoquality', 'filmstrip', 'stats', 'shortcuts',
                'tileview', 'download', 'help', 'mute-everyone'
            ],
            SHOW_JITSI_WATERMARK: false,
            SHOW_WATERMARK_FOR_GUESTS: false,
            MOBILE_APP_PROMO: false
        },
        userInfo: {
            displayName: consultationData.doctor_name || 'Participant'
        }
    };
    
    try {
        jitsiApi = new JitsiMeetExternalAPI(domain, options);
        
        // Hide loading screen when ready
        jitsiApi.addEventListener('videoConferenceJoined', () => {
            if (loadingScreen) {
                loadingScreen.style.display = 'none';
            }
            console.log('Joined video conference');
        });
        
        // Handle participant leaving
        jitsiApi.addEventListener('participantLeft', () => {
            console.log('Participant left');
        });
        
        // Handle video conference left
        jitsiApi.addEventListener('videoConferenceLeft', () => {
            console.log('Left video conference');
            window.location.href = '/consultation';
        });
        
        // Handle errors
        jitsiApi.addEventListener('errorOccurred', (error) => {
            console.error('Jitsi error:', error);
            showNotification('An error occurred during the call', 'error');
        });
        
    } catch (error) {
        console.error('Error initializing Jitsi:', error);
        showError('Failed to initialize video call');
    }
}

function showError(message) {
    const loadingScreen = document.getElementById('loadingScreen');
    const errorScreen = document.getElementById('errorScreen');
    const errorMessage = document.getElementById('errorMessage');
    
    if (loadingScreen) loadingScreen.style.display = 'none';
    if (errorScreen) errorScreen.style.display = 'flex';
    if (errorMessage) errorMessage.textContent = message;
}

function showEndCallModal() {
    const modal = document.getElementById('endCallModal');
    if (modal) {
        modal.style.display = 'flex';
    }
}

function hideEndCallModal() {
    const modal = document.getElementById('endCallModal');
    if (modal) {
        modal.style.display = 'none';
    }
}

async function endConsultation(roomId) {
    try {
        const response = await fetch(`${API_BASE}/end`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ room_id: roomId })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Dispose Jitsi
            if (jitsiApi) {
                jitsiApi.dispose();
            }
            
            showNotification('Consultation ended successfully', 'success');
            
            // Redirect to consultation page
            setTimeout(() => {
                window.location.href = '/consultation';
            }, 1000);
        } else {
            showNotification(`Error ending consultation: ${data.error}`, 'error');
            hideEndCallModal();
        }
    } catch (error) {
        console.error('Error ending consultation:', error);
        showNotification('Failed to end consultation', 'error');
        hideEndCallModal();
    }
}
