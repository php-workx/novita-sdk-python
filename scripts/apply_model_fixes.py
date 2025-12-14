#!/usr/bin/env python3
"""Apply model fixes to generated Pydantic models using AST manipulation.

This script modifies the generated models.py file to fix validation issues:
1. Add 'field_validator' to pydantic imports
2. Add 'pending' status to Status enum
3. Add validator to InstanceInfo.spot_status to convert empty strings to None
"""

import ast
import sys
from pathlib import Path


class ModelFixesTransformer(ast.NodeTransformer):
    """AST transformer to add model fixes."""

    def __init__(self) -> None:
        self.modified_imports = False

    def visit_ImportFrom(self, node: ast.ImportFrom) -> ast.ImportFrom:
        """Add 'field_validator' to pydantic imports."""
        if node.module == "pydantic" and not self.modified_imports:
            # Check if field_validator is already imported
            has_field_validator = any(
                isinstance(alias, ast.alias) and alias.name == "field_validator"
                for alias in node.names
            )

            if not has_field_validator:
                # Add field_validator to imports
                node.names.append(ast.alias(name="field_validator", asname=None))
                self.modified_imports = True

        return node

    def visit_ClassDef(self, node: ast.ClassDef) -> ast.ClassDef:
        """Transform specific model classes."""
        if node.name == "Status":
            return self._add_pending_status(node)
        elif node.name == "InstanceInfo":
            return self._add_spot_status_validator(node)

        return node

    def _add_pending_status(self, node: ast.ClassDef) -> ast.ClassDef:
        """Add 'pending' status to Status enum if not present."""
        # Check if 'pending' already exists
        has_pending = False
        for item in node.body:
            if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                if item.target.id == "pending":
                    has_pending = True
                    break
            elif isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name) and target.id == "pending":
                        has_pending = True
                        break

        # If 'pending' doesn't exist, add it after the docstring
        if not has_pending:
            new_body = []
            inserted = False
            for item in node.body:
                new_body.append(item)
                # Add after docstring (first Expr) or config
                if not inserted and (
                    isinstance(item, ast.Expr)
                    or (
                        isinstance(item, ast.Assign)
                        and any(
                            isinstance(t, ast.Name) and t.id == "model_config" for t in item.targets
                        )
                    )
                ):
                    # Add pending = "pending"
                    pending_assign = ast.Assign(
                        targets=[ast.Name(id="pending", ctx=ast.Store())],
                        value=ast.Constant(value="pending"),
                    )
                    new_body.append(pending_assign)
                    inserted = True

            node.body = new_body

        return node

    def _add_spot_status_validator(self, node: ast.ClassDef) -> ast.ClassDef:
        """Add field validators to InstanceInfo for spot_status and billing_mode to convert empty strings to None.

        Also makes billing_mode nullable.
        """
        # First, make billing_mode nullable
        new_body = []
        for item in node.body:
            if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                if item.target.id == "billing_mode":
                    # Make the annotation nullable: BillingMode1 -> BillingMode1 | None
                    # And set default value to None
                    if isinstance(item.annotation, ast.Subscript):
                        # It's Annotated[BillingMode1, Field(...)]
                        subscript = item.annotation
                        if (
                            isinstance(subscript.slice, ast.Tuple)
                            and len(subscript.slice.elts) >= 1
                        ):
                            # Make the type nullable: BillingMode1 -> BillingMode1 | None
                            old_type = subscript.slice.elts[0]
                            new_type = ast.BinOp(
                                left=old_type, op=ast.BitOr(), right=ast.Constant(value=None)
                            )
                            subscript.slice.elts[0] = new_type
                    # Set default value to None
                    item.value = ast.Constant(value=None)
                    new_body.append(item)
                else:
                    new_body.append(item)
            else:
                new_body.append(item)
        node.body = new_body

        # Check if validator already exists
        has_validator = False
        for item in node.body:
            if isinstance(item, ast.FunctionDef) and item.name == "empty_str_to_none":
                has_validator = True
                break

        if not has_validator:
            # Create the validator method that handles both fields
            validator = self._create_empty_str_validator()
            node.body.append(validator)

        return node

    def _create_empty_str_validator(self) -> ast.FunctionDef:
        """Create field_validator for spot_status and billing_mode."""
        # Create: @field_validator("spot_status", "billing_mode", mode="before")
        field_validator_decorator = ast.Call(
            func=ast.Name(id="field_validator", ctx=ast.Load()),
            args=[ast.Constant(value="spot_status"), ast.Constant(value="billing_mode")],
            keywords=[ast.keyword(arg="mode", value=ast.Constant(value="before"))],
        )

        # Parse the complete validator body
        validator_code = """
if v == "":
    return None
return v
"""
        body_nodes = ast.parse(validator_code.strip()).body

        # Create the validator function
        func = ast.FunctionDef(
            name="empty_str_to_none",
            args=ast.arguments(
                posonlyargs=[],
                args=[
                    ast.arg(arg="cls", annotation=None),
                    ast.arg(arg="v", annotation=ast.Name(id="Any", ctx=ast.Load())),
                ],
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[],
            ),
            body=[
                ast.Expr(
                    value=ast.Constant(
                        value="Convert empty string to None for spot_status and billing_mode fields."
                    )
                ),
            ]
            + body_nodes,
            decorator_list=[
                field_validator_decorator,
                ast.Name(id="classmethod", ctx=ast.Load()),
            ],
            returns=ast.Name(id="Any", ctx=ast.Load()),
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
    transformer = ModelFixesTransformer()
    transformed_tree = transformer.visit(tree)
    ast.fix_missing_locations(transformed_tree)

    # Convert back to source code
    result = ast.unparse(transformed_tree)

    # Write back
    models_path.write_text(result, encoding="utf-8")

    print(f"✓ Applied model fixes to {models_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
