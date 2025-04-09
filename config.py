import os

# Get the absolute path to the directory this script lives in
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Example configuration - modified to use paths relative to this script
CONFIGURATIONS = [
    {
        "base_file": os.path.join(BASE_DIR, "sinteticDB", "IMDB", "IMDB_Base.csv"),
        "new_file": os.path.join(BASE_DIR, "sinteticDB", "IMDB", "Versions", "imdb_with_financials_l.csv"),
        "candidate_dir": os.path.join(BASE_DIR, "sinteticDB", "IMDB", "externalTables")
    },
    # Add more configurations as needed
]

# Or to analyze all files in a directory:
"""
import os

# Get the directory this script is in
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Now make BASE_DIR relative to this script's location
BASE_DIR = os.path.join(SCRIPT_DIR, "sinteticDB", "IMDB")

CONFIGURATIONS = [
    {
        "base_file": os.path.join(BASE_DIR, "IMDB_Base.csv"),
        "new_file": os.path.join(BASE_DIR, "Versions", filename),
        "candidate_dir": os.path.join(BASE_DIR, "externalTables")
    }
    for filename in os.listdir(os.path.join(BASE_DIR, "Versions"))
    if filename.endswith(".csv")
]
"""