import subprocess
from pathlib import Path


def get_changed_files():
    """Get files changed in the latest Git commit."""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )

        return result.stdout.splitlines()

    except subprocess.CalledProcessError:
        return []


def get_changed_modules(changed_files):
    """Convert changed source files into module names."""
    modules = set()

    for file in changed_files:
        if file.startswith("src/") and file.endswith(".py"):
            modules.add(Path(file).stem)

    return modules


def expand_dependencies(modules):
    """Find source modules that depend on changed modules."""
    impacted = set(modules)

    changed = True

    while changed:
        changed = False

        for source_file in Path("src").glob("*.py"):
            module_name = source_file.stem

            if module_name in impacted:
                continue

            content = source_file.read_text()

            for impacted_module in impacted:
                if (
                    f"src.{impacted_module}" in content
                    or f"from .{impacted_module}" in content
                ):
                    impacted.add(module_name)
                    changed = True
                    break

    return impacted


def select_tests(impacted_modules):
    """Select tests related to impacted source modules."""
    selected = []

    for test_file in Path("tests").glob("test_*.py"):
        content = test_file.read_text()

        for module in impacted_modules:
            if f"src.{module}" in content:
                selected.append(str(test_file))
                break

    return selected


def main():
    changed_files = get_changed_files()

    changed_modules = get_changed_modules(changed_files)

    impacted_modules = expand_dependencies(changed_modules)

    selected_tests = select_tests(impacted_modules)

    if selected_tests:
        print(" ".join(sorted(selected_tests)))
    else:
        # Safe fallback: if unsure, run everything.
        print("tests")


if __name__ == "__main__":
    main()