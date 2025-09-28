import { useState } from 'react';
import HomePage from './components/HomePage';
import ClientePortal from './components/ClientePortal';
import FuncionarioPortal from './components/FuncionarioPortal';
import { STORAGE_KEYS, USER_TYPES } from './config/constants';
import './App.css';

function App() {
  const [currentView, setCurrentView] = useState('home');
  const [currentUser, setCurrentUser] = useState(() => {
    const saved = localStorage.getItem(STORAGE_KEYS.CURRENT_USER);
    return saved ? JSON.parse(saved) : null;
  });

  const handleNavigate = (view) => {
    setCurrentView(view);
  };

  const handleUserLogin = (user, userType) => {
    setCurrentUser({ ...user, userType });
    localStorage.setItem(STORAGE_KEYS.CURRENT_USER, JSON.stringify({ ...user, userType }));
    localStorage.setItem(STORAGE_KEYS.USER_TYPE, userType);
  };

  const handleLogout = () => {
    setCurrentUser(null);
    localStorage.removeItem(STORAGE_KEYS.CURRENT_USER);
    localStorage.removeItem(STORAGE_KEYS.USER_TYPE);
    setCurrentView('home');
  };

  return (
    <div className="app">
      {currentView === 'home' && (
        <HomePage onNavigate={handleNavigate} />
      )}
      
      {currentView === 'cliente' && (
        <ClientePortal 
          user={currentUser?.userType === USER_TYPES.CLIENTE ? currentUser : null}
          onLogin={(user) => handleUserLogin(user, USER_TYPES.CLIENTE)}
          onLogout={handleLogout}
          onNavigateHome={() => handleNavigate('home')}
        />
      )}
      
      {currentView === 'funcionario' && (
        <FuncionarioPortal 
          onLogout={handleLogout}
          onNavigateHome={() => handleNavigate('home')}
        />
      )}
    </div>
  );
}

export default App;
