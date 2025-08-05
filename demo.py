#!/usr/bin/env python3
"""
Demo script for mufetch Python version
Shows the authentication and search workflow
"""

import os
from src.config import Config
from src.spotify_client import SpotifyClient
from src.display import DisplayFormatter


def demo_auth():
    """Demo authentication process"""
    print("=== mufetch Python Version Demo ===\n")
    print("1. Authentication Setup:")
    print("   python mufetch.py auth")
    print("   - Prompts for Spotify Client ID and Secret")
    print("   - Saves credentials to ~/.config/mufetch/config.yaml")
    print("   - Also supports environment variables:")
    print("     MUFETCH_SPOTIFY_CLIENT_ID")
    print("     MUFETCH_SPOTIFY_CLIENT_SECRET")
    print()


def demo_search():
    """Demo search functionality"""
    print("2. Search Commands:")
    print("   # Auto search (tries track, album, then artist)")
    print("   python mufetch.py search \"Bohemian Rhapsody\"")
    print()
    print("   # Specific search types")
    print("   python mufetch.py search \"Queen\" --type artist")
    print("   python mufetch.py search \"A Night at the Opera\" --type album")
    print("   python mufetch.py search \"We Will Rock You\" --type track")
    print()
    print("   # Custom image size")
    print("   python mufetch.py search \"Pink Floyd\" --size 25")
    print()


def demo_features():
    """Demo key features"""
    print("3. Key Features:")
    print("   ✓ Beautiful terminal display with album cover art")
    print("   ✓ Comprehensive metadata (duration, popularity, genres, etc.)")
    print("   ✓ Interactive clickable links for Spotify URLs")
    print("   ✓ Responsive image sizing (15-35)")
    print("   ✓ Cross-platform support (Linux, macOS, Windows)")
    print("   ✓ Image rendering with chafa support + ANSI fallback")
    print("   ✓ Auto-detection of search type")
    print("   ✓ Top tracks display for albums and artists")
    print()


def demo_structure():
    """Demo project structure"""
    print("4. Project Structure:")
    print("   mufetch.py              # Main CLI entry point")
    print("   requirements.txt        # Python dependencies")
    print("   src/")
    print("   ├── config.py          # Configuration management")
    print("   ├── spotify_client.py  # Spotify API client")
    print("   ├── display.py         # Terminal display & formatting")
    print("   └── commands/")
    print("       ├── auth.py        # Authentication command")
    print("       └── search.py      # Search command")
    print()


def demo_install():
    """Demo installation"""
    print("5. Installation & Setup:")
    print("   # Install dependencies")
    print("   pip install -r requirements.txt")
    print()
    print("   # Optional: Install chafa for better image rendering")
    print("   sudo apt install chafa      # Ubuntu/Debian")
    print("   brew install chafa          # macOS")
    print("   sudo pacman -S chafa        # Arch Linux")
    print()
    print("   # Make executable")
    print("   chmod +x mufetch.py")
    print()


def main():
    """Run the demo"""
    demo_auth()
    demo_search()
    demo_features()
    demo_structure()
    demo_install()
    
    print("=== Ready to use! ===")
    print("Run 'python mufetch.py auth' to get started!")


if __name__ == "__main__":
    main()
