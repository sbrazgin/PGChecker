Easy PostgreSql databases status checker

1) create user:

CREATE USER pgmonitor WITH PASSWORD 'pgmonitor' CONNECTION LIMIT 2;
REVOKE ALL ON SCHEMA public FROM pgmonitor;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO pgmonitor;


2) add to pg_hba:

host    postgres        pgmonitor       all                     md5

3) reload

4) check login:
 psql -d postgres -U pgmonitor
 
 