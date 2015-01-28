# coding:utf-8
from os.path import dirname, join
from random import choice
from string import printable

import clipboard
from wox import Wox, WoxAPI


class RandomPasswordGenerator(Wox):
    """
    Password Generator plugin.
    """
    icon = join(dirname(__file__), 'icon', 'password.png')

    def get_integer_arg(self, args, position, default):
        """
        Validates the existence of an argument into the argument list and
        validates it's format/quantity or returns a default value if any of
        these validations fails.
        """
        return int(args[position]) \
            if len(args) > position and args[position] and \
                args[position].isdigit() and int(args[position]) > 0 \
            else default

    def query(self, query):
        """
        Entry method. Splits the arguments, validates them, rips some annoying
        characters and builds the option list.
        """
        args = query.split(' ')
        length = self.get_integer_arg(args, 0, 20)
        password_qty = self.get_integer_arg(args, 1, 6)
        chars = printable[:-6].replace('\\', '').replace('$', '')
        passwords = [r''.join(choice(chars) for __ in xrange(length))
                     for _ in xrange(password_qty)]
        return [{
            'Title': password,
            'SubTitle': 'Copy this password to clipboard.',
            'IcoPath': self.icon,
            'JsonRPCAction': {
                'method': 'copy_password',
                'parameters': [password],
                'dontHideAfterAction': False
            }
        } for password in passwords]

    def copy_password(self, password):
        """
        Copies the given password to the clipboard.
        WARNING:Uses yet-to-be-known Win32 API and ctypes black magic to work.
        """
        clipboard.put(password)
        WoxAPI.show_msg(password, 'Password has been copied to clipboard.',
                        self.icon)


# Following statement is necessary
if __name__ == '__main__':
    RandomPasswordGenerator()