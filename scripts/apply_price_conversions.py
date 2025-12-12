#!/usr/bin/env python3
"""Apply price conversions to generated Pydantic models using AST manipulation.

This script modifies the generated models.py file to convert price fields from
raw integer values (in 1/100000 USD units) to computed float properties in standard USD.

The transformations applied:
1. Add 'computed_field' to pydantic imports
2. SubscriptionPrice: price -> price_raw + @computed_field price property
3. GPUProduct: price -> price_raw, spot_price -> spot_price_raw + @computed_field properties
4. CPUProduct: price -> price_raw + @computed_field price property
"""

import ast
import sys
from pathlib import Path
from typing import Any


class PriceConversionTransformer(ast.NodeTransformer):
    """AST transformer to add price conversion logic to model classes."""

    def __init__(self) -> None:
        self.modified_imports = False

    def visit_ImportFrom(self, node: ast.ImportFrom) -> ast.ImportFrom:
        """Add 'computed_field' to pydantic imports."""
        if node.module == "pydantic" and not self.modified_imports:
            # Check if computed_field is already imported
            has_computed_field = any(
                isinstance(alias, ast.alias) and alias.name == "computed_field"
                for alias in node.names
            )

            if not has_computed_field:
                # Add computed_field to imports
                node.names.append(ast.alias(name="computed_field", asname=None))
                self.modified_imports = True

        return node

    def visit_ClassDef(self, node: ast.ClassDef) -> ast.ClassDef:
        """Transform price fields in specific model classes."""
        if node.name == "SubscriptionPrice":
            return self._transform_subscription_price(node)
        elif node.name == "GPUProduct":
            return self._transform_gpu_product(node)
        elif node.name == "CPUProduct":
            return self._transform_cpu_product(node)

        return node

    def _transform_subscription_price(self, node: ast.ClassDef) -> ast.ClassDef:
        """Transform SubscriptionPrice class to use price_raw and computed price."""
        # Add docstring
        docstring = ast.Expr(
            value=ast.Constant(
                value="""Subscription pricing information.

    Note: Prices are automatically converted from the API's raw format (1/100000 USD)
    to standard USD. For example, an API value of 350000 represents $3.50.
    """
            )
        )

        # Find and transform the price field
        new_body = []
        for item in node.body:
            if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                if item.target.id == "price":
                    # Transform to price_raw with alias
                    item.target.id = "price_raw"
                    # Update the annotation to add alias in Field
                    new_body.append(item)
                else:
                    new_body.append(item)
            else:
                new_body.append(item)

        # Add computed_field property
        price_property = self._create_price_property(
            property_name="price",
            raw_field="price_raw",
            return_type="float",
            docstring="""Get subscription price in USD.

        Returns:
            Price in USD (converted from raw API value in 1/100000 USD units)
        """,
            conversion="self.price_raw / 100000"
        )
        new_body.append(price_property)

        # Insert docstring at the beginning (after model_config if present)
        insert_pos = 0
        for i, item in enumerate(new_body):
            if isinstance(item, ast.Assign) and isinstance(item.targets[0], ast.Name):
                if item.targets[0].id == "model_config":
                    insert_pos = i + 1
                    break

        new_body.insert(insert_pos, docstring)
        node.body = new_body

        return node

    def _transform_gpu_product(self, node: ast.ClassDef) -> ast.ClassDef:
        """Transform GPUProduct class to use price_raw/spot_price_raw and computed properties."""
        # Add docstring
        docstring = ast.Expr(
            value=ast.Constant(
                value="""GPU product information.

    Note: All prices are automatically converted from the API's raw format (1/100000 USD)
    to standard USD per hour. For example, an API value of 35000 represents $0.35/hour.
    """
            )
        )

        # Find and transform price fields
        new_body = []
        for item in node.body:
            if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                if item.target.id == "price":
                    item.target.id = "price_raw"
                    new_body.append(item)
                elif item.target.id == "spot_price":
                    item.target.id = "spot_price_raw"
                    new_body.append(item)
                else:
                    new_body.append(item)
            else:
                new_body.append(item)

        # Add computed properties
        price_property = self._create_price_property(
            property_name="price",
            raw_field="price_raw",
            return_type="float",
            docstring="""Get on-demand price in USD per hour.

        Returns:
            Price in USD per hour (converted from raw API value in 1/100000 USD units)
        """,
            conversion="self.price_raw / 100000"
        )
        new_body.append(price_property)

        spot_price_property = self._create_price_property(
            property_name="spot_price",
            raw_field="spot_price_raw",
            return_type="float | None",
            docstring="""Get spot price in USD per hour.

        Returns:
            Spot price in USD per hour, or None if spot pricing is not available
        """,
            conversion="self.spot_price_raw / 100000 if self.spot_price_raw is not None else None"
        )
        new_body.append(spot_price_property)

        # Insert docstring
        insert_pos = 0
        for i, item in enumerate(new_body):
            if isinstance(item, ast.Assign) and isinstance(item.targets[0], ast.Name):
                if item.targets[0].id == "model_config":
                    insert_pos = i + 1
                    break

        new_body.insert(insert_pos, docstring)
        node.body = new_body

        return node

    def _transform_cpu_product(self, node: ast.ClassDef) -> ast.ClassDef:
        """Transform CPUProduct class to use price_raw and computed price."""
        # Add docstring
        docstring = ast.Expr(
            value=ast.Constant(
                value="""CPU product information.

    Note: Prices are automatically converted from the API's raw format (1/100000 USD)
    to standard USD per hour.
    """
            )
        )

        # Find and transform price field
        new_body = []
        for item in node.body:
            if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                if item.target.id == "price":
                    item.target.id = "price_raw"
                    new_body.append(item)
                else:
                    new_body.append(item)
            else:
                new_body.append(item)

        # Add computed property
        price_property = self._create_price_property(
            property_name="price",
            raw_field="price_raw",
            return_type="float | None",
            docstring="""Get price in USD per hour.

        Returns:
            Price in USD per hour, or None if pricing is not available
        """,
            conversion="self.price_raw / 100000 if self.price_raw is not None else None"
        )
        new_body.append(price_property)

        # Insert docstring
        insert_pos = 0
        for i, item in enumerate(new_body):
            if isinstance(item, ast.Assign) and isinstance(item.targets[0], ast.Name):
                if item.targets[0].id == "model_config":
                    insert_pos = i + 1
                    break

        new_body.insert(insert_pos, docstring)
        node.body = new_body

        return node

    def _create_price_property(
        self,
        property_name: str,
        raw_field: str,
        return_type: str,
        docstring: str,
        conversion: str
    ) -> ast.FunctionDef:
        """Create a @computed_field @property method for price conversion."""
        # Parse the conversion expression
        conversion_node = ast.parse(f"return {conversion}").body[0]

        # Create the property function
        func = ast.FunctionDef(
            name=property_name,
            args=ast.arguments(
                posonlyargs=[],
                args=[ast.arg(arg="self", annotation=None)],
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[],
            ),
            body=[
                ast.Expr(value=ast.Constant(value=docstring)),
                conversion_node,
            ],
            decorator_list=[
                ast.Call(
                    func=ast.Name(id="computed_field", ctx=ast.Load()),
                    args=[],
                    keywords=[],
                ),
                ast.Name(id="property", ctx=ast.Load()),
            ],
            returns=ast.parse(return_type, mode="eval").body,
        )

        return func


