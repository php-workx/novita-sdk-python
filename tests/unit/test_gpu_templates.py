"""Tests for templates API."""

import pytest
from pytest_httpx import HTTPXMock

from novita import NovitaClient


def test_list_templates(httpx_mock: HTTPXMock) -> None:
    """Test listing templates."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/templates",
        json={"templates": []},
    )

    client = NovitaClient(api_key="test-key")
    response = client.gpu.templates.list()

    assert "templates" in response
    assert isinstance(response["templates"], list)
    client.close()


def test_get_template(httpx_mock: HTTPXMock) -> None:
    """Test getting a specific template."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/template?template_id=tpl-123",
        json={"template_id": "tpl-123", "name": "My Template"},
    )

    client = NovitaClient(api_key="test-key")
    response = client.gpu.templates.get("tpl-123")

    assert response["template_id"] == "tpl-123"
    client.close()


def test_create_template(httpx_mock: HTTPXMock) -> None:
    """Test creating a template."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/template/create",
        json={"template_id": "tpl-new", "name": "New Template"},
    )

    client = NovitaClient(api_key="test-key")
    response = client.gpu.templates.create(name="New Template", instance_id="inst-123")

    assert response["template_id"] == "tpl-new"
    client.close()


def test_delete_template(httpx_mock: HTTPXMock) -> None:
    """Test deleting a template."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/template/delete",
        status_code=200,
    )

    client = NovitaClient(api_key="test-key")
    client.gpu.templates.delete("tpl-123")

    request_made = httpx_mock.get_request()
    assert request_made.method == "POST"
    client.close()


@pytest.mark.asyncio
async def test_async_list_templates(httpx_mock: HTTPXMock) -> None:
    """Test listing templates using async client."""
    from novita import AsyncNovitaClient

    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/templates",
        json={"templates": [{"template_id": "tpl-1"}]},
    )

    async with AsyncNovitaClient(api_key="test-key") as client:
        response = await client.gpu.templates.list()

        assert len(response["templates"]) == 1
