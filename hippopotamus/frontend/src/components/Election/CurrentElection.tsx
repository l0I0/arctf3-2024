import React, { useState, useEffect } from 'react';
import { 
  Box, Typography, Button, TextField, List, ListItem, 
  ListItemText, Divider, Paper, Alert, CircularProgress,
  ListItemSecondaryAction, Chip
} from '@mui/material';
import HowToVoteIcon from '@mui/icons-material/HowToVote';
import PersonAddIcon from '@mui/icons-material/PersonAdd';
import { getCurrentElection, nominateCandidate, voteForCandidate } from '../../services/api';
import { Election } from '../../types';

const ELECTION_RULES = {
  nominationCost: 200000,
  minVotesToWin: 10,
  restrictions: [
    'Только верифицированные пользователи могут голосовать',
    'Нельзя голосовать за себя',
    'Можно голосовать только один раз за выборы',
    'Для победы нужно набрать минимум 10 голосов'
  ]
};

const CurrentElection: React.FC = () => {
  const [election, setElection] = useState<Election | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');
  const [candidateName, setCandidateName] = useState('');

  const loadElection = async () => {
    try {
      const data = await getCurrentElection();
      setElection(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка загрузки данных о выборах');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadElection();
    const interval = setInterval(loadElection, 10000);
    return () => clearInterval(interval);
  }, []);

  const handleNominate = async () => {
    try {
      await nominateCandidate(candidateName);
      setMessage('Кандидат успешно выдвинут');
      setCandidateName('');
      loadElection();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка при выдвижении кандидата');
    }
  };

  const handleVote = async (candidateId: number) => {
    try {
      await voteForCandidate(candidateId);
      setMessage('Ваш голос успешно учтен');
      loadElection();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка при голосовании');
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" p={3}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      {(message || error) && (
        <Alert 
          severity={error ? "error" : "success"}
          onClose={() => { setMessage(''); setError(''); }}
          sx={{ mb: 2 }}
        >
          {error || message}
        </Alert>
      )}

      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Правила выборов
        </Typography>
        <Typography variant="body2" paragraph>
          Стоимость выдвижения: {ELECTION_RULES.nominationCost.toLocaleString('ru-RU')} монет
        </Typography>
        <Typography variant="subtitle2" gutterBottom>
          Основные правила:
        </Typography>
        <List dense>
          {ELECTION_RULES.restrictions.map((rule, index) => (
            <ListItem key={index}>
              <ListItemText primary={`• ${rule}`} />
            </ListItem>
          ))}
        </List>
      </Paper>

      {election ? (
        <>
          <Box sx={{ mb: 4, textAlign: 'center' }}>
            <Typography variant="h5" gutterBottom>
              Текущие выборы
            </Typography>
            <Chip 
              label={`Окончание: ${new Date(election.election_end!).toLocaleString('ru-RU')}`}
              color="primary"
              sx={{ mt: 1 }}
            />
          </Box>

          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Выдвижение кандидата
            </Typography>
            <Box sx={{ display: 'flex', gap: 2, alignItems: 'flex-start' }}>
              <TextField
                fullWidth
                label="Имя кандидата"
                value={candidateName}
                onChange={(e) => setCandidateName(e.target.value)}
                size="small"
              />
              <Button 
                variant="contained" 
                onClick={handleNominate}
                disabled={!candidateName}
                startIcon={<PersonAddIcon />}
              >
                Выдвинуть
              </Button>
            </Box>
          </Paper>

          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Кандидаты
            </Typography>
            <List>
              {election.candidates.map((candidate, index) => (
                <React.Fragment key={candidate.id}>
                  {index > 0 && <Divider />}
                  <ListItem>
                    <ListItemText 
                      primary={candidate.name}
                      secondary={`Голосов: ${candidate.votes}`}
                    />
                    <ListItemSecondaryAction>
                      <Button
                        variant="outlined"
                        onClick={() => handleVote(candidate.id)}
                        startIcon={<HowToVoteIcon />}
                        size="small"
                      >
                        Голосовать
                      </Button>
                    </ListItemSecondaryAction>
                  </ListItem>
                </React.Fragment>
              ))}
              {election.candidates.length === 0 && (
                <ListItem>
                  <ListItemText 
                    primary="Пока нет кандидатов"
                    secondary="Станьте первым кандидатом!"
                  />
                </ListItem>
              )}
            </List>
          </Paper>
        </>
      ) : (
        <Paper sx={{ p: 3, textAlign: 'center' }}>
          <Typography variant="h6" color="textSecondary">
            В данный момент нет активных выборов
          </Typography>
        </Paper>
      )}
    </Box>
  );
};

export default CurrentElection;