#!/usr/bin/env python3

from typing import Tuple, List, Dict
from sys import argv
from os import mkdir, environ, system, walk
from os.path import isdir, isfile, join


def errorMessage(programName: str) -> None:
    print("\n'Niffler': Waiting for orders...")
    print(f"'Niffler': Try using '{programName} --help' for more information!")


def helpMessage(programName: str, supportedOptions: Dict[Tuple[str, str], str]) -> None:
    print("\n'Niffler': A CLI tool for indexing the contents of text files in a searchable Inverted Index.\n")
    print(f"Usage: {programName} <OPTION> [FILES...]\n")

    for keyPair, argDescription in supportedOptions.items():
        shortVersion, fullVersion = keyPair
        print(f"{'' + shortVersion +  ', ' + fullVersion:<30} {argDescription}")


def validateOption(supportedOptions: Dict[Tuple[str, str], str], recievedOption: str, hasComplement: bool = True) -> bool:
    for keyPair, argDescription in supportedOptions.items():
        if recievedOption in keyPair and hasComplement:
            return True
        elif recievedOption in keyPair and not hasComplement:
            print(f"You selected the '{recievedOption}' option! {argDescription}'")
            return False

    print(f"You selected the '{recievedOption}' option! 'Niffler' doesn't know this one...")
    return False


def validatePaths(recievedPaths: List[str]) -> Tuple[List[str], List[str]]:
    validPaths: List[str] = []
    invalidPaths: List[str] = []

    for currentPath in recievedPaths:
        if isdir(currentPath):
            for rootPath, _, filePaths in walk(currentPath):
                for filePath in filePaths:
                    if isfile(join(rootPath, filePath)):
                        validPaths.append(join(rootPath, filePath))
                    else:
                        invalidPaths.append(join(rootPath, filePath))
        elif isfile(currentPath):
            validPaths.append(currentPath)
        else:
            invalidPaths.append(currentPath)

    return validPaths, invalidPaths


def validateArguments(programName: str, supportedOptions: Dict[Tuple[str, str], str], recievedOption: List[str], recievedPaths: List[str]) -> bool:
    if len(recievedOption) == 0 and len(recievedPaths) == 0:
        errorMessage(programName)
        return False

    if len(recievedOption) == 0:
        helpMessage(programName, supportedOptions)
        return False

    if len(recievedOption) == 1 and len(recievedPaths) == 0:
        if recievedOption[0] in ["-h", "--help"]:
            helpMessage(programName, supportedOptions)
            return True
        return validateOption(supportedOptions, recievedOption[0], hasComplement=False)

    if len(recievedOption) == 1 and len(recievedOption) > 0:
        return validateOption(supportedOptions, recievedOption[0])

    if len(recievedOption) > 1:
        print("ERROR: 'Niffler' can only run ONE operation at a time!")
        return False

    return True


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

    recievedOptions: List[str] = [x for x in argv if x.startswith("-") or x.startswith("--")]
    recievedPaths: List[str] = list(set(argv) - set(recievedOptions))

    if not ensureDependencies():
        print("ERROR: Couldn't create nedded dependencies!")
        exit(1)

    if not validateArguments(programName, supportedArguments, recievedOptions, recievedPaths):
        exit(1)

    validPaths, invalidPaths = validatePaths(recievedPaths)

    if len(invalidPaths) > 0:
        print("\nWARNING: The following files were out of reach!\n")
        for currentPath in invalidPaths:
            print(f"- {currentPath}")

    if len(validPaths) > 0:
        print("\nINFO: Indexing the following files...\n")
        for currentPath in validPaths:
            print(f"- {currentPath}")


if __name__ == "__main__":
    main()
