import shutil
from pathlib import Path
from datetime import datetime

def extract_metabase_db():
    source_path = Path("/metabase_data/metabase.db.mv.db")
    output_dir = Path("/outputs")
    output_dir.mkdir(parents=True, exist_ok=True)
    if not source_path.exists():
        print(f"[ERROR] Source DB file not found at {source_path}")
        return {'error': 'Source DB file not found'}, 500
    # Nom du backup avec timestamp
    timestamp = datetime.now().strftime("%Y_%m_%d")
    backup_filename = f"metabase_backup_{timestamp}.mv.db"
    destination_path = output_dir / backup_filename
    try:
        shutil.copy(source_path, destination_path)
        print(f"[INFO] Metabase DB copied to {destination_path}")
        return {'message': 'Backup done', 'file': str(destination_path)}
    except Exception as e:
        print(f"[ERROR] Failed to copy DB: {e}")
        return {'error': str(e)}, 500