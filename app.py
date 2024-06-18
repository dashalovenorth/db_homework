from flask import Flask
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import request
from psycopg2.sql import SQL, Literal
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)
app.json.ensure_ascii = False

connection = psycopg2.connect(
    host=os.getenv('POSTGRES_HOST') if os.getenv('DEBUG_MODE') == 'false' else 'localhost',
    port=os.getenv('POSTGRES_PORT'),
    database=os.getenv('POSTGRES_DB'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
    cursor_factory=RealDictCursor
)
connection.autocommit = True

@app.get("/teams")
def get_teams():
    query = """
with 
    teams_with_projects as (
        select
            t.id,
            t.name,
            t.creation_date,
            coalesce(jsonb_agg(jsonb_build_object(
                'id', p.id, 'name', p.name, 'start_date', p.start_date, 'status', p.status))
                filter (where p.id is not null), '[]') as projects
            from api_data.teams t
            left join api_data.project_to_team pt on t.id = pt.team_id
            left join api_data.projects p on p.id = pt.project_id
            group by t.id
        ),
        teams_with_employees as (
            select
                te.id,
                coalesce(json_agg(json_build_object(
                'id', em.id, 'first_name', em.first_name, 'last_name', em.last_name, 'position', em.position))
                    filter (where em.id is not null), '[]') as employees
            from api_data.teams te
            left join api_data.employees em on te.id = em.team_id
            group by te.id
        )
select twp.id, name, creation_date, projects, employees
from teams_with_projects twp
join teams_with_employees twe on twp.id = twe.id
"""

    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

    return result

@app.post('/teams/create')
def create_team():
    body = request.json

    name = body['name']
    creation_date = body['creation_date']

    query = SQL("""
insert into api_data.teams(name, creation_date)
values ({name}, {creation_date})
returning id
""").format(name=Literal(name), creation_date=Literal(creation_date))
    
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchone()

    return result

@app.put('/teams/update')
def update_team():
    body = request.json

    id = body['id']
    name = body['name']
    creation_date = body['creation_date']

    query = SQL("""
update api_data.teams
set
    name = {name},
    creation_date = {creation_date}
where id = {id}
returning id
""").format(name=Literal(name), creation_date=Literal(creation_date), id=Literal(id))
    
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

    if len(result) == 0:
        return '', 404

    return '', 204

@app.delete('/teams/delete')
def delete_team():
    body = request.json

    id = body['id']

    deleteTeamLinks = SQL(
        "delete from api_data.project_to_team where team_id = {id}").format(
            id=Literal(id))
    deleteTeam = SQL("delete from api_data.teams where id = {id}").format(
        id=Literal(id))
    
    with connection.cursor() as cursor:
        cursor.execute(deleteTeamLinks)
        cursor.execute(deleteTeam)

    return '', 204

@app.get('/teams/find_by_name')
def get_team_by_name():
    name = request.args.get('name')

    query = SQL("""
select id, name, creation_date
from api_data.teams
where name ilike {name}
""").format(name=Literal(name))
    
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

    return result

@app.get('/teams/find_by_creation_date')
def get_team_by_creation_date():
    creation_date = request.args.get('creation_date')

    query = SQL("""
select id, name, creation_date
from api_data.teams
where creation_date = {creation_date}
""").format(creation_date=Literal(creation_date))
    
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

    return result

if __name__ == '__main__':
    app.run(port=os.getenv('FLASK_PORT'))