"""
Search command handler for mufetch
"""

import sys
from ..config import Config
from ..spotify_client import SpotifyClient
from ..display import DisplayFormatter


def handle_search(args):
    """Handle the search command"""
    query = args.query
    search_type = args.type
    image_size = args.size
    
    # Load config
    config = Config.load_config()
    
    if not config.has_credentials():
        print("No Spotify credentials found!")
        print("Run 'python mufetch.py auth' to set up your API credentials.")
        sys.exit(1)
    
    # Initialize Spotify client
    client = SpotifyClient(config.spotify_client_id, config.spotify_client_secret)
    
    # Hide cursor
    print('\033[?25l', end='')
    try:
        print()
        
        # Validate image size
        if image_size < 15:
            image_size = 15
        if image_size > 35:
            image_size = 35
        
        # Initialize display formatter
        formatter = DisplayFormatter(image_size)
        
        # Perform search
        if search_type == "auto":
            search_auto(query, client, formatter)
        else:
            search_specific(query, search_type, client, formatter)
        
        # Move cursor up and clear the line
        print('\033[F\033[K\n')
        
    finally:
        # Show cursor
        print('\033[?25h', end='')


def search_auto(query: str, client: SpotifyClient, formatter: DisplayFormatter):
    """Perform automatic search based on query"""
    # Try track first
    try:
        result = client.search(query, "track")
        if result.get('tracks', {}).get('items'):
            track_data = result['tracks']['items'][0]
            track = client._parse_track(track_data)
            formatter.display_track(track, client)
            return
    except Exception:
        pass
    
    # Try album
    try:
        result = client.search(query, "album")
        if result.get('albums', {}).get('items'):
            album_data = result['albums']['items'][0]
            album = client.get_album(album_data['id'])
            formatter.display_album(album, client)
            return
    except Exception:
        pass
    
    # Try artist
    try:
        result = client.search(query, "artist")
        if result.get('artists', {}).get('items'):
            artist_data = result['artists']['items'][0]
            artist = client.get_artist(artist_data['id'])
            formatter.display_artist(artist, client)
            return
    except Exception:
        pass
    
    print(f"No results found for: {query}")


def search_specific(query: str, search_type: str, client: SpotifyClient, formatter: DisplayFormatter):
    """Perform search for specific type"""
    try:
        result = client.search(query, search_type)
        
        if search_type == "track":
            tracks = result.get('tracks', {}).get('items', [])
            if tracks:
                track = client._parse_track(tracks[0])
                formatter.display_track(track, client)
            else:
                print(f"No tracks found for: {query}")
        
        elif search_type == "album":
            albums = result.get('albums', {}).get('items', [])
            if albums:
                album = client.get_album(albums[0]['id'])
                formatter.display_album(album, client)
            else:
                print(f"No albums found for: {query}")
        
        elif search_type == "artist":
            artists = result.get('artists', {}).get('items', [])
            if artists:
                artist = client.get_artist(artists[0]['id'])
                formatter.display_artist(artist, client)
            else:
                print(f"No artists found for: {query}")
    
    except Exception as e:
        print(f"Search failed: {e}")
        sys.exit(1)
