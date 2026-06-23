# MySQL Initialization for NileVoice AI

This folder contains the MySQL initialization script used by the production Docker Compose deployment.

## Files

- `init.sql` - creates the database schema and tables with MySQL-compatible configuration.

## Notes

- The `docker-compose.prod.yml` file mounts this script into `docker-entrypoint-initdb.d/`.
- It runs only when the MySQL container initializes a new data volume.
- If the volume already exists, this file will not be re-run automatically.
