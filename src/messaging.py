"""Module for messaging."""
from typing import Self

# DEFAULT
import logging
import os


class Failure(int):
    """
    Failure Object class. To be used as a return object in method calls.
    """

    def __init__(self, message: str=None) -> None:
        self._message = message

    def __new__(cls, message: str=None) -> int:
        return int.__new__(cls, bool(0))

    def __nonzero__(self) -> bool:
        return False

    def __str__(self) -> Self:
        return self

    @property
    def message(self) -> str:
        return self._message

    @message.setter
    def message(self, value: str) -> None:
        self._message = value


class Success(int):
    """
    Success Object class. To be used as a return object in method calls.
    """
    def __init__(self, message: str = None) -> None:
        self._message = message

    def __new__(cls, message: str = None) -> int:
        return int.__new__(cls, bool(1))

    def __nonzero__(self) -> bool:
        return True

    def __str__(self) -> Self:
        return self

    @property
    def message(self) -> str:
        return self._message

    @message.setter
    def message(self, value: str) -> None:
        self._message = value


class Logger(logging.Logger):
    """Subclass of logging which implements colored output to shell."""
    def __init__(self, name='Logger1', filename: str = None) -> None:
        self.name = name
        logging.Logger.__init__(self, self.name, logging.DEBUG)
        self.handler = ColorHandler()
        if filename:
            # IF THE USER SENDS IN A FILENAME CONFIGURE AND ADD HANDLER
            logging.basicConfig(filename=filename, level=logging.DEBUG)
            self.addHandler(logging.FileHandler(filename))
        else:
            self.handler.setLevel(logging.DEBUG)

        # CHECK PYTHON VERSION, FORMAT Formatter correctly for 2.6.x versions
        formatter = None
        formatter = logging.Formatter("%(levelname)s: {:<10}%(message)s".format(''))
        self.handler.setFormatter(formatter)
        self.addHandler(self.handler)

    def show_level(self, state: bool = True) -> None:
        """Show or hide the level data associated with this logger.

        Args:
            state: Visibility state of level display.
        """
        if state:
            formatter = logging.Formatter("%(levelname)s: {:<10}%(message)s".format(''))
            self.handler.setFormatter(formatter)
            self.addHandler(self.handler)
        else:
            formatter = logging.Formatter("{:<4}%(message)s".format(''))
            self.handler.setFormatter(formatter)
            self.addHandler(self.handler)

    def set_color_scheme(self, scheme: int = 0) -> None:
        """Set the color scheme of the logger.

        Notes:
            Useful if you need to change your scheme based on what your script is doing.

        Args:
            scheme: color scheme to use
        """
        self.handler.update_color_scheme(scheme)

    def set_debug_level(self, level: int = 4) -> None:
        """Wrapper function to set debug levels based on an int value.

        Args:
        level: print various levels of debug information
               0 - Equivalent of calling logging.DEBUG
               1 - Equivalent of calling logging.ERROR
               2 - Equivalent of calling logging.WARNING
               3 - Equivalent of calling logging.INFO
               4 - Equivalent of calling logging.CRITICAL
        """
        if type(level) != int:
            print("level must be of type (int) with range 0-4")
        if level == 4:
            self.setLevel(logging.CRITICAL)
        elif level == 3:
            self.setLevel(logging.INFO)
        elif level == 2:
            self.setLevel(logging.WARNING)
        elif level == 1:
            self.setLevel(logging.ERROR)
        elif level == 0:
            self.setLevel(logging.DEBUG)
        else:
            print("level Not supported")

    @classmethod
    def format_msg(cls, _module: str = None, _class: str = None, _method: str = None, _property: str = None,
                   msg_list: str = None, msg_type: str = 'info') -> str:
        """Format a message for logging.

        Args:
            _module: path to module from which log is being called. (optional)
            _class: class name from which msg originated. (optional)
            _method: method name from which msg originated. (optional)
            msg_list: list of message data. Each entry in the list is a new line in the message output.
            msg_type: type of message to format for. Valid values are: info, warning, error
        """
        _msg_list = msg_list
        if not _msg_list:
            _msg_list = []
        new_line_break = "\n{0:>16}".format(" ")
        if msg_type == 'warning':
            new_line_break = "\n{0:>19}".format(" ")
        elif msg_type == 'error':
            new_line_break = "\n{0:>17}".format(" ")
        msg = ""

        if _module:
            msg += "{0}".format(_module)
        if _class:
            msg += ".{0}".format(_class)
        if _method:
            msg += ".{0}()".format(_method)
        if _property:
            msg += ".{0}".format(_property)
        msg += new_line_break
        msg += "{0}".format(new_line_break).join(msg_list)
        return msg


