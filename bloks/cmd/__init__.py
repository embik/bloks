from flask.ext.script import Manager, Command, Option
from blog.models import User, Hash
from blog.auth import create_hash
from blog import db


class UserCommand(Command):
    '''Creates a new user'''

    option_list = (
        Option('--name', dest='name', help='create user with nickname NAME'),
        Option('--password', dest='password', help='create user with password PASSWORD'),
        Option('--is-admin', action='store_true', dest='admin',
               help='create user as admin (only works in non-interactive mode)'),
        Option('--no-interactive', action='store_true', dest='non_interactive',
               help='non-interactive mode (no questions asked)'),
    )

    def run(self, name=None, password=None, admin=False, non_interactive=False):
        if name is None and not non_interactive:
            name = input('Nickname: ')
        if password is None and not non_interactive:
            password = input('Password: ')

        if not non_interactive:
            admin_input = input('Create as administrator? [Y/N] ')
            if admin_input == 'Y' or admin_input == 'y':
                admin = True
            elif admin_input == 'N' or admin_input == 'n':
                admin = False
            else:
                print('Error: Unrecognized input. Aborting.')
                return 1

        if name is None or password is None:
            print('Error: Missing keys. Aborting.')
            return 1

        user = User(nickname=name, is_admin=admin)
        db.session.add(user)
        db.session.commit()
        h = Hash(user_id=user.id, passwd_hash=create_hash(password))
        db.session.add(h)
        db.session.commit()

        return 0

AddCommand = Manager(usage='Adds additional objects to the database')
AddCommand.add_command('user', UserCommand())
