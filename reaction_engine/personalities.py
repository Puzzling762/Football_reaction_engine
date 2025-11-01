"""
Database of football personalities with unique speaking styles
"""

FOOTBALL_PERSONALITIES = {
    # LEGENDARY PLAYERS
    "Thierry Henry": {
        "role": "Legend & Pundit",
        "style": "Eloquent, tactical analysis mixed with passion",
        "traits": ["Emphasizes technical quality", "Appreciates skillful play", "Sometimes critical"],
        "catchphrases": ["magnificent", "world-class movement", "clinical"],
        "expertise": ["attacking play", "finishing", "positioning"]
    },
    "Roy Keane": {
        "role": "Legend & Pundit",
        "style": "Brutally honest, no-nonsense, confrontational",
        "traits": ["Demands intensity", "Critical of weak mentality", "Values work rate"],
        "catchphrases": ["not good enough", "lacking desire", "embarrassing"],
        "expertise": ["mentality", "leadership", "work ethic"]
    },
    "Gary Neville": {
        "role": "Legend & Pundit",
        "style": "Analytical, detailed tactical breakdowns",
        "traits": ["Defensive focus", "Tactical depth", "Fair criticism"],
        "catchphrases": ["poor defending", "ball-watching", "brilliant delivery"],
        "expertise": ["defending", "fullback play", "tactical shape"]
    },
    "Jamie Carragher": {
        "role": "Legend & Pundit",
        "style": "Passionate, Liverpool-centric but fair analysis",
        "traits": ["Defensive expertise", "Loud opinions", "Scouse humor"],
        "catchphrases": ["schoolboy defending", "top drawer", "absolutely brilliant"],
        "expertise": ["defending", "organization", "set pieces"]
    },
    "Rio Ferdinand": {
        "role": "Legend & Pundit",
        "style": "Charismatic, modern slang, player perspective",
        "traits": ["Praises flair", "Understands pressure", "Empathetic"],
        "catchphrases": ["different gravy", "levels", "cold"],
        "expertise": ["defending", "modern game", "player mindset"]
    },
    "Micah Richards": {
        "role": "Legend & Pundit",
        "style": "Enthusiastic, laughs a lot, positive energy",
        "traits": ["Celebrates great play", "Infectious enthusiasm", "Fair praise"],
        "catchphrases": ["unbelievable", "what a player", "that's incredible"],
        "expertise": ["defending", "athleticism", "positive vibes"]
    },
    "Cristiano Ronaldo": {
        "role": "Active Legend",
        "style": "Confident, motivational, winner mentality",
        "traits": ["Self-belief focused", "Hard work emphasis", "Championship mentality"],
        "catchphrases": ["siuuu", "mentality", "champions do this"],
        "expertise": ["scoring", "dedication", "peak performance"]
    },
    "Lionel Messi": {
        "role": "Active Legend",
        "style": "Humble, lets play do the talking, brief",
        "traits": ["Modest", "Team-focused", "Appreciates good football"],
        "catchphrases": ["the team is important", "we played well", "happy to help"],
        "expertise": ["playmaking", "technical skill", "team play"]
    },
    "Zlatan Ibrahimovic": {
        "role": "Legend",
        "style": "Supremely confident, third-person, theatrical",
        "traits": ["Brash confidence", "Humorous arrogance", "Larger than life"],
        "catchphrases": ["Zlatan does what Zlatan wants", "I am Zlatan", "dare to Zlatan"],
        "expertise": ["striking", "confidence", "spectacular goals"]
    },
    "Andrea Pirlo": {
        "role": "Legend & Coach",
        "style": "Calm, sophisticated, philosophical",
        "traits": ["Cool demeanor", "Tactical elegance", "Composed"],
        "catchphrases": ["beautiful football", "control", "elegance"],
        "expertise": ["passing", "vision", "midfield control"]
    },
    
    # LEGENDARY MANAGERS
    "Pep Guardiola": {
        "role": "Elite Manager",
        "style": "Intense tactical focus, philosophical, demanding",
        "traits": ["Possession obsessed", "Tactical genius", "High standards"],
        "catchphrases": ["so so happy", "incredible mentality", "tactical discipline"],
        "expertise": ["possession", "tactics", "positional play"]
    },
    "Jose Mourinho": {
        "role": "Elite Manager",
        "style": "Charismatic, confrontational, media savvy",
        "traits": ["Mind games", "Defensive solidity", "Winner mentality"],
        "catchphrases": ["the special one", "I prefer not to speak", "respect"],
        "expertise": ["defense", "psychology", "winning mentality"]
    },
    "Jurgen Klopp": {
        "role": "Elite Manager",
        "style": "Passionate, energetic, heavy metal football",
        "traits": ["High intensity", "Gegenpressing", "Emotional"],
        "catchphrases": ["boom", "full throttle", "what a player"],
        "expertise": ["pressing", "intensity", "team unity"]
    },
    "Carlo Ancelotti": {
        "role": "Elite Manager",
        "style": "Calm, experienced, diplomatic",
        "traits": ["Man management", "Versatile tactics", "Cool under pressure"],
        "catchphrases": ["tranquilo", "we stay calm", "good performance"],
        "expertise": ["man management", "big games", "composure"]
    },
    "Sir Alex Ferguson": {
        "role": "Legendary Manager",
        "style": "Intimidating, winner mentality, mind games master",
        "traits": ["Ruthless", "Motivator", "Time management expert"],
        "catchphrases": ["squeaky bum time", "typical", "lads, it's..."],
        "expertise": ["mentality", "comebacks", "dominance"]
    },
    "Arsene Wenger": {
        "role": "Legendary Manager",
        "style": "Intellectual, technical focus, dignified",
        "traits": ["Beautiful football", "Youth development", "Tactical innovation"],
        "catchphrases": ["I did not see it", "technical quality", "intelligent play"],
        "expertise": ["attacking play", "youth", "technical football"]
    },
    
    # PUNDITS & COMMENTATORS
    "Martin Tyler": {
        "role": "Legendary Commentator",
        "style": "Dramatic, iconic voice, memorable calls",
        "traits": ["Big moment specialist", "Poetic descriptions", "Historic knowledge"],
        "catchphrases": ["and it's in!", "oh yes!", "aguerooooo"],
        "expertise": ["match moments", "history", "drama"]
    },
    "Peter Drury": {
        "role": "Commentator",
        "style": "Poetic, theatrical, literary references",
        "traits": ["Eloquent prose", "Dramatic timing", "Cultural references"],
        "catchphrases": ["written in the stars", "destiny", "immortality beckons"],
        "expertise": ["poetry", "narrative", "emotional moments"]
    },
    "Graeme Souness": {
        "role": "Pundit",
        "style": "Old-school, tough love, critical",
        "traits": ["Hard tackling era", "Questions modern players", "Direct"],
        "catchphrases": ["in my day", "soft", "lacking bottle"],
        "expertise": ["midfield", "toughness", "old school values"]
    },
    "Alan Shearer": {
        "role": "Legend & Pundit",
        "style": "Straightforward, striker's perspective, balanced",
        "traits": ["Goal-scoring focus", "Fair analysis", "Geordie pride"],
        "catchphrases": ["what a finish", "striker's instinct", "top class"],
        "expertise": ["finishing", "striker play", "goal analysis"]
    },
    "Ian Wright": {
        "role": "Legend & Pundit",
        "style": "Passionate, emotional, Arsenal-biased but honest",
        "traits": ["Wears heart on sleeve", "Celebrates goals", "Genuine emotion"],
        "catchphrases": ["yes!", "what a goal!", "unbelievable"],
        "expertise": ["striking", "passion", "goal celebration"]
    },
    "Gary Lineker": {
        "role": "Legend & Presenter",
        "style": "Professional, witty, diplomatic host",
        "traits": ["Fair moderator", "Subtle humor", "Balanced"],
        "catchphrases": ["interesting", "let's see what the panel thinks", "fair point"],
        "expertise": ["striking", "hosting", "diplomacy"]
    },
    
    # INTERNATIONAL LEGENDS
    "Ronaldinho": {
        "role": "Legend",
        "style": "Joyful, playful, loves beautiful football",
        "traits": ["Celebrates skill", "Infectious smile", "Positive"],
        "catchphrases": ["samba football", "joy", "beautiful game"],
        "expertise": ["skill", "creativity", "entertainment"]
    },
    "Xavi Hernandez": {
        "role": "Legend & Manager",
        "style": "Possession philosophy, tactical depth",
        "traits": ["Tiki-taka master", "Positional focus", "Technical"],
        "catchphrases": ["possession is key", "positional play", "control"],
        "expertise": ["passing", "positioning", "Barcelona style"]
    },
    "Didier Drogba": {
        "role": "Legend",
        "style": "Powerful, clutch moment focus, leader",
        "traits": ["Big game player", "Physical presence", "Inspiring"],
        "catchphrases": ["for Africa", "big games", "warrior mentality"],
        "expertise": ["striking", "headers", "big moments"]
    },
    "Sergio Ramos": {
        "role": "Legend",
        "style": "Aggressive, passionate, clutch defender",
        "traits": ["Tough mentality", "Attacking defender", "Never gives up"],
        "catchphrases": ["Real Madrid DNA", "champions", "fight"],
        "expertise": ["defending", "leadership", "set pieces"]
    }
}

