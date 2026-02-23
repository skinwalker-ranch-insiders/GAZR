# GAZR - Gazing Adaptive Zoom Robot

A Python-based automation tool that integrates YouTube Live Chat with Stellarium astronomy software to enable real-time remote control of a telescope through chat commands.

## Overview

GAZR monitors YouTube Live Chat for specific command hashtags and relays them to Stellarium's remote control API, allowing moderators to direct a telescope to celestial objects mentioned in the chat stream.

## Video Demonstration

See GAZR in action: https://www.youtube.com/watch?v=pwOECgUMnO8

## Features

- **YouTube Live Chat Integration**: Real-time chat monitoring using the pytchat library
- **Stellarium API Integration**: HTTP-based remote control of Stellarium astronomy software
- **User Mode System**: Configurable permission levels (#UMODE) for command access control
- **Horizon Checking**: Validates celestial objects are visible before issuing commands
- **Moderator Privileges**: Automatic permission elevation for YouTube chat moderators/owners
- **Auto-Restart Capability**: Shell script wrapper for automatic process recovery
- **Docker Support**: Containerized deployment ready

## Technical Stack

- **Language**: Python 3.9+
- **Libraries**: pytchat, mechanize, BeautifulSoup4, requests
- **Target Software**: Stellarium (desktop planetarium)
- **Container**: Docker

## Installation

### Local Setup

```bash
git clone https://github.com/skinwalker-ranch-insiders/gazr.git
cd gazr
pip install -r requirements.txt
```

### Docker Setup

```bash
docker build -t gazr .
docker run -it --name gazr --rm --volume $(pwd):/usr/src/gazr --net=host gazr:latest sh ./rcloak.sh
```

## Configuration

Edit `settings.py` with your credentials:

```python
S_LOGIN = 'your_insiders_email@example.com'
S_PASSWORD = 'your_password'
STELLARIUM_SERVER = '192.168.1.100'  # IP of Stellarium host
STELLARIUM_PORT = '8090'
USER_LIST = ["user1", "user2"]  # Approved users for restricted commands
```

## Available Commands

| Command | Description |
|---------|-------------|
| `#SKY <object>` | Point telescope at specified celestial object |
| `#ZOOMIN` | Zoom in (placeholder) |
| `#ZOOMOUT` | Zoom out (placeholder) |
| `#HOME` | Return to home position (placeholder) |
| `#UMODE 1/2` | Switch user mode (1=restricted, 2=open) |

## Project Structure

```
GAZR/
├── gazr.py          # Main application logic
├── settings.py     # Configuration file
├── requirements.txt # Python dependencies
├── Dockerfile      # Docker image definition
├── rcloak.sh       # Auto-restart wrapper script
└── LICENSE          # Public domain license
```

## Key Implementation Details

- **Authentication**: Uses mechanize for web form authentication to access the YouTube stream
- **API Communication**: RESTful HTTP requests to Stellarium's built-in web server
- **Chat Parsing**: Regex-based command detection with case-insensitive matching
- **Error Handling**: Automatic reconnection on stream disconnect
- **Logging**: Configurable logging for debugging and monitoring

## License

This project is released into the public domain under the terms of the Unlicense. See [LICENSE](LICENSE) for details.

## Acknowledgments

- [pytchat](https://pytchat.readthedocs.io/) - YouTube chat extraction library
- Skinwalker Ranch Insiders community for testing and feedback
