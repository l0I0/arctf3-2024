import React, { useState, useEffect } from 'react';
import { Box, Grid, Card, CardContent, Typography, Button, Alert, Tabs, Tab } from '@mui/material';
import { getShopItems, buyItem, getUserPurchases, sellItem } from '../services/api';
import { ShopItem, Purchase } from '../types';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

const TabPanel = (props: TabPanelProps) => {
  const { children, value, index, ...other } = props;
  return (
    <div role="tabpanel" hidden={value !== index} {...other}>
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
};

const Shop: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [items, setItems] = useState<ShopItem[]>([]);
  const [purchases, setPurchases] = useState<Purchase[]>([]);
  const [error, setError] = useState<string>('');
  const [success, setSuccess] = useState<string>('');

  const loadShopItems = async () => {
    try {
      const data = await getShopItems();
      setItems(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load shop items');
    }
  };

  const loadPurchases = async () => {
    try {
      const data = await getUserPurchases();
      setPurchases(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load purchases');
    }
  };

  useEffect(() => {
    loadShopItems();
    loadPurchases();
  }, []);

  const handleBuy = async (itemId: number) => {
    try {
      const response = await buyItem(itemId);
      setSuccess(`Successfully purchased item! Content: ${response.item_content}`);
      loadPurchases();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to buy item');
    }
  };

  const handleSell = async (purchaseId: number) => {
    try {
      const response = await sellItem(purchaseId);
      setSuccess(`Successfully sold item for ${response.earned_amount} coins`);
      loadPurchases();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to sell item');
    }
  };

  return (
    <Box sx={{ width: '100%' }}>
      {error && (
        <Alert severity="error" onClose={() => setError('')} sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}
      {success && (
        <Alert severity="success" onClose={() => setSuccess('')} sx={{ mb: 2 }}>
          {success}
        </Alert>
      )}

      <Tabs value={tabValue} onChange={(_, newValue) => setTabValue(newValue)}>
        <Tab label="Shop" />
        <Tab label="My Purchases" />
      </Tabs>

      <TabPanel value={tabValue} index={0}>
        <Grid container spacing={3}>
          {items.map((item) => (
            <Grid item xs={12} sm={6} md={4} key={item.id}>
              <Card>
                <CardContent>
                  <Typography variant="h6">{item.name}</Typography>
                  <Typography color="textSecondary" gutterBottom>
                    {item.description}
                  </Typography>
                  <Typography variant="h6" color="primary">
                    {item.price.toLocaleString()} coins
                  </Typography>
                  <Button
                    variant="contained"
                    onClick={() => handleBuy(item.id)}
                    fullWidth
                    sx={{ mt: 2 }}
                  >
                    Buy
                  </Button>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </TabPanel>

      <TabPanel value={tabValue} index={1}>
        <Grid container spacing={3}>
          {purchases.map((purchase) => (
            <Grid item xs={12} sm={6} md={4} key={purchase.id}>
              <Card>
                <CardContent>
                  <Typography variant="h6">{purchase.item_name}</Typography>
                  <Typography color="textSecondary" gutterBottom>
                    {purchase.description}
                  </Typography>
                  <Typography variant="body2" sx={{ mb: 2 }}>
                    Purchased: {purchase.formatted_date}
                  </Typography>
                  <Typography 
                    variant="body1" 
                    sx={{ 
                      mb: 2, 
                      p: 2, 
                      bgcolor: 'grey.100', 
                      borderRadius: 1,
                      whiteSpace: 'pre-wrap',
                      wordBreak: 'break-word'
                    }}
                  >
                    {purchase.content}
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
          ))}
        </Grid>
      </TabPanel>
    </Box>
  );
};

export default Shop; 