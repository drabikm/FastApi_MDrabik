import sqlite3
from http.client import HTTPException

from fastapi import FastAPI, HTTPException
from typing import Any

app = FastAPI()

@app.get('/movies')
def get_movies():
    db = sqlite3.connect('movies-extended.db')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM movie')
    movies = []
    for row in cursor:
        movie = {"id": row[0], "title": row[1], "director": row[2], "year": row[3], "description": row[4]}
        movies.append(movie)
    return movies

@app.get('/movies/{movie_id}')
def get_single_movie(movie_id:int):
    db = sqlite3.connect('movies-extended.db')
    cursor = db.cursor()
    movie = cursor.execute(f'SELECT * FROM movie where ID = {movie_id}').fetchone()
    if not movie:
        raise HTTPException(status_code=404, detail=f'Movie with id {movie_id} does not exist in database')
    return {"id": movie[0], "title": movie[1], "director": movie[2], "year": movie[3], "description": movie[4]}

@app.post("/movies")
def add_movie(params: dict[str, Any]):
    if "title" in params and "year" in params and "director" in params and "description" in params:
        db = sqlite3.connect('movies-extended.db')
        cursor = db.cursor()
        cursor.execute(f'INSERT INTO movie (title, director, year, description) VALUES ("{params.get('title')}","{params.get('director')}","{params.get('year')}", "{params.get('description')}")')
        db.commit()
    else:
        raise HTTPException(status_code=400, detail="Data is incomplete, check your request")

    return {f"Movie added successfully with id: {cursor.lastrowid}"}

@app.put("/movies/{movie_id}")
def update_movie(params: dict[str, Any], movie_id:int):
    db = sqlite3.connect('movies-extended.db')
    cursor = db.cursor()
    movie = cursor.execute(f'SELECT * FROM movie where ID = {movie_id}').fetchone()
    if not movie:
        raise HTTPException(status_code=404, detail=f'Movie with id {movie_id} does not exist in database')
    title = params.get('title')
    year = params.get('year')
    director = params.get('director')
    description = params.get('description')
    cursor.execute(f"""UPDATE movie SET title='{title}', director='{director}', year='{year}', description='{description}' WHERE id='{movie_id}'""")
    db.commit()
    return {f"Movie edited successfully"}

@app.delete("/movies/{movie_id}")
def deleteMovie(movie_id:int):
    db = sqlite3.connect('movies-extended.db')
    cursor = db.cursor()
    movie = cursor.execute(f'SELECT * FROM movie where ID = {movie_id}').fetchone()
    if not movie:
        raise HTTPException(status_code=404, detail=f'Movie with id {movie_id} does not exist in database')
    cursor.execute(f'DELETE from movie where id = {movie_id}')
    db.commit()
    return {"message": f"Movie with id {movie_id} deleted successfully!"}

@app.delete("/movies")
def delete_many_movies(params: dict[str, Any]):
    movies_to_delete = tuple(params.get("ids_movies_to_delete"))
    db = sqlite3.connect('movies-extended.db')
    cursor = db.cursor()
    cursor.execute(f'DELETE from movie where id IN {movies_to_delete}')
    db.commit()
    return {"message": f"No of movies: {cursor.rowcount} deleted successfully! None of the IDs you provided exist in the database anynmore :)"}

@app.get('/actors')
def get_movies():
    db = sqlite3.connect('movies-extended.db')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM movie_actor_through')
    actors = []
    for row in cursor:
        actor = {"id": row[0], "name": row[1], "surname": row[2]}
        actors.append(actor)
    return actors

@app.get('/actors/{actor_id}')
def get_single_movie(actor_id:int):
    db = sqlite3.connect('movies-extended.db')
    cursor = db.cursor()
    actor = cursor.execute(f'SELECT * FROM actor where ID = {actor_id}').fetchone()
    if not actor:
        raise HTTPException(status_code=404, detail=f'Actor with id {actor_id} does not exist in database')
    return {"id": actor[0], "name": actor[1], "surname": actor[2]}

@app.post("/actors")
def add_movie(params: dict[str, Any]):
    if "name" in params and "surname" in params:
        db = sqlite3.connect('movies-extended.db')
        cursor = db.cursor()
        cursor.execute(f'INSERT INTO actor (name, surname) VALUES ("{params.get('name')}", "{params.get('surname')}")')
        db.commit()
    else:
        raise HTTPException(status_code=400, detail="Data is incomplete, check your request")

    return {f"Actor added successfully with id: {cursor.lastrowid}"}

@app.delete("/actors/{actor_id}")
def deleteMovie(actor_id:int):
    db = sqlite3.connect('movies-extended.db')
    cursor = db.cursor()
    actor = cursor.execute(f'SELECT * FROM actor where ID = {actor_id}').fetchone()
    if not actor:
        raise HTTPException(status_code=404, detail=f'Actor with id {actor_id} does not exist in database')
    cursor.execute(f'DELETE from actor where id = {actor_id}')
    db.commit()
    return {"message": f"Actor with id {actor_id} deleted successfully!"}

@app.put("/actors/{actor_id}")
def update_movie(params: dict[str, Any], actor_id:int):
    db = sqlite3.connect('movies-extended.db')
    cursor = db.cursor()
    actor = cursor.execute(f'SELECT * FROM actor where ID = {actor_id}').fetchone()
    if not actor:
        raise HTTPException(status_code=404, detail=f'Actor with id {actor_id} does not exist in database')
    name = params.get('name')
    surname = params.get('surname')
    cursor.execute(f"""UPDATE actor SET name='{name}', surname='{surname}' WHERE id='{actor_id}'""")
    db.commit()
    return {f"Actor edited successfully"}

@app.get("/movies/{movie_id}/actors")
def get_actors_for_movie(movie_id:int):
    db = sqlite3.connect('movies-extended.db')
    cursor = db.cursor()
    movie = cursor.execute(f'SELECT * FROM movie where ID = {movie_id}').fetchone()
    if not movie:
        raise HTTPException(status_code=404, detail=f'Movie with id {movie_id} does not exist in database')
    cursor.execute(f'SELECT actor.name, actor.surname FROM actor INNER JOIN movie_actor_through ON movie_actor_through.actor_id = actor.id where movie_actor_through.movie_id = {movie_id}')
    actors = []
    for row in cursor:
        actor = {"Name": row[0], "Surname": row[1]}
        actors.append(actor)
    if not actors:
        return f'There is no actor for movie with id {movie_id}'
    else:
        return {f"Actors {actors}"}