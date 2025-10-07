# Code Style & Project Conventions

## File Organization
- **Clear directory structure**: Organized by function (warp/, logs/, backups/, etc.)
- **Template-based configuration**: Use `.template` files with environment variable substitution
- **Documentation**: README.md files in each major directory
- **Security**: Never commit secrets - use environment variables

## Shell Script Conventions (from setup-mcp.sh)
- Executable permissions on shell scripts
- Clear error handling and user feedback
- Environment variable validation
- Use of `envsubst` for template processing

## Configuration Management
- **Template Pattern**: Use `.template` files with placeholder variables
- **Environment Variables**: Secure secret management via env vars
- **Portability**: Cross-machine deployment considerations
- **Version Control**: Git-friendly structure without sensitive data

## Database Conventions
- SQLite for local data storage
- Migration system for schema changes
- Organized in migrations/ directory

## Documentation Standards
- Comprehensive README files
- Step-by-step setup instructions
- Troubleshooting sections
- Cross-reference related configurations