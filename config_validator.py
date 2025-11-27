"""
Configuration Validator Module

This module provides functionality to validate application configuration dictionaries.
It ensures that required keys are present and that values meet expected formats.
"""

import re
from typing import Dict, Any


def validate_config(config: Dict[str, Any]) -> bool:
    """
    Validate a configuration dictionary.

    This function checks that all required configuration keys are present
    and that their values meet the expected format requirements.

    Args:
        config: A dictionary containing configuration key-value pairs

    Returns:
        bool: True if the configuration is valid

    Raises:
        ValueError: If required keys are missing or values are invalid

    Examples:
        >>> validate_config({"app_name": "MyApp", "version": "1.2.3"})
        True

        >>> validate_config({"app_name": "MyApp"})
        Traceback (most recent call last):
            ...
        ValueError: Missing required configuration key: version

        >>> validate_config({"app_name": "MyApp", "version": "1.2"})
        Traceback (most recent call last):
            ...
        ValueError: Invalid version format: 1.2. Expected semver format (e.g., 1.2.3)
    """
    # Define required keys
    required_keys = ["app_name", "version"]

    # Check for missing required keys
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required configuration key: {key}")

    # Validate version format (semver: major.minor.patch)
    version = config["version"]
    semver_pattern = r'^\d+\.\d+\.\d+$'

    if not isinstance(version, str):
        raise ValueError(f"Version must be a string, got {type(version).__name__}")

    if not re.match(semver_pattern, version):
        raise ValueError(
            f"Invalid version format: {version}. "
            f"Expected semver format (e.g., 1.2.3)"
        )

    return True


def is_valid_semver(version: str) -> bool:
    """
    Check if a string is a valid semantic version.

    Args:
        version: The version string to validate

    Returns:
        bool: True if valid semver format, False otherwise
    """
    semver_pattern = r'^\d+\.\d+\.\d+$'
    return bool(re.match(semver_pattern, version))


# Test/Example usage
if __name__ == "__main__":
    print("Configuration Validator - Test Examples\n")
    print("=" * 50)

    # Example 1: Valid configuration
    print("\n1. Testing valid configuration:")
    valid_config = {
        "app_name": "TodoApp",
        "version": "1.0.0"
    }
    try:
        result = validate_config(valid_config)
        print(f"   Config: {valid_config}")
        print(f"   Result: ✓ Valid (returned {result})")
    except ValueError as e:
        print(f"   Result: ✗ Error - {e}")

    # Example 2: Missing required key
    print("\n2. Testing configuration with missing 'version' key:")
    invalid_config_1 = {
        "app_name": "TodoApp"
    }
    try:
        result = validate_config(invalid_config_1)
        print(f"   Config: {invalid_config_1}")
        print(f"   Result: ✓ Valid (returned {result})")
    except ValueError as e:
        print(f"   Config: {invalid_config_1}")
        print(f"   Result: ✗ Error - {e}")

    # Example 3: Invalid version format
    print("\n3. Testing configuration with invalid version format:")
    invalid_config_2 = {
        "app_name": "TodoApp",
        "version": "1.2"
    }
    try:
        result = validate_config(invalid_config_2)
        print(f"   Config: {invalid_config_2}")
        print(f"   Result: ✓ Valid (returned {result})")
    except ValueError as e:
        print(f"   Config: {invalid_config_2}")
        print(f"   Result: ✗ Error - {e}")

    # Example 4: Another invalid version format
    print("\n4. Testing configuration with non-numeric version:")
    invalid_config_3 = {
        "app_name": "TodoApp",
        "version": "v1.2.3"
    }
    try:
        result = validate_config(invalid_config_3)
        print(f"   Config: {invalid_config_3}")
        print(f"   Result: ✓ Valid (returned {result})")
    except ValueError as e:
        print(f"   Config: {invalid_config_3}")
        print(f"   Result: ✗ Error - {e}")

    # Example 5: Valid configuration with additional keys
    print("\n5. Testing valid configuration with extra keys:")
    valid_config_2 = {
        "app_name": "TodoApp",
        "version": "2.1.0",
        "debug": True,
        "port": 8080
    }
    try:
        result = validate_config(valid_config_2)
        print(f"   Config: {valid_config_2}")
        print(f"   Result: ✓ Valid (returned {result})")
    except ValueError as e:
        print(f"   Result: ✗ Error - {e}")

    print("\n" + "=" * 50)
    print("\nAll tests completed!")
