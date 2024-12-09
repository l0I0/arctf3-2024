import React, { useState, useEffect } from 'react';
import { Box, Typography, Card, CardContent, Button, Grid, Alert } from '@mui/material';
import { getUserPurchases, sellItem } from '../services/api';
import { Purchase } from '../types';

const UserPurchases: React.FC = () => {
  const [purchases, setPurchases] = useState<Purchase[]>([]);
  const [message, setMessage] = useState<string>('');
  const [error, setError] = useState<string>('');

  const loadPurchases = async () => {
    try {
      const data = await getUserPurchases();
      setPurchases(data.map((purchase: Purchase) => ({
        ...purchase,
        formatted_date: new Date(purchase.purchase_date).toLocaleString('ru-RU')
      })));
    } catch (err) {
      setError('Failed to load purchases');
    }
  };

  useEffect(() => {
    loadPurchases();
  }, []);

  const handleSell = async (purchaseId: number) => {
    try {
      const response = await sellItem(purchaseId);
      setMessage(`Successfully sold item for ${response.earned_amount} coins`);
      loadPurchases(); // Refresh the list
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to sell item');
    }
  };

  return (
    <Box sx={{ mt: 3 }}>
      <Typography variant="h5" gutterBottom>
        Your Purchases
      </Typography>

      {message && (
        <Alert severity="success" sx={{ mb: 2 }} onClose={() => setMessage('')}>
          {message}
        </Alert>
      )}

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError('')}>
          {error}
        </Alert>
      )}

      <Grid container spacing={2}>
        {purchases.length === 0 ? (
          <Grid item xs={12}>
            <Typography color="textSecondary">
              You haven't made any purchases yet
            </Typography>
          </Grid>
        ) : (
          purchases.map((purchase) => (
            <Grid item xs={12} sm={6} md={4} key={purchase.id}>
              <Card>
                <CardContent>
                  <Typography variant="h6">
                    {purchase.item_name}
                  </Typography>
                  <Typography color="textSecondary" gutterBottom>
                    {purchase.description}
                  </Typography>
                  <Typography variant="body2" sx={{ mb: 2 }}>
                    Purchased: {purchase.formatted_date}
                  </Typography>
                  <Button
                    variant="contained"
                    color="warning"
                    onClick={() => handleSell(purchase.id)}
                    fullWidth
                  >
                    Sell Item
                  </Button>
                </CardContent>
              </Card>
            </Grid>
          ))
        )}
      </Grid>
    </Box>
  );
};

export default UserPurchases; 