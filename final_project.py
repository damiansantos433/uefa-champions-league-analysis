import pandas as pd

# 1. LOAD DATA
df = pd.read_csv("UEFA Champions League 2004-2021.csv.xls")

# 2. BASIC CLEANING
df["homeScore"] = pd.to_numeric(df["homeScore"], errors="coerce")
df["awayscore"] = pd.to_numeric(df["awayscore"], errors="coerce")

# 3. DERIVED COLUMNS AT MATCH LEVEL
df["goal_differential"] = df["homeScore"] - df["awayscore"]
df["total_goals"] = df["homeScore"] + df["awayscore"]

df["home_win"] = (df["goal_differential"] > 0).astype(int)
df["away_win"] = (df["goal_differential"] < 0).astype(int)

# 4. TEAM-LEVEL STATS (BOTH HOME + AWAY)

# wins
home_wins = df.groupby("homeTeam")["home_win"].sum()
away_wins = df.groupby("awayteam")["away_win"].sum()
wins = home_wins.add(away_wins, fill_value=0)

# goals scored
goals_scored_home = df.groupby("homeTeam")["homeScore"].sum()
goals_scored_away = df.groupby("awayteam")["awayscore"].sum()
goals_scored = goals_scored_home.add(goals_scored_away, fill_value=0)

# goals conceded
goals_conceded_home = df.groupby("homeTeam")["awayscore"].sum()
goals_conceded_away = df.groupby("awayteam")["homeScore"].sum()
goals_conceded = goals_conceded_home.add(goals_conceded_away, fill_value=0)

# goal difference (team level)
goal_difference = goals_scored - goals_conceded

# put everything into one table
team_stats = pd.DataFrame({
    "wins": wins,
    "goals_scored": goals_scored,
    "goals_conceded": goals_conceded,
    "goal_difference": goal_difference
}).sort_values(by="wins", ascending=False)

# 5. TOP / BOTTOM TEAMS

top_5 = team_stats.head(5)
bottom_5 = team_stats.tail(5)

top_scorers = team_stats.sort_values("goals_scored", ascending=False).head(5)
worst_defense = team_stats.sort_values("goals_conceded", ascending=False).head(5)

# 6. CORRELATION: HOW SCORING RELATES TO WINNING
corr = team_stats[["wins", "goals_scored", "goals_conceded", "goal_difference"]].corr()

print("TOP 5 TEAMS BY WINS")
print(top_5)
print()

print("BOTTOM 5 TEAMS BY WINS")
print(bottom_5)
print()

print("TOP 5 TEAMS BY GOALS SCORED")
print(top_scorers)
print()

print("TOP 5 TEAMS BY GOALS CONCEDED (WORST DEFENSE)")
print(worst_defense)
print()

print("CORRELATION BETWEEN WINS AND SCORING FACTORS")
print(corr)


# Finding the country where the teams win the most

team_to_country = {
    # Spain
    "Barcelona": "Spain",
    "Real Madrid": "Spain",
    "Atlético Madrid": "Spain",
    "Sevilla": "Spain",
    "Valencia": "Spain",
    "Villarreal": "Spain",

    # England
    "Manchester United": "England",
    "Chelsea": "England",
    "Arsenal": "England",
    "Liverpool": "England",
    "Manchester City": "England",
    "Tottenham Hotspur": "England",
    "Leicester City": "England",

    # Germany
    "Bayern München": "Germany",
    "Borussia Dortmund": "Germany",
    "Bayer Leverkusen": "Germany",
    "Schalke 04": "Germany",
    "VfL Wolfsburg": "Germany",

    # Italy
    "Juventus": "Italy",
    "Inter": "Italy",
    "Milan": "Italy",
    "Roma": "Italy",
    "Napoli": "Italy",
    "Lazio": "Italy",

    # France
    "Paris Saint-Germain": "France",
    "Olympique Lyonnais": "France",
    "AS Monaco": "France",
    "Marseille": "France",

    # Portugal
    "FC Porto": "Portugal",
    "SL Benfica": "Portugal",
    "Sporting CP": "Portugal",

    # Netherlands
    "Ajax": "Netherlands",
    "PSV Eindhoven": "Netherlands",
    "Feyenoord": "Netherlands",

    # Ukraine
    "Shakhtar Donetsk": "Ukraine",
    "Dynamo Kyiv": "Ukraine",

    # Russia
    "Zenit": "Russia",
    "CSKA Moskva": "Russia",

    # Turkey
    "Galatasaray": "Turkey",
    "Fenerbahçe": "Turkey",
    "Beşiktaş": "Turkey",

    # Belgium
    "Club Brugge": "Belgium",
    "Anderlecht": "Belgium",

    # Scotland
    "Celtic": "Scotland",
    "Rangers": "Scotland",

    # Switzerland
    "Basel": "Switzerland",
    "Young Boys": "Switzerland",

    # Greece
    "Olympiacos": "Greece",
    "Panathinaikos": "Greece",

    # Denmark
    "FC København": "Denmark",

    # Others 
    "Rosenborg": "Norway",
    "Malmö FF": "Sweden",
}


team_stats_with_country = team_stats.copy()
team_stats_with_country["country"] = team_stats_with_country.index.map(team_to_country)

# Removing teams not in dictionary
team_stats_with_country = team_stats_with_country.dropna(subset=["country"])


wins_by_country = (
    team_stats_with_country
    .groupby("country")["wins"]
    .sum()
    .sort_values(ascending=False)
)

print("WINS BY COUNTRY:")
print(wins_by_country)
print()

# Country with most wins
country_most_wins = wins_by_country.idxmax()
max_wins = wins_by_country.max()

print(f"Country with the most wins: {country_most_wins} ({max_wins} wins)")
