import pytest
from app import schemas

def test_get_all_issues(authorized_client, test_issues):
    res = authorized_client.get("/issues/")
    def validate(issue):
        return schemas.IssueOut(**issue)
    issues_map = map(validate, res.json())
    issues_list = list(issues_map)
    assert len(res.json()) == len(test_issues)
    assert res.status_code == 200

def test_unauthorized_user_get_all_issues(client, test_issues):
    res = client.get("/issues/")
    assert res.status_code == 401

def test_unauthorized_user_get_one_issue(client, test_issues):
    res = client.get(f"/issues/{test_issues[0].id}")
    assert res.status_code == 401

def test_get_one_issue_not_exist(authorized_client, test_issues):
    res = authorized_client.get(f"/issues/88888")
    assert res.status_code == 404

def test_get_one_issue(authorized_client, test_issues):
    res = authorized_client.get(f"/issues/{test_issues[0].id}")
    issue = schemas.IssueOut(**res.json())
    assert issue.Issue.id == test_issues[0].id
    assert issue.Issue.content == test_issues[0].content
    assert issue.Issue.title == test_issues[0].title

@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("favorite pizza", "i love pepperoni", False),
    ("tallest skyscrapers", "wahoo", True),
])
def test_create_issue(authorized_client, test_user, test_issues, title, content, published):
    res = authorized_client.post(
        "/issues/", json={"title": title, "content": content, "published": published})
    created_issue = schemas.Issue(**res.json())
    assert res.status_code == 201
    assert created_issue.title == title
    assert created_issue.content == content
    assert created_issue.published == published
    assert created_issue.owner_id == test_user['id']

def test_create_issue_default_published_true(authorized_client, test_user, test_issues):
    res = authorized_client.post(
        "/issues/", json={"title": "arbitrary title", "content": "aasdfjasdf"})
    created_issue = schemas.Issue(**res.json())
    assert res.status_code == 201
    assert created_issue.title == "arbitrary title"
    assert created_issue.content == "aasdfjasdf"
    assert created_issue.published == True
    assert created_issue.owner_id == test_user['id']

def test_unauthorized_user_create_issue(client, test_user, test_issues):
    res = client.post(
        "/issues/", json={"title": "arbitrary title", "content": "aasdfjasdf"})
    assert res.status_code == 401

def test_unauthorized_user_delete_Issue(client, test_user, test_issues):
    res = client.delete(
        f"/issues/{test_issues[0].id}")
    assert res.status_code == 401

def test_delete_issue_success(authorized_client, test_user, test_issues):
    res = authorized_client.delete(
        f"/issues/{test_issues[0].id}")
    assert res.status_code == 204

def test_delete_issue_non_exist(authorized_client, test_user, test_issues):
    res = authorized_client.delete(
        f"/issues/8000000")
    assert res.status_code == 404

def test_delete_other_user_issue(authorized_client, test_user, test_issues):
    res = authorized_client.delete(
        f"/issues/{test_issues[3].id}")
    assert res.status_code == 403

def test_update_issue(authorized_client, test_user, test_issues):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_issues[0].id
    }
    res = authorized_client.put(f"/issues/{test_issues[0].id}", json=data)
    updated_issue = schemas.Issue(**res.json())
    assert res.status_code == 200
    assert updated_issue.title == data['title']
    assert updated_issue.content == data['content']

def test_update_other_user_issue(authorized_client, test_user, test_user2, test_issues):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_issues[3].id
    }
    res = authorized_client.put(f"/issues/{test_issues[3].id}", json=data)
    assert res.status_code == 403

def test_unauthorized_user_update_issue(client, test_user, test_issues):
    res = client.put(
        f"/issues/{test_issues[0].id}")
    assert res.status_code == 401

def test_update_issue_non_exist(authorized_client, test_user, test_issues):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_issues[3].id
    }
    res = authorized_client.put(
        f"/issues/8000000", json=data)
    assert res.status_code == 404
