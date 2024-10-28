from typing import Optional, List, Dict, Any
import requests
from app.core.cache import cache  # Updated import
from app.core.config import Config
from dataclasses import dataclass
from datetime import datetime

@dataclass
class UnsplashImage:
    id: str
    width: int
    height: int
    color: str
    description: Optional[str]
    alt_description: Optional[str]
    urls: Dict[str, str]
    user: Dict[str, Any]
    created_at: datetime

class UnsplashAPI:
    BASE_URL = "https://api.unsplash.com"
    
    @classmethod
    def _get_headers(cls) -> Dict[str, str]:
        """Get API headers with auth"""
        return {
            "Authorization": f"Client-ID {Config.UNSPLASH_ACCESS_KEY}",
            "Accept-Version": "v1"
        }
    
    @classmethod
    def _process_photo_response(cls, photo: Dict) -> Dict:
        """Process individual photo response"""
        return {
            "id": photo.get("id"),
            "width": photo.get("width"),
            "height": photo.get("height"),
            "color": photo.get("color"),
            "description": photo.get("description"),
            "alt_description": photo.get("alt_description"),
            "urls": {
                "raw": photo.get("urls", {}).get("raw"),
                "full": photo.get("urls", {}).get("full"),
                "regular": photo.get("urls", {}).get("regular"),
                "small": photo.get("urls", {}).get("small"),
                "thumb": photo.get("urls", {}).get("thumb"),
            },
            "user": {
                "name": photo.get("user", {}).get("name"),
                "username": photo.get("user", {}).get("username"),
                "portfolio_url": photo.get("user", {}).get("portfolio_url"),
            },
            "created_at": photo.get("created_at"),
        }

    @classmethod
    @cache.memoize(timeout=300)  # Cache for 5 minutes
    def get_random_photos(
        cls, 
        count: int = 30,
        collections: Optional[List[str]] = None,
        query: Optional[str] = None,
        orientation: Optional[str] = None,
    ) -> List[Dict]:
        """Get random photos from Unsplash with caching"""
        # Build request parameters
        params = {"count": count}
        if collections:
            params["collections"] = ",".join(collections)
        if query:
            params["query"] = query
        if orientation:
            params["orientation"] = orientation
            
        try:
            # Make API request
            response = requests.get(
                f"{cls.BASE_URL}/photos/random",
                headers=cls._get_headers(),
                params=params
            )
            response.raise_for_status()
            
            # Process response
            photos = response.json()
            return [cls._process_photo_response(photo) for photo in photos]
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Unsplash API error: {str(e)}")

    @classmethod
    @cache.memoize(timeout=300)  # Cache for 5 minutes
    def get_photo_by_id(cls, photo_id: str) -> Dict:
        """Get a specific photo by ID"""
        try:
            response = requests.get(
                f"{cls.BASE_URL}/photos/{photo_id}",
                headers=cls._get_headers()
            )
            response.raise_for_status()
            
            photo = response.json()
            return cls._process_photo_response(photo)
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Unsplash API error: {str(e)}")
        
    @classmethod
    @cache.memoize(timeout=300)  # Cache for 5 minutes
    def search_photos(
        cls,
        query: str,
        page: int = 1,
        per_page: int = 30,
        orientation: Optional[str] = None,
        color: Optional[str] = None,
        order_by: str = "relevant"
    ) -> Dict[str, Any]:
        """
        Search photos on Unsplash
        
        Args:
            query: Search query term
            page: Page number (default: 1)
            per_page: Number of items per page (default: 30)
            orientation: Filter by photo orientation (landscape, portrait, or squarish)
            color: Filter by color (black_and_white, black, white, yellow, orange, red, etc.)
            order_by: How to sort photos (relevant or latest)
            
        Returns:
            Dict containing total and total_pages counts, and list of processed photos
        """
        params = {
            "query": query,
            "page": page,
            "per_page": per_page,
            "order_by": order_by
        }
        
        if orientation:
            params["orientation"] = orientation
        if color:
            params["color"] = color
            
        try:
            response = requests.get(
                f"{cls.BASE_URL}/search/photos",
                headers=cls._get_headers(),
                params=params
            )
            response.raise_for_status()
            
            data = response.json()
            processed_photos = [
                cls._process_photo_response(photo) 
                for photo in data.get("results", [])
            ]
            
            return {
                "total": data.get("total", 0),
                "total_pages": data.get("total_pages", 0),
                "photos": processed_photos
            }
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Unsplash API error: {str(e)}")