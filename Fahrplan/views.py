from flask_admin import BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

import ReadInput

# Admin Views
class PlanView(BaseView):
    @expose('/')
    def index(self):
        column_names = ['id', 'name']
        temp = dict(ReadInput.get_routes_mock())['routes']
        return self.render('admin/admin_data_routes_overview.html', records=temp, colnames=column_names)

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin_check
        else:
            return False

class ModelViewWithoutCreate(ModelView):
    can_create=False

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin_check
        else:
            return False

class HomeAdminView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin_check
        else:
            return False

class ModelViewCustom(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin_check
        else:
            return False