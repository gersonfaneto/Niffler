Niffler
=======

[![License](https://img.shields.io/github/license/gersonfaneto/Niffler?style=for-the-badge&logo=appveyor)](https://github.com/gersonfaneto/Niffler/blob/main/LICENSE)
[![Stars](https://img.shields.io/github/stars/gersonfaneto/Niffler?style=for-the-badge&logo=appveyor)](https://github.com/gersonfaneto/Niffler)
![Status](https://img.shields.io/static/v1?label=STATUS&message=DEVELOPMENT+🚧&color=yellow&style=for-the-badge)
![Language](https://img.shields.io/static/v1?label=LANGUAGE&message=Python&color=informational&style=for-the-badge)
![Version](https://img.shields.io/static/v1?label=VERSION&message=1.0&color=success&style=for-the-badge)

> This project was based on a college assignment, so don't expect much of it 😉.

## What is this?

'Niffler' is inspired on the functionality of other tools like 'fzf' and 'grep'. It is a tool
capable of sweeping through a collection of files and summarize their contents on
a searchable 'Inverted Index'.

## How to use it?

> **Note**: 'Niffler' is a CLI tool built on a GNU/Linux based system. Support for
> other operating systems is under testing.

1. Clone this repository into your local machine.

```console
$ git clone https://github.com/gersonfaneto/Niffler
```

2. Execute the `Niffler.py` using your installed python interpreter (version >= 3.10)
or as any other bash like script.

```console
$ python Niffler.py --help # Display the help message.
```

```console
$ ./Niffler.py -h # Equivalent to the above.
```

> **Note**: 'Niffler' will create and keep it's dependencies on a folder called 
`./niffler` located on your `$HOME` directory.

## License

Released under [MIT](https://github.com/gersonfaneto/Niffler/blob/main/LICENSE) by [gersonfaneto](https://github.com/gersonfaneto).
