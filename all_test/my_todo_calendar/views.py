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

from .models import MyEvent
from .utils import Calendar
from .forms import EventForm

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


class MyCalendarView(LoginRequiredMixin, generic.ListView):
    login_url = 'accounts:login'
    model = MyEvent
    template_name = 'my_todo_calendar/calendar.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        user = self.request.user
        cal = Calendar(d.year, d.month, user)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

@login_required(login_url='accounts:login')
def create_event(request):    
    form = EventForm(request.POST or None)
    if request.POST and form.is_valid():
        title = form.cleaned_data['title']
        description = form.cleaned_data['description']
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']
        MyEvent.objects.get_or_create(
            user=request.user, 
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time
        )
        return HttpResponseRedirect(reverse('my_todo_calendar:my_calendar'))
    return render(request, 'my_todo_calendar/event.html', {'form': form})

class EventEdit(generic.UpdateView):
    model = MyEvent
    fields = ['title', 'description', 'start_time', 'end_time']
    template_name = 'my_todo_calendar/event.html'

@login_required(login_url='accounts:login')
def event_details(request, event_id):
    event = MyEvent.objects.get(id=event_id)
    context = {
        'event': event,
    }
    return render(request, 'my_todo_calendar/event_details.html', context)

class EventDelete(generic.DeleteView):
    model = MyEvent
    success_url = '/my_todo_calendar/'
