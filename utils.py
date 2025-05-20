import json
import logging
from typing import Dict, List, Any, Optional
import pandas as pd
from pathlib import Path
import hashlib
import pickle

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_json(file_path: str) -> Any:
    """Load data from a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading JSON from {file_path}: {e}")
        raise

def save_json(data: Any, file_path: str) -> None:
    """Save data to a JSON file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"Data saved to {file_path}")
    except Exception as e:
        logger.error(f"Error saving JSON to {file_path}: {e}")
        raise

def load_pickle(file_path: str) -> Any:
    """Load data from a pickle file."""
    try:
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        logger.error(f"Error loading pickle from {file_path}: {e}")
        raise

def save_pickle(data: Any, file_path: str) -> None:
    """Save data to a pickle file."""
    try:
        with open(file_path, 'wb') as f:
            pickle.dump(data, f)
        logger.info(f"Data saved to {file_path}")
    except Exception as e:
        logger.error(f"Error saving pickle to {file_path}: {e}")
        raise

def generate_id(*args) -> str:
    """Generate a unique ID based on input arguments."""
    hash_input = "".join(str(arg) for arg in args).encode('utf-8')
    return hashlib.md5(hash_input).hexdigest()

def clean_text(text: str) -> str:
    """Clean and normalize text."""
    if not text:
        return ""
    # Remove extra whitespace and normalize newlines
    return " ".join(str(text).split())

def safe_get(dictionary: Dict, *keys, default=None):
    """Safely get a value from a nested dictionary."""
    current = dictionary
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current if current is not None else default

class DataProcessor:
    """Utility class for processing and analyzing data."""
    
    @staticmethod
    def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """Normalize a pandas DataFrame."""
        # Convert all column names to lowercase and replace spaces with underscores
        df.columns = df.columns.str.lower().str.replace(' ', '_')
        
        # Convert string columns to string type and strip whitespace
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].astype(str).str.strip()
            
        return df
    
    @staticmethod
    def filter_by_keywords(
        df: pd.DataFrame, 
        column: str, 
        keywords: List[str], 
        case_sensitive: bool = False
    ) -> pd.DataFrame:
        """Filter DataFrame rows where the specified column contains any of the keywords."""
        if not keywords:
            return df
            
        if case_sensitive:
            mask = df[column].str.contains('|'.join(keywords), na=False)
        else:
            mask = df[column].str.lower().str.contains('|'.join(k.lower() for k in keywords), na=False)
            
        return df[mask].copy()

class CacheManager:
    """Simple cache manager for storing and retrieving computed results."""
    
    def __init__(self, cache_dir: str = '.cache'):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
    
    def get_cache_path(self, key: str) -> Path:
        """Get the cache file path for a given key."""
        return self.cache_dir / f"{key}.pkl"
    
    def get(self, key: str) -> Any:
        """Get a value from the cache."""
        cache_file = self.get_cache_path(key)
        if cache_file.exists():
            try:
                return load_pickle(str(cache_file))
            except Exception as e:
                logger.warning(f"Error loading from cache {key}: {e}")
        return None
    
    def set(self, key: str, value: Any) -> None:
        """Store a value in the cache."""
        try:
            save_pickle(value, str(self.get_cache_path(key)))
        except Exception as e:
            logger.warning(f"Error saving to cache {key}: {e}")
