import random
from personalities import FOOTBALL_PERSONALITIES, get_personality_for_context, PERSONALITY_GROUPS

class PersonalityReactor:
    """Generates reactions from different football personalities"""
    
    def __init__(self, llm_client):
        self.llm = llm_client
        self.used_personalities = []  # Prevent immediate repetition
        
    def select_personalities(self, row, context_tags, num_personalities=3):
        """
        Select diverse personalities for this match
        
        Returns list of personality names
        """
        performance_quality = self._assess_performance(row)
        is_big_match = context_tags.get('is_big_match', False)
        position = self._guess_position(row)
        
        selected = []
        available = list(FOOTBALL_PERSONALITIES.keys())
        
        # Remove recently used to increase variety
        if len(self.used_personalities) > 10:
            self.used_personalities = self.used_personalities[-10:]
        
        for personality in self.used_personalities[-3:]:
            if personality in available:
                available.remove(personality)
        
        # Get context-appropriate personality
        primary = get_personality_for_context(performance_quality, is_big_match, position)
        if primary in available:
            selected.append(primary)
            available.remove(primary)
        
        # Add contrasting personality (if primary is harsh, add enthusiastic)
        if primary in PERSONALITY_GROUPS['harsh_critics']:
            contrasting = random.choice(PERSONALITY_GROUPS['enthusiastic_supporters'])
            if contrasting in available and contrasting not in selected:
                selected.append(contrasting)
                available.remove(contrasting)
        
        # Fill remaining slots with variety
        while len(selected) < num_personalities and available:
            choice = random.choice(available)
            selected.append(choice)
            available.remove(choice)
        
        # Remember these
        self.used_personalities.extend(selected)
        
        return selected
    
    def generate_personality_reaction(self, personality_name, row, context_tags, context_narrative):
        """Generate reaction from specific personality's perspective"""
        
        personality = FOOTBALL_PERSONALITIES[personality_name]
        
        player = row.get('playername', 'Unknown Player')
        team = row.get('team', 'Unknown Team')
        opponent = row.get('opponent', 'Unknown Opponent')
        goals = row.get('goals', 0)
        rating = row.get('rating', 'N/A')
        mins = row.get('minsplayed', 0)
        
        # Build personality-specific prompt
        prompt = f"""You are {personality_name}, the {personality['role']}.

YOUR CHARACTER TRAITS:
- Speaking Style: {personality['style']}
- Key Traits: {', '.join(personality['traits'])}
- Expertise: {', '.join(personality['expertise'])}
- Common Phrases (use sparingly and naturally): {', '.join(personality['catchphrases'][:2])}

MATCH PERFORMANCE TO ANALYZE:
Player: {player}
Team: {team} vs {opponent}
Goals: {goals}
Rating: {rating}/10
Minutes: {mins}

MATCH CONTEXT:
{context_narrative}

YOUR TASK:
React to {player}'s performance in YOUR authentic voice. Stay true to your personality:
- Use YOUR typical speaking patterns
- Reference YOUR areas of expertise
- Show YOUR characteristic attitude (critical/supportive/analytical)
- Keep it 2-4 sentences
- Sound EXACTLY like the real {personality_name} would

CRITICAL: Do NOT use generic commentary. This must sound like YOU specifically. What would {personality_name} actually say about this?"""

        return self.llm.generate_reaction(prompt, temperature=0.88)
    
    def generate_multi_personality_panel(self, row, context_tags, context_narrative, num_personalities=3):
        """
        Generate a panel discussion with multiple personalities
        
        Returns dict with personality names as keys
        """
        personalities = self.select_personalities(row, context_tags, num_personalities)
        
        reactions = {}
        player = row.get('playername', 'Unknown Player')
        
        print(f"   🎙️ Panel: {', '.join(personalities)}")
        
        for personality in personalities:
            reaction = self.generate_personality_reaction(
                personality, row, context_tags, context_narrative
            )
            reactions[personality] = reaction
        
        return reactions
    
    def generate_coach_reaction(self, row, context_tags, is_own_team=True):
        """Generate reaction from a manager's perspective"""
        
        # Select a manager
        managers = [p for p, data in FOOTBALL_PERSONALITIES.items() 
                   if 'Manager' in data['role'] or 'Coach' in data['role']]
        manager = random.choice(managers)
        
        personality = FOOTBALL_PERSONALITIES[manager]
        player = row.get('playername', 'Unknown Player')
        rating = row.get('rating', 'N/A')
        
        perspective = "your player" if is_own_team else "the opposition player"
        
        prompt = f"""You are {manager}, speaking in your post-match press conference.

You're being asked about {player}'s performance ({rating}/10 rating).
This is {perspective}.

Respond in YOUR authentic managerial style:
- {personality['style']}
- Traits: {', '.join(personality['traits'])}

Keep it brief (2-3 sentences), authentic to YOUR character, and appropriate for a press conference."""

        return {
            'manager': manager,
            'reaction': self.llm.generate_reaction(prompt, temperature=0.80)
        }
    
    def generate_player_reaction(self, row, context_tags, reaction_type='teammate'):
        """
        Generate reaction from another player's perspective
        
        reaction_type: 'teammate', 'opponent', 'legend'
        """
        # Filter active players vs legends
        if reaction_type == 'legend':
            players = ['Thierry Henry', 'Ronaldinho', 'Zlatan Ibrahimovic', 
                      'Andrea Pirlo', 'Xavi Hernandez', 'Didier Drogba']
        else:
            players = ['Cristiano Ronaldo', 'Lionel Messi', 'Sergio Ramos']
        
        reactor = random.choice(players)
        personality = FOOTBALL_PERSONALITIES[reactor]
        
        player = row.get('playername', 'Unknown Player')
        goals = row.get('goals', 0)
        rating = row.get('rating', 'N/A')
        
        relationship = {
            'teammate': 'playing alongside',
            'opponent': 'playing against',
            'legend': 'watching from retirement'
        }[reaction_type]
        
        prompt = f"""You are {reactor}, {relationship} {player}.

Their performance today: {goals} goals, {rating}/10 rating

React in YOUR authentic voice as {reactor}:
- Style: {personality['style']}
- Traits: {', '.join(personality['traits'])}

1-2 sentences maximum. Sound exactly like {reactor} would."""

        return {
            'reactor': reactor,
            'relationship': reaction_type,
            'reaction': self.llm.generate_reaction(prompt, temperature=0.85)
        }
    
    def _assess_performance(self, row):
        """Assess performance quality"""
        rating = row.get('rating', 0)
        if isinstance(rating, (int, float)):
            if rating >= 8.0:
                return 'excellent'
            elif rating >= 6.5:
                return 'good'
            else:
                return 'poor'
        return 'good'
    
    def _guess_position(self, row):
        """Guess position from goals scored (rough heuristic)"""
        goals = row.get('goals', 0)
        if goals >= 2:
            return 'striker'
        # Could enhance this with actual position data
        return random.choice(['midfielder', 'defender', 'striker'])
    
    def generate_full_reaction_package(self, row, context_tags, context_narrative):
        """
        Generate complete reaction package:
        - 3 pundit/legend reactions
        - 1 manager reaction
        - 1 player reaction
        """
        package = {
            'pundits': self.generate_multi_personality_panel(
                row, context_tags, context_narrative, num_personalities=3
            ),
            'manager': self.generate_coach_reaction(row, context_tags, is_own_team=True),
            'player': self.generate_player_reaction(row, context_tags, reaction_type='teammate')
        }
        
        return package