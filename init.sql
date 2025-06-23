-- Initialize the spades3 database
-- This script runs when the PostgreSQL container starts for the first time

-- Create the database if it doesn't exist
-- (PostgreSQL creates it automatically based on POSTGRES_DB environment variable)

-- Set timezone
SET timezone = 'UTC';

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Grant necessary permissions
GRANT ALL PRIVILEGES ON DATABASE spades3 TO postgres;

-- Log successful initialization
DO $$
BEGIN
    RAISE NOTICE 'Spades3 database initialized successfully';
END $$; 