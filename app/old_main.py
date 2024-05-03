from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import time

import psycopg2
from  psycopg2.extras import RealDictCursor


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
    try:
        conn = psycopg2.connect(host='127.0.0.1', database='fastapi', user='postgres', password='mysql', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database Connection established...')
        break
    except Exception as error:
        print('Database Connection failed...')
        print('Error: ', error)
        time.sleep(2)


my_posts = [{"id": 1, "title": "post 1 title", "content": "post 1 content"},
            {"id": 2, "title": "favorite foods", "content": "pizza"}]

def find_posts(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

@app.get("/")
async def root():
    return {"message": "Welcome to my api."}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f"post with id {id} not found.")
    return {"post_details": post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    # Here we are using placeholder (%s) to replace values as the execute mehod will sanitize the inputs and it will check if there is any sql queries passed as input.
    # It helps to prevent SQL injection.
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, id))
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f"post with id {id} not found.")
    
    return {"data": updated_post}
