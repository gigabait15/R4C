from django.http import HttpResponse
from django.views import generic
from orders.models import Order
from robots.models import Robot


class OrderListView(generic.ListView):
    model = Order
    template_name = 'orders/order_list.html'
    

class CreateOrderView(generic.CreateView):
    model = Order
    fields = ('robot_serial',)
    template_name = 'orders/order_create.html'

    def form_valid(self, form):
        robot_serial = form.cleaned_data.get('robot_serial')

        try:
            robot = Robot.objects.get(serial=robot_serial)
        except Robot.DoesNotExist:
            form.add_error('robot_serial', 'Робот не найден')
            return self.form_invalid(form)

        if robot.sold is False:
            order = form.save(commit=False)
            order.status = False
            order.save()

            robot.sold = True
            robot.save()
            return HttpResponse(f"Заказ № {order.id} о приобритении робота {robot.serial} прошел успешно.")

        else:
            order = form.save(commit=False)
            order.status = True
            order.save()
            return HttpResponse(f"Заказ № {order.id} ожидает поступление робота {robot.serial}.")


