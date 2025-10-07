# Development Environment & Infrastructure

## Container System
- **Docker**: Engine Community Edition 28.0.0 with Orbstack (NOT Podman)
- **Platform**: macOS arm64 (M1 Mac)

## Key Container Workflows
- **Audiobookshelf**: Container named 'orb'
- **auto-m4b**: Audio processing container
- Directory bind mounts for media processing workflows

## File System Layout
- **Main work directory**: `/Users/cerinawithasea/Music`
- **Project files**: `/Volumes/Cerina/Documents/4warp/`
- **Config directory**: `/Users/cerinawithasea/config` (current project)
- **AI documentation**: `/Users/cerinawithasea/Documents/shAIs stuff`

## Hardware Considerations
- M1 Mac-specific container compatibility requirements
- Need to verify arm64 support for containers