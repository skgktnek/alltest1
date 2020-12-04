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


from .models import MyEvent
from .utils import Calendar
from .forms import EventForm

def index(request):
    events = MyEvent.objects.all()
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
    return render(request, 'my_todo_calendar/index.html', context)

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

class EventDelete(generic.DeleteView):
    model = MyEvent
    success_url = '/my_todo_calendar/'


class EventEdit(generic.UpdateView):
    model = MyEvent
    form = EventForm()
    fields = ['title', 'description', 'start_time', 'end_time']
    template_name = 'my_todo_calendar/event.html'

    def form_valid(self, form):
        form.save()
        return render(self.request, 'my_todo_calendar/event_edit_success.html', {"message" : "일정 업데이트 완료"})

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form(EventForm)
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

@login_required(login_url='accounts:login')
def event_details(request, event_id):
    event = MyEvent.objects.get(id=event_id)
    context = {
        'event': event,
    }
    return render(request, 'my_todo_calendar/event_details.html', context)

@login_required(login_url='accounts:login')
def my_today(request, year, month, day):
    events = MyEvent.objects.filter(start_time__year=year, start_time__month=month, end_time__day = day, user=request.user)
    context = {
        'events' : events,
        'year' : year,
        'month' : month,
        'day' : day,
    }
    return render(request, 'my_todo_calendar/my_today.html', context)


