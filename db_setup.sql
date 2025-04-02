CREATE DATABASE Git_tracker;
CREATE USER your_db_user WITH PASSWORD 'Root12345';
ALTER ROLE your_db_user SET client_encoding TO 'utf8';
ALTER ROLE your_db_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE your_db_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE git_tracker_db TO your_db_user;
