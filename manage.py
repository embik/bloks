#!venv/bin/python
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from bloks import app, db
from bloks.cmd import AddCommand

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('add', AddCommand)

if __name__ == '__main__':
    manager.run()
