import { signInWithPopup, signInWithRedirect, getRedirectResult } from 'firebase/auth';
import { useEffect, useState } from 'react';
import { auth, googleProvider } from '../config/firebase';
import api from '../services/api';
import ThemeToggle from './ThemeToggle';

const Auth = ({ onLogin }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Check for redirect result on component mount
  useEffect(() => {
    const checkRedirectResult = async () => {
      try {
        const result = await getRedirectResult(auth);
        if (result) {
          // User successfully signed in with redirect
          await handleGoogleAuthSuccess(result.user);
        }
      } catch (err) {
        console.error('Redirect result error:', err);
        setError('Google authentication failed. Please try again.');
      }
    };
    checkRedirectResult();
  }, []);

  const handleGoogleAuthSuccess = async (user) => {
    try {
      // Send the Google user data to your backend
      const endpoint = '/api/auth/google';
      const response = await api.post(endpoint, {
        uid: user.uid,
        email: user.email,
        displayName: user.displayName,
        photoURL: user.photoURL
      });

      if (response.data.token) {
        localStorage.setItem('token', response.data.token);
        localStorage.setItem('username', response.data.username);
        onLogin(response.data);
      }
    } catch (err) {
      console.error('Google auth backend error:', err);
      throw err;
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const endpoint = isLogin ? '/api/auth/login' : '/api/auth/register';
      const response = await api.post(endpoint, formData);
      
      if (response.data.token) {
        localStorage.setItem('token', response.data.token);
        localStorage.setItem('username', response.data.username);
        onLogin(response.data);
      }
    } catch (err) {
      console.error('Auth error:', err);
      console.error('Response:', err.response);
      setError(err.response?.data?.error || 'Authentication failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleAuth = async () => {
    setError('');
    setLoading(true);

    try {
      // Try popup first
      try {
        const result = await signInWithPopup(auth, googleProvider);
        await handleGoogleAuthSuccess(result.user);
      } catch (popupError) {
        // If popup fails (blocked or COOP issue), use redirect instead
        if (
          popupError.code === 'auth/popup-blocked' ||
          popupError.code === 'auth/popup-closed-by-user' ||
          popupError.code === 'auth/cancelled-popup-request' ||
          popupError.message?.includes('Cross-Origin')
        ) {
          console.log('Popup blocked or COOP issue, using redirect instead');
          // Use redirect method instead
          await signInWithRedirect(auth, googleProvider);
          // The page will reload and handle the result in useEffect
          return;
        }
        throw popupError;
      }
    } catch (err) {
      console.error('Google auth error:', err);
      setError(err.response?.data?.error || 'Google authentication failed. Please try again.');
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-background text-foreground py-12 px-4 sm:px-6 lg:px-8 relative">
      {/* Theme Toggle - Fixed Position */}
      <div className="fixed top-4 right-4 z-10">
        <ThemeToggle />
      </div>

      <div className="max-w-md w-full">
        <div className="text-center">
          <h1 className="text-4xl font-bold mb-2 cyberpunk-text">PhishShield</h1>
          <h2 className="text-2xl font-semibold cyberpunk-text">
            {isLogin ? 'Access Portal' : 'New User Registration'}
          </h2>
        </div>

        <div className="mt-8 cyberpunk-card p-6 rounded-lg">
          <form className="space-y-6" onSubmit={handleSubmit}>
            <div className="space-y-4">
              <div>
                <input
                  name="username"
                  type="text"
                  required
                  value={formData.username}
                  onChange={handleChange}
                  placeholder="Username"
                  className="cyberpunk-input w-full px-4 py-2 rounded"
                />
              </div>

              {!isLogin && (
                <div>
                  <input
                    name="email"
                    type="email"
                    required
                    value={formData.email}
                    onChange={handleChange}
                    placeholder="Email"
                    className="cyberpunk-input w-full px-4 py-2 rounded"
                  />
                </div>
              )}

              <div>
                <input
                  name="password"
                  type="password"
                  required
                  value={formData.password}
                  onChange={handleChange}
                  placeholder="Password"
                  className="cyberpunk-input w-full px-4 py-2 rounded"
                />
              </div>
            </div>

            {error && (
              <div className="bg-destructive/10 text-destructive px-4 py-3 rounded text-sm">
                {error}
              </div>
            )}

            <div className="space-y-4">
              <button
                type="submit"
                disabled={loading}
                className="cyberpunk-button w-full py-2 rounded disabled:opacity-50"
              >
                {loading ? 'Please wait...' : (isLogin ? 'Sign In' : 'Create Account')}
              </button>

              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-accent/20"></div>
                </div>
                <div className="relative flex justify-center text-sm">
                  <span className="px-2 bg-card text-muted-foreground">Or continue with</span>
                </div>
              </div>

              <button
                type="button"
                onClick={handleGoogleAuth}
                disabled={loading}
                className="w-full flex items-center justify-center gap-3 px-4 py-2 border border-accent/30 rounded hover:bg-accent/10 transition-colors disabled:opacity-50"
              >
                <svg className="w-5 h-5" viewBox="0 0 24 24">
                  <path
                    fill="#4285F4"
                    d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                  />
                  <path
                    fill="#34A853"
                    d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                  />
                  <path
                    fill="#FBBC05"
                    d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                  />
                  <path
                    fill="#EA4335"
                    d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                  />
                </svg>
                <span>Sign {isLogin ? 'in' : 'up'} with Google</span>
              </button>

              <button
                type="button"
                onClick={() => setIsLogin(!isLogin)}
                className="text-primary hover:text-secondary transition-colors text-sm w-full text-center"
              >
                {isLogin
                  ? "Don't have an account? Sign up"
                  : 'Already have an account? Sign in'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Auth;
