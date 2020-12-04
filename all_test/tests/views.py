from datetime import datetime, date
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe
from datetime import timedelta
import calendar
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
# import pandas


from .models import Test, Mytests
from .utils import Calendar
from .forms import TestForm

@login_required
def trial(request):
    user = []
    user.append(request.user)
    mytests = Test.objects.filter(liked_users__in=user)
    # mytests = Mytests.objects.filter(user=request.user).values('test')
    # test_id_list = []
    # for mytest in mytests:
    #     test_id = mytest.values()
    #     test_id_list.append(test_id)



    #     # tests = Test.objects.filter(pk=test_id)

    context = {
      
       'tests' : mytests
    }
    return render(request, 'tests/trial.html', context)

    # for event in events:
    #     start_time = event.start_time
    #     end_time = event.end_time
    #     # datelist = [ ]
    #     # datelist.append(start_time)

    # # form_to = pandas.date_range(start=start_time, end=end_time)
    # # start_time = '2020-04-20'
    # # end_time = '2020-04-21'
    # form_to = pandas.date_range(start=start_time, end=end_time)
    # context = {
      
    #     'from_to' : form_to
    # }
    


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

class TestCalendarView(generic.ListView):
    model = Test
    template_name = 'my_test_calendar/calendar.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def index(request):
    tests = Test.objects.all()
    context = {
        'tests' : tests,
    }
    return render(request, 'tests/index.html', context)

def detail(request, test_id):
    test = Test.objects.get(id=test_id)
    context = { 'test' : test }
    return render(request, 'tests/detail.html', context)

@login_required
def like(request, test_id):

    if request.method == 'POST':
        try:
            test = Test.objects.get(id=test_id)

            if request.user in test.liked_users.all():
                test.liked_users.remove(request.user)
            else:
                test.liked_users.add(request.user)

            return redirect('tests:detail', test_id=test.id)

        except Test.DoesNotExist:
            pass

    return redirect('tests:index')
