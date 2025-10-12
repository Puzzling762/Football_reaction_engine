import pandas as pd
import os
from prompt_templates import match_reaction_prompt
from text_generator import generate_text

# Paths
BASE_DIR = r"D:\Projects\Fifa15_AI\exported_data"
BIGMATCHUPS_CSV = os.path.join(BASE_DIR, "bigmatchups.csv")
SEASONSTATS_CSV = os.path.join(BASE_DIR, "seasonstats.csv")
PLAYERMATCH_CSV = os.path.join(BASE_DIR, "playermatchratinghistory.csv")

OUTPUT_DIR = r"D:\Projects\Fifa15_AI\reaction_engine\outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUT_FILE = os.path.join(OUTPUT_DIR, "reactions.txt")

# Clear previous output
open(OUT_FILE, "w").close()

# Read CSVs
df_big = pd.read_csv(BIGMATCHUPS_CSV)
df_season = pd.read_csv(SEASONSTATS_CSV)
df_player = pd.read_csv(PLAYERMATCH_CSV)

# Helper: check if match is a big matchup
def is_big_match(team_id, opponent_id):
    return ((df_big['teamid1'] == team_id) & (df_big['teamid2'] == opponent_id)).any() or \
           ((df_big['teamid2'] == team_id) & (df_big['teamid1'] == opponent_id)).any()

# Helper: get team season stats
def get_team_stats(team_name):
    row = df_season[df_season['team'] == team_name]
    if not row.empty:
        return row.iloc[0].to_dict()
    return {}

# Generate reactions for each player
for _, row in df_player.iterrows():
    # Extract team stats
    team_stats = get_team_stats(row.get('team', 'Unknown'))
    big_match = "Yes" if is_big_match(row.get('teamid', 0), row.get('opponentid', 0)) else "No"

    prompt = match_reaction_prompt.format(
        player=row.get('playername', 'Unknown Player'),
        team=row.get('team', 'Unknown Team'),
        team_points=team_stats.get('points', 0),
        team_wins=team_stats.get('wins', 0),
        team_draws=team_stats.get('draws', 0),
        team_losses=team_stats.get('losses', 0),
        opponent=row.get('opponent', 'Unknown Opponent'),
        goals=row.get('goals', 0),
        minsplayed=row.get('minsplayed', 0),
        rating=row.get('rating', 'N/A'),
        motm=row.get('MOTM', 'No'),
        big_match=big_match
    )

    # Generate mock reaction
    reaction = generate_text(prompt)

    # Append to output file
    with open(OUT_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n=== {row.get('playername', 'Unknown Player')} ===\n")
        f.write(reaction + "\n")

print(f"✅ Reactions generated: {OUT_FILE}")
