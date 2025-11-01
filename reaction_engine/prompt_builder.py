import random

class DynamicPromptBuilder:
    """Builds varied, context-rich prompts for LLM"""
    
    def __init__(self):
        self.emotion_modifiers = [
            "passionate", "analytical", "excited", "dramatic", 
            "balanced", "enthusiastic", "critical", "celebratory"
        ]
        
        self.focus_areas = [
            "the player's overall impact",
            "key moments and decisive plays",
            "technical ability and decision-making",
            "work rate and positioning",
            "clutch performance under pressure"
        ]
    
    def build_enriched_prompt(self, row, team_stats, context_tags, context_narrative):
        """Build a rich, varied prompt with full context"""
        
        # Random emotional modifier for variety
        tone_modifier = random.choice(self.emotion_modifiers)
        focus = random.choice(self.focus_areas)
        
        # Base player/match info
        player = row.get('playername', 'Unknown Player')
        team = row.get('team', 'Unknown Team')
        opponent = row.get('opponent', 'Unknown Opponent')
        goals = row.get('goals', 0)
        mins = row.get('minsplayed', 0)
        rating = row.get('rating', 'N/A')
        
        # Team standing
        team_record = f"{team_stats.get('wins', 0)}W-{team_stats.get('draws', 0)}D-{team_stats.get('losses', 0)}L"
        team_pts = team_stats.get('points', 0)
        
        # Build comprehensive prompt
        prompt = f"""You are a {tone_modifier} football journalist covering this match performance.

🎯 MATCH DETAILS:
Player: {player}
Team: {team} ({team_pts} points, {team_record})
Opponent: {opponent}
Goals Scored: {goals}
Minutes Played: {mins}
Match Rating: {rating}/10

📊 CONTEXT & NARRATIVE:
{context_narrative}

🎨 YOUR TASK:
Focus on {focus}. Be authentic and varied - never use clichéd phrases like "clinical finish" or "exceptional display" unless truly warranted. 

Generate a natural, flowing reaction that captures the essence of this performance. Make it feel real and spontaneous, like you're genuinely excited or analytical about what you witnessed.

IMPORTANT: 
- Vary your vocabulary every time
- Use specific details from the stats
- Don't overuse adjectives
- Sound like a real human, not a template
- If the performance was average, say so honestly
"""
        
        return prompt
    
    def build_comparative_prompt(self, row, team_stats, context_tags, recent_performances):
        """Build prompt that compares to recent form"""
        
        player = row.get('playername', 'Unknown Player')
        current_rating = row.get('rating', 0)
        current_goals = row.get('goals', 0)
        
        prompt = f"""Compare {player}'s performance today to recent matches:

TODAY'S PERFORMANCE:
- Rating: {current_rating}/10
- Goals: {current_goals}
- Minutes: {row.get('minsplayed', 0)}

CONTEXT:
{context_tags}

Generate a reaction that acknowledges their recent form trajectory. Is this a return to form? A continuation of great play? A dip? Be specific and honest."""

        return prompt
    
    def build_headline_prompt(self, row, context_tags):
        """Generate just a punchy headline"""
        
        player = row.get('playername', 'Unknown Player')
        goals = row.get('goals', 0)
        
        narratives = context_tags.get('performance_narratives', [])
        
        prompt = f"""Generate ONE creative headline (10 words max) for {player}'s performance:
- Goals: {goals}
- Key narratives: {', '.join(narratives) if narratives else 'Standard performance'}

Make it catchy, not clichéd. Be creative with wordplay if appropriate."""
        
        return prompt
    
    def build_critic_prompt(self, row, team_stats):
        """Build critical analysis prompt"""
        
        player = row.get('playername', 'Unknown Player')
        rating = row.get('rating', 0)
        
        tone = "critical but fair" if rating < 7 else "balanced"
        
        prompt = f"""As a {tone} football analyst, provide a brief critical assessment of {player}'s performance:

Rating: {rating}/10
Goals: {row.get('goals', 0)}
Minutes: {row.get('minsplayed', 0)}

What did they do well? What could be improved? Be honest and insightful (2-3 sentences)."""
        
        return prompt
    
    def randomize_prompt_style(self):
        """Return random style variations"""
        styles = [
            "Tell me about this performance as if you're a passionate commentator",
            "Write a match report focusing on",
            "Give me your hot take on",
            "Break down this performance analytically",
            "React to this match performance with genuine emotion"
        ]
        return random.choice(styles)