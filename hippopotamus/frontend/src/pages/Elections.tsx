import React, { useState } from 'react';
import { Box, Tabs, Tab, Container, Paper } from '@mui/material';
import CurrentElection from '../components/Election/CurrentElection';
import ElectionHistory from '../components/Election/ElectionHistory';

const Elections: React.FC = () => {
  const [tab, setTab] = useState(0);

  return (
    <Container maxWidth="lg">
      <Paper sx={{ mt: 3, p: 2 }}>
        <Tabs 
          value={tab} 
          onChange={(_, newValue) => setTab(newValue)}
          sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}
          centered
        >
          <Tab label="Текущие выборы" />
          <Tab label="История выборов" />
        </Tabs>

        <Box sx={{ p: 2 }}>
          {tab === 0 && <CurrentElection />}
          {tab === 1 && <ElectionHistory />}
        </Box>
      </Paper>
    </Container>
  );
};

export default Elections; 