from collections import UserDict
from datetime import datetime, timedelta
import json


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        if len(value) > 20:
            msg = 'Name shouln\'t be longer than 20 symbols.'
            raise ValueError(msg)
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if not len(value) == 10 or not value.isnumeric():
            msg = 'Phone number should be 10 digits long.'
            raise ValueError(msg)
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            date_obj = datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError(value + ' does not match DD.MM.YYYY format')
        super().__init__(date_obj)

    def __str__(self):
        if self.value:
            return self.value.strftime('%d.%m.%Y')
        return ''


class Record:
    def __init__(self, name, phone):
        self.name = Name(name)
        self.phone = Phone(phone)
        self.bday = ''

    def edit_phone(self, new_phone):
        self.phone = Phone(new_phone)

    def add_birthday(self, bday):
        if bool(self.bday):
            raise ValueError('Birthday is already set.')
        self.bday = Birthday(bday)

    def __str__(self):
        return f'Contact name: {self.name.value}, phone: {self.phone}'


class AddressBook(UserDict):
    def add_record(self, record_candidate):
        if not type(record_candidate) == Record:
            raise ValueError('Record should instance of corresponfing class.')
        if record_candidate.name.value in self.data:
            raise ValueError('Record is already present.')
        self.data[record_candidate.name.value] = record_candidate

    def delete(self, record_name):
        if record_name not in self.data:
            raise KeyError
        del self.data[record_name]

    def find(self, record_name):
        if record_name not in self.data:
            raise KeyError
        return self.data[record_name]

    def get_all(self):
        lines = []
        for key in self.data.keys():
            rec: Record = self.data[key]
            lines.append({
                'name': str(rec.name),
                'phone': str(rec.phone),
                'birtday': str(rec.bday)
            })

        return lines

    def __str__(self):
        lines = []
        for key in self.data.keys():
            rec: Record = self.data[key]
            lines.append(
                'Name: {}; Phone: {}; Birthday: {}.'.format(
                    str(rec.name),
                    str(rec.phone),
                    str(rec.bday)
                )
            )

        return '\n'.join(lines)

    def get_birthdays_per_week(self):
        def get_congratulation_day(day_str: str):
            if day_str in ['Sunday', 'Saturday']:
                return 'Monday'
            return day_str

        today_dt = datetime.today().date()
        days = {}
        for key in self.data:
            try:
                user_bd = self.data[key].bday.value.date()
            except AttributeError:
                continue
            
            try:
                bday_this_year = user_bd.replace(year=today_dt.year)
            except ValueError:
                # user is born in a leap year, celebration is shifted to 28.02
                prev_day = user_bd.day - 1
                bday_this_year = user_bd.replace(year=today_dt.year,
                                                 day=prev_day)
            delta_days = (bday_this_year - today_dt).days

            # > 0 to show only preceeding birthdays
            if delta_days < 7 and delta_days > 0:
                birthday_week_day = bday_this_year.strftime('%A')
                congratulation_day = get_congratulation_day(birthday_week_day)

                if congratulation_day not in days:
                    days[congratulation_day] = []
                days[congratulation_day].append(str(self.data[key].name))

        result = {}
        # to show days of week starting from today
        for i in range(0, 7):
            dt = (datetime.now() + timedelta(days=i)).date()
            day_in_week = dt.strftime('%A')

            if day_in_week in days:
                result[day_in_week] = days[day_in_week]

        lines = []
        for day in result:
            lines.append('{}: {}'.format(day, ', '.join(result[day])))

        return '\n'.join(lines)
