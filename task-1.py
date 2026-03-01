from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name is required")
        super().__init__(value)


class Phone(Field):
    def __init__(self, value: str):
            if not (value.isdigit() and len(value) == 10):
                raise ValueError ("phone must contain 10 digits")
            super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            parsed_date = datetime.strptime(value, "%d.%m.%Y")
            super().__init__(parsed_date)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record():
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday = None
    
    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday: datetime):
        self.birthday = Birthday(birthday)

    def remove_phone(self, phone: str):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return True
        return False

    def edit_phone(self, old_phone: str, new_phone: str):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return True
        return False

    def find_phone(self, phone: str):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones}"
    
    
class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str):
        return self.data.get(name)

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]
            return True
        return False
    
    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        result = []

        for record in self.data.values():
            if not record.birthday:
                continue

            birthday = record.birthday.value.date()

            birthday_this_year = birthday.replace(year=today.year)
            if birthday_this_year < today:
                birthday_this_year = birthday.replace(year=today.year + 1)

            days_diff = (birthday_this_year - today).days

            if 0 <= days_diff <= 7:
                congratulation_date = birthday_this_year

                if congratulation_date.weekday() == 5:
                    congratulation_date += timedelta(days=2)
                elif congratulation_date.weekday() == 6:
                    congratulation_date += timedelta(days=1)

                result.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
                })

            return result
    
def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"Error: {e}"
        except IndexError:
            return "Error: not enough arguments"
        except KeyError:
            return "Error: contact not found"
    return wrapper

@input_error
def add_contact(args, book):
    name, phone = args
    record = book.find(name)
    
    if record is None:
        record = Record(name)
        book.add_record(record)
        if phone:
            record.add_phone(phone)
        return "Contact added."
    else:
        if phone:
            record.add_phone(phone)
        return "Phone added."


@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record and record.edit_phone(old_phone, new_phone):
        return "Phone updated."
    return "Phone not found."


@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    if record:
        return "; ".join(p.value for p in record.phones)
    return "Contact not found."


@input_error
def add_birthday(args, book):
    name, date = args
    record = book.find(name)
    if record:
        record.add_birthday(date)
        return "Birthday added."
    return "Contact not found."


@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return record.birthday.value.strftime("%d.%m.%Y")
    return "Birthday not set."


@input_error
def birthdays(book):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays next week."
    return "\n".join(f"{i['name']} → {i['congratulation_date']}" for i in upcoming)


def main():
    print("Welcome!")
    book = AddressBook()

    print("=== ДОДАЄМО КОНТАКТИ ===")
    print(add_contact(["John", "1234567890"], book))
    print(add_contact(["Anna", "1112223333"], book))

    print("\n=== ДОДАЄМО ДНІ НАРОДЖЕННЯ ===")
    print(add_birthday(["John", "05.03.1990"], book))
    print(add_birthday(["Anna", "07.03.1995"], book))

    print("\n=== ПОКАЗАТИ ДНІ НАРОДЖЕННЯ ===")
    print("John:", show_birthday(["John"], book))
    print("Anna:", show_birthday(["Anna"], book))

    print("\n=== ВСІ КОНТАКТИ ===")
    for record in book.data.values():
        print(record)

    print("\n=== НАЙБЛИЖЧІ ДНІ НАРОДЖЕННЯ ===")
    print(birthdays(book))

if __name__ == "__main__":
    main()
        


