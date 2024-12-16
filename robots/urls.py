from django.urls.conf import path
from robots.apps import RobotsConfig
from robots.views import RobotsView, CreateRobotView

app_name = RobotsConfig.name


urlpatterns = [
    path('view_robots/', RobotsView.as_view(), name='view_robots'),
    path('create_robot/', CreateRobotView.as_view(), name='create_robot'),
]