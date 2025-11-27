#!/usr/bin/env python3
"""
Demonstration of two-factor validation threshold fix.

This file demonstrates that the threshold fix is working:
- Confidence >= 75% (threshold)
- AND should_commit == True (AI decision)

Both conditions must be met for a commit to proceed.
"""


def validate_commit(confidence: float, should_commit: bool, threshold: float = 0.75) -> bool:
    """
    Two-factor validation for git commits.

    Args:
        confidence: AI confidence score (0.0 to 1.0)
        should_commit: AI's boolean decision to commit
        threshold: Minimum confidence threshold (default 0.75)

    Returns:
        True if both conditions met, False otherwise
    """
    return confidence >= threshold and should_commit is True


# Test cases
if __name__ == "__main__":
    print("Two-Factor Validation Test Cases:")
    print()

    # Test 1: Complete code (high confidence, AI says yes)
    result1 = validate_commit(confidence=0.95, should_commit=True)
    print(f"1. Complete code (95%, True): {'✅ COMMIT' if result1 else '❌ REJECT'}")

    # Test 2: Incomplete code (high confidence, AI says no)
    result2 = validate_commit(confidence=0.85, should_commit=False)
    print(f"2. Incomplete code (85%, False): {'✅ COMMIT' if result2 else '❌ REJECT'}")

    # Test 3: Low confidence
    result3 = validate_commit(confidence=0.60, should_commit=True)
    print(f"3. Low confidence (60%, True): {'✅ COMMIT' if result3 else '❌ REJECT'}")

    print()
    print("Expected results:")
    print("1. ✅ COMMIT (both conditions met)")
    print("2. ❌ REJECT (AI detected incomplete code)")
    print("3. ❌ REJECT (below threshold)")
