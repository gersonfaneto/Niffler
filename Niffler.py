#!/usr/bin/env python3

from os import mkdir, environ, system
from os.path import isdir, isfile


# WARNING: Linux/Unix compatible only!
def ensureDependencies() -> bool:
    try:
        HOME_PATH: str = environ['HOME']
        INSTALL_PATH: str = HOME_PATH + "/.niffler/"
        INDEX_PATH: str = INSTALL_PATH + "InvertedIndex.niffler"
        IGNORE_PATH: str = INSTALL_PATH + "Ignore.niffler"

        if not isdir(INSTALL_PATH):
            mkdir(INSTALL_PATH)

        if not isfile(INDEX_PATH):
            system("touch " + INDEX_PATH)

        if not isfile(IGNORE_PATH):
            system("touch " + IGNORE_PATH)

        return True
    except:
        return False


def main() -> None:
    if not ensureDependencies():
        print("Error: Couldn't create nedded dependencies!")
        exit(1)
    else:
        print("Ready! Set! Go!")


if __name__ == "__main__":
    main()
