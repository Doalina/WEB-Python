from AddressBook import *


class AddContactAction:
    @staticmethod
    def execute(book):
        name = Name(input("Name: ")).value.strip()
        phones = Phone().value
        birth = Birthday().value
        email = Email().value.strip()
        status = Status().value.strip()
        note = Note(input("Note: ")).value
        record = Record(name, phones, birth, email, status, note)
        return book.add(record)


class SearchContactAction:
    @staticmethod
    def execute(book):
        print("There are following categories: \nName \nPhones \nBirthday \nEmail \nStatus \nNote")
        category = input('Search category: ')
        pattern = input('Search pattern: ')
        result = (book.search(pattern, category))
        for account in result:
            if account['birthday']:
                birth = account['birthday'].strftime("%d/%m/%Y")
                result = "_" * 50 + "\n" + f"Name: {account['name']} \nPhones: {', '.join(account['phones'])} \nBirthday: {birth} \nEmail: {account['email']} \nStatus: {account['status']} \nNote: {account['note']}\n" + "_" * 50
                print(result)


class EditContactAction:
    @staticmethod
    def execute(book):
        contact_name = input('Contact name: ')
        parameter = input('Which parameter to edit(name, phones, birthday, status, email, note): ').strip()
        new_value = input("New Value: ")
        return book.edit(contact_name, parameter, new_value)


class RemoveContactAction:
    @staticmethod
    def execute(book):
        pattern = input("Remove (contact name or phone): ")
        return book.remove(pattern)


class SaveContactAction:
    @staticmethod
    def execute(book):
        file_name = input("File name: ")
        return book.save(file_name)


class LoadContactAction:
    @staticmethod
    def execute(book):
        file_name = input("File name: ")
        return book.load(file_name)


class CongratulateAction:
    @staticmethod
    def execute(book):
        print(book.congratulate())


class ViewContactsAction:
    @staticmethod
    def execute(book):
        print(book)


class Bot:
    def __init__(self):
        self.book = AddressBook()

    def execute(self, action):
        actions = {
            'add': AddContactAction(),
            'search': SearchContactAction(),
            'edit': EditContactAction(),
            'remove': RemoveContactAction(),
            'save': SaveContactAction(),
            'load': LoadContactAction(),
            'congratulate': CongratulateAction(),
            'view': ViewContactsAction(),
        }

        if action in actions:
            result = actions[action].execute(self.book)
            if result is not None:
                print(result)
        else:
            print("There is no such command!")


if __name__ == "__main__":
    bot = Bot()

