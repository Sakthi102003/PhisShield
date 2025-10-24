import { Camera, Mail, Shield, User as UserIcon, Calendar, Edit2, Save, X } from 'lucide-react';
import { useEffect, useState } from 'react';
import { toast } from 'react-toastify';
import api from '../services/api';

const Profile = ({ user }) => {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    display_name: ''
  });

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const response = await api.get('/api/profile');
      setProfile(response.data);
      setFormData({
        username: response.data.username,
        display_name: response.data.display_name || ''
      });
    } catch (err) {
      console.error('Profile fetch error:', err);
      setError(err.response?.data?.error || 'Failed to fetch profile');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await api.put('/api/profile', formData);
      setProfile({ ...profile, ...formData });
      setEditing(false);
      
      // Update localStorage username if changed
      if (formData.username !== profile.username) {
        localStorage.setItem('username', formData.username);
      }
      
      toast.success('Profile updated successfully!', {
        position: "top-right",
        autoClose: 3000,
      });
    } catch (err) {
      console.error('Profile update error:', err);
      const errorMsg = err.response?.data?.error || 'Failed to update profile';
      setError(errorMsg);
      toast.error(errorMsg, {
        position: "top-right",
        autoClose: 3000,
      });
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    setFormData({
      username: profile.username,
      display_name: profile.display_name || ''
    });
    setEditing(false);
    setError('');
  };

  if (loading && !profile) {
    return (
      <div className="flex justify-center items-center p-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (error && !profile) {
    return (
      <div className="cyberpunk-card p-4 rounded-lg text-destructive">
        {error}
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold cyberpunk-text flex items-center gap-2">
          <UserIcon size={28} />
          Profile
        </h2>
      </div>

      {/* Profile Card */}
      <div className="cyberpunk-card rounded-lg p-6">
        <div className="flex flex-col md:flex-row gap-6">
          {/* Avatar Section */}
          <div className="flex flex-col items-center space-y-4">
            <div className="relative">
              {profile?.photo_url ? (
                <img
                  src={profile.photo_url}
                  alt={profile.display_name || profile.username}
                  className="w-32 h-32 rounded-full border-4 border-accent/30 object-cover"
                />
              ) : (
                <div className="w-32 h-32 rounded-full border-4 border-accent/30 bg-accent/10 flex items-center justify-center">
                  <UserIcon size={48} className="text-accent" />
                </div>
              )}
              <div className="absolute bottom-0 right-0 bg-accent/20 p-2 rounded-full border-2 border-accent/50">
                <Camera size={20} className="text-accent" />
              </div>
            </div>
            
            {/* Auth Provider Badge */}
            <div className={`px-3 py-1 rounded-full text-sm font-medium ${
              profile?.auth_provider === 'google'
                ? 'bg-blue-500/10 text-blue-500 border border-blue-500/30'
                : 'bg-accent/10 text-accent border border-accent/30'
            }`}>
              {profile?.auth_provider === 'google' ? '🔐 Google Account' : '🔐 Local Account'}
            </div>
          </div>

          {/* Profile Information */}
          <div className="flex-1 space-y-6">
            {editing ? (
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-muted-foreground mb-2">
                    Username
                  </label>
                  <input
                    type="text"
                    value={formData.username}
                    onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                    className="cyberpunk-input w-full px-4 py-2 rounded"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-muted-foreground mb-2">
                    Display Name
                  </label>
                  <input
                    type="text"
                    value={formData.display_name}
                    onChange={(e) => setFormData({ ...formData, display_name: e.target.value })}
                    className="cyberpunk-input w-full px-4 py-2 rounded"
                    placeholder="Your display name"
                  />
                </div>

                {error && (
                  <div className="bg-destructive/10 text-destructive p-3 rounded text-sm">
                    {error}
                  </div>
                )}

                <div className="flex gap-3">
                  <button
                    type="submit"
                    disabled={loading}
                    className="cyberpunk-button px-4 py-2 rounded flex items-center gap-2 disabled:opacity-50"
                  >
                    <Save size={18} />
                    Save Changes
                  </button>
                  <button
                    type="button"
                    onClick={handleCancel}
                    className="cyberpunk-button-secondary px-4 py-2 rounded flex items-center gap-2"
                  >
                    <X size={18} />
                    Cancel
                  </button>
                </div>
              </form>
            ) : (
              <>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <div className="flex items-center gap-2 text-muted-foreground text-sm">
                      <UserIcon size={16} />
                      <span>Username</span>
                    </div>
                    <div className="text-lg font-semibold text-foreground">
                      {profile?.username}
                    </div>
                  </div>

                  {profile?.display_name && (
                    <div className="space-y-2">
                      <div className="flex items-center gap-2 text-muted-foreground text-sm">
                        <UserIcon size={16} />
                        <span>Display Name</span>
                      </div>
                      <div className="text-lg font-semibold text-foreground">
                        {profile.display_name}
                      </div>
                    </div>
                  )}

                  <div className="space-y-2">
                    <div className="flex items-center gap-2 text-muted-foreground text-sm">
                      <Mail size={16} />
                      <span>Email</span>
                    </div>
                    <div className="text-lg font-semibold text-foreground break-all">
                      {profile?.email}
                    </div>
                  </div>

                  <div className="space-y-2">
                    <div className="flex items-center gap-2 text-muted-foreground text-sm">
                      <Shield size={16} />
                      <span>Total Scans</span>
                    </div>
                    <div className="text-lg font-semibold text-accent">
                      {profile?.total_scans || 0}
                    </div>
                  </div>

                  <div className="space-y-2">
                    <div className="flex items-center gap-2 text-muted-foreground text-sm">
                      <Calendar size={16} />
                      <span>Member Since</span>
                    </div>
                    <div className="text-lg font-semibold text-foreground">
                      {profile?.created_at ? new Date(profile.created_at).toLocaleDateString() : 'N/A'}
                    </div>
                  </div>
                </div>

                <button
                  onClick={() => setEditing(true)}
                  className="cyberpunk-button px-4 py-2 rounded flex items-center gap-2 mt-4"
                >
                  <Edit2 size={18} />
                  Edit Profile
                </button>
              </>
            )}
          </div>
        </div>
      </div>

      {/* Account Information */}
      <div className="cyberpunk-card rounded-lg p-6">
        <h3 className="text-xl font-semibold cyberpunk-text mb-4">Account Information</h3>
        <div className="space-y-3">
          <div className="flex justify-between items-center p-3 bg-black/20 rounded">
            <span className="text-muted-foreground">Account Type</span>
            <span className="font-mono text-accent">
              {profile?.auth_provider === 'google' ? 'Google OAuth' : 'Email/Password'}
            </span>
          </div>
          
          {profile?.auth_provider === 'google' && (
            <div className="flex justify-between items-center p-3 bg-black/20 rounded">
              <span className="text-muted-foreground">Google Account</span>
              <span className="font-mono text-accent">✓ Linked</span>
            </div>
          )}
          
          <div className="flex justify-between items-center p-3 bg-black/20 rounded">
            <span className="text-muted-foreground">Account Status</span>
            <span className="font-mono text-[#34c759]">Active</span>
          </div>
        </div>
      </div>

      {/* Security Notice for Google Users */}
      {profile?.auth_provider === 'google' && (
        <div className="cyberpunk-card rounded-lg p-4 bg-blue-500/10 border border-blue-500/30">
          <div className="flex items-start gap-3">
            <Shield className="text-blue-500 mt-1" size={20} />
            <div className="flex-1">
              <h4 className="font-semibold text-blue-500 mb-1">Google Account</h4>
              <p className="text-sm text-muted-foreground">
                You signed up using Google authentication. Your account is secured by Google's authentication system.
                You can update your username and display name here, but your email is managed through your Google account.
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Profile;
