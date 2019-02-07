from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, View
from django.shortcuts import render
from django.utils import  timezone
import datetime

from orders.models import Order

# Create your views here.


class SalesView(LoginRequiredMixin, TemplateView):
  template_name = 'analytics/sales.html'

  def dispatch(self, *args, **kwargs):
    user = self.request.user
    if not user.is_staff:
      return render(self.request, "400.html", {})
    return super(SalesView, self).dispatch(*args, **kwargs)

  def get_context_data(self, *args, **kwargs):
    context = super(SalesView, self).get_context_data(*args, **kwargs)
    # two_weeks_ago = timezone.now() - datetime.timedelta(days=14)
    # one_week_ago = timezone.now() - datetime.timedelta(days=7)
    qs = Order.objects.all().by_weeks_range(weeks_ago=10, number_of_weeks=10)
    start_date = timezone.now().date() - datetime.timedelta(hours=24)
    end_date = timezone.now().date() + datetime.timedelta(hours=12)
    yesterday_data = qs.by_range(start_date=start_date, end_date=end_date).get_sales_breakdown()
    context['yesterday'] = yesterday_data
    context['today'] = qs.by_range(start_date=timezone.now().date()).get_sales_breakdown()
    context['this_week'] = qs.by_weeks_range(weeks_ago=1, number_of_weeks=1).get_sales_breakdown()
    context['last_four_weeks'] = qs.by_weeks_range(weeks_ago=5, number_of_weeks=4).get_sales_breakdown()
    return context


class SalesAjaxView(View):
  def get(self, request, *args, **kwargs):
    if request.is_ajax():
      data = {}
      if request.user.is_staff:
        qs = Order.objects.all().by_weeks_range(weeks_ago=5, number_of_weeks=5)
        if request.GET.get('type') == 'week':
          days = 7
          start_date = timezone.now().today() - datetime.timedelta(days=days-1)
          datetime_list = []
          labels = []
          salesItems = []
          # labels2 = []
          for x in range(0, days):
            new_time = start_date + datetime.timedelta(days=x)
            datetime_list.append(new_time)
            labels.append(new_time.strftime("%A")) # mon

            # labels2.append(new_time.strftime("%Y")) # 2019
            # labels2.append(new_time.strftime("%y")) # 19
            # labels2.append(new_time.strftime("%B")) # February
            # labels2.append(new_time.strftime("%h")) # Feb
            # labels2.append(new_time.strftime("%b")) # Feb
            # labels2.append(new_time.strftime("%m")) # 02
            # labels2.append(new_time.strftime("%d")) # 01
            # labels2.append(new_time.strftime("%A")) # Friday
            # labels2.append(new_time.strftime("%a")) # Fri
            # labels2.append(new_time.strftime("%H:%M:%S")) # 09:03:34
            # labels2.append(new_time.strftime("%H")) # 09
            # labels2.append(new_time.strftime("%I%p")) # 09AM
            # labels2.append(new_time.strftime("%M")) # 03
            # labels2.append(new_time.strftime("%S")) # 34
            # labels2.append(new_time.strftime("%d/%m/%Y, %H:%M:%S")) # 01/02/2019, 09:03:34
            # labels2.append(new_time.strftime("%c")) # Fri Feb  1 09:03:34 2019
            # labels2.append(new_time.strftime("%x")) # 02/01/19
            # labels2.append(new_time.strftime("%X")) # 09:03:34

            new_qs = qs.filter(updated__day=new_time.day, updated__month=new_time.month)
            day_total = new_qs.totals_data()['total__sum'] or 0
            salesItems.append(day_total)
          data['labels'] = labels
          data['data'] = salesItems
        if request.GET.get('type') == '4weeks':
          data['labels'] = ["Four Weeks Ago", "Three Weeks Ago", "Two Weeks Ago", "Last Week", "This Week"]
          current = 5
          data['data'] = []
          for i in range(0, 5):
            new_qs = qs.by_weeks_range(weeks_ago=current, number_of_weeks=1)
            sales_total = new_qs.totals_data()['total__sum'] or 0
            data['data'].append(sales_total)
            current -= 1
      return JsonResponse(data)
    return JsonResponse({'msg': 'Not Allowed'})