def update_field_descriptions(source: str) -> str:
    """Update Field descriptions to mention raw values and add aliases.

    This uses simple regex-based replacements for field definitions.
    """
    import re

    # Add alias="price" to price_raw fields that don't already have an alias
    # Match price_raw field, look ahead to Field( that doesn't contain alias=
    source = re.sub(
        r'(price_raw: Annotated\[.*?Field\()(?!.*?alias=)',
        r'\1alias="price", ',
        source
    )

    # Add alias="spotPrice" to spot_price_raw fields that don't already have an alias
    source = re.sub(
        r'(spot_price_raw: Annotated\[.*?Field\()(?!.*?alias=)',
        r'\1alias="spotPrice", ',
        source
    )

    return source


def main() -> int:
    """Main entry point."""
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <models.py>", file=sys.stderr)
        return 1

    models_path = Path(sys.argv[1])
    if not models_path.exists():
        print(f"Error: File not found: {models_path}", file=sys.stderr)
        return 1

    # Read the original source
    source = models_path.read_text()

    # Parse and transform AST
    tree = ast.parse(source)
    transformer = PriceConversionTransformer()
    transformed_tree = transformer.visit(tree)
    ast.fix_missing_locations(transformed_tree)

    # Convert back to source code
    import ast as ast_module
    result = ast_module.unparse(transformed_tree)

    # Apply string-based transformations for field descriptions and aliases
    result = update_field_descriptions(result)

    # Write back
    models_path.write_text(result)

    print(f"✓ Applied price conversions to {models_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
