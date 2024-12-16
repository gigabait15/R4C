from django.urls.base import reverse_lazy
from django.http import JsonResponse
from django.views import generic
from .models import Robot
from django.core.serializers import serialize


class RobotsView(generic.ListView):
    """
    Класс для представления просмотра всех экземпляров класса Robot
    """
    model = Robot
    # template_name = 'robots/list_robots.html'

    def get(self, request, *args, **kwargs):
        """
        Метод get возвращает все экземпляры из БД
        :return: возвращает все объекты модели в JSON формате
        """
        robots = self.model.objects.all()
        robots_data = serialize('json', robots)

        return JsonResponse(robots_data, safe=False, content_type='application/json')


class CreateRobotView(generic.CreateView):
    model = Robot
    fields = ('model', 'version')
    template_name = 'robots/robots_create.html'
    success_url = reverse_lazy("robots:view_robots")

    def form_valid(self, form):
        model = form.cleaned_data.get('model')
        version = form.cleaned_data.get('version')
        serial = f"{model}-{version}"

        if Robot.objects.filter(serial=serial).exists():
            form.add_error(None, "Робот с этой серией уже существует.")
            return self.form_invalid(form)

        robot = form.save(commit=False)
        robot.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)



