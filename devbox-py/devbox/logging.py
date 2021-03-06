import logging
import os
import sys


from .config import Config


LEVEL_COLORS = {
    logging.CRITICAL: '\x1b[31m',
    logging.ERROR: '\x1b[31m',
    logging.WARNING: '\x1b[33m',
    logging.INFO: '\x1b[34m',
    logging.DEBUG: '\x1b[36m',
}


COLOR_RESET = '\x1b[0m'


class CliFormatter(logging.Formatter):
    use_colors: bool

    def __init__(self, use_colors: bool = True) -> None:
        self.use_colors = use_colors
        super().__init__(fmt='[devbox] %(levelname)s: %(msg)s')

    def format(self, record: logging.LogRecord) -> str:
        color = self.getLevelColor(record.levelno)
        color_reset = self.getResetColor()
        s = logging.Formatter.format(self, record)
        s = f'{color}{s}{color_reset}'
        return s

    def getLevelColor(self, levelno: int) -> str:
        if not self.use_colors:
            return ''
        return LEVEL_COLORS[levelno]

    def getResetColor(self) -> str:
        if not self.use_colors:
            return ''
        return COLOR_RESET


def init(config: Config) -> None:
    use_colors = 'NO_COLOR' not in os.environ

    handler = logging.StreamHandler(stream=sys.stderr)
    handler.setFormatter(CliFormatter(use_colors))

    # some of the libraries we use emit log records too which we dont
    # necessarily care about, so we'll filter them by default
    handler.addFilter(lambda record: record.name == 'root')

    if config.cli.debug:
        level = logging.DEBUG
    else:
        level = logging.WARNING

    logging.basicConfig(level=level, handlers=[handler])
