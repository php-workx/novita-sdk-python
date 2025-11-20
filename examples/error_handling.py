"""Error handling patterns example.

This example demonstrates:
- Handling different types of errors
- Using specific exception types
- Error recovery strategies
- Best practices for error handling
"""

from novita import (
    APIError,
    AuthenticationError,
    BadRequestError,
    CreateInstanceRequest,
    Kind,
    NotFoundError,
    NovitaClient,
)


def create_instance_with_error_handling(client: NovitaClient, name: str) -> str | None:
    """Create instance with comprehensive error handling.

    Args:
        client: Novita client instance
        name: Name for the new instance

    Returns:
        Instance ID if successful, None otherwise
    """
    try:
        request = CreateInstanceRequest(
            name=name,
            product_id="prod-1",
            gpu_num=1,
            rootfs_size=50,
            image_url="docker.io/library/ubuntu:latest",
            kind=Kind.gpu,
        )
        response = client.gpu.instances.create(request)
        print(f"✓ Successfully created instance: {response.id}")
        return response.id

    except AuthenticationError as e:
        print(f"✗ Authentication failed: {e.message}")
        print("  → Check your API key (NOVITA_API_KEY environment variable)")
        return None

    except BadRequestError as e:
        print(f"✗ Bad request: {e.message}")
        if e.details:
            print(f"  Details: {e.details}")
        print("  → Verify your request parameters")
        return None

    except APIError as e:
        print(f"✗ API error: {e.message}")
        print(f"  Status code: {e.status_code}")
        if e.response_body:
            print(f"  Response: {e.response_body}")
        return None


def get_instance_with_retry(client: NovitaClient, instance_id: str, max_retries: int = 3) -> None:
    """Get instance with retry logic for 404 errors.

    Args:
        client: Novita client instance
        instance_id: ID of the instance to fetch
        max_retries: Maximum number of retry attempts
    """
    import time

    for attempt in range(max_retries):
        try:
            instance = client.gpu.instances.get(instance_id)
            status = instance.status.value if hasattr(instance.status, "value") else instance.status
            print(f"✓ Found instance: {instance.name} ({status})")
            return

        except NotFoundError:
            if attempt < max_retries - 1:
                print(f"⚠ Instance not found (attempt {attempt + 1}/{max_retries})")
                print("  Retrying in 2 seconds...")
                time.sleep(2)
            else:
                print(f"✗ Instance {instance_id} not found after {max_retries} attempts")
                print("  → The instance may have been deleted")


def main() -> None:
    """Demonstrate error handling patterns."""
    print("=" * 60)
    print("Error Handling Examples")
    print("=" * 60)

    # Example 1: Create instance with error handling
    print("\n1. Creating instance with error handling:")
    try:
        client = NovitaClient()  # May raise AuthenticationError
    except AuthenticationError as e:
        print(f"✗ Failed to initialize client: {e.message}")
        print("  → Set NOVITA_API_KEY environment variable")
        return

    instance_id = create_instance_with_error_handling(client, "error-demo")

    if instance_id:
        # Example 2: Handle NotFoundError with retry
        print("\n2. Getting instance with retry logic:")
        get_instance_with_retry(client, instance_id)

        # Example 3: Handle NotFoundError for non-existent instance
        print("\n3. Attempting to get non-existent instance:")
        try:
            client.gpu.instances.get("nonexistent-id")
        except NotFoundError as e:
            print(f"✗ Expected error: {e.message}")
            print("  → This is expected behavior for invalid IDs")

    # Always close the client
    client.close()
    print("\n✓ Error handling demo complete!")


if __name__ == "__main__":
    main()
