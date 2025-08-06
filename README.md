<h1 align="center">mufetch</h1>

<p align="center">Neofetch-style CLI for music written in Python</p>

<p align="center">
<img src="https://img.shields.io/badge/python-3.7+-blue.svg" alt="Python Version">
<img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
</p>

---

## Acknowledgments

This project is originally created and maintained by [ashish0kumar](https://github.com/ashish0kumar/mufetch). Please visit the [original repository](https://github.com/ashish0kumar/mufetch) to show your support.

---

## Features

- **Beautiful terminal display** with album cover art and artist photos
- **Comprehensive metadata** including tracks, albums, and artist information  
- **Interactive clickable links** for Spotify URLs and cover art
- **Responsive sizing** via customizable image dimensions
- **Cross-platform support**, works in all modern terminals
- **Image rendering** with chafa support and fallback ANSI block art

### Supported Content Types

| Type | Metadata Displayed |
|------|-------------------|
| **Tracks** | Name, Artist, Album, Duration, Track Number, Explicit, Release Date, Popularity, Genres |
| **Albums** | Name, Artist, Type, Release Date, Track Count, Duration, Popularity, Genres, Label, Top Tracks |
| **Artists** | Name, Followers, Popularity, Genres, Albums & Singles Count, Top Tracks |

## Installation

### Manual Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/elxecutor/mufetch.git
cd mufetch

# Install dependencies
pip install -r requirements.txt

# Make executable (optional)
chmod +x mufetch.py
```

### Development Installation

```bash
git clone https://github.com/elxecutor/mufetch.git
cd mufetch
pip install -e .
```

After development installation, you can use `mufetch` command directly:
```bash
mufetch auth  # Setup Spotify credentials
mufetch search "your song"
```

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Optional: Install chafa for better image rendering

```bash
# Ubuntu/Debian
sudo apt install chafa

# macOS
brew install chafa

# Arch Linux
sudo pacman -S chafa
```

## Usage

### Setup Authentication

First, set up your Spotify API credentials:

```bash
python mufetch.py auth
```

You'll need to:
1. Go to https://developer.spotify.com/dashboard
2. Create a new app
3. Copy your Client ID and Client Secret

### Search for Music

```bash
# Auto search (tries track, then album, then artist)
python mufetch.py search "Bohemian Rhapsody"

# Search for specific types
python mufetch.py search "Queen" --type artist
python mufetch.py search "A Night at the Opera" --type album
python mufetch.py search "We Will Rock You" --type track

# Customize image size (15-35)
python mufetch.py search "Pink Floyd" --size 25
```

### Command Line Options

```bash
python mufetch.py search --help
```

- `-t, --type`: Search type (auto, track, album, artist) - default: auto
- `-s, --size`: Image size (15-35) - default: 20

## Configuration

Configuration is stored in `~/.config/mufetch/config.yaml`.

You can also set credentials via environment variables:
- `MUFETCH_SPOTIFY_CLIENT_ID`
- `MUFETCH_SPOTIFY_CLIENT_SECRET`

## Project Structure

```
mufetch/
├── mufetch.py              # Main entry point
├── requirements.txt        # Python dependencies
├── setup.py               # Installation script
├── demo.py                # Feature demonstration script
├── README.md              # Project documentation
├── LICENSE                # MIT license
├── CODE_OF_CONDUCT.md     # Code of conduct
├── CONTRIBUTING.md        # Contribution guidelines
├── .github/               # GitHub workflows and templates
└── src/
    ├── __init__.py
    ├── config.py          # Configuration management
    ├── spotify_client.py  # Spotify API client
    ├── display.py         # Terminal display and formatting
    └── commands/
        ├── __init__.py
        ├── auth.py        # Authentication command
        └── search.py      # Search command
```

## Dependencies

- **requests**: HTTP client for Spotify API calls
- **PyYAML**: Configuration file parsing
- **Pillow**: Image processing for fallback rendering

## Image Rendering

The tool supports two image rendering methods:

1. **chafa** (recommended): High-quality terminal graphics
2. **ANSI blocks**: Fallback method using colored terminal blocks

Install chafa for the best visual experience.

## Examples

```bash
# Search for a popular track
python mufetch.py search "Hotel California"

# Find artist information
python mufetch.py search "The Beatles" --type artist

# Look up an album with custom image size
python mufetch.py search "Dark Side of the Moon" --type album --size 30
```

### Demo Script

A demonstration script is included to showcase the features:

```bash
python demo.py
```

This script will walk you through the authentication process and demonstrate various search capabilities.

## Compatibility

- Works on Linux, macOS, and Windows
- Requires a terminal with true color support for best results
- Supports clickable links in compatible terminals

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting pull requests or issues.

## License

MIT License - see LICENSE file for details.
