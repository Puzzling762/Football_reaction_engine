import pandas as pd
import random

class MatchContextAnalyzer:
    """Analyzes match context to add narrative depth"""
    
    def __init__(self, df_big, df_season, df_player):
        self.df_big = df_big
        self.df_season = df_season
        self.df_player = df_player
        self.player_memory = {}  # Track recent performances
        
    def is_big_match(self, team_id, opponent_id):
        """Check if this is a rivalry/big matchup"""
        return ((self.df_big['teamid1'] == team_id) & (self.df_big['teamid2'] == opponent_id)).any() or \
               ((self.df_big['teamid2'] == team_id) & (self.df_big['teamid1'] == opponent_id)).any()
    
    def get_team_stats(self, team_name):
        """Get team's season statistics"""
        row = self.df_season[self.df_season['team'] == team_name]
        if not row.empty:
            return row.iloc[0].to_dict()
        return {'points': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'goals_for': 0, 'goals_against': 0}
    
    def get_team_form(self, team_name):
        """Calculate recent form (last 5 matches)"""
        team_matches = self.df_player[self.df_player['team'] == team_name].tail(5)
        if team_matches.empty:
            return "Unknown"
        
        wins = (team_matches['goals'] > 0).sum()  # Simplified
        if wins >= 4:
            return "🔥 Red Hot"
        elif wins >= 3:
            return "💪 Strong"
        elif wins >= 2:
            return "📊 Decent"
        else:
            return "😰 Struggling"
    
    def detect_performance_narrative(self, row):
        """Detect special performance narratives"""
        narratives = []
        
        # Hat-trick hero
        if row.get('goals', 0) >= 3:
            narratives.append("HAT_TRICK")
        
        # Brace
        elif row.get('goals', 0) == 2:
            narratives.append("BRACE")
        
        # High rating performance
        rating = row.get('rating', 0)
        if isinstance(rating, (int, float)):
            if rating >= 9.0:
                narratives.append("WORLD_CLASS")
            elif rating >= 8.5:
                narratives.append("EXCEPTIONAL")
            elif rating < 6.0:
                narratives.append("POOR")
        
        # Full 90 minutes
        if row.get('minsplayed', 0) >= 90:
            narratives.append("FULL_NINETY")
        
        # Man of the Match
        if row.get('MOTM', 'No') == 'Yes':
            narratives.append("MOTM")
        
        # Late sub appearance
        if 0 < row.get('minsplayed', 0) < 30:
            narratives.append("CAMEO")
        
        return narratives
    
    def get_player_context(self, player_name):
        """Get player's recent history"""
        player_matches = self.df_player[
            self.df_player['playername'] == player_name
        ].tail(3)
        
        if player_matches.empty:
            return None
        
        total_goals = player_matches['goals'].sum()
        avg_rating = player_matches['rating'].mean()
        
        return {
            'recent_goals': total_goals,
            'avg_rating': round(avg_rating, 1),
            'matches': len(player_matches)
        }
    
    def compare_with_opponent(self, team_stats, opponent_name):
        """Compare team standings"""
        opp_stats = self.get_team_stats(opponent_name)
        
        team_pts = team_stats.get('points', 0)
        opp_pts = opp_stats.get('points', 0)
        
        if team_pts > opp_pts + 10:
            return "DOMINANT_FAVORITE"
        elif team_pts > opp_pts + 5:
            return "FAVORITE"
        elif abs(team_pts - opp_pts) <= 5:
            return "EVENLY_MATCHED"
        elif opp_pts > team_pts + 5:
            return "UNDERDOG"
        else:
            return "MAJOR_UNDERDOG"
    
    def generate_context_tags(self, row, team_stats):
        """Generate rich context tags for the prompt"""
        tags = {
            'is_big_match': self.is_big_match(
                row.get('teamid', 0), 
                row.get('opponentid', 0)
            ),
            'team_form': self.get_team_form(row.get('team', '')),
            'performance_narratives': self.detect_performance_narrative(row),
            'player_context': self.get_player_context(row.get('playername', '')),
            'match_competitiveness': self.compare_with_opponent(
                team_stats, 
                row.get('opponent', '')
            ),
            'home_away': random.choice(['Home', 'Away'])  # Add if you have this data
        }
        
        return tags
    
    def build_narrative_string(self, tags):
        """Convert context tags to natural language prompt additions"""
        parts = []
        
        if tags['is_big_match']:
            parts.append("⚡ This is a BIG RIVALRY MATCH - high stakes and emotions!")
        
        parts.append(f"Team Form: {tags['team_form']}")
        
        if 'HAT_TRICK' in tags['performance_narratives']:
            parts.append("🎩 HAT-TRICK HERO!")
        elif 'BRACE' in tags['performance_narratives']:
            parts.append("⚽⚽ Two-goal performance!")
        
        if 'MOTM' in tags['performance_narratives']:
            parts.append("🌟 Man of the Match winner!")
        
        if 'WORLD_CLASS' in tags['performance_narratives']:
            parts.append("🔥 World-class rating (9.0+)")
        elif 'EXCEPTIONAL' in tags['performance_narratives']:
            parts.append("💎 Exceptional performance (8.5+)")
        
        comp = tags['match_competitiveness']
        if comp == "MAJOR_UNDERDOG":
            parts.append("😤 Major upset potential - huge underdog!")
        elif comp == "UNDERDOG":
            parts.append("🎯 Fighting as underdogs")
        
        if tags['player_context']:
            ctx = tags['player_context']
            parts.append(f"Recent form: {ctx['recent_goals']} goals in last {ctx['matches']} games")
        
        return "\n".join(parts)