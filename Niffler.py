#!/usr/bin/env python3

from typing import Tuple, List, Dict
from sys import argv
from os import mkdir, environ, system
from os.path import isdir, isfile


def helpMessage(programName: str, supportedArguments: Dict[Tuple[str, str], str]) -> None:
    print("'Niffler': A CLI tool for indexing the contents of text files in a searchable Inverted Index.\n")
    print(f"Usage: {programName} <OPTION> [FILES...]\n")

    for keyPair, argDescription in supportedArguments.items():
        shortVersion, fullVersion = keyPair
        print(f"{'' + shortVersion +  ', ' + fullVersion:<30} {argDescription}")


def validateArguments(programName: str, supportedArguments: Dict[Tuple[str, str], str], recievedArgs: List[str]) -> bool:
    if len(recievedArgs) == 0:
        helpMessage(programName, supportedArguments)
        return False

    if len(recievedArgs) > 1:
        print("Error: 'Niffler' can only run ONE operation at a time!")
        return False

    return True


def validateOption(selectedOption: str, supportedArguments: Dict[Tuple[str, str], str]) -> bool:
    if len(selectedOption) > 0:
        for keyPair, argDescription in supportedArguments.items():
            if selectedOption in keyPair:
                print(
                    f"You selected the option '{selectedOption}'! {argDescription}"
                )
                return True
    print(
        f"You selected '{selectedOption}! 'Niffler' doesn't know that one..."
    )
    return False


# WARNING: Linux/Unix compatible only!
def ensureDependencies() -> bool:
    try:
        homePath: str = environ['HOME']
        installPath: str = homePath + "/.niffler/"
        indexPath: str = installPath + "InvertedIndex.niffler"
        ignorePath: str = installPath + "Ignore.niffler"

        if not isdir(installPath):
            mkdir(installPath)

        if not isfile(indexPath):
            system("touch " + indexPath)

        if not isfile(ignorePath):
            system("touch " + ignorePath)

        return True
    except:
        return False


def main() -> None:

    supportedArguments: Dict[Tuple[str, str], str] = {
        ("-a", "--add"): "Give a file (or some) to 'Niffler' and it will analyze it!",
        ("-r", "--remove"): "Give a file to 'Niffler' and it will be erased from his knowledge!",
        ("-s", "--search-index"): "Give a term/word to 'Niffler' and he will find its ocurrences on the Index!",
        ("-S", "--show-index"): "Displays 'Niffler' immense knowledge, use with caution!",
    }

    programName: str = argv.pop(0)
    arguments: List[str] = [
        x for x in argv if x.startswith("-") or x.startswith("--")
    ]

    if not ensureDependencies():
        print("Error: Couldn't create nedded dependencies!")
        exit(1)

    if not validateArguments(programName, supportedArguments, arguments):
        exit(1)


if __name__ == "__main__":
    main()
