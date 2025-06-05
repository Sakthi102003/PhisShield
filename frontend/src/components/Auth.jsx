import axios from 'axios';
import { useState } from 'react';
import { config } from '../config';

const Auth = ({ onLogin }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: ''
  });
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const endpoint = isLogin ? '/api/auth/login' : '/api/auth/register';
      const response = await axios({
        method: 'post',
        url: `${config.apiUrl}${endpoint}`,
        data: formData,
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        withCredentials: true
      });
      
      if (response.data.token) {
        localStorage.setItem('token', response.data.token);
        localStorage.setItem('username', response.data.username);
        onLogin(response.data);
      }
    } catch (err) {
      console.error('Auth error:', err);
      console.error('Response:', err.response);
      setError(err.response?.data?.error || 'Authentication failed. Please try again.');
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-background text-foreground py-12 px-4 sm:px-6 lg:px-8">
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
                className="cyberpunk-button w-full py-2 rounded"
              >
                {isLogin ? 'Sign In' : 'Create Account'}
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
