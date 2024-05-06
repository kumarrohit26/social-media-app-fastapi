from typing import List
from app import schemas
import pytest


# Test related to retreiving posts
def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    posts = res.json()

    def validate(post):
        return schemas.PostOut(**post)
    post_map = map(validate, posts)
    posts_list = list(post_map)

    assert res.status_code == 200
    assert len(res.json()) == len(test_posts)
    #assert posts_list[0].Post.id == test_post[0].id

def test_unauthorized_user_get_all_post(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_exists(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/88888")
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert res.status_code == 200
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title

# Create post tests

@pytest.mark.parametrize('title, content, published',[
    ('Title 1', 'Content 1', True),
    ('Title 2', 'Content 2', False),
    ('Title 3', 'Content 3', False)
])
def test_create_post(authorized_client, test_posts, test_user, title, content, published):
    res = authorized_client.post("/posts/", json={'title': title, 'content': content, 'published': published})

    created_post = schemas.Post(**res.json())

    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.user_id == test_user['id']

def test_create_post_default_published(authorized_client, test_posts, test_user):
    res = authorized_client.post("/posts/", json={'title': 'title 4', 'content': 'content 4'})

    created_post = schemas.Post(**res.json())

    assert res.status_code == 201
    assert created_post.title == 'title 4'
    assert created_post.content == 'content 4'
    assert created_post.published == True
    assert created_post.user_id == test_user['id']

def test_unauthorized_user_create_post(client, test_posts, test_user):
    res = client.post("/posts/", json={'title': 'title 5', 'content': 'content 5'})
    assert res.status_code == 401

# Delete a post test

def test_unauthorized_user_delete_post(client, test_posts, test_user):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post_success(authorized_client, test_posts, test_user):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_post_non_exist(authorized_client, test_posts, test_user):
    res = authorized_client.delete(f"/posts/8888")
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_posts, test_user):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403

# Update a post test

def test_update_post(authorized_client, test_posts, test_user):
    data = {
        'title': 'updated title',
        'content': 'updated content',
        'id': test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json = data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']

def test_update_other_user_post(authorized_client, test_posts, test_user):
    data = {
        'title': 'updated title',
        'content': 'updated content',
        'id': test_posts[3].id
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json = data)
    assert res.status_code == 403

def test_unauthorized_user_update_post(client, test_posts, test_user):
    data = {
        'title': 'updated title',
        'content': 'updated content',
        'id': test_posts[3].id
    }
    res = client.put(f"/posts/{test_posts[0].id}", json = data)
    assert res.status_code == 401

def test_update_post_non_exist(authorized_client, test_posts, test_user):
    data = {
        'title': 'updated title',
        'content': 'updated content',
        'id': test_posts[3].id
    }
    res = authorized_client.put(f"/posts/8888", json = data)
    assert res.status_code == 404
