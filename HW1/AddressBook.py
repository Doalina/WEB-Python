from collections import UserList
from datetime import datetime as dt, timedelta
from info import *
import pickle
import os


class LogAction:
    @staticmethod
    def log(action):
        current_time = dt.strftime(dt.now(), '%H:%M:%S')
        message = f'[{current_time}] {action}'
        with open('logs.txt', 'a') as file:
            file.write(f'{message}\n')


class SaveData:
    @staticmethod
    def save(data, file_name):
        with open(file_name + '.bin', 'wb') as file:
            pickle.dump(data, file)
        LogAction.log("Addressbook has been saved!")


class LoadData:
    @staticmethod
    def load(file_name):
        data = []
        emptyness = os.stat(file_name + '.bin')
        if emptyness.st_size != 0:
            with open(file_name + '.bin', 'rb') as file:
                data = pickle.load(file)
            LogAction.log("Addressbook has been loaded!")
        else:
            LogAction.log('Adressbook has been created!')
        return data


class SearchContact:
    @staticmethod
    def search(data, pattern, category):
        result = []
        category_new = category.strip().lower().replace(' ', '')
        pattern_new = pattern.strip().lower().replace(' ', '')

        for account in data:
            if category_new == 'phones':
                for phone in account['phones']:
                    if phone.lower().startswith(pattern_new):
                        result.append(account)
            elif account[category_new].lower().replace(' ', '') == pattern_new:
                result.append(account)

        if not result:
            print('There is no such contact in the address book!')
        return result


class EditContact:
    @staticmethod
    def edit(data, contact_name, parameter, new_value):
        names = []
        try:
            for account in data:
                names.append(account['name'])
                if account['name'] == contact_name:
                    if parameter == 'birthday':
                        new_value = Birthday(new_value).value
                    elif parameter == 'email':
                        new_value = Email(new_value).value
                    elif parameter == 'status':
                        new_value = Status(new_value).value
                    elif parameter == 'phones':
                        new_contact = new_value.split(' ')
                        new_value = []
                        for number in new_contact:
                            new_value.append(Phone(number).value)
                    if parameter in account.keys():
                        account[parameter] = new_value
                    else:
                        raise ValueError
            if contact_name not in names:
                raise NameError
        except ValueError:
            print('Incorrect parameter! Please provide the correct parameter')
        except NameError:
            print('There is no such contact in the address book!')
        else:
            LogAction.log(f"Contact {contact_name} has been edited!")
            return True
        return False


class RemoveContact:
    @staticmethod
    def remove(data, pattern):
        flag = False
        for account in data:
            if account['name'] == pattern:
                data.remove(account)
                LogAction.log(f"Contact {account['name']} has been removed!")
                flag = True
        return flag


class CongratulateContact:
    @staticmethod
    def __get_current_week():
        now = dt.now()
        current_weekday = now.weekday()
        if current_weekday < 5:
            week_start = now - timedelta(days=2 + current_weekday)
        else:
            week_start = now - timedelta(days=current_weekday - 5)
        return [week_start.date(), week_start.date() + timedelta(days=7)]

    @staticmethod
    def congratulate(data):
        result = []
        WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        current_year = dt.now().year
        congratulate = {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}
        for account in data:
            if account['birthday']:
                new_birthday = account['birthday'].replace(year=current_year)
                birthday_weekday = new_birthday.weekday()
                if CongratulateContact.__get_current_week()[0] <= new_birthday.date() < CongratulateContact.__get_current_week()[1]:
                    if birthday_weekday < 5:
                        congratulate[WEEKDAYS[birthday_weekday]].append(account['name'])
                    else:
                        congratulate['Monday'].append(account['name'])
        for key, value in congratulate.items():
            if len(value):
                result.append(f"{key}: {' '.join(value)}")
        return '_' * 50 + '\n' + '\n'.join(result) + '\n' + '_' * 50


class AddressBook(UserList):
    def __init__(self, data=None):
        if data is None:
            data = []
        self.data = data
        self.counter = -1

    def __str__(self):
        result = []
        for account in self.data:
            if account['birthday']:
                birth = account['birthday'].strftime("%d/%m/%Y")
            else:
                birth = ''
            if account['phones']:
                new_value = []
                for phone in account['phones']:
                    print(phone)
                    if phone:
                        new_value.append(phone)
                phone = ', '.join(new_value)
            else:
                phone = ''
            result.append(
                "_" * 50 + "\n" + f"Name: {account['name']} \nPhones: {phone} \nBirthday: {birth} \nEmail: {account['email']} \nStatus: {account['status']} \nNote: {account['note']}\n" + "_" * 50 + '\n')
        return '\n'.join(result)

    def __next__(self):
        phones = []
        self.counter += 1
        if self.data[self.counter]['birthday']:
            birth = self.data[self.counter]['birthday'].strftime("%d/%m/%Y")
        if self.counter == len(self.data):
            self.counter = -1
            raise StopIteration
        for number in self.data[self.counter]['phones']:
            if number:
                phones.append(number)
        result = "_" * 50 + "\n" + f"Name: {self.data[self.counter]['name']} \nPhones: {', '.join(phones)} \nBirthday: {birth} \nEmail: {self.data[self.counter]['email']} \nStatus: {self.data[self.counter]['status']} \nNote: {self.data[self.counter]['note']}\n" + "_" * 50
        return result

    def __iter__(self):
        return self

    def __setitem__(self, index, record):
        self.data[index] = {'name': record.name,
                            'phones': record.phones,
                            'birthday': record.birthday}

    def __getitem__(self, index):
        return self.data[index]

    def add(self, record):
        account = {'name': record.name,
                   'phones': record.phones,
                   'birthday': record.birthday,
                   'email': record.email,
                   'status': record.status,
                   'note': record.note}
        self.data.append(account)
        LogAction.log(f"Contact {record.name} has been added.")

    def save(self, file_name):
        SaveData.save(self.data, file_name)

    def load(self, file_name):
        self.data = LoadData.load(file_name)
        return self.data

    def search(self, pattern, category):
        return SearchContact.search(self.data, pattern, category)

    def edit(self, contact_name, parameter, new_value):
        return EditContact.edit(self.data, contact_name, parameter, new_value)

    def remove(self, pattern):
        return RemoveContact.remove(self.data, pattern)

    def congratulate(self):
        return CongratulateContact.congratulate(self.data)
