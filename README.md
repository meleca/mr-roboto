# mr_roboto
A fun IRC bot that help us on work days

# Development

Prior to start the development on mr_roboto it's necessary to follow some steps
in order to setup the environment: [*virtual environment*][pipenv], [*database
migration*][alembic] and [*pre-commit hooks*][pre-commit].

## Virtual environment through [**Pipenv**][pipenv]

The first thing you need to do after the `git clone` is setup the *virtual
environment* using **pipenv** tool. This tool requires you have at least
*Python3* (used in this project) and **Python3-pip** (or install **pipenv**
directly through your system's package manager).

```
$ pip install --user pipenv
$ cd <cloned-repo-folder>
$ pipenv --python python3
$ pipenv shell
$ pipenv install --dev
```

Once it's done you're ready to start coding, but you still need the database
setup in order to run it properly.

## Database migration through [**alembic**][alembic]

This tool will be the one to create and maintain your database running and
up-to-date. Every time a new database relation (table) is created or modified
you need to make sure to rerun the command:

```
$ pipenv run alembic upgrade head
```

## Compliance hook during code commit

Git allow us to create hook for its different stages, like *commit*, *merge* and
*push*. We've created one on *commit* stage to ensure some checking tools run
before the code even reach the git remote server. The hook was created using
[**pre-commit**][pre-commit] tool and in order to get it running correctly run:

```
$ pipenv run pre-commit install
```

From now on every time you hit `git commit` you're going to see some additional
information from the commit hook tools in case something fails, otherwise
nothing else will be prompted.

**Note:** *To make sure the hooks got your changes correctly and will run the
checking tools over it it's important to get them on **staging area** before
actually commit it. Unstaged files being directly commited through `git commit
-a` can lead to false results. Thus, please, whenever you need to actually
commit something first add them to your staging area with `git add`.*

## Running

With the three steps done you can easily run mr_roboto:

```
$ python mr_roboto.py settings.ini
```

[pipenv]: https://pipenv.readthedocs.io/en/latest/
[alembic]: https://alembic.sqlalchemy.org/en/latest/
[pre-commit]: https://pre-commit.com/
