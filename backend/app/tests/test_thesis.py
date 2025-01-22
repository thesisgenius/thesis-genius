import pytest
from app.models.data import Role


@pytest.fixture
def create_role():
    """
    Fixture to create default roles in the database.
    """
    for role_name in ["Student", "Teacher", "Admin"]:
        Role.get_or_create(name=role_name)


@pytest.fixture
def user_token(client, create_role):
    """
    Fixture to register and log in a user, returning the JWT token.
    """
    client.post(
        "/api/auth/register",
        json={
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "institution": "National University",
            "username": "testuser",
            "password": "password123",
            "role": "Student",
        },
    )
    login_response = client.post(
        "/api/auth/signin",
        json={"email": "test@example.com", "password": "password123"},
    )
    token = login_response.json["token"]
    assert token is not None
    return token


@pytest.fixture
def sample_thesis(client, user_token):
    """
    Fixture to create a sample thesis.
    """
    response = client.post(
        "/api/thesis/new",
        json={
            "title": "Sample Thesis",
            "abstract": "This is a sample abstract.",
            "content": "This is the main content of the thesis.",
            "status": "Draft",
        },
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 201
    return response.json["id"]


@pytest.fixture
def create_thesis(client, user_token):
    """
    Fixture to create a thesis, returning the thesis data.
    """
    response = client.post(
        "/api/thesis/new",
        json={
            "title": "Test Thesis",
            "abstract": "This is a test thesis.",
            "content": "This is the content of the thesis.",
            "status": "Pending",
        },
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 201
    return response.json


def test_create_thesis(client, user_token):
    """
    Test creating a thesis.
    """
    response = client.post(
        "/api/thesis/new",
        json={
            "title": "Test Thesis",
            "abstract": "This is a test thesis.",
            "status": "Pending",
        },
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 201
    assert response.json["success"] is True
    assert response.json["id"] is not None


def test_create_thesis_missing_fields(client, user_token):
    """
    Test creating a thesis with missing required fields.
    """
    response = client.post(
        "/api/thesis/new",
        json={"title": "Incomplete Thesis"},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 400
    assert response.json["success"] is False
    assert "Title, abstract, and status are required" in response.json["message"]


def test_get_theses(client, user_token, create_thesis):
    """
    Test fetching theses for a user.
    """
    response = client.get(
        "/api/thesis/theses", headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    assert response.json["success"] is True
    assert isinstance(response.json["theses"], list)
    assert len(response.json["theses"]) > 0


def test_update_thesis(client, create_thesis, user_token):
    """
    Test updating a thesis.
    """
    thesis_id = create_thesis["id"]

    response = client.put(
        f"/api/thesis/{thesis_id}",
        json={
            "title": "Updated Title",
            "abstract": "Updated Abstract",
            "status": "Approved",
        },
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 200
    assert response.json["success"] is True
    assert "Thesis updated successfully" in response.json["message"]


def test_update_thesis_invalid_id(client, user_token):
    """
    Test updating a thesis with an invalid ID.
    """
    response = client.put(
        "/api/thesis/99999",
        json={
            "title": "Updated Title",
            "abstract": "Updated Abstract",
            "status": "Approved",
        },
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 400
    assert response.json["success"] is False
    assert "Failed to update thesis" in response.json["message"]


def test_delete_thesis(client, create_thesis, user_token):
    """
    Test deleting a thesis.
    """
    thesis_id = create_thesis["id"]

    response = client.delete(
        f"/api/thesis/{thesis_id}",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 200
    assert response.json["success"] is True
    assert "Thesis deleted successfully" in response.json["message"]


def test_delete_thesis_invalid_id(client, user_token):
    """
    Test deleting a thesis with an invalid ID.
    """
    response = client.delete(
        "/api/thesis/99999",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 400
    assert response.json["success"] is False
    assert "Failed to delete thesis" in response.json["message"]


# --- Footnotes Tests ---
def test_add_footnote(client, user_token, sample_thesis):
    """
    Test adding a footnote to a thesis.
    """
    response = client.post(
        f"/api/thesis/{sample_thesis}/footnotes",
        json={"content": "This is a sample footnote."},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 201
    assert response.json["success"] is True
    assert "footnote" in response.json


def test_list_footnotes(client, user_token, sample_thesis):
    """
    Test listing all footnotes for a thesis.
    """
    response = client.get(
        f"/api/thesis/{sample_thesis}/footnotes",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 200
    assert response.json["success"] is True
    assert "footnotes" in response.json


def test_update_footnote(client, user_token, sample_thesis):
    """
    Test updating a footnote.
    """
    # Add a footnote
    add_response = client.post(
        f"/api/thesis/{sample_thesis}/footnotes",
        json={"content": "This is a sample footnote."},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    footnote_id = add_response.json["footnote"]["id"]

    # Update the footnote
    update_response = client.put(
        f"/api/thesis/footnote/{footnote_id}",
        json={"content": "This is an updated footnote."},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert update_response.status_code == 200
    assert update_response.json["success"] is True


def test_delete_footnote(client, user_token, sample_thesis):
    """
    Test deleting a footnote.
    """
    # Add a footnote
    add_response = client.post(
        f"/api/thesis/{sample_thesis}/footnotes",
        json={"content": "This is a sample footnote."},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    footnote_id = add_response.json["footnote"]["id"]

    # Delete the footnote
    delete_response = client.delete(
        f"/api/thesis/footnote/{footnote_id}",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert delete_response.status_code == 200
    assert delete_response.json["success"] is True


# --- Tables Tests ---
def test_add_table(client, user_token, sample_thesis):
    """
    Test adding a table to a thesis.
    """
    response = client.post(
        f"/api/thesis/{sample_thesis}/tables",
        json={"caption": "Sample Table", "file_path": "/path/to/table.png"},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 201
    assert response.json["success"] is True
    assert "table" in response.json


def test_list_tables(client, user_token, sample_thesis):
    """
    Test listing all tables for a thesis.
    """
    response = client.get(
        f"/api/thesis/{sample_thesis}/tables",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 200
    assert response.json["success"] is True
    assert "tables" in response.json


def test_update_table(client, user_token, sample_thesis):
    """
    Test updating a table.
    """
    # Add a table
    add_response = client.post(
        f"/api/thesis/{sample_thesis}/tables",
        json={"caption": "Sample Table", "file_path": "/path/to/table.png"},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    table_id = add_response.json["table"]["id"]

    # Update the table
    update_response = client.put(
        f"/api/thesis/table/{table_id}",
        json={"caption": "Updated Table Caption"},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert update_response.status_code == 200
    assert update_response.json["success"] is True


def test_delete_table(client, user_token, sample_thesis):
    """
    Test deleting a table.
    """
    # Add a table
    add_response = client.post(
        f"/api/thesis/{sample_thesis}/tables",
        json={"caption": "Sample Table", "file_path": "/path/to/table.png"},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    table_id = add_response.json["table"]["id"]

    # Delete the table
    delete_response = client.delete(
        f"/api/thesis/table/{table_id}",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert delete_response.status_code == 200
    assert delete_response.json["success"] is True


def test_add_figure(client, user_token, sample_thesis):
    """
    Test adding a figure to a thesis.
    """
    response = client.post(
        f"/api/thesis/{sample_thesis}/figures",
        json={"caption": "Sample Figure", "file_path": "/path/to/figure.png"},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 201
    assert response.json["success"] is True
    assert "figure" in response.json


def test_list_figures(client, user_token, sample_thesis):
    """
    Test listing all figures for a thesis.
    """
    response = client.get(
        f"/api/thesis/{sample_thesis}/figures",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 200
    assert response.json["success"] is True
    assert "figures" in response.json


def test_update_figure(client, user_token, sample_thesis):
    """
    Test updating a figure.
    """
    # Add a figure
    add_response = client.post(
        f"/api/thesis/{sample_thesis}/figures",
        json={"caption": "Sample Figure", "file_path": "/path/to/figure.png"},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    figure_id = add_response.json["figure"]["id"]

    # Update the figure
    update_response = client.put(
        f"/api/thesis/figure/{figure_id}",
        json={"caption": "Updated Figure Caption"},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert update_response.status_code == 200
    assert update_response.json["success"] is True


def test_delete_figure(client, user_token, sample_thesis):
    """
    Test deleting a figure.
    """
    # Add a figure
    add_response = client.post(
        f"/api/thesis/{sample_thesis}/figures",
        json={"caption": "Sample Figure", "file_path": "/path/to/figure.png"},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    figure_id = add_response.json["figure"]["id"]

    # Delete the figure
    delete_response = client.delete(
        f"/api/thesis/figure/{figure_id}",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert delete_response.status_code == 200
    assert delete_response.json["success"] is True


def test_add_appendix(client, user_token, sample_thesis):
    """
    Test adding an appendix to a thesis.
    """
    response = client.post(
        f"/api/thesis/{sample_thesis}/appendices",
        json={"title": "Sample Appendix", "content": "This is the appendix content."},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 201
    assert response.json["success"] is True
    assert "appendix" in response.json


def test_list_appendices(client, user_token, sample_thesis):
    """
    Test listing all appendices for a thesis.
    """
    response = client.get(
        f"/api/thesis/{sample_thesis}/appendices",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 200
    assert response.json["success"] is True
    assert "appendices" in response.json


def test_update_appendix(client, user_token, sample_thesis):
    """
    Test updating an appendix.
    """
    # Add an appendix
    add_response = client.post(
        f"/api/thesis/{sample_thesis}/appendices",
        json={"title": "Sample Appendix", "content": "This is the appendix content."},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    appendix_id = add_response.json["appendix"]["id"]

    # Update the appendix
    update_response = client.put(
        f"/api/thesis/appendix/{appendix_id}",
        json={"title": "Updated Appendix Title"},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert update_response.status_code == 200
    assert update_response.json["success"] is True


def test_delete_appendix(client, user_token, sample_thesis):
    """
    Test deleting an appendix.
    """
    # Add an appendix
    add_response = client.post(
        f"/api/thesis/{sample_thesis}/appendices",
        json={"title": "Sample Appendix", "content": "This is the appendix content."},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    appendix_id = add_response.json["appendix"]["id"]

    # Delete the appendix
    delete_response = client.delete(
        f"/api/thesis/appendix/{appendix_id}",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert delete_response.status_code == 200
    assert delete_response.json["success"] is True
