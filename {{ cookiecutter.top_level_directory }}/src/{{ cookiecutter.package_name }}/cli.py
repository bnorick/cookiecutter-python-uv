"""Console script for {{cookiecutter.package_name}}."""
{%- if cookiecutter.command_line_interface|lower == 'click' %}
import os
import sys

import click
{% elif cookiecutter.command_line_interface|lower == 'simple-parsing' %}
# ruff: noqa: RUF009

import dataclasses
import inspect
import pathlib
import os
import sys
from typing import Union

import simple_parsing
{%- endif %}

{{ cookiecutter.package_name.upper() }}_CLI_PWD = os.getenv("{{ cookiecutter.package_name.upper() }}_CLI_PWD")
if {{ cookiecutter.package_name.upper() }}_CLI_PWD is not None:
    os.chdir({{ cookiecutter.package_name.upper() }}_CLI_PWD)

{% if cookiecutter.command_line_interface|lower == 'click' -%}
@click.command()
def main() -> int:
    """Console script for {{cookiecutter.package_name}}."""
    click.echo("Replace this message by putting your code into {{cookiecutter.package_name}}.cli:main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0
{% elif cookiecutter.command_line_interface|lower == 'simple-parsing' %}
@dataclasses.dataclass(kw_only=True)
class GlobalArguments:
    # whether or not to be extra noisy
    verbose: bool = simple_parsing.flag(default=False, negative_prefix="--no-", alias=["-v"])
    # do nothing, just print intentions
    dry_run: bool = simple_parsing.flag(default=False, negative_prefix="--no-", alias=["-dr"])

    def __post_init__(self):
        if self.verbose:
            log.reset()
            log.init(verbose=True)


@dataclasses.dataclass(kw_only=True)
class Action1(GlobalArguments):
    """Action1"""

    foo: str
    bar: int

    def run(self):
        print(f"{self.foo=} {self.bar=}")


@dataclasses.dataclass(kw_only=True)
class Action2(GlobalArguments):
    """Action2"""

    path: pathlib.Path
    hello: str = "world"

    def run(self):
        print(f"{self.path=} {self.hello=}")


@dataclasses.dataclass
class Arguments:
    # action
    action: Union[Action1, Action2] = simple_parsing.subparsers(
        {
            "action1": Action1,
            "action2": Action2,
        }
    )


FIRST_KWARGS = None
class ArgumentParser(simple_parsing.ArgumentParser):
    def __init__(self, *args, **kwargs):
        global FIRST_KWARGS
        if FIRST_KWARGS is None:
            FIRST_KWARGS = kwargs

        caller = inspect.stack()[1]
        caller_path = pathlib.Path(caller.filename)
        if caller_path.match("*lib/**/argparse.py"):
            super().__init__(*args, **FIRST_KWARGS)
        else:
            super().__init__(*args, **kwargs)


def parse_args() -> GlobalArguments:
    parser = ArgumentParser(
        add_option_string_dash_variants="only",
        nested_mode=simple_parsing.NestedMode.WITHOUT_ROOT
    )
    parser.add_arguments(Arguments, "args")
    args: Arguments = getattr(parser.parse_args(), "args")
    return args.action


def run(args: GlobalArguments):
    args.run()


def main():
    args = parse_args()
    return run(args)
{%- endif %}


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
