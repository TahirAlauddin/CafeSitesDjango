from django.urls import path, include
from django.http import HttpResponse
from .views import *

urlpatterns = [
    path('', view_home, name='home'),
    
    # CRUD for cafe
    path('create-cafe/', view_create_cafe, name='create-cafe'),
    path('cafe-detail/<int:pk>/', view_detail_cafe, name='cafe-detail'),
    path('delete-cafe/<int:pk>/', view_delete_cafe, name='delete-cafe'),
    path('update-cafe/<int:pk>/', view_update_cafe, name='update-cafe'),

    path('delete-table/', view_delete_table, name='delete-table'),
    path('color-picklist/', view_color_picklist, name='color-picklist'),
    
    path('data-for-analysis/', view_admin_board, name='admin-board'),
    path('__debug__/', include('debug_toolbar.urls')),

]
