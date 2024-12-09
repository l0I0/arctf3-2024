import React, { useState, useEffect, useRef } from 'react';
import { Box, Typography, Paper } from '@mui/material';
import { tapHippo } from '../services/api';
import { ClickEffect } from '../types';

const HippoClicker: React.FC = () => {
  const [clickEffects, setClickEffects] = useState<ClickEffect[]>([]);
  const [scale, setScale] = useState(1);
  const [lastClickAmount, setLastClickAmount] = useState(1);
  const [warning, setWarning] = useState<string | null>(null);
  const effectIdRef = useRef(0);

  const handleClick = async (e: React.MouseEvent<HTMLDivElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    setScale(0.95);
    setTimeout(() => setScale(1), 100);

    const newEffect: ClickEffect = {
      id: effectIdRef.current++,
      x,
      y,
      amount: lastClickAmount,
      opacity: 1
    };
    setClickEffects(prev => [...prev, newEffect]);

    try {
      const response = await tapHippo(lastClickAmount);
      setLastClickAmount(prev => prev + 1);
      
      if (response.warning) {
        setWarning(response.warning);
        setTimeout(() => setWarning(null), 3000);
      }
    } catch (error: any) {
      setWarning(error.response?.data?.detail || 'Error occurred while tapping');
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
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100vh',
        position: 'relative',
        overflow: 'hidden',
        userSelect: 'none'
      }}
    >
      {warning && (
        <Paper
          sx={{
            position: 'absolute',
            top: 20,
            padding: 2,
            backgroundColor: 'error.main',
            color: 'white',
            zIndex: 1000,
            animation: 'fadeIn 0.3s ease-in'
          }}
        >
          <Typography>{warning}</Typography>
        </Paper>
      )}

      <Box
        onClick={handleClick}
        sx={{
          width: '300px',
          height: '300px',
          backgroundColor: '#f0f0f0',
          borderRadius: '50%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          cursor: 'pointer',
          transition: 'transform 0.1s',
          transform: `scale(${scale})`,
          '&:hover': {
            transform: `scale(${scale * 1.05})`
          },
          '&:active': {
            transform: `scale(${scale * 0.95})`
          }
        }}
      >
        <Typography variant="h4" color="primary">
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
              color: 'primary.main',
              fontWeight: 'bold',
              fontSize: '24px',
              pointerEvents: 'none',
              transform: 'translate(-50%, -50%)',
              textShadow: '2px 2px 4px rgba(0,0,0,0.3)',
              transition: 'all 0.016s linear'
            }}
          >
            +{effect.amount}
          </Typography>
        ))}
      </Box>
    </Box>
  );
};

export default HippoClicker; 