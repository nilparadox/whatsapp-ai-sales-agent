from pathlib import Path
import shutil

def ensure_seed_files() -> None:
    data_dir = Path("data")
    data_dir.mkdir(parents=True, exist_ok=True)

    # Seed default catalog if missing
    seed_default = Path("data/seed/catalog_default.csv")
    live_default = Path("data/catalog_default.csv")
    if seed_default.exists() and not live_default.exists():
        shutil.copyfile(seed_default, live_default)