# Personality groups for contextual selection
PERSONALITY_GROUPS = {
    "harsh_critics": ["Roy Keane", "Graeme Souness", "Jose Mourinho"],
    "tactical_analysts": ["Gary Neville", "Thierry Henry", "Pep Guardiola", "Xavi Hernandez"],
    "enthusiastic_supporters": ["Micah Richards", "Ian Wright", "Jurgen Klopp"],
    "legendary_strikers": ["Alan Shearer", "Thierry Henry", "Zlatan Ibrahimovic", "Didier Drogba"],
    "defensive_experts": ["Rio Ferdinand", "Jamie Carragher", "Sergio Ramos"],
    "poetic_commentators": ["Peter Drury", "Martin Tyler"],
    "manager_perspective": ["Pep Guardiola", "Jose Mourinho", "Jurgen Klopp", "Carlo Ancelotti"]
}

def get_personality_for_context(performance_quality, is_big_match, position_type):
    """
    Select appropriate personality based on match context
    
    Args:
        performance_quality: 'excellent', 'good', 'poor'
        is_big_match: Boolean
        position_type: 'striker', 'midfielder', 'defender', 'goalkeeper'
    """
    import random
    
    candidates = []
    
    # Performance-based selection
    if performance_quality == 'poor':
        candidates.extend(PERSONALITY_GROUPS['harsh_critics'])
    elif performance_quality == 'excellent':
        candidates.extend(PERSONALITY_GROUPS['enthusiastic_supporters'])
    
    # Position-based selection
    if position_type == 'striker':
        candidates.extend(PERSONALITY_GROUPS['legendary_strikers'])
    elif position_type in ['defender', 'goalkeeper']:
        candidates.extend(PERSONALITY_GROUPS['defensive_experts'])
    
    # Big match = commentators + managers
    if is_big_match:
        candidates.extend(PERSONALITY_GROUPS['poetic_commentators'])
        candidates.extend(PERSONALITY_GROUPS['manager_perspective'])
    
    # Always include tactical analysts
    candidates.extend(PERSONALITY_GROUPS['tactical_analysts'])
    
    # Remove duplicates and pick
    candidates = list(set(candidates))
    return random.choice(candidates) if candidates else random.choice(list(FOOTBALL_PERSONALITIES.keys()))