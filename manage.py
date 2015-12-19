#!venv/bin/python
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from blog import app, db
from blog.cmd import AddCommand

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('add', AddCommand)

if __name__ == '__main__':
    manager.run()
