import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Game from './pages/Game';
import Shop from './pages/Shop';
import Profile from './pages/Profile';
import Login from './pages/Login';
import Register from './pages/Register';
import Balance from './components/Balance';
import PrivateRoute from './components/PrivateRoute';
import Elections from './pages/Elections';

function App() {
  const token = localStorage.getItem('token');

  return (
    <Router>
      <div className="App">
        <Navbar />
        {token && <Balance />}
        <main>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route
              path="/"
              element={
                <PrivateRoute>
                  <Game />
                </PrivateRoute>
              }
            />
            <Route
              path="/shop"
              element={
                <PrivateRoute>
                  <Shop />
                </PrivateRoute>
              }
            />
            <Route
              path="/profile"
              element={
                <PrivateRoute>
                  <Profile />
                </PrivateRoute>
              }
            />
            <Route
              path="/elections"
              element={
                <PrivateRoute>
                  <Elections />
                </PrivateRoute>
              }
            />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
