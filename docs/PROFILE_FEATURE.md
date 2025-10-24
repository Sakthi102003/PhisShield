# Profile Feature Documentation

## Overview
Added a comprehensive Profile section that displays user information and is especially useful for users who sign up through Google authentication.

## Features

### User Profile Display
- **Avatar/Photo**: Displays Google profile photo for OAuth users or default avatar icon
- **Username**: Editable username field
- **Display Name**: Optional display name (especially useful for Google users)
- **Email**: User's email address (read-only)
- **Total Scans**: Number of URL scans performed
- **Member Since**: Account creation date
- **Account Type**: Shows whether user signed up via Google or email/password

### Profile Editing
- Users can update their username and display name
- Real-time validation for username uniqueness
- Save/Cancel functionality with error handling

### Google Authentication Integration
- Automatically stores Google profile information (display name, photo URL)
- Shows "Google Account" badge for OAuth users
- Special notice explaining Google account security
- Links Google UID to prevent duplicate accounts

## Database Changes

### New User Model Fields
```python
display_name = db.Column(db.String(120), nullable=True)
photo_url = db.Column(db.String(512), nullable=True)
auth_provider = db.Column(db.String(20), default='local')  # 'local' or 'google'
google_uid = db.Column(db.String(128), nullable=True)
```

### Migration
The `migrate_db.py` script adds these columns to existing databases without data loss.

## API Endpoints

### GET /api/profile
**Authentication**: Required (JWT token)

**Response**:
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "display_name": "John Doe",
  "photo_url": "https://lh3.googleusercontent.com/...",
  "auth_provider": "google",
  "created_at": "2025-10-24T12:00:00",
  "total_scans": 42
}
```

### PUT /api/profile
**Authentication**: Required (JWT token)

**Request Body**:
```json
{
  "username": "new_username",
  "display_name": "New Display Name"
}
```

**Response**:
```json
{
  "message": "Profile updated successfully",
  "username": "new_username",
  "display_name": "New Display Name"
}
```

## Frontend Components

### Profile.jsx
Main profile component with:
- Profile information display
- Edit mode with form validation
- Avatar display (Google photo or default)
- Account information section
- Security notice for Google users

### Navigation
Added "Profile" tab to main navigation with User icon

## User Experience

### For Google Auth Users:
1. Sign up with Google → Profile automatically populated with:
   - Display name from Google
   - Profile photo from Google
   - Email from Google
   - Google UID for account linking

2. Can customize:
   - Username (unique)
   - Display name (optional)

3. Cannot change:
   - Email (managed by Google)
   - Profile photo (uses Google photo)

### For Email/Password Users:
1. Sign up with email/password → Basic profile:
   - Username (chosen during signup)
   - Email (from signup)
   - Default avatar

2. Can customize:
   - Username (unique)
   - Display name (optional)

## Security Features

- **JWT Authentication**: All profile endpoints require valid JWT token
- **Username Uniqueness**: Validated before allowing updates
- **Google Account Linking**: Prevents duplicate accounts via google_uid
- **Auto-update**: Updates Google info (photo, display name) on each login if changed

## Visual Design

### Profile Card
- Cyberpunk-themed styling matching app design
- Responsive layout (mobile-friendly)
- Avatar with camera icon overlay (future upload feature)
- Provider badge (Google/Local) with color coding

### Account Information
- Card showing account type, provider, and status
- Visual distinction between Google and local accounts
- Security notice for Google users with shield icon

### Edit Mode
- Inline form for profile editing
- Save/Cancel buttons with icons
- Real-time error display
- Loading states during updates

## Files Modified/Created

### Backend
- ✅ `backend/models/__init__.py` - Updated User model with new fields
- ✅ `backend/app.py` - Added profile endpoints (GET, PUT)
- ✅ `backend/app.py` - Updated Google auth to save profile info
- ✅ `backend/migrate_db.py` - Database migration script

### Frontend
- ✅ `frontend/src/components/Profile.jsx` - New profile component
- ✅ `frontend/src/App.jsx` - Integrated profile into navigation

## Testing

### Test Profile View
1. Log in with any account
2. Click "Profile" tab in navigation
3. Verify all information displays correctly
4. Check avatar displays (Google photo or default)

### Test Profile Edit
1. Click "Edit Profile" button
2. Change username and/or display name
3. Click "Save Changes"
4. Verify success message and updated info
5. Test Cancel button functionality

### Test Google Auth Integration
1. Sign up with Google account
2. Navigate to Profile
3. Verify Google info populated:
   - Display name from Google
   - Profile photo visible
   - "Google Account" badge shown
   - Security notice displayed

### Test Validation
1. Try updating username to one that already exists
2. Verify error message appears
3. Try empty username
4. Verify validation prevents submission

## Future Enhancements

- [ ] Profile photo upload for local accounts
- [ ] Email change functionality (with verification)
- [ ] Password change for local accounts
- [ ] Account linking (add Google to existing account)
- [ ] Two-factor authentication
- [ ] Account deletion
- [ ] Activity log/session history
- [ ] Privacy settings
- [ ] Notification preferences

## Migration Instructions

### For Existing Databases:
```bash
cd backend
python migrate_db.py
```

This will:
1. Check existing columns in users table
2. Add new columns: display_name, photo_url, auth_provider, google_uid
3. Preserve all existing user data
4. Display success/error messages

### For New Installations:
No migration needed - new tables will be created with all fields automatically.

## Benefits

### For Users:
- ✅ View account information at a glance
- ✅ Customize username and display name
- ✅ See scan statistics
- ✅ Understand account type and security

### For Google Auth Users Specifically:
- ✅ Profile auto-populated with Google info
- ✅ Professional photo from Google account
- ✅ Clear indication of authentication method
- ✅ No need to set up profile manually

### For Development:
- ✅ Foundation for future user features
- ✅ Clean separation of auth providers
- ✅ Easy to extend with more fields
- ✅ Proper error handling and validation
