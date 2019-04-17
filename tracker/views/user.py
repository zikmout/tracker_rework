from tracker.views.base import BaseView
from tracker.models import User
from tracker.utils import flash_message, login_required, get_url_from_id
from tracker.models import User

class UserListView(BaseView):
    """View for reading and adding new roles."""
    SUPPORTED_METHODS = ['GET']
    @login_required
    def get(self):
        """Get all tasks for an existing user."""
        username = self.get_current_user()
        users_json = list()
        users = self.request_db.query(User).all()
        if users:
            [users_json.append(user.as_dict()) for user in users]
        self.render('admin/list_users.html', users_json=users_json)

class UserDelete(BaseView):
    SUPPORTED_METHODS = ['POST']
    def post(self, username):
        user = self.request_db.query(User).filter_by(username=username).first()
        if user:
            try:
                self.request_db.delete(user)
                self.request_db.commit()
                flash_message(self, 'success', 'User {} succesfully deleted.'.format(username))
                self.redirect('/api/v1/users_list')
            except Exception as e:
                flash_message(self, 'success', 'Impossible to delete user. Check shell logs for more information.')
                print('Exception : Impossible to delete user because : {}'.format(e))
                self.redirect('/api/v1/users_list')
        else:
            flash_message(self, 'danger', 'Username {} not found. Delete aborded.'.format(username))
            self.redirect('/api/v1/users_list')

class UserUnitView(BaseView):
    SUPPORTED_METHODS = ['GET']
    def get(self, username, projectname, uid):
        url = get_url_from_id(self.session['units'], uid)
        self.render('unit/index.html', url=url)