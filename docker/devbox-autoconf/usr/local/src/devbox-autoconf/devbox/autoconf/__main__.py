from sys import argv, stderr, exit
import logging

from .autoconf import Autoconf


def main():
    if len(argv) != 2:
        print("error: argument must be a single config file", file=stderr)
        exit(1)

    logging.basicConfig(level=logging.INFO)

    a = Autoconf(argv[1])
    a.watch_and_update_vhosts()


if __name__ == '__main__':
    main()