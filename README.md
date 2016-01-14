# bloks

`bloks` is a simple blogging software written in Python 3. It's based on Flask and SQLAlchemy.

## Setup

* Run `bash bootstrap`. It will check for Python requirements present on your system and run necessary steps for the initial setup (create directories, install pip packages into virtual environment, etc).
* Create initial user via `./manage.py add user` and input all data
* Start development server via `./manage.py runserver` or start production stack

## Attribution

The default template is based on (read: partially copied from) html5up.net's [future imperfect design](http://html5up.net/future-imperfect). It's released under [CC-BY 3.0](http://html5up.net/license). The theme incorporates noticeable changes and differs from the original work.

Additionally, I'd like to thank everyone involved with dependencies `bloks` incorporates. The authors and contributors of Flask (Armin Ronacher and many others), Miguel Grinberg for his [Flask Mega-Tutorial](http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) and various Flask extensions he released, and many more.

## License

[MIT](https://github.com/embik/bloks/blob/master/LICENSE). Because why not?

## Notes

* Yes, alembic revisions are ignored via `.gitignore`. It looks like alembic doesn't handle migrations for sqlite3 too well (read: it failed multiple times for me).
