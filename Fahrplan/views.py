from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView

import ReadInput

class PlanView(BaseView):
    @expose('/')
    def index(self):
        column_names = ['id', 'name']
        temp = dict(ReadInput.get_routes_mock())['routes']
        return self.render('admin/admin_data_routes_overview.html', records=temp, colnames=column_names)

class ModelViewWithoutCreate(ModelView):
    can_create=False
