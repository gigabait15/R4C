from django.urls.base import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.views import generic
from robots.models import Robot
from django.core.serializers import serialize
from django.core.management import call_command
import os


class RobotsView(generic.ListView):
    """
    Класс представления для просмотра всех экземпляров класса Robot
    """
    model = Robot
    template_name = 'robots/list_robots.html'

    def get_queryset(self):
        """
        Возвращает всеx роботов.
        """
        return self.model.objects.all()

    # данный метод для возвращает данные в json формате
    # def get(self, request, *args, **kwargs):
    #     """
    #     Метод get возвращает все экземпляры из БД
    #     :return: возвращает все объекты модели в JSON формате
    #     """
    #     robots = self.model.objects.all()
    #     robots_data = serialize('json', robots)
    #
    #     return JsonResponse(robots_data, safe=False, content_type='application/json')


class CreateRobotView(generic.CreateView):
    """
    класс представления для создание экземпляра в БД
    """
    model = Robot
    fields = ('model', 'version')
    template_name = 'robots/robots_create.html'
    success_url = reverse_lazy("robots:view_robots")


def download_weekly_report(request):
    """
    Функция представления для получения отчета.
    При переходе по данному эндпоинту формируется недельный отчет и скачивается файл.
    """
    try:
        report_filepath = call_command('get_weekly_report')

        if report_filepath and os.path.exists(report_filepath):
            with open(report_filepath, 'rb') as f:
                response = HttpResponse(
                    f.read(),
                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )

                response['Content-Disposition'] = f'attachment; filename={os.path.basename(report_filepath)}'

                return response
        else:
            return HttpResponse("Отчет не найден", status=404)

    except Exception as e:
        return HttpResponse(f"Произошла ошибка при создании отчета: {str(e)}", status=500)