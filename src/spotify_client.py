"""
Spotify API client for mufetch
Handles authentication and API requests to Spotify Web API
"""

import time
import base64
import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Image:
    """Spotify image metadata"""
    url: str
    height: int
    width: int


@dataclass
class ExternalURL:
    """External URLs for Spotify entities"""
    spotify: str


@dataclass
class Followers:
    """Artist follower count"""
    total: int


@dataclass
class Artist:
    """Spotify artist with metadata"""
    id: str
    name: str
    images: List[Image]
    genres: List[str]
    popularity: int
    followers: Followers
    external_urls: ExternalURL
    type: str = "artist"


@dataclass
class Album:
    """Spotify album with metadata"""
    id: str
    name: str
    artists: List[Artist]
    images: List[Image]
    release_date: str
    release_date_precision: str
    total_tracks: int
    genres: List[str]
    popularity: int
    album_type: str
    album_group: Optional[str]
    label: str
    external_urls: ExternalURL
    tracks: Optional[List['Track']] = None


@dataclass
class Track:
    """Spotify track with metadata"""
    id: str
    name: str
    artists: List[Artist]
    album: Album
    duration_ms: int
    popularity: int
    track_number: int
    disc_number: int
    explicit: bool
    preview_url: Optional[str]
    external_urls: ExternalURL
    available_markets: List[str]


class SpotifyClient:
    """Spotify Web API client with OAuth authentication"""
    
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token: Optional[str] = None
        self.token_expiry: float = 0
        self.base_url = "https://api.spotify.com/v1"
        self.auth_url = "https://accounts.spotify.com/api/token"
    
    def _authenticate(self) -> None:
        """Obtain or refresh access token for API calls"""
        if time.time() < self.token_expiry:
            return  # Token still valid
        
        # Prepare credentials for Basic authentication
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {'grant_type': 'client_credentials'}
        
        response = requests.post(self.auth_url, headers=headers, data=data, timeout=30)
        
        if response.status_code != 200:
            raise Exception(f"Authentication failed: {response.status_code} - {response.text}")
        
        token_data = response.json()
        self.access_token = token_data['access_token']
        self.token_expiry = time.time() + token_data['expires_in']
    
    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make authenticated request to Spotify API"""
        self._authenticate()
        
        headers = {'Authorization': f'Bearer {self.access_token}'}
        url = f"{self.base_url}/{endpoint}"
        
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        if response.status_code != 200:
            raise Exception(f"API request failed: {response.status_code} - {response.text}")
        
        return response.json()
    
    def search(self, query: str, search_type: str) -> Dict[str, Any]:
        """Search for tracks, albums, or artists"""
        params = {
            'q': query,
            'type': search_type,
            'limit': 1
        }
        
        return self._make_request('search', params)
    
    def get_album(self, album_id: str) -> Album:
        """Get detailed album information by ID"""
        data = self._make_request(f'albums/{album_id}')
        return self._parse_album(data)
    
    def get_artist(self, artist_id: str) -> Artist:
        """Get detailed artist information by ID"""
        data = self._make_request(f'artists/{artist_id}')
        return self._parse_artist(data)
    
    def get_artist_top_tracks(self, artist_id: str) -> List[Track]:
        """Get artist's most popular tracks"""
        data = self._make_request(f'artists/{artist_id}/top-tracks', {'market': 'US'})
        return [self._parse_track(track_data) for track_data in data.get('tracks', [])]
    
    def get_artist_albums(self, artist_id: str, include_groups: str = 'album') -> List[Album]:
        """Get artist's albums by type"""
        params = {
            'include_groups': include_groups,
            'limit': 50,
            'market': 'US'
        }
        
        data = self._make_request(f'artists/{artist_id}/albums', params)
        return [self._parse_album(album_data) for album_data in data.get('items', [])]
    
    def _parse_image(self, image_data: Dict[str, Any]) -> Image:
        """Parse image data from API response"""
        return Image(
            url=image_data.get('url', ''),
            height=image_data.get('height', 0),
            width=image_data.get('width', 0)
        )
    
    def _parse_external_urls(self, urls_data: Dict[str, Any]) -> ExternalURL:
        """Parse external URLs from API response"""
        return ExternalURL(spotify=urls_data.get('spotify', ''))
    
    def _parse_followers(self, followers_data: Dict[str, Any]) -> Followers:
        """Parse followers data from API response"""
        return Followers(total=followers_data.get('total', 0))
    
    def _parse_artist(self, artist_data: Dict[str, Any]) -> Artist:
        """Parse artist data from API response"""
        images = [self._parse_image(img) for img in artist_data.get('images', [])]
        external_urls = self._parse_external_urls(artist_data.get('external_urls', {}))
        followers = self._parse_followers(artist_data.get('followers', {}))
        
        return Artist(
            id=artist_data.get('id', ''),
            name=artist_data.get('name', ''),
            images=images,
            genres=artist_data.get('genres', []),
            popularity=artist_data.get('popularity', 0),
            followers=followers,
            external_urls=external_urls,
            type=artist_data.get('type', 'artist')
        )
    
    def _parse_album(self, album_data: Dict[str, Any]) -> Album:
        """Parse album data from API response"""
        images = [self._parse_image(img) for img in album_data.get('images', [])]
        artists = [self._parse_artist(artist) for artist in album_data.get('artists', [])]
        external_urls = self._parse_external_urls(album_data.get('external_urls', {}))
        
        # Parse tracks if available
        tracks = None
        if 'tracks' in album_data and 'items' in album_data['tracks']:
            tracks = [self._parse_track(track) for track in album_data['tracks']['items']]
        
        return Album(
            id=album_data.get('id', ''),
            name=album_data.get('name', ''),
            artists=artists,
            images=images,
            release_date=album_data.get('release_date', ''),
            release_date_precision=album_data.get('release_date_precision', ''),
            total_tracks=album_data.get('total_tracks', 0),
            genres=album_data.get('genres', []),
            popularity=album_data.get('popularity', 0),
            album_type=album_data.get('album_type', ''),
            album_group=album_data.get('album_group'),
            label=album_data.get('label', ''),
            external_urls=external_urls,
            tracks=tracks
        )
    
    def _parse_track(self, track_data: Dict[str, Any]) -> Track:
        """Parse track data from API response"""
        artists = [self._parse_artist(artist) for artist in track_data.get('artists', [])]
        album = self._parse_album(track_data.get('album', {}))
        external_urls = self._parse_external_urls(track_data.get('external_urls', {}))
        
        return Track(
            id=track_data.get('id', ''),
            name=track_data.get('name', ''),
            artists=artists,
            album=album,
            duration_ms=track_data.get('duration_ms', 0),
            popularity=track_data.get('popularity', 0),
            track_number=track_data.get('track_number', 0),
            disc_number=track_data.get('disc_number', 0),
            explicit=track_data.get('explicit', False),
            preview_url=track_data.get('preview_url'),
            external_urls=external_urls,
            available_markets=track_data.get('available_markets', [])
        )
