-- migrate:up
create extension if not exists "uuid-ossp";

create schema if not exists api_data;

create table if not exists api_data.teams
(
    id uuid primary key default uuid_generate_v4(),
    name text not null,
    creation_date date not null
);

create table if not exists api_data.projects
(
    id uuid primary key default uuid_generate_v4(),
    name text not null,
    start_date date not null,
    status text not null
);

create table if not exists api_data.project_to_team
(
    team_id uuid references api_data.teams(id),
    project_id uuid references api_data.projects(id),
    primary key (team_id, project_id)
);

insert into api_data.teams(name, creation_date)
values 
    ('Альфа', '2012-06-01'),
    ('Бета', '2021-08-19'),
    ('Гамма', '2023-03-11'),
    ('Дельта', '2023-08-11'),
    ('Сигма', '2022-03-15');

insert into api_data.projects(name, start_date, status)
values 
    ('Первый', '2021-05-12', 'В процессе'),
    ('Второй', '2020-03-21', 'Завершен'),
    ('Третий', '2023-07-09', 'На паузе'),
    ('Четвертый', '2022-10-22', 'В процессе');

insert into api_data.project_to_team(team_id, project_id)
values
    ((select id from api_data.teams where name = 'Альфа'), 
     (select id from api_data.projects where name = 'Первый')),
    ((select id from api_data.teams where name = 'Бета'), 
     (select id from api_data.projects where name = 'Первый')),
    ((select id from api_data.teams where name = 'Бета'), 
     (select id from api_data.projects where name = 'Третий')),
    ((select id from api_data.teams where name = 'Гамма'), 
     (select id from api_data.projects where name = 'Второй')),
    ((select id from api_data.teams where name = 'Дельта'), 
     (select id from api_data.projects where name = 'Первый')),
    ((select id from api_data.teams where name = 'Сигма'), 
     (select id from api_data.projects where name = 'Четвертый'));

-- migrate:down