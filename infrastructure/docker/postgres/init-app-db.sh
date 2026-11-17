#!/bin/bash
set -e

# ==============================================================================
# Dedicated Application Database & User Initialization
# ==============================================================================
# This script runs during the initial startup of the PostgreSQL container.
# It creates a dedicated application user with restricted privileges, ensuring
# the application never connects using the 'postgres' superuser.
# ==============================================================================

echo "Initializing Project Babel dedicated application user and database..."

APP_USER="${APP_DB_USER:-babel_app}"
APP_PASS="${APP_DB_PASSWORD:-babel_dev_password}"
APP_DB="${POSTGRES_DB:-babel_db}"

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Create application user if not exists
    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '$APP_USER') THEN
            CREATE ROLE $APP_USER WITH LOGIN PASSWORD '$APP_PASS' NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT;
        END IF;
    END
    \$\$;

    -- Ensure database permissions
    GRANT CONNECT ON DATABASE $APP_DB TO $APP_USER;
EOSQL

# Connect to target database to configure schema permissions
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$APP_DB" <<-EOSQL
    -- Grant schema privileges
    GRANT USAGE, CREATE ON SCHEMA public TO $APP_USER;
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO $APP_USER;
    GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO $APP_USER;

    -- Set default privileges for future tables and sequences created in this schema
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO $APP_USER;
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO $APP_USER;
EOSQL

echo "Application database and user initialized successfully."
