from collections import UserDict
from datetime import datetime
import re
import pickle
filename = 'Addressbook.dat'

class Field():
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
       self._value = new_value

class Name(Field):
    pass

class Phone(Field):

    @Field.value.setter
    def value(self, new_value):
        if bool(re.match('\d{3}.\d{3}.\d{2}.\d{2}', new_value)):
            self._value = new_value
        else:
            raise ValueError("Input phone in format ***-***-**-**")

class Birthday(Field):

     @Field.value.setter
     def value(self, new_value):
         if bool(re.match('\d{4}[.]\d{2}[.]\d{2}', new_value)):
             self._value = datetime.strptime(new_value, "%Y.%m.%d")
         else:
            raise ValueError("Input date in format YYYY.MM.DD")

class Record():
    def __init__(self, name, *phones):
        self.name = Name(name)
        self.phones = []
        if phones:
            for phone in phones:
                self.put_phone_list(phone)
        self.birthday = ''

    def put_phone_list(self, phone_new):
        phone_new = Phone(phone_new).value
        for phone in self.phones:
            if phone_new == phone.value:
                print(f"{phone_new} already recorded for {self.name.value}")
        self.phones.append(Phone(phone_new))

    def change(self, phone_old, phone_new):

        phone_old = Phone(phone_old).value
        phone_new = Phone(phone_new).value
        match = False

        for phone in self.phones:

            if phone.value == phone_new:
                return f"{phone_new} already recorded for {self.name.value}"

            if phone.value == phone_old:
                match = True

        if not match:
            return f"{phone_old} is not exist in the contact {self.name.value}"

        for index, phone in enumerate(self.phones):
            if phone.value == phone_old:
                self.phones.remove(phone)
                self.phones.insert(index, Phone(phone_new))
                return f"{phone_old} changed to {phone_new}"

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
        return f"{birthday} added to {self.name.value}"

    def days_to_birthday(self):
        today = datetime.today()
        bday = self.birthday.value
        nday = datetime(today.year, bday.month, bday.day)
        timediff = (nday - today).days + 1 if (today - nday).days < 0 else (datetime(nday.year + 1, nday.month, nday.day) - today).days + 1
        return f'{timediff} days till {self.name.value} birthday left!'

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def iterator(self, count=5):
        page = []
        i = 0
        for record in self.data.values():
            page.append(record)
            i += 1
            if i == count:
                yield page
                page = []
                i = 0
        if page:
            yield page

    def search(self, value):
        result = []
        for record in self.data.values():
            if re.search(value, record.name.value):
                result.append(f"{record.name.value}: {', '.join([phone.value for phone in record.phones])}")
            for phone in record.phones:
                if re.search(value, phone.value):
                    result.append(f"{record.name.value}: {', '.join([phone.value for phone in record.phones])}")
        return result

    def save_to_file(self):
        with open(filename, "wb") as pack:
            pickle.dump(self.data, pack)
        return f'all data was recorded successfully'

    def read_from_file(self):
        with open(filename, "rb") as unpack:
            self.data = pickle.load(unpack)
