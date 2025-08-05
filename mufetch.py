#!/usr/bin/env python3
"""
mufetch - Neofetch-style CLI for music
A beautiful terminal music information display tool
"""

import sys
import argparse
from src.commands import auth, search
from src.config import Config

__version__ = "1.0.0"


def main():
    """Main entry point for the application"""
    parser = argparse.ArgumentParser(
        prog="mufetch",
        description="neofetch-like CLI for music",
        epilog="Search for tracks, albums, or artists and display their metadata"
    )
    
    parser.add_argument('--version', action='version', version=f'mufetch {__version__}')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Auth command
    auth_parser = subparsers.add_parser('auth', help='Authenticate with Spotify API')
    auth_parser.set_defaults(func=auth.handle_auth)
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search for music')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument(
        '-t', '--type', 
        choices=['auto', 'track', 'album', 'artist'],
        default='auto',
        help='Search type (default: auto)'
    )
    search_parser.add_argument(
        '-s', '--size',
        type=int,
        default=20,
        help='Image size (15-35, default: 20)'
    )
    search_parser.set_defaults(func=search.handle_search)
    
    # Parse arguments
    args = parser.parse_args()
    
    # Initialize config
    try:
        Config.init_config()
    except Exception as e:
        print(f"Failed to initialize config: {e}")
        sys.exit(1)
    
    # Execute command
    if hasattr(args, 'func'):
        try:
            args.func(args)
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            sys.exit(0)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
