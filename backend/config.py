import os
from typing import Optional

class Config:
    # Configuration for the research summarization system
    
    @classmethod
    def get_model_cache_dir(cls) -> str:
        """Get the directory for caching downloaded models"""
        cache_dir = os.getenv("TRANSFORMERS_CACHE", "models")
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        return cache_dir
    
    @classmethod
    def is_offline_mode(cls) -> bool:
        """Check if running in offline mode (no internet for model downloads)"""
        return os.getenv("OFFLINE_MODE", "false").lower() == "true" 