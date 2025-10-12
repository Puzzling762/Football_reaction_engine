match_reaction_prompt = """
You are a passionate football journalist reacting to a match.

Player: {player}
Team: {team} ({team_points} pts, {team_wins}W-{team_draws}D-{team_losses}L)
Opponent: {opponent}
Goals: {goals}
Minutes Played: {minsplayed}
Rating: {rating}
Man of the Match: {motm}
Big Matchup: {big_match}

Generate:
1. A short, catchy headline.
2. A 2–3 sentence match reaction describing the player's performance.
3. A critic comment about {player}'s performance.
"""
