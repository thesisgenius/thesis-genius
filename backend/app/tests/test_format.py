from io import BytesIO
from unittest.mock import patch


@patch(
    "app.services.apaservice.APAService.get_thesis_data",
    return_value={"cover": {"title": "Sample Thesis"}},
)
def test_get_apa_format_json(mock_get_thesis_data, client, user_token):
    """
    Test get_apa_format with format=json, requiring a real auth token.
    """
    response = client.get(
        "/api/format/apa/1?format=json",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 200


@patch(
    "app.services.apaservice.APAService.get_thesis_data",
    return_value={"cover": {"title": "Sample Thesis"}},
)
def test_get_apa_format_html(mock_get_thesis_data, client, user_token):
    """
    Test get_apa_format with format=html.
    """
    with patch(
        "app.utils.formatter.APAFormatter.to_html",
        return_value="<html>Sample Thesis</html>",
    ):
        response = client.get(
            "/api/format/apa/1?format=html",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 200


@patch(
    "app.services.apaservice.APAService.get_thesis_data",
    return_value={"cover": {"title": "Sample Thesis"}},
)
def test_get_apa_format_docx(mock_get_thesis_data, client, user_token):
    fake_docx = BytesIO(b"Fake DOCX data")
    with patch("app.utils.formatter.APAFormatter.to_docx", return_value=fake_docx):
        response = client.get(
            "/api/format/apa/1?format=docx",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 200


@patch(
    "app.services.apaservice.APAService.get_thesis_data",
    return_value={"cover": {"title": "Sample Thesis"}},
)
def test_get_apa_format_pdf(mock_get_thesis_data, client, user_token):
    fake_pdf = BytesIO(b"Fake PDF data")
    with patch("app.utils.formatter.APAFormatter.to_pdf", return_value=fake_pdf):
        response = client.get(
            "/api/format/apa/1?format=pdf",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 200


@patch(
    "app.services.apaservice.APAService.get_thesis_data",
    return_value={"cover": {"title": "Sample Thesis"}},
)
def test_get_apa_format_unsupported_format(mock_get_thesis_data, client, user_token):
    """
    Test get_apa_format with unsupported format.
    """
    response = client.get(
        "/api/format/apa/1?format=unsupported",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 400


@patch("app.services.apaservice.APAService.get_thesis_data", return_value=None)
def test_get_apa_format_not_found(mock_get_thesis_data, client, user_token):
    """
    Test get_apa_format when thesis is not found.
    """
    response = client.get(
        "/api/format/apa/1", headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 404


@patch(
    "app.services.apaservice.APAService.get_thesis_data",
    side_effect=ValueError("Invalid data"),
)
def test_get_apa_format_value_error(mock_get_thesis_data, client, user_token):
    """
    Test get_apa_format when a ValueError occurs.
    """
    response = client.get(
        "/api/format/apa/1", headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 404


@patch(
    "app.services.apaservice.APAService.get_thesis_data",
    side_effect=Exception("Unexpected error"),
)
def test_get_apa_format_generic_error(mock_get_thesis_data, client, user_token):
    """
    Test get_apa_format when a generic exception occurs.
    """
    response = client.get(
        "/api/format/apa/1", headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 500
