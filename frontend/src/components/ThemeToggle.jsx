import { Moon, Sun } from 'lucide-react';
import { useEffect, useState } from 'react';

const ThemeToggle = () => {
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    // Check for saved theme preference or system preference
    const savedTheme = localStorage.getItem('theme');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    setIsDark(savedTheme === 'dark' || (!savedTheme && systemPrefersDark));
  }, []);

  useEffect(() => {
    // Update document theme attribute when isDark changes
    document.documentElement.setAttribute('data-theme', isDark ? 'dark' : 'light');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
  }, [isDark]);

  return (
    <button
      onClick={() => setIsDark(!isDark)}
      className="p-2 rounded-md cyberpunk-button"
      title={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
    >
      {isDark ? (
        <Sun className="h-5 w-5 text-primary-foreground" />
      ) : (
        <Moon className="h-5 w-5 text-primary-foreground" />
      )}
    </button>
  );
};

export default ThemeToggle;
