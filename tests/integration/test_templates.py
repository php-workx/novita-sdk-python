"""Integration tests for template endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from novita import NovitaClient


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


# Placeholder for full lifecycle tests (to be implemented later)
@pytest.mark.integration
@pytest.mark.invasive
@pytest.mark.skip(reason="Lifecycle tests to be implemented later")
class TestTemplateLifecycle:
    """Test full template lifecycle (create, delete)."""

    def test_create_delete_template(self, client: NovitaClient) -> None:
        """
        Test full template lifecycle.

        This test will:
        1. Create an instance
        2. Create a template from the instance
        3. Verify the template appears in the list
        4. Delete the template
        5. Verify it's removed from the list
        6. Clean up the instance

        TODO: Implement this test sequence
        """
        pass
