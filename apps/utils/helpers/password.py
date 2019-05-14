from string import ascii_letters, digits

from random import choice


def generator(size=6, chars=ascii_letters + digits):
    """
        Returns a string of random characters, useful in generating temporary
        passwords for automated password resets.

        size: default=6; override to provide smaller/larger passwords
        chars: default=A-Za-z0-9; override to provide more/less diversity
    """
    return ''.join(choice(chars) for _ in range(size))
