import re
import sys

PACKAGE_PATTERN = r"^[_a-zA-Z][_a-zA-Z0-9]*$"

package_name = "{{ cookiecutter.package_name }}"
if not re.match(PACKAGE_PATTERN, package_name):
    print(f"ERROR: The package name ({package_name}) is not a valid Python package name. "
          f"Package names should start with a letter or underscore and be composed entirely "
          f"of letters, digits, and/or underscores.")

    # exit to cancel recipe
    sys.exit(1)

is_monorepo_tools = "{{ cookiecutter._is_monorepo_tools }}" == "True"
in_monorepo = "{{ cookiecutter._in_monorepo }}" == "True"
if is_monorepo_tools and in_monorepo:
    print(f"ERROR: Both _is_monorepo_tools and _in_monorepo were set to true, which is invalid.")

    # exit to cancel recipe
    sys.exit(1) 
