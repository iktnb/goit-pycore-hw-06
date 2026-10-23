"""Адресна книга: поля, контакти та керування записами."""

from collections import UserDict


class Field:
    """Базовий клас поля запису."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Обов'язкове непорожнє ім'я контакту."""

    def __init__(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Contact name must be a non-empty string.")
        super().__init__(value.strip())


class Phone(Field):
    """Номер телефону, що містить рівно 10 цифр від 0 до 9."""

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if (
            not isinstance(value, str)
            or len(value) != 10
            or not value.isascii()
            or not value.isdigit()
        ):
            raise ValueError("Phone number must contain exactly 10 digits.")
        # Валідація працює і під час створення, і під час зміни номера.
        self._value = value


class Record:
    """Контакт з обов'язковим ім'ям і списком телефонів."""

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        found_phone = self.find_phone(phone)
        if found_phone is None:
            raise ValueError("Phone number not found.")
        self.phones.remove(found_phone)

    def edit_phone(self, old_phone, new_phone):
        found_phone = self.find_phone(old_phone)
        if found_phone is None:
            raise ValueError("Phone number not found.")
        # Setter перевіряє нове значення до зміни збереженого номера.
        found_phone.value = new_phone

    def find_phone(self, phone):
        for saved_phone in self.phones:
            if saved_phone.value == phone:
                return saved_phone
        return None

    def __str__(self):
        phones = "; ".join(phone.value for phone in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones}"


class AddressBook(UserDict):
    """Словник записів, ключами якого є імена контактів."""

    def add_record(self, record):
        if not isinstance(record, Record):
            raise TypeError("Address book entries must be Record objects.")
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        return self.data.pop(name, None)


def main():
    """Демонструє використання класів на прикладі з умови."""
    book = AddressBook()

    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    for record in book.data.values():
        print(record)

    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")
    print(john)

    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")

    book.delete("Jane")


if __name__ == "__main__":
    main()
