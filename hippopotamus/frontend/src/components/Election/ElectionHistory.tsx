import React, { useState, useEffect } from 'react';
import { 
  Box, Typography, List, ListItem, ListItemText, 
  Divider, Paper, Alert, CircularProgress,
  Accordion, AccordionSummary, AccordionDetails,
  Chip
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import EmojiEventsIcon from '@mui/icons-material/EmojiEvents';
import getElectionHistory from '../../services/api';
import { Election } from '../../types';

const ElectionHistory: React.FC = () => {
  const [elections, setElections] = useState<Election[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const loadHistory = async () => {
      try {
        const data = await getElectionHistory('/election/history');
        setElections(data.data);
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Ошибка загрузки истории выборов');
      } finally {
        setLoading(false);
      }
    };
    loadHistory();
  }, []);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" p={3}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mb: 2 }}>
        {error}
      </Alert>
    );
  }

  return (
    <Box>
      <Typography variant="h5" gutterBottom align="center">
        История выборов
      </Typography>

      {elections.length === 0 ? (
        <Paper sx={{ p: 3, textAlign: 'center' }}>
          <Typography color="textSecondary">
            История выборов пуста
          </Typography>
        </Paper>
      ) : (
        elections.map((election, index) => (
          <Accordion key={election.id} sx={{ mb: 1 }}>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, width: '100%' }}>
                <Typography>
                  Выборы #{election.id}
                </Typography>
                {election.winner && (
                  <Chip
                    icon={<EmojiEventsIcon />}
                    label={`Победитель: ${election.winner.name}`}
                    color="primary"
                    size="small"
                  />
                )}
              </Box>
            </AccordionSummary>
            <AccordionDetails>
              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" color="textSecondary">
                  Начало: {new Date(election.election_start!).toLocaleString('ru-RU')}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Окончание: {new Date(election.election_end!).toLocaleString('ru-RU')}
                </Typography>
              </Box>
              
              <List>
                {election.candidates.map((candidate, idx) => (
                  <React.Fragment key={candidate.id}>
                    {idx > 0 && <Divider />}
                    <ListItem>
                      <ListItemText
                        primary={candidate.name}
                        secondary={`Голосов: ${candidate.votes}`}
                      />
                      {election.winner?.id === candidate.id && (
                        <Chip
                          icon={<EmojiEventsIcon />}
                          label="Победитель"
                          color="primary"
                          size="small"
                        />
                      )}
                    </ListItem>
                  </React.Fragment>
                ))}
              </List>
            </AccordionDetails>
          </Accordion>
        ))
      )}
    </Box>
  );
};

export default ElectionHistory;