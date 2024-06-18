-- migrate:up

insert into api_data.teams (name, creation_date)
select SUBSTRING(MD5(RANDOM()::TEXT) FROM 1 FOR 20), NOW() + (random() * (NOW()+'90 days' - NOW())) + '30 days'
from generate_series(1, 100000);
create index teams_creation_date_idx on api_data.teams using btree(creation_date);

create extension pg_trgm;
create index teams_name_idx on api_data.teams using gist(name gist_trgm_ops);

-- migrate:down

