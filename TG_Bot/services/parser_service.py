import pandas as pd
import random
from datetime import datetime, timedelta
class BetBoomService:
    def __init__(self):
        self._matches = pd.DataFrame()
        self._last_update = None
        self.language = "ru"
        self.ru_teams = ["Спартак", "Зенит", "ЦСКА", "Краснодар", "Локомотив"]
        self.en_teams = ["Spartak", "Zenit", "CSKA", "Krasnodar", "Lokomotiv"]
    def _generate_matches(self):
        teams = self.ru_teams if self.language == "ru" else self.en_teams
        matches = []
        for _ in range(25):
            team1, team2 = random.sample(teams, 2)
            matches.append({
                'team1': team1,
                'team2': team2,
                'coeff_win1': round(random.uniform(1.5, 3.5), 2),
                'coeff_draw': round(random.uniform(2.0, 4.0), 2),
                'coeff_win2': round(random.uniform(1.5, 3.5), 2),
                'betboom_url': f"https://betboom.ru/search?q={team1}+{team2}"
            })
        return pd.DataFrame(matches)
    def get_cached_matches(self):
        if self._matches.empty or (datetime.now() - self._last_update) > timedelta(minutes=5):
            self._matches = self._generate_matches()
            self._last_update = datetime.now()
        return self._matches
    def get_recommendations(self):
        df = self.get_cached_matches()
        return df.nlargest(3, 'coeff_win1').copy()
    def search_teams(self, search_query: str):
        df = self.get_cached_matches()
        if df.empty:
            return pd.DataFrame()
        search_query = search_query.lower()
        mask = (df['team1'].str.lower().str.contains(search_query)) | \
               (df['team2'].str.lower().str.contains(search_query))
        return df[mask].copy()
    def switch_language(self):
        self.language = "en" if self.language == "ru" else "ru"
        self._matches = pd.DataFrame()