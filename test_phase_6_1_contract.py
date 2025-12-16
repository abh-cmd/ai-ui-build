"""
PHASE 6.1 TEST: Command UX Contract Validation
"""
from backend.utils.command_validator import CommandValidator, CommandValidationError, is_valid_command


print("\n" + "=" * 70)
print("PHASE 6.1: COMMAND UX CONTRACT VALIDATION TEST")
print("=" * 70)

# Valid commands
valid_commands = [
    "Make button bigger",
    "Change primary color to #FF5733",
    "Increase heading size",
    "Add more spacing",
    "Make CTA taller",
    "Move button to bottom",
    "Make the header smaller",
    "Increase padding",
    "Make images larger",
    "Change accent to blue",
]

# Invalid commands (should be rejected)
invalid_commands = [
    ("", "empty command"),
    ("a b c", "gibberish"),
    ("Redesign page", "vague redesign"),
    ("Make it modern", "vague make it"),
    ("Improve UX", "improve"),
    ("Add a button", "adds component - not implementation"),
    ("Animate on click", "unsupported animation"),
    ("Add hover effects", "unsupported hover"),
    ("Add dark mode", "unsupported mode"),
    ("Lorem ipsum dolor sit", "gibberish"),
]

print("\nVALID COMMANDS TEST")
print("-" * 70)
passed = 0
for cmd in valid_commands:
    is_valid, error = is_valid_command(cmd)
    if is_valid:
        print("  [PASS] %s" % cmd)
        passed += 1
    else:
        print("  [FAIL] %s - ERROR: %s" % (cmd, error))

print("\n  Valid Commands Passed: %d/%d" % (passed, len(valid_commands)))

print("\nINVALID COMMANDS TEST (Should Reject)")
print("-" * 70)
rejected = 0
for cmd, reason in invalid_commands:
    is_valid, error = is_valid_command(cmd)
    if not is_valid:
        print("  [PASS] REJECTED: '%s' (%s)" % (cmd, reason))
        print("         Reason: %s" % error)
        rejected += 1
    else:
        print("  [FAIL] SHOULD REJECT: '%s' - But didn't!" % cmd)

print("\n  Invalid Commands Rejected: %d/%d" % (rejected, len(invalid_commands)))

print("\n" + "=" * 70)
print("PHASE 6.1 TEST SUMMARY")
print("=" * 70)

total_valid = len(valid_commands)
total_invalid = len(invalid_commands)
success = (passed == total_valid) and (rejected == total_invalid)

if success:
    print("\n[PASS] PHASE 6.1 COMPLETE")
    print("   Valid:   %d/%d [PASS]" % (passed, total_valid))
    print("   Invalid: %d/%d [PASS]" % (rejected, total_invalid))
    print("\n[PASS] Command UX Contract is FROZEN and ENFORCED")
else:
    print("\n[FAIL] PHASE 6.1 FAILED")
    print("   Valid:   %d/%d" % (passed, total_valid))
    print("   Invalid: %d/%d" % (rejected, total_invalid))

print("\n" + "=" * 70)
