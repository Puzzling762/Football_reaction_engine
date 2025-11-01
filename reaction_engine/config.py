import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "your-groq-api-key-here")
GROQ_MODEL = "llama-3.3-70b-versatile"  # Fast and powerful for sports commentary

# Paths
BASE_DIR = r"D:\Projects\Fifa15_AI\exported_data"
BIGMATCHUPS_CSV = os.path.join(BASE_DIR, "bigmatchups.csv")
SEASONSTATS_CSV = os.path.join(BASE_DIR, "seasonstats.csv")
PLAYERMATCH_CSV = os.path.join(BASE_DIR, "playermatchratinghistory.csv")

OUTPUT_DIR = r"D:\Projects\Fifa15_AI\reaction_engine\outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Output files
REACTIONS_TXT = os.path.join(OUTPUT_DIR, "reactions.txt")
REACTIONS_JSON = os.path.join(OUTPUT_DIR, "reactions.json")
REACTIONS_CSV = os.path.join(OUTPUT_DIR, "reactions_export.csv")
PERSONALITIES_TXT = os.path.join(OUTPUT_DIR, "personality_reactions.txt")

# LLM Settings
MAX_TOKENS = 350
TEMPERATURE = 0.85  # High creativity for varied reactions
TOP_P = 0.9

# Feature Flags
ENABLE_CONTEXT_MEMORY = True  # Remember recent performances
ENABLE_RIVALRY_DETECTION = True
ENABLE_FORM_ANALYSIS = True
ENABLE_STAT_COMPARISONS = True
ENABLE_PERSONALITY_REACTIONS = True  # NEW: Multi-personality reactions

# Personality Reaction Settings
NUM_PUNDITS = 3  # Number of pundits per match
INCLUDE_MANAGER_REACTION = True
INCLUDE_PLAYER_REACTION = True
PERSONALITY_VARIETY_WINDOW = 10  # Avoid repeating same personality within N matches