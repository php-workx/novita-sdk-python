"""Tests for templates API."""

import pytest
from pytest_httpx import HTTPXMock

from novita import NovitaClient
from novita.generated.models import (
    CreateTemplateRequest,
    CreateTemplateResponse,
    Template,
    TemplateCreatePayload,
)


def _template_payload(**overrides: object) -> dict[str, object]:
    base = {
        "Id": "tpl-1",
        "name": "Template 1",
        "type": "instance",
        "channel": "private",
        "image": "repo/image:tag",
        "startCommand": "bash run.sh",
        "rootfsSize": 50,
    }
    base.update(overrides)
    model = Template.model_validate(base)
    return model.model_dump(by_alias=True, mode="json")


def test_list_templates(httpx_mock: HTTPXMock) -> None:
    """Test listing templates."""
    mock_templates = [
        _template_payload(Id="tpl-1", name="Serving template"),
        _template_payload(Id="tpl-2", name="Batch template"),
    ]
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/templates",
        json={
            "template": mock_templates,
            "pageSize": len(mock_templates),
            "pageNum": 1,
            "total": len(mock_templates),
        },
    )

    client = NovitaClient(api_key="test-key")
    templates = client.gpu.templates.list()

    assert isinstance(templates, list)
    assert len(templates) == 2
    assert isinstance(templates[0], Template)
    assert templates[0].id == "tpl-1"
    assert templates[0].name == "Serving template"
    assert templates[1].id == "tpl-2"
    client.close()


def test_get_template(httpx_mock: HTTPXMock) -> None:
    """Test getting a specific template."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.novita.ai/gpu-instance/openapi/v1/template?templateId=tpl-123",
        json={"template": _template_payload(Id="tpl-123", name="My Template")},
    )

    client = NovitaClient(api_key="test-key")
    template = client.gpu.templates.get("tpl-123")

    assert isinstance(template, Template)
    assert template.id == "tpl-123"
    assert template.name == "My Template"
    client.close()


def test_create_template(httpx_mock: HTTPXMock) -> None:
    """Test creating a template."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.novita.ai/gpu-instance/openapi/v1/template/create",
        json={"templateId": "tpl-new"},
    )

    client = NovitaClient(api_key="test-key")
    # Create a minimal TemplateCreatePayload for testing
    template_payload = TemplateCreatePayload.model_validate(
        {
            "name": "New Template",
            "readme": "Test template",
            "type": "instance",
            "channel": "private",
            "image": "docker.io/test:latest",
            "startCommand": "bash run.sh",
            "rootfsSize": 50,
            "ports": [],
            "volumes": [],
            "envs": [],
        }
    )
    response = client.gpu.templates.create(CreateTemplateRequest(template=template_payload))

    assert isinstance(response, CreateTemplateResponse)
    assert response.template_id == "tpl-new"
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
        json={
            "template": [_template_payload()],
            "pageSize": 10,
            "pageNum": 1,
            "total": 1,
        },
    )

    async with AsyncNovitaClient(api_key="test-key") as client:
        templates = await client.gpu.templates.list()

        assert isinstance(templates, list)
        assert len(templates) == 1
        assert templates[0].id == "tpl-1"
        assert isinstance(templates[0], Template)
