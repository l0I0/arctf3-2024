import React, { useState } from 'react';
import { Box, Button, Typography, Alert, Paper, Snackbar, Link } from '@mui/material';
import { generateVerificationCode, donate } from '../services/api';

const Profile: React.FC = () => {
  const [verificationCode, setVerificationCode] = useState<string>('');
  const [message, setMessage] = useState<string>('');
  const [error, setError] = useState<string>('');

  const handleGenerateCode = async () => {
    try {
      const response = await generateVerificationCode();
      setVerificationCode(response.verification_code);
      setMessage('Code generated successfully!');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate code');
    }
  };

  const handleDonate = async () => {
    try {
      const response = await donate();
      setMessage(`Задоначено ${response.donated_amount} коинов! Партия гордится тобой!`);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to donate');
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>Profile</Typography>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>Telegram Verification</Typography>
        <Typography variant="body2" sx={{ mb: 2 }}>
          1. First, start our bot: <Link href="https://t.me/h1ppo_bot" target="_blank" rel="noopener">@h1ppo_bot</Link>
        </Typography>
        <Typography variant="body2" sx={{ mb: 2 }}>
          2. Generate and copy the verification code below
        </Typography>
        <Typography variant="body2" sx={{ mb: 2 }}>
          3. Send the code to the bot to verify your account
        </Typography>
        <Button variant="contained" onClick={handleGenerateCode}>
          Generate Verification Code
        </Button>
        {verificationCode && (
          <Typography sx={{ mt: 2 }}>
            Your verification code: <strong>{verificationCode}</strong>
          </Typography>
        )}
      </Paper>

      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>Donate Coins</Typography>
        <Typography variant="body2" gutterBottom>
          Donate all your coins
        </Typography>
        <Button variant="contained" color="warning" onClick={handleDonate}>
          Donate All Coins
        </Button>
      </Paper>

      <Snackbar
        open={!!message || !!error}
        autoHideDuration={6000}
        onClose={() => { setMessage(''); setError(''); }}
      >
        <Alert severity={error ? 'error' : 'success'}>
          {error || message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default Profile; 