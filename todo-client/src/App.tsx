import React, { useState, useEffect } from 'react';
import { CssBaseline, ThemeProvider, createTheme } from '@mui/material';
import { TodoList } from './components/TodoList';
import { Login } from './components/Login';
import { Register } from './components/Register';

function App() {
  const [darkMode, setDarkMode] = useState<boolean>(() => {
    // Inicializamos desde localStorage
    return localStorage.getItem('darkMode') === 'true';
    });
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [token, setToken] = useState('');
  const [username, setUsername] = useState('');
  const [showRegister, setShowRegister] = useState(false);

  useEffect(() => {
    const savedToken = localStorage.getItem('token');
    const savedUsername = localStorage.getItem('username');
    if (savedToken && savedUsername) {
      setToken(savedToken);
      setUsername(savedUsername);
      setIsAuthenticated(true);
    }
  }, []);

  const theme = createTheme({
    palette: {
      mode: darkMode ? 'dark' : 'light',
    },
  });

  const handleLogin = (token: string, username: string) => {
    localStorage.setItem('token', token);
    localStorage.setItem('username', username);
    setToken(token);
    setUsername(username);
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    setToken('');
    setUsername('');
    setIsAuthenticated(false);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      {!isAuthenticated ? (
        showRegister ? (
          <Register
            onRegister={handleLogin}
            onToggleLogin={() => setShowRegister(false)}
          />
        ) : (
          <Login
            onLogin={handleLogin}
            onToggleRegister={() => setShowRegister(true)}
          />
        )
      ) : (
        <TodoList
        darkMode={darkMode}
        setDarkMode={(dm: boolean) => {
         setDarkMode(dm);
         localStorage.setItem('darkMode', dm.toString());
        }}
          token={token}
          username={username}
          onLogout={handleLogout}
        />
      )}
    </ThemeProvider>
  );
}

export default App;
