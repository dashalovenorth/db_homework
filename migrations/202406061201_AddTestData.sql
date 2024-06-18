-- migrate:up

create table if not exists api_data.employees
(
    id uuid primary key default uuid_generate_v4(),
    team_id uuid references api_data.teams not null,
    first_name text,
    last_name text,
    position text
);

insert into api_data.employees(team_id, first_name, last_name, position)
values ((select id from api_data.teams where name = 'Сигма'), 'Андрей', 'Иванов', 'программист'),
       ((select id from api_data.teams where name = 'Альфа'), 'Илья', 'Смирнов', 'разработчик'),
       ((select id from api_data.teams where name = 'Бета'), 'Кирилл', 'Петров', 'художник'),
       ((select id from api_data.teams where name = 'Гамма'), 'Андрей', 'Попов', 'повар'),
       ((select id from api_data.teams where name = 'Сигма'), 'Илья', 'Иванов', 'художник');

-- migrate:down