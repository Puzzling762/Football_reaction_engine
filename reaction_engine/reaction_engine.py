import sys
from pathlib import Path
import pandas as pd
import json
import time
from datetime import datetime
from config import *
from llm_client import LLMClient
from context_analyzer import MatchContextAnalyzer
from prompt_builder import DynamicPromptBuilder
from personality_reactor import PersonalityReactor

class ReactionEngine:
    """Main reaction generation engine with personality reactions"""
    
    def __init__(self):
        print("🚀 Initializing Enhanced Reaction Engine...")
        
        # Load data
        self.df_big = pd.read_csv(BIGMATCHUPS_CSV)
        self.df_season = pd.read_csv(SEASONSTATS_CSV)
        self.df_player = pd.read_csv(PLAYERMATCH_CSV)
        
        # Initialize components
        self.llm = LLMClient()
        self.context = MatchContextAnalyzer(self.df_big, self.df_season, self.df_player)
        self.prompt_builder = DynamicPromptBuilder()
        self.personality_reactor = PersonalityReactor(self.llm)
        
        self.reactions_data = []
        
        print("✅ Engine ready with personality system!\n")
    
    def generate_single_reaction(self, row, output_format='all', include_personalities=True):
        """
        Generate reactions for a single match/player
        
        Args:
            row: DataFrame row with match data
            output_format: 'all', 'commentator', 'journalist', 'fan_tweet', 'personalities'
            include_personalities: Add pundit/manager/player reactions
        """
        player_name = row.get('playername', 'Unknown Player')
        team = row.get('team', 'Unknown Team')
        opponent = row.get('opponent', 'Unknown Opponent')
        
        print(f"⚡ Generating reaction: {player_name} ({team} vs {opponent})")
        
        # Get context
        team_stats = self.context.get_team_stats(team)
        context_tags = self.context.generate_context_tags(row, team_stats)
        context_narrative = self.context.build_narrative_string(context_tags)
        
        # Build base prompt
        base_prompt = self.prompt_builder.build_enriched_prompt(
            row, team_stats, context_tags, context_narrative
        )
        
        reaction_entry = {
            'player': player_name,
            'team': team,
            'opponent': opponent,
            'goals': row.get('goals', 0),
            'rating': row.get('rating', 'N/A'),
            'minutes': row.get('minsplayed', 0),
            'timestamp': datetime.now().isoformat(),
            'context_tags': context_tags['performance_narratives']
        }
        
        # Generate standard tones
        if output_format == 'all' or output_format != 'personalities':
            if output_format == 'all':
                reactions = self.llm.generate_multi_tone_reactions(base_prompt, player_name)
                reaction_entry.update(reactions)
            else:
                reaction = self.llm.generate_reaction(base_prompt)
                reaction_entry[output_format] = reaction
        
        # Generate personality reactions
        if include_personalities and ENABLE_PERSONALITY_REACTIONS:
            print(f"   🎭 Adding personality panel...")
            
            personality_package = self.personality_reactor.generate_full_reaction_package(
                row, context_tags, context_narrative
            )
            
            reaction_entry['personality_reactions'] = personality_package
            
            # Preview one pundit
            first_pundit = list(personality_package['pundits'].keys())[0]
            preview = personality_package['pundits'][first_pundit][:80]
            print(f"   💬 {first_pundit}: {preview}...\n")
        
        self.reactions_data.append(reaction_entry)
        
        return reaction_entry
    
    def process_batch(self, df=None, max_rows=None, output_format='all', 
                     include_personalities=True, delay=0.5):
        """
        Process multiple matches/players
        
        Args:
            df: DataFrame to process (defaults to self.df_player)
            max_rows: Limit number of rows (for testing)
            output_format: Reaction format to generate
            include_personalities: Add personality reactions
            delay: Delay between API calls (seconds)
        """
        if df is None:
            df = self.df_player
        
        if max_rows:
            df = df.head(max_rows)
        
        total = len(df)
        print(f"🎯 Processing {total} matches...\n")
        
        start_time = time.time()
        
        for idx, (_, row) in enumerate(df.iterrows(), 1):
            try:
                print(f"[{idx}/{total}] ", end="")
                reaction = self.generate_single_reaction(
                    row, output_format, include_personalities
                )
                
                time.sleep(delay)  # Rate limiting
                
            except Exception as e:
                print(f"❌ Error processing row {idx}: {e}\n")
                continue
        
        elapsed = time.time() - start_time
        print(f"\n✅ Batch complete! Processed {len(self.reactions_data)} reactions in {elapsed:.1f}s")
        
        return self.reactions_data
    
    def save_outputs(self):
        """Save reactions to multiple formats"""
        
        # 1. JSON output (complete data)
        with open(REACTIONS_JSON, 'w', encoding='utf-8') as f:
            json.dump(self.reactions_data, f, indent=2, ensure_ascii=False)
        print(f"📄 Saved JSON: {REACTIONS_JSON}")
        
        # 2. Standard text output
        with open(REACTIONS_TXT, 'w', encoding='utf-8') as f:
            for entry in self.reactions_data:
                f.write(f"\n{'='*80}\n")
                f.write(f"PLAYER: {entry['player']} ({entry['team']} vs {entry['opponent']})\n")
                f.write(f"Stats: {entry['goals']} goals | {entry['rating']} rating | {entry['minutes']} mins\n")
                f.write(f"{'='*80}\n\n")
                
                if 'commentator' in entry:
                    f.write(f"🎙️ COMMENTATOR:\n{entry['commentator']}\n\n")
                
                if 'journalist' in entry:
                    f.write(f"📰 JOURNALIST:\n{entry['journalist']}\n\n")
                
                if 'fan_tweet' in entry:
                    f.write(f"💬 FAN TWEET:\n{entry['fan_tweet']}\n\n")
        
        print(f"📄 Saved TXT: {REACTIONS_TXT}")
        
        # 3. Personality reactions (separate file for readability)
        if ENABLE_PERSONALITY_REACTIONS:
            with open(PERSONALITIES_TXT, 'w', encoding='utf-8') as f:
                for entry in self.reactions_data:
                    if 'personality_reactions' not in entry:
                        continue
                    
                    f.write(f"\n{'#'*80}\n")
                    f.write(f"MATCH: {entry['player']} - {entry['team']} vs {entry['opponent']}\n")
                    f.write(f"Performance: {entry['goals']} goals, {entry['rating']} rating\n")
                    f.write(f"{'#'*80}\n\n")
                    
                    pr = entry['personality_reactions']
                    
                    # Pundit panel
                    f.write("🎙️ PUNDIT PANEL:\n")
                    f.write("-" * 80 + "\n")
                    for pundit, reaction in pr['pundits'].items():
                        f.write(f"\n{pundit.upper()}:\n\"{reaction}\"\n")
                    
                    # Manager reaction
                    if 'manager' in pr:
                        f.write(f"\n{'='*80}\n")
                        f.write(f"⚽ MANAGER'S VIEW ({pr['manager']['manager']}):\n")
                        f.write(f"\"{pr['manager']['reaction']}\"\n")
                    
                    # Player reaction
                    if 'player' in pr:
                        f.write(f"\n{'='*80}\n")
                        f.write(f"👤 PLAYER REACTION ({pr['player']['reactor']} - {pr['player']['relationship']}):\n")
                        f.write(f"\"{pr['player']['reaction']}\"\n")
                    
                    f.write("\n\n")
            
            print(f"📄 Saved Personalities: {PERSONALITIES_TXT}")
        
        # 4. CSV export (flat structure, no nested personality data)
        df_export = pd.DataFrame([
            {
                'player': e['player'],
                'team': e['team'],
                'opponent': e['opponent'],
                'goals': e['goals'],
                'rating': e['rating'],
                'minutes': e['minutes'],
                'commentator': e.get('commentator', ''),
                'journalist': e.get('journalist', ''),
                'fan_tweet': e.get('fan_tweet', '')
            }
            for e in self.reactions_data
        ])
        df_export.to_csv(REACTIONS_CSV, index=False, encoding='utf-8')
        print(f"📄 Saved CSV: {REACTIONS_CSV}")
        
        # 5. Print stats
        stats = self.llm.get_stats()
        print(f"\n📊 LLM Usage Stats:")
        print(f"   Total Requests: {stats['requests']}")
        print(f"   Total Tokens: {stats['total_tokens']:,}")
        print(f"   Avg Tokens/Request: {stats['avg_tokens_per_request']:.1f}")
        
        if ENABLE_PERSONALITY_REACTIONS:
            total_personalities = sum(
                len(e.get('personality_reactions', {}).get('pundits', {})) + 2
                for e in self.reactions_data if 'personality_reactions' in e
            )
            print(f"   Personality Reactions: {total_personalities}")
    
    def generate_for_player(self, player_name, include_personalities=True):
        """Generate reactions for specific player's matches"""
        player_matches = self.df_player[
            self.df_player['playername'].str.contains(player_name, case=False, na=False)
        ]
        
        if player_matches.empty:
            print(f"❌ No matches found for player: {player_name}")
            return []
        
        print(f"🎯 Found {len(player_matches)} matches for {player_name}")
        return self.process_batch(player_matches, include_personalities=include_personalities)
    
    def generate_highlight_reel(self, min_rating=8.0, include_personalities=True):
        """Generate reactions only for standout performances"""
        highlights = self.df_player[self.df_player['rating'] >= min_rating]
        
        print(f"🌟 Generating reactions for {len(highlights)} standout performances (rating >= {min_rating})")
        return self.process_batch(highlights, include_personalities=include_personalities)
    
    def generate_rivalry_matches(self, include_personalities=True):
        """Generate reactions only for big rivalry matches"""
        rivalry_matches = []
        
        for _, row in self.df_player.iterrows():
            if self.context.is_big_match(row.get('teamid', 0), row.get('opponentid', 0)):
                rivalry_matches.append(row)
        
        if not rivalry_matches:
            print("❌ No rivalry matches found")
            return []
        
        df_rivalries = pd.DataFrame(rivalry_matches)
        print(f"⚔️ Generating reactions for {len(df_rivalries)} RIVALRY matches")
        return self.process_batch(df_rivalries, include_personalities=include_personalities)


def main():
    """Main execution"""
    engine = ReactionEngine()
    
    # Choose your mode:
    
    # Mode 1: Process limited sample WITH personalities (RECOMMENDED for testing)
    engine.process_batch(max_rows=3, output_format='all', include_personalities=True, delay=0.8)
    
    # Mode 2: Only rivalry matches with full personality panel
    # engine.generate_rivalry_matches(include_personalities=True)
    
    # Mode 3: Only highlights with personalities
    # engine.generate_highlight_reel(min_rating=8.0, include_personalities=True)
    
    # Mode 4: Specific player with personalities
    # engine.generate_for_player("Messi", include_personalities=True)
    
    # Mode 5: Full season WITHOUT personalities (faster, cheaper)
    # engine.process_batch(max_rows=None, include_personalities=False, delay=0.5)
    
    # Save outputs
    engine.save_outputs()
    
    print("\n🎉 Reaction Engine Complete!")
    print("\n📂 Check outputs folder for:")
    print("   - reactions.txt (standard tones)")
    print("   - personality_reactions.txt (legends & pundits)")
    print("   - reactions.json (complete data)")
    print("   - reactions_export.csv (spreadsheet)")


if __name__ == "__main__":
    main()