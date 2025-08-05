"""
Configuration management for mufetch
Handles Spotify API credentials and configuration storage
"""

import os
import yaml
from pathlib import Path
from typing import Optional


class Config:
    """Configuration manager for mufetch"""
    
    def __init__(self):
        self.spotify_client_id: Optional[str] = None
        self.spotify_client_secret: Optional[str] = None
        self._config_dir = Path.home() / ".config" / "mufetch"
        self._config_file = self._config_dir / "config.yaml"
    
    @classmethod
    def init_config(cls) -> None:
        """Initialize configuration directory and file"""
        config = cls()
        config._config_dir.mkdir(parents=True, exist_ok=True)
        
        # Create config file if it doesn't exist
        if not config._config_file.exists():
            default_config = {
                'spotify_client_id': '',
                'spotify_client_secret': ''
            }
            with open(config._config_file, 'w') as f:
                yaml.dump(default_config, f, default_flow_style=False)
    
    @classmethod
    def load_config(cls) -> 'Config':
        """Load configuration from file"""
        config = cls()
        
        if config._config_file.exists():
            with open(config._config_file, 'r') as f:
                data = yaml.safe_load(f) or {}
                config.spotify_client_id = data.get('spotify_client_id', '').strip()
                config.spotify_client_secret = data.get('spotify_client_secret', '').strip()
        
        # Also check environment variables
        if not config.spotify_client_id:
            config.spotify_client_id = os.getenv('MUFETCH_SPOTIFY_CLIENT_ID', '').strip()
        if not config.spotify_client_secret:
            config.spotify_client_secret = os.getenv('MUFETCH_SPOTIFY_CLIENT_SECRET', '').strip()
        
        return config
    
    def save_credentials(self, client_id: str, client_secret: str) -> None:
        """Save Spotify API credentials to config file"""
        config_data = {
            'spotify_client_id': client_id.strip(),
            'spotify_client_secret': client_secret.strip()
        }
        
        with open(self._config_file, 'w') as f:
            yaml.dump(config_data, f, default_flow_style=False)
        
        self.spotify_client_id = client_id.strip()
        self.spotify_client_secret = client_secret.strip()
    
    def has_credentials(self) -> bool:
        """Check if valid Spotify credentials are configured"""
        return bool(self.spotify_client_id and self.spotify_client_secret)
