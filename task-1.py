from collections import UserDict

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

class Record(Name):
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []
    
    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

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


book = AddressBook()

john = Record("John")
john.add_phone("1234567890")
john.add_phone("0987654321")

book.add_record(john)

# пошук
record = book.find("John")
print(record)

# редагування
record.edit_phone("1234567890", "1112223333")
print(record)

# видалення телефону
record.remove_phone("0987654321")
print(record)

# видалення контакту
book.delete("John")