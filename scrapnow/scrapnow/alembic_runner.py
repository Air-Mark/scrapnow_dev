import importlib
import sys
from pathlib import Path

from alembic.config import CommandLine, Config


def main():
    db_package_path = sys.argv[1]
    module = importlib.import_module(db_package_path)
    db_package_file_path = Path(module.__file__).parent.resolve()

    alembic = CommandLine()
    options = alembic.parser.parse_args(sys.argv[2:])
    cfg = Config(file_=options.config, ini_section=options.name,
                 cmd_opts=options)
    cfg.set_main_option('script_location', str(db_package_file_path))
    exit(alembic.run_cmd(cfg, options))


if __name__ == '__main__':
    main()
