from datetime import timedelta

# Интервал выборов в минутах
ELECTION_INTERVAL_MINUTES = 15

# Вспомогательные функции для работы с интервалом
ELECTION_INTERVAL = timedelta(minutes=ELECTION_INTERVAL_MINUTES)
ELECTIONS_PER_DAY = 24 * 60 // ELECTION_INTERVAL_MINUTES 