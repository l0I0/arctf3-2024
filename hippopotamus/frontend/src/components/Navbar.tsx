import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box, ListItem, ListItemIcon, ListItemText } from '@mui/material';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import HowToVoteIcon from '@mui/icons-material/HowToVote';

interface NavbarProps {
  onLogout?: () => void;
}

const Navbar: React.FC<NavbarProps> = ({ onLogout }) => {
  const token = localStorage.getItem('token');
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    if (onLogout) onLogout();
    navigate('/login');
  };

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Hippo Clicker
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          {token ? (
            <>
              <Button color="inherit" component={RouterLink} to="/">
                Game
              </Button>
              <Button color="inherit" component={RouterLink} to="/shop">
                Shop
              </Button>
              <Button color="inherit" component={RouterLink} to="/profile">
                Profile
              </Button>
              <Button color="inherit" component={RouterLink} to="/elections">
                Elections
              </Button>
              <Button color="inherit" onClick={handleLogout}>
                Logout
              </Button>
            </>
          ) : (
            <>
              <Button color="inherit" component={RouterLink} to="/login">
                Login
              </Button>
              <Button color="inherit" component={RouterLink} to="/register">
                Register
              </Button>
            </>
          )}
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar; 