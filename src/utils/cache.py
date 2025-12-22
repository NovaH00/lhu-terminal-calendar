import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
from hashlib import md5


class CacheManager:
    """
    A simple file-based cache manager for storing API responses.
    """
    
    def __init__(self, cache_dir: str = ".cache", ttl_hours: int = 24):
        """
        Initialize the cache manager.
        
        Args:
            cache_dir: Directory to store cache files
            ttl_hours: Time-to-live in hours for cached data
        """
        self.cache_dir: Path = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.ttl: timedelta = timedelta(hours=ttl_hours)
    
    def _get_cache_key(self, api_url: str, student_id: str, query_time: datetime, day_range: int) -> str:
        """
        Generate a unique cache key based on API parameters.
        """
        # Convert datetime to ISO format string for consistent hashing
        time_str = query_time.astimezone().isoformat() if query_time.tzinfo else query_time.isoformat()
        key_str = f"{api_url}:{student_id}:{time_str}:{day_range}"
        return md5(key_str.encode()).hexdigest()
    
    def _get_cache_file_path(self, cache_key: str) -> Path:
        """
        Get the file path for a cache key.
        """
        return self.cache_dir / f"{cache_key}.json"
    
    def get(
            self, 
            api_url: str, 
            student_id: str, 
            query_time: datetime, 
            day_range: int
        ) -> list[dict[str, str]] | None:
        """
        Retrieve cached data if it exists and hasn't expired.
        
        Returns:
            Cached data if found and valid, None otherwise
        """
        cache_key = self._get_cache_key(api_url, student_id, query_time, day_range)
        cache_file = self._get_cache_file_path(cache_key)
        
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cached_data = json.load(f)
            
            # Check if the cache has expired
            cache_time = datetime.fromisoformat(cached_data['timestamp'])
            if datetime.now() - cache_time > self.ttl:
                # Remove expired cache file
                cache_file.unlink()
                return None
            
            return cached_data['data']
        except (json.JSONDecodeError, KeyError, ValueError, OSError):
            # If there's any issue reading the cache, remove the file and return None
            if cache_file.exists():
                cache_file.unlink()
            return None
    
    def set(
            self, 
            api_url: str, 
            student_id: str, 
            query_time: datetime, 
            day_range: int, 
            data: list[dict[str, str]]
        ) -> None:
        """
        Store data in the cache.
        """
        cache_key = self._get_cache_key(api_url, student_id, query_time, day_range)
        cache_file = self._get_cache_file_path(cache_key)
        
        cache_data = {
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
        except OSError:
            # If we can't write to cache, just ignore (don't break the app)
            pass
    
    def clear_expired(self) -> int:
        """
        Remove all expired cache files.
        
        Returns:
            Number of files removed
        """
        count = 0
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cached_data = json.load(f)
                
                cache_time = datetime.fromisoformat(cached_data['timestamp'])
                if datetime.now() - cache_time > self.ttl:
                    cache_file.unlink()
                    count += 1
            except (json.JSONDecodeError, KeyError, ValueError, OSError):
                # If there's any issue reading the cache file, remove it
                cache_file.unlink()
                count += 1
        
        return count
