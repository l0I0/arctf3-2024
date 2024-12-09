import React, { useState, useEffect } from 'react';
import { Box, Typography, Paper } from '@mui/material';
import { getBalance } from '../services/api';

interface BalanceProps {
  onBalanceUpdate?: (balance: number) => void;
}

const Balance: React.FC<BalanceProps> = ({ onBalanceUpdate }) => {
  const [balance, setBalance] = useState<number>(0);

  const updateBalance = async () => {
    try {
      const response = await getBalance();
      setBalance(response.coin_balance);
      if (onBalanceUpdate) {
        onBalanceUpdate(response.coin_balance);
      }
    } catch (error) {
      console.error('Failed to fetch balance:', error);
    }
  };

  useEffect(() => {
    updateBalance();
    const interval = setInterval(updateBalance, 2000); // Update every 2 seconds
    return () => clearInterval(interval);
  }, []);

  return (
    <Paper 
      sx={{ 
        position: 'fixed', 
        top: 70, 
        right: 20, 
        p: 2, 
        zIndex: 1000,
        backgroundColor: 'rgba(255, 255, 255, 0.9)'
      }}
    >
      <Typography variant="h6">
        Balance: {balance.toLocaleString()} coins
      </Typography>
    </Paper>
  );
};

export default Balance; 