"""
Authentication command handler for mufetch
"""

import sys
from ..config import Config


def handle_auth(args):
    """Handle the auth command"""
    print("Spotify API Authentication Setup")
    print()
    print("To get your Spotify API credentials:")
    print("1. Go to: https://developer.spotify.com/dashboard")
    print("2. Log in with your Spotify account")
    print("3. Click 'Create an App'")
    print("4. Fill in app name and description")
    print("5. Copy your Client ID and Client Secret")
    print()
    
    try:
        client_id = input("Enter your Spotify Client ID: ").strip()
        client_secret = input("Enter your Spotify Client Secret: ").strip()
        
        # Validate credentials
        if not client_id or not client_secret:
            print("Error: Both Client ID and Client Secret are required!")
            sys.exit(1)
        
        if len(client_id) < 10 or len(client_secret) < 10:
            print("Warning: Credentials seem too short. Please verify they are correct.")
        
        # Save credentials
        config = Config()
        config.save_credentials(client_id, client_secret)
        
        print("Credentials saved successfully!")
        print("You can now use 'python mufetch.py search <query>' to search for music.")
        
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(0)
    except Exception as e:
        print(f"Failed to save credentials: {e}")
        sys.exit(1)
