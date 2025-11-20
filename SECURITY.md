# Security Guidelines

## Password and Sensitive Data Handling

### Registry Authentication Passwords

The SDK uses Pydantic's `SecretStr` type to protect registry authentication passwords from being exposed in logs, error messages, or stack traces.

#### Automatic Protection

When you create a registry authentication, passwords are automatically wrapped in `SecretStr`:

```python
from novita import NovitaClient

client = NovitaClient(api_key="your-api-key")

# Password is automatically protected - will not appear in logs
client.gpu.registries.create(
    name="docker.io",
    username="myuser",
    password="my-secret-password"  # Automatically wrapped in SecretStr
)
```

#### What SecretStr Does

1. **Prevents Logging**: Passwords are masked as `**********` in string representations
2. **Stack Trace Protection**: If an error occurs, the password won't be visible in the stack trace
3. **Secure by Default**: No additional configuration needed

#### Example - Password is Masked

```python
from pydantic import SecretStr
from novita.generated.models import CreateRepositoryAuthRequest

request = CreateRepositoryAuthRequest(
    name="docker.io",
    username="myuser",
    password=SecretStr("my-secret-password")
)

print(request)  # Output: name='docker.io' username='myuser' password=SecretStr('**********')
```

#### Accessing the Password Value

If you need to access the actual password value (e.g., for debugging), use `get_secret_value()`:

```python
# Only when absolutely necessary
actual_password = request.password.get_secret_value()
```

⚠️ **Warning**: Only call `get_secret_value()` when you explicitly need the plaintext password, and ensure it's not logged or exposed.

### API Key Protection

Your Novita API key should also be handled securely:

1. **Use Environment Variables**: Store your API key in environment variables, not in code
2. **Use `.env` files**: For local development, use `.env` files (and add them to `.gitignore`)
3. **Never Commit Credentials**: Never commit API keys or passwords to version control

#### Best Practice Example

```python
import os
from novita import NovitaClient

# Read from environment variable
api_key = os.getenv("NOVITA_API_KEY")
if not api_key:
    raise ValueError("NOVITA_API_KEY environment variable not set")

client = NovitaClient(api_key=api_key)
```

Or let the client read it automatically:

```python
from novita import NovitaClient

# Automatically reads from NOVITA_API_KEY environment variable
client = NovitaClient()
```

### Additional Security Recommendations

1. **Use Secret Management Tools**: For production, consider using AWS Secrets Manager, HashiCorp Vault, or similar tools
2. **Rotate Credentials Regularly**: Periodically rotate API keys and registry passwords
3. **Use Least Privilege**: Only grant the minimum necessary permissions
4. **Enable Audit Logging**: Monitor API usage for unusual activity
5. **Secure Network Communication**: All API requests use HTTPS by default

### Reporting Security Issues

If you discover a security vulnerability in this SDK, please report it to the maintainers privately. Do not create public GitHub issues for security vulnerabilities.
