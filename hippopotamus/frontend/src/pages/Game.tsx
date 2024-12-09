import React, { useState, useEffect } from 'react';
import { Box, Typography, Paper } from '@mui/material';
import { tapHippo } from '../services/api';

interface ClickEffect {
  id: number;
  x: number;
  y: number;
  opacity: number;
}

const Game: React.FC = () => {
  const [balance, setBalance] = useState<number>(0);
  const [clickEffects, setClickEffects] = useState<ClickEffect[]>([]);
  const [warning, setWarning] = useState<string | null>(null);
  const [isPressed, setIsPressed] = useState(false);

  const handleTap = async (e: React.MouseEvent<HTMLDivElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    setIsPressed(true);
    setTimeout(() => setIsPressed(false), 100);

    const newEffect: ClickEffect = {
      id: Date.now(),
      x,
      y,
      opacity: 1
    };

    setClickEffects(prev => [...prev, newEffect]);

    try {
      const response = await tapHippo(1);
      setBalance(response.new_balance);
      
      if (response.warning) {
        setWarning(response.warning);
        setTimeout(() => setWarning(null), 3000);
      }
    } catch (error: any) {
      setWarning(error.response?.data?.detail || 'Error occurred');
      setTimeout(() => setWarning(null), 3000);
    }
  };

  useEffect(() => {
    const interval = setInterval(() => {
      setClickEffects(prev => {
        const newEffects = prev.map(effect => ({
          ...effect,
          opacity: effect.opacity - 0.02,
          y: effect.y - 1
        }));
        return newEffects.filter(effect => effect.opacity > 0);
      });
    }, 16);

    return () => clearInterval(interval);
  }, []);

  return (
    <Box sx={{ textAlign: 'center', p: 4 }}>
      {warning && (
        <Paper 
          elevation={3}
          sx={{ 
            p: 2, 
            mb: 2, 
            bgcolor: 'error.main', 
            color: 'white',
            maxWidth: 600,
            mx: 'auto'
          }}
        >
          <Typography>{warning}</Typography>
        </Paper>
      )}

      <Typography variant="h4" gutterBottom>
        Balance: {balance} coins
      </Typography>

      <Box 
        onClick={handleTap}
        sx={{
          position: 'relative',
          width: 300,
          height: 300,
          borderRadius: '50%',
          bgcolor: 'primary.main',
          mx: 'auto',
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          transition: 'transform 0.1s',
          transform: isPressed ? 'scale(0.95)' : 'scale(1)',
          '&:hover': {
            transform: 'scale(1.05)',
            bgcolor: 'primary.dark'
          },
          userSelect: 'none'
        }}
      >
        <Typography variant="h4" color="white">
          HIPPO
        </Typography>

        {clickEffects.map(effect => (
          <Typography
            key={effect.id}
            sx={{
              position: 'absolute',
              left: effect.x,
              top: effect.y,
              opacity: effect.opacity,
              color: 'white',
              fontWeight: 'bold',
              fontSize: '24px',
              pointerEvents: 'none',
              transform: 'translate(-50%, -50%)',
              textShadow: '2px 2px 4px rgba(0,0,0,0.3)'
            }}
          >
            +1
          </Typography>
        ))}
      </Box>
    </Box>
  );
};

export default Game; 