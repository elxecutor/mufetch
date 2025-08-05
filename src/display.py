"""
Display module for mufetch
Handles terminal image rendering and information formatting
"""

import os
import sys
import tempfile
import subprocess
from typing import List, Optional
from datetime import datetime, timedelta
import requests
from PIL import Image, ImageOps
from io import BytesIO

from .spotify_client import Track, Album, Artist, SpotifyClient


# ANSI color codes for terminal output
class Colors:
    RESET = '\033[0m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BOLD = '\033[1m'


class ImageRenderer:
    """Handles terminal image rendering using chafa or fallback methods"""
    
    def __init__(self, size: int = 20):
        self.width = size
        self.height = size
    
    def render_image_lines(self, image_url: str) -> List[str]:
        """Convert image URL to terminal-displayable lines"""
        if not image_url:
            return self._get_placeholder_lines()
        
        # Try chafa first if available
        if self._is_chafa_available():
            lines = self._render_with_chafa(image_url)
            if lines:
                return lines
        
        # Fallback to ANSI block art
        try:
            img = self._download_image(image_url)
            return self._get_block_art_lines(img)
        except Exception:
            return self._get_placeholder_lines()
    
    def _is_chafa_available(self) -> bool:
        """Check if chafa command is installed"""
        try:
            subprocess.run(['chafa', '--version'], 
                         capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def _render_with_chafa(self, image_url: str) -> Optional[List[str]]:
        """Use chafa command to render image"""
        try:
            # Download image to temporary file
            temp_file = self._download_to_temp(image_url)
            if not temp_file:
                return None
            
            # Run chafa command
            cmd = [
                'chafa',
                '--size', f'{self.width * 2}x{self.height}',
                '--dither', 'ordered',
                temp_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Clean up temporary file
            os.unlink(temp_file)
            
            lines = result.stdout.strip().split('\n')
            
            # Add left padding
            lines = [' ' + line for line in lines]
            
            # Ensure correct number of lines
            while len(lines) < self.height:
                lines.append(' ' * (self.width * 2 + 1))
            if len(lines) > self.height:
                lines = lines[:self.height]
            
            return lines
            
        except Exception:
            return None
    
    def _download_to_temp(self, image_url: str) -> Optional[str]:
        """Download image to temporary file"""
        try:
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as f:
                f.write(response.content)
                return f.name
        except Exception:
            return None
    
    def _download_image(self, url: str) -> Image.Image:
        """Download and decode image from URL"""
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    
    def _get_block_art_lines(self, img: Image.Image) -> List[str]:
        """Convert image to colored terminal blocks"""
        # Resize image
        img = img.convert('RGB')
        img = ImageOps.fit(img, (self.width, self.height), Image.Resampling.LANCZOS)
        
        lines = []
        for y in range(self.height):
            line = ' '  # Left padding
            for x in range(self.width):
                r, g, b = img.getpixel((x, y))
                # Create colored block using true color ANSI codes
                line += f'\033[48;2;{r};{g};{b}m  \033[0m'
            lines.append(line)
        
        return lines
    
    def _get_placeholder_lines(self) -> List[str]:
        """Create placeholder when no image is available"""
        lines = [
            f' {Colors.WHITE}┌───────────────────────────────┐{Colors.RESET}',
            f' {Colors.WHITE}│                               │{Colors.RESET}',
            f' {Colors.WHITE}│                               │{Colors.RESET}',
            f' {Colors.WHITE}│           NO IMAGE            │{Colors.RESET}',
            f' {Colors.WHITE}│           AVAILABLE           │{Colors.RESET}',
            f' {Colors.WHITE}│                               │{Colors.RESET}',
            f' {Colors.WHITE}│                               │{Colors.RESET}',
            f' {Colors.WHITE}└───────────────────────────────┘{Colors.RESET}',
        ]
        
        # Pad to match image height
        while len(lines) < 20:
            lines.append(' ' * 33)
        
        return lines


class DisplayFormatter:
    """Formats and displays music information"""
    
    def __init__(self, image_size: int = 20):
        self.renderer = ImageRenderer(image_size)
    
    def display_track(self, track: Track, client: Optional[SpotifyClient] = None):
        """Display track information with album art"""
        # Get image lines
        image_lines = []
        if track.album.images:
            image_lines = self.renderer.render_image_lines(track.album.images[0].url)
        else:
            image_lines = self.renderer._get_placeholder_lines()
        
        # Create artist links
        artist_names = [self._create_clickable_link(artist.external_urls.spotify, artist.name) 
                       for artist in track.artists]
        
        duration = timedelta(milliseconds=track.duration_ms)
        
        # Get genres from album or artist
        genres = track.album.genres
        if not genres and track.artists and client:
            try:
                artist = client.get_artist(track.artists[0].id)
                genres = artist.genres
            except Exception:
                pass
        
        # Create album link
        album_name = self._create_clickable_link(track.album.external_urls.spotify, track.album.name)
        
        info_lines = [
            self._format_info_line("Name", track.name, Colors.GREEN),
            self._format_info_line("Artist", ", ".join(artist_names), Colors.YELLOW),
            self._format_info_line("Album", album_name, Colors.BLUE),
            self._format_info_line("Duration", self._format_duration(duration), Colors.WHITE),
            self._format_info_line("Track", str(track.track_number), Colors.CYAN),
            self._format_info_line("Explicit", self._format_bool(track.explicit), Colors.RED),
            self._format_info_line("Released", self._format_ordinal_date(track.album.release_date), Colors.CYAN),
            self._format_info_line("Popularity", f"{track.popularity}%", Colors.PURPLE),
        ]
        
        if genres:
            display_genres = genres[:2]
            genre_string = ", ".join(display_genres)
            info_lines.append(self._format_info_line("Genres", genre_string, Colors.RED))
        
        # Prepare links
        links = []
        if track.album.images:
            links.append(f"{Colors.BLUE}{self._create_clickable_link(track.album.images[0].url, 'Album Cover')}{Colors.RESET}")
        links.append(f"{Colors.GREEN}{self._create_clickable_link(track.external_urls.spotify, 'Spotify')}{Colors.RESET}")
        
        self._display_side_by_side_with_links(image_lines, info_lines, links)
    
    def display_album(self, album: Album, client: Optional[SpotifyClient] = None):
        """Display album information with cover art"""
        # Get image lines
        image_lines = []
        if album.images:
            image_lines = self.renderer.render_image_lines(album.images[0].url)
        else:
            image_lines = self.renderer._get_placeholder_lines()
        
        # Create artist links
        artist_names = [self._create_clickable_link(artist.external_urls.spotify, artist.name) 
                       for artist in album.artists]
        
        # Calculate total duration
        total_duration = 0
        if album.tracks:
            total_duration = sum(track.duration_ms for track in album.tracks)
        
        # Get genres
        genres = album.genres
        if not genres and album.artists and client:
            try:
                artist = client.get_artist(album.artists[0].id)
                genres = artist.genres
            except Exception:
                pass
        
        info_lines = [
            self._format_info_line("Name", album.name, Colors.GREEN),
            self._format_info_line("Artist", ", ".join(artist_names), Colors.YELLOW),
            self._format_info_line("Type", album.album_type, Colors.BLUE),
            self._format_info_line("Released", self._format_ordinal_date(album.release_date), Colors.CYAN),
            self._format_info_line("Tracks", str(album.total_tracks), Colors.PURPLE),
            self._format_info_line("Duration", self._format_duration(timedelta(milliseconds=total_duration)), Colors.WHITE),
            self._format_info_line("Popularity", f"{album.popularity}%", Colors.PURPLE),
        ]
        
        if genres:
            display_genres = genres[:2]
            genre_string = ", ".join(display_genres)
            info_lines.append(self._format_info_line("Genres", genre_string, Colors.RED))
        
        if album.label:
            info_lines.append(self._format_info_line("Label", album.label, Colors.WHITE))
        
        # Add top tracks
        if album.tracks:
            info_lines.append("")
            info_lines.append(f"{Colors.BOLD}Top Tracks{Colors.RESET}")
            
            for i, track in enumerate(album.tracks[:5]):
                track_link = self._create_clickable_link(track.external_urls.spotify, track.name)
                info_lines.append(f"{Colors.GREEN}{track_link}{Colors.RESET}")
        
        # Prepare links
        links = []
        if album.images:
            links.append(f"{Colors.BLUE}{self._create_clickable_link(album.images[0].url, 'Album Cover')}{Colors.RESET}")
        links.append(f"{Colors.GREEN}{self._create_clickable_link(album.external_urls.spotify, 'Spotify')}{Colors.RESET}")
        
        self._display_side_by_side_with_links(image_lines, info_lines, links)
    
    def display_artist(self, artist: Artist, client: Optional[SpotifyClient] = None):
        """Display artist information with profile image"""
        # Get image lines
        image_lines = []
        if artist.images:
            image_lines = self.renderer.render_image_lines(artist.images[0].url)
        else:
            image_lines = self.renderer._get_placeholder_lines()
        
        # Fetch additional artist data
        top_tracks = []
        albums_count = 0
        singles_count = 0
        
        if client:
            try:
                top_tracks = client.get_artist_top_tracks(artist.id)
                albums = client.get_artist_albums(artist.id, 'album')
                singles = client.get_artist_albums(artist.id, 'single')
                albums_count = len(albums)
                singles_count = len(singles)
            except Exception:
                pass
        
        info_lines = [
            self._format_info_line("Name", artist.name, Colors.GREEN),
            self._format_info_line("Followers", self._format_number(artist.followers.total), Colors.YELLOW),
            self._format_info_line("Popularity", f"{artist.popularity}%", Colors.PURPLE),
        ]
        
        if artist.genres:
            display_genres = artist.genres[:2]
            genre_string = ", ".join(display_genres)
            info_lines.append(self._format_info_line("Genres", genre_string, Colors.RED))
        
        if albums_count > 0:
            info_lines.append(self._format_info_line("Albums", str(albums_count), Colors.GREEN))
        
        if singles_count > 0:
            info_lines.append(self._format_info_line("Singles", str(singles_count), Colors.YELLOW))
        
        # Add top tracks
        if top_tracks:
            info_lines.append("")
            info_lines.append(f"{Colors.BOLD}Top Tracks{Colors.RESET}")
            
            for track in top_tracks[:5]:
                track_link = self._create_clickable_link(track.external_urls.spotify, track.name)
                info_lines.append(f"{Colors.GREEN}{track_link}{Colors.RESET}")
        
        # Prepare links
        links = []
        links.append(f"{Colors.GREEN}{self._create_clickable_link(artist.external_urls.spotify, 'Spotify')}{Colors.RESET}")
        if artist.images:
            links.append(f"{Colors.BLUE}{self._create_clickable_link(artist.images[0].url, 'Artist Photo')}{Colors.RESET}")
        
        self._display_side_by_side_with_links(image_lines, info_lines, links)
    
    def _create_clickable_link(self, url: str, text: str) -> str:
        """Create terminal hyperlink using ANSI escape codes"""
        return f'\033]8;;{url}\033\\{text}\033]8;;\033\\'
    
    def _format_info_line(self, label: str, value: str, color: str) -> str:
        """Create consistently formatted label-value pairs"""
        min_padding = 2
        max_label_width = 12
        
        label_width = len(label)
        padding = max_label_width - label_width + min_padding
        if padding < min_padding:
            padding = min_padding
        
        return f"{Colors.BOLD}{label}{Colors.RESET}{' ' * padding}{color}{value}{Colors.RESET}"
    
    def _format_ordinal_date(self, date_str: str) -> str:
        """Convert date string to ordinal format (1st Jan 2020)"""
        if not date_str:
            return "N/A"
        
        try:
            # Parse YYYY-MM-DD format
            date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            try:
                # Fallback to year-only format
                date = datetime.strptime(date_str, "%Y")
                return date.strftime("%Y")
            except ValueError:
                return date_str
        
        day = date.day
        month = date.strftime("%b")
        year = date.year
        
        # Add ordinal suffix
        if 11 <= day <= 13:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
        
        return f"{day}{suffix} {month} {year}"
    
    def _format_duration(self, duration: timedelta) -> str:
        """Convert duration to MM:SS format"""
        total_seconds = int(duration.total_seconds())
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes}:{seconds:02d}"
    
    def _format_number(self, n: int) -> str:
        """Convert large numbers to readable format (1.2M, 15.3K)"""
        if n >= 1000000:
            return f"{n / 1000000:.1f}M"
        elif n >= 1000:
            return f"{n / 1000:.1f}K"
        return str(n)
    
    def _format_bool(self, b: bool) -> str:
        """Convert boolean to Yes/No string"""
        return "Yes" if b else "No"
    
    def _display_side_by_side_with_links(self, image_lines: List[str], info_lines: List[str], links: List[str]):
        """Display image and info side-by-side with links at bottom"""
        max_lines = max(len(image_lines), len(info_lines))
        
        # Pad info lines to match image height minus 2 for link placement
        target_lines = max_lines - 2
        while len(info_lines) < target_lines:
            info_lines.append("")
        
        # Display main content side by side
        for i in range(target_lines):
            image_line = image_lines[i] if i < len(image_lines) else ' ' * 46
            info_line = info_lines[i] if i < len(info_lines) else ""
            print(f"{image_line}   {info_line}")
        
        # Display links
        if links:
            image_line = image_lines[target_lines] if target_lines < len(image_lines) else ' ' * 46
            
            # Separate Spotify and image links
            spotify_link = ""
            image_link = ""
            
            for link in links:
                if 'spotify' in link.lower():
                    spotify_link = link
                else:
                    image_link = link
            
            # Use first link as fallback
            if not spotify_link and links:
                spotify_link = links[0]
            if not image_link and len(links) > 1:
                image_link = links[1]
            
            # Format link line
            if spotify_link and image_link:
                link_line = f"{spotify_link}   {image_link}"
            elif spotify_link:
                link_line = spotify_link
            else:
                link_line = image_link
            
            print(f"{image_line}   {link_line}")
            
            # Display remaining image lines
            for i in range(target_lines + 1, len(image_lines)):
                print(f"{image_lines[i]}   ")
        else:
            # If no links, display remaining image lines normally
            for i in range(target_lines, len(image_lines)):
                print(f"{image_lines[i]}   ")
