from app import schemas
import pytest


def test_get_all_posts(authorized_client, test_posts):

    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)
    posts_map = map(validate, res.json())

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_unauthorized_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id + 100}")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    print(res.json())
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert res.status_code == 200


@pytest.mark.parametrize("title, content, published", [
    ("awesome pizza", "this is awesome peporining", True),
    ("awesome pizza", "this is awesome chicken", False),
    ("awesome pizza", "this is awesome bbq", False)])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post(
        "/posts/", json={"title": title, "content": content, "published": published})
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published


def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post(
        "/posts/", json={"title": "awesome pizza", "content": "this is awesome peporining"})
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.published == True


@pytest.mark.parametrize("title, content, published", [
    ("awesome pizza", "this is awesome peporining", None),
    ("awesome pizza", None, False),
    (None, "this is awesome bbq", False)])
def test_create_post_invalid_data(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post(
        "/posts/", json={"title": title, "content": content, "published": published})
    assert res.status_code == 422


def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post(
        "/posts/", json={"title": "arbitrary title", "content": "arbitrary content"})
    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_delete_post_success(authorized_client, test_posts, session):
    len_post = len(test_posts)

    # Add the test_posts[0] to the session
    session.add(test_posts[0])

    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    print("Response Status Code:", res.status_code)
    assert res.status_code == 204
    res = authorized_client.get("/posts/")
    assert len(res.json()) == len_post - 1


def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[0].id + 1000000000000000}")
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts, test_user2):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403


def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']


def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title 4",
        "content": "updated content 4",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id + 1000000000000000
    }
    res = authorized_client.put(
        f"/posts/{test_posts[0].id + 1000000000000000}", json=data)
    assert res.status_code == 404
