import argparse
import asyncio
import importlib
import logging
import logging.config
import signal

import setproctitle
import yaml


def read_cfg(path):
    with open(path) as stream:
        return yaml.load(stream, Loader=yaml.SafeLoader)


def get_class(service_path):
    module = importlib.import_module(service_path)
    cls_name = 'Service'
    return getattr(module, cls_name)


def configure_logs(cfg: dict) -> None:
    if cfg.get('logging'):
        logging_cfg = cfg.pop('logging')
        logging.config.dictConfig(logging_cfg)
    else:
        fmt = cfg.get('base_fmt', logging.BASIC_FORMAT)
        logging.basicConfig(format=fmt, level=logging.INFO)


def run(service_cls, cfg):
    try:
        loop = service_cls.get_event_loop()
        loop.add_signal_handler(signal.SIGINT, loop.stop)
        asyncio.set_event_loop(loop)
        service = service_cls(cfg, loop)
        loop.run_until_complete(service.start())
        loop.run_forever()
    finally:
        loop.run_until_complete(service.stop())
        loop.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'service',
        help=(
            'python style path to module with Service class.'
        )
    )
    parser.add_argument(
        '-c', '--cfg', required=True, help='path to cfg file in yaml format'
    )

    args, extra = parser.parse_known_args()
    service_cls = get_class(args.service)
    cfg = read_cfg(args.cfg)
    setproctitle.setproctitle(service_cls.proc_title(cfg))
    configure_logs(cfg)
    run(service_cls, cfg)


if __name__ == '__main__':
    main()
