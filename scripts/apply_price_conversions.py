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


class PriceConversionTransformer(ast.NodeTransformer):
    """AST transformer to add price conversion logic to model classes."""

    def __init__(self) -> None:
        self.modified_imports = False

    def _add_alias_to_field(self, ann_assign: ast.AnnAssign, alias_value: str) -> None:
        """Add alias parameter to Field() call in Annotated type annotation.

        Args:
            ann_assign: The annotated assignment node containing the field
            alias_value: The alias value to add (e.g., "price", "spotPrice")
        """
        # The annotation should be Annotated[type, Field(...)]
        # Navigate: AnnAssign.annotation -> Subscript (Annotated[...])
        if not isinstance(ann_assign.annotation, ast.Subscript):
            return

        subscript = ann_assign.annotation
        # subscript.slice should be a Tuple containing the type and Field()
        if not isinstance(subscript.slice, ast.Tuple):
            return

        # Find Field() call in the tuple elements
        for element in subscript.slice.elts:
            if (
                isinstance(element, ast.Call)
                and isinstance(element.func, ast.Name)
                and element.func.id == "Field"
            ):
                # Check if alias already exists
                has_alias = any(kw.arg == "alias" for kw in element.keywords)
                if not has_alias:
                    # Add alias as keyword argument
                    element.keywords.insert(
                        0, ast.keyword(arg="alias", value=ast.Constant(value=alias_value))
                    )
                break

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
                    # Add alias="price" to Field() call
                    self._add_alias_to_field(item, "price")
                    new_body.append(item)
                else:
                    new_body.append(item)
            else:
                new_body.append(item)

        # Add computed_field property
        price_property = self._create_price_property(
            property_name="price",
            return_type="float",
            docstring="""Get subscription price in USD.

        Returns:
            Price in USD (converted from raw API value in 1/100000 USD units)
        """,
            conversion="self.price_raw / 100000",
        )
        new_body.append(price_property)

        # Insert docstring at the beginning of the class body (must be first for __doc__)
        new_body.insert(0, docstring)
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
                    # Add alias="price" to Field() call
                    self._add_alias_to_field(item, "price")
                    new_body.append(item)
                elif item.target.id == "spot_price":
                    item.target.id = "spot_price_raw"
                    # Add alias="spotPrice" to Field() call
                    self._add_alias_to_field(item, "spotPrice")
                    new_body.append(item)
                else:
                    new_body.append(item)
            else:
                new_body.append(item)

        # Add computed properties
        price_property = self._create_price_property(
            property_name="price",
            return_type="float",
            docstring="""Get on-demand price in USD per hour.

        Returns:
            Price in USD per hour (converted from raw API value in 1/100000 USD units)
        """,
            conversion="self.price_raw / 100000",
        )
        new_body.append(price_property)

        spot_price_property = self._create_price_property(
            property_name="spot_price",
            return_type="float | None",
            docstring="""Get spot price in USD per hour.

        Returns:
            Spot price in USD per hour, or None if spot pricing is not available
        """,
            conversion="self.spot_price_raw / 100000 if self.spot_price_raw is not None else None",
        )
        new_body.append(spot_price_property)

        # Insert docstring at the beginning of the class body (must be first for __doc__)
        new_body.insert(0, docstring)
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
                    # Add alias="price" to Field() call
                    self._add_alias_to_field(item, "price")
                    new_body.append(item)
                else:
                    new_body.append(item)
            else:
                new_body.append(item)

        # Add computed property
        price_property = self._create_price_property(
            property_name="price",
            return_type="float | None",
            docstring="""Get price in USD per hour.

        Returns:
            Price in USD per hour, or None if pricing is not available
        """,
            conversion="self.price_raw / 100000 if self.price_raw is not None else None",
        )
        new_body.append(price_property)

        # Insert docstring at the beginning of the class body (must be first for __doc__)
        new_body.insert(0, docstring)
        node.body = new_body

        return node

    def _create_price_property(
        self, property_name: str, return_type: str, docstring: str, conversion: str
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
    source = models_path.read_text(encoding="utf-8")

    # Parse and transform AST
    tree = ast.parse(source)
    transformer = PriceConversionTransformer()
    transformed_tree = transformer.visit(tree)
    ast.fix_missing_locations(transformed_tree)

    # Convert back to source code
    result = ast.unparse(transformed_tree)

    # Write back
    models_path.write_text(result, encoding="utf-8")

    print(f"✓ Applied price conversions to {models_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
