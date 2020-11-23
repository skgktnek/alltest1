from datetime import datetime, timedelta
from calendar import HTMLCalendar

from .models import Test


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None, user=None):
        self.user = user
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    def formatday(self, day, tests):
        tests_register_day_start_per_day = tests.filter(register_day_start__day=day) 
       	tests_register_day_end_per_day = tests.filter(register_day_end__day=day) 
        tests_test_day_per_day = tests.filter(test_day__day=day) 
        tests_results_day_per_day = tests.filter(results_day__day=day)   
        rs = ''
        re = ''
        t = ''
        r = ''
    	
        for test_register_day_start in tests_register_day_start_per_day:
            rs += f'<li> {test_register_day_start.get_html_url} -시험등록시작일 </li>'

        for test_register_day_end in tests_register_day_end_per_day:
            re += f'<li> {test_register_day_end.get_html_url} -시험등록마감일 </li>'

        for test_test_day in tests_test_day_per_day:
            t += f'<li> {test_test_day.get_html_url} -시험일 </li>'

        for test_results_day in tests_results_day_per_day:
            r += f'<li> {test_results_day.get_html_url} -시험결과발표일 </li>'

        if day != 0: 
            return f"<td><span class='date'><a href='my_today/{self.year}/{self.month}/{day}'>{day}</a></span><ul> {rs}{re}{t}{r}</ul></td>"
        return '<td></td>'

    def formatweek(self, theweek, tests):
        week =''
        for d, weekday in theweek:
            week += self.formatday(d, tests)
        return f'<tr> {week} </tr>'
    
    def formatmonth(self, withyear=True):
        tests = Test.objects.filter(register_day_start__year=self.year, register_day_start__month=self.month) | Test.objects.filter(register_day_end__year=self.year, register_day_end__month=self.month) | Test.objects.filter(test_day__year=self.year, test_day__month=self.month) | Test.objects.filter(results_day__year=self.year, results_day__month=self.month)   
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, tests)}\n'
        return cal
        
