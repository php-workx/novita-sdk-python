"""Integration tests for template endpoints."""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from novita import NovitaClient

from novita.exceptions import BadRequestError, NotFoundError


@pytest.mark.integration
@pytest.mark.safe
class TestTemplates:
    """Test template-related endpoints."""

    def test_list_templates(self, client: NovitaClient) -> None:
        """Test listing all templates."""
        templates = client.gpu.templates.list()

        assert isinstance(templates, list)

    def test_template_structure(self, client: NovitaClient) -> None:
        """Test that templates have all expected fields."""
        templates = client.gpu.templates.list()

        if len(templates) > 0:
            template = templates[0]

            # Required fields
            assert hasattr(template, "id")
            assert hasattr(template, "name")

            # Verify data types
            assert isinstance(template.id, str)
            assert isinstance(template.name, str)

            # IDs should be non-empty
            assert len(template.id) > 0
            assert len(template.name) > 0

    def test_get_template_details(self, client: NovitaClient) -> None:
        """Test getting details of a specific template."""
        # First get list of templates
        templates = client.gpu.templates.list()

        if len(templates) > 0:
            template_id = templates[0].id

            # Get detailed information
            template = client.gpu.templates.get(template_id=template_id)

            assert template is not None

    def test_templates_have_unique_ids(self, client: NovitaClient) -> None:
        """Test that all templates have unique IDs."""
        templates = client.gpu.templates.list()

        if len(templates) > 1:
            ids = [template.id for template in templates]
            # Check for uniqueness
            assert len(ids) == len(set(ids))


@pytest.mark.integration
@pytest.mark.invasive
class TestTemplateLifecycle:
    """Test full template lifecycle (create, delete)."""

    def test_create_delete_template(self, client: NovitaClient) -> None:
        """
        Test full template lifecycle.

        This test will:
        1. Create a template
        2. Verify the template appears in the list
        3. Delete the template
        4. Verify it's removed from the list
        """
        from novita.generated.models import (
            Channel,
            CreateTemplateRequest,
            TemplateCreatePayload,
        )

        from .test_utils import generate_test_name

        # Generate unique test template name
        test_name = generate_test_name("template")
        template_id = None

        try:
            # Step 1: Create a minimal template
            response = client.gpu.templates.create(
                CreateTemplateRequest(
                    template=TemplateCreatePayload(
                        name=test_name,
                        readme="Test template created by integration tests",
                        type="instance",
                        channel=Channel.private,
                        image="ubuntu:22.04",
                        start_command="bash",
                        rootfs_size=50,
                        ports=[],
                        volumes=[],
                        envs=[],
                    )
                )
            )
            assert response.template_id is not None
            template_id = response.template_id

            # Step 2: Verify the template can be retrieved by ID
            # Note: The list endpoint may be paginated and not show newly created templates immediately
            created_template = client.gpu.templates.get(template_id=template_id)
            assert created_template is not None
            assert created_template.name == test_name

            # Step 3: Delete the template
            client.gpu.templates.delete(template_id)

            # Step 4: Verify it's removed (get should raise an error)
            try:
                client.gpu.templates.get(template_id=template_id)
                # If we get here, template still exists
                raise AssertionError(f"Template {template_id} still exists after deletion")
            except (NotFoundError, BadRequestError) as e:
                # Expected - template should not exist anymore
                # API returns BadRequestError with "template not found" message
                if "not found" in str(e).lower():
                    pass
                else:
                    raise

        finally:
            # Cleanup: ensure the template is deleted even if test fails
            if template_id is not None:
                try:
                    # Always try to delete - API will handle if already deleted
                    client.gpu.templates.delete(template_id)
                except (NotFoundError, BadRequestError):
                    # If template is already gone, that's fine
                    pass
                except Exception as e:
                    # Log unexpected cleanup errors but don't fail the test
                    warnings.warn(
                        f"Failed to cleanup template {template_id}: {e}",
                        ResourceWarning,
                        stacklevel=2,
                    )
