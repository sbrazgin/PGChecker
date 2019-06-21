Easy PostgreSql databases status checker

1) create PostgreSql user:
1.1)
CREATE USER pgmonitor WITH PASSWORD '......' CONNECTION LIMIT 2;
REVOKE ALL ON SCHEMA public FROM pgmonitor;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO pgmonitor;
grant select on pg_stat_replication to pgmonitor;
grant pg_read_all_stats to pgmonitor;

CREATE FUNCTION func_stat_replication() RETURNS SETOF pg_stat_replication as
$$ select * from pg_stat_replication; $$
LANGUAGE sql SECURITY DEFINER;

REVOKE EXECUTE ON FUNCTION func_stat_replication() FROM public;
GRANT EXECUTE ON FUNCTION func_stat_replication() to pgmonitor;


1.2) add to pg_hba:

host    postgres        pgmonitor       all                     md5

1.3) reload

1.4) check login:
 psql -d postgres -U pgmonitor
 
2) add db...ini file

3) Example out check file:


=====================================================================================
== Database: hostName=srv-.....-pg01, portNumber=5432, database=......
=====================================================================================
 
-------------------------------------------------------
-- cache hit ratio
-------------------------------------------------------
Value : 0.99 OK
 
-------------------------------------------------------
-- session count info
-------------------------------------------------------
ehdapi2              NULL                       4
pgmonitor            active                     1
postgres             NULL                       1
NULL                 NULL                       4
 
-------------------------------------------------------
-- Size of all databases
-------------------------------------------------------
database_name        | size_in_mb          
-------------        | ---------           
postgres             |         17          
template1            |          7          
template0            |          7          
template_postgis     |         14          
ehdapi2              |         19          
 

 
 