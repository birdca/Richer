# Richer
## **Prerequisite**
- [Python 3.11.2](https://www.python.org/downloads/release/python-3112/)
- [poetry](https://github.com/python-poetry/install.python-poetry.org#osx--linux--bashonwindows--windowsmingw-install-instructions)
## Installation
### Poetry
#### Global Installation
```bash
$ curl -sSL https://install.python-poetry.org | python3 -
```
#### PATH Setting
```bash
$ vim ~/.bash_profile # or .bashrc or .zshrc

# Setting PATH for Poetry (1.3.1)
export PATH=$PATH:$HOME/.local/bin

$ source ~/.bash_profile
```
#### Dependencies
```bash
$ poetry env use python3
$ poetry shell
$ poetry install
```