class ColorHandler(logging.StreamHandler):
    """Subclass of stream handler to support color."""
    # MAP COLOR NAME TO INDICES
    color_map = {
        'black': 0,
        'red': 1,
        'green': 2,
        'yellow': 3,
        'blue': 4,
        'magenta': 5,
        'cyan': 6,
        'white': 7
    }

    # CONSTRUCT LEVEL MAP (background, foreground, bold/intensity)
    level_map = {
        logging.DEBUG: (None, 'magenta', False),
        logging.INFO: (None, 'green', False),
        logging.WARNING:  (None, 'yellow', False),
        logging.ERROR: (None, 'red', False),
        logging.CRITICAL: ('red', 'white', True)
    }

    csi = '\x1b['
    reset = '\x1b[0m'

    @property
    def is_tty(self):
        isatty = getattr(self.stream, 'isatty', None)
        return isatty and isatty()

    def update_color_scheme(self, scheme: int = 0) -> None:
        """Update the color scheme of the logger.

        Notes:
            Useful if you need to change your scheme based on what your script is doing.

        Args:
            scheme: color scheme to use 0 default, 1 alternate INFO
        """
        if scheme == 0:
            # DEFAULT
            if os.name == 'nt':
                self.level_map = {
                    logging.DEBUG: (None, 'magenta', True),
                    logging.INFO: (None, 'green', False),
                    logging.WARNING:  (None, 'yellow', True),
                    logging.ERROR: (None, 'red', True),
                    logging.CRITICAL: ('red', 'white', True)
                }
            else:
                self.level_map = {
                    logging.DEBUG: (None, 'magenta', False),
                    logging.INFO: (None, 'green', False),
                    logging.WARNING:  (None, 'yellow', False),
                    logging.ERROR: (None, 'red', False),
                    logging.CRITICAL: ('red', 'white', True)
                }
        elif scheme == 1:
            # SWITCH INFO TO CYAN
            if os.name == 'nt':
                self.level_map = {
                    logging.DEBUG: (None, 'magenta', True),
                    logging.INFO: (None, 'cyan', False),
                    logging.WARNING:  (None, 'yellow', True),
                    logging.ERROR: (None, 'red', True),
                    logging.CRITICAL: ('red', 'white', True)
                }
            else:
                self.level_map = {
                    logging.DEBUG: (None, 'magenta', False),
                    logging.INFO: (None, 'cyan', False),
                    logging.WARNING:  (None, 'yellow', False),
                    logging.ERROR: (None, 'red', False),
                    logging.CRITICAL: ('red', 'white', True)
                }
        elif scheme == 2:
            # SWITCH INFO TO CYAN
            if os.name == 'nt':
                self.level_map = {
                    logging.DEBUG: (None, 'magenta', True),
                    logging.INFO: (None, 'white', False),
                    logging.WARNING: (None, 'yellow', True),
                    logging.ERROR: (None, 'red', True),
                    logging.CRITICAL: ('red', 'cyan', True)
                }
            else:
                self.level_map = {
                    logging.DEBUG: (None, 'magenta', False),
                    logging.INFO: (None, 'cyan', False),
                    logging.WARNING: (None, 'yellow', False),
                    logging.ERROR: (None, 'red', False),
                    logging.CRITICAL: ('red', 'white', True)
                }
        else:
            # DEFAULT, IN CASE WE GET A NON VALID SCHEME
            if os.name == 'nt':
                self.level_map = {
                    logging.DEBUG: (None, 'magenta', True),
                    logging.INFO: (None, 'green', False),
                    logging.WARNING:  (None, 'yellow', True),
                    logging.ERROR: (None, 'red', True),
                    logging.CRITICAL: ('red', 'white', True)
                }
            else:
                self.level_map = {
                    logging.DEBUG: (None, 'magenta', False),
                    logging.INFO: (None, 'green', False),
                    logging.WARNING:  (None, 'yellow', False),
                    logging.ERROR: (None, 'red', False),
                    logging.CRITICAL: ('red', 'white', True)
                }

    def emit(self, record: logging.LogRecord) -> None:
        """Override class method.

        Args:
            record: log record.
        """
        try:
            message = self.format(record)
            stream = self.stream
            if not self.is_tty:
                stream.write(message)
            else:
                self.output_colorized(message)
            stream.write(getattr(self, 'terminator', '\n'))
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def format(self, record: logging.LogRecord) -> str:
        """Override class method which determines if our message should be colorized.

        Args:
            record: log record
        """
        message = logging.StreamHandler.format(self, record)
        if self.is_tty:
            parts = message.split('\n', 1)
            parts[0] = self.colorize(parts[0], record)
            message = '\n'.join(parts)
        return message

    def colorize(self, message: str, record: logging.LogRecord) -> str:
        """Format data with color.

        Args:
            message: message to format.
            record: log record.
        """
        if record.levelno in self.level_map:
            bg, fg, bold = self.level_map[record.levelno]
            params = []
            if bg in self.color_map:
                params.append(str(self.color_map[bg] + 40))
            if fg in self.color_map:
                params.append(str(self.color_map[fg] + 30))
            if bold:
                params.append('1')
            if params:
                message = ''.join((self.csi, ';'.join(params), 'm', message, self.reset))
        return message

    def output_colorized(self, message: str) -> None:
        self.stream.write(message)