from collections import UserDict
from datetime import datetime, timedelta, date
import pickle
from pathlib import Path


class Field:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value
        
    def __repr__(self):
        return self.value


class Name(Field):
    def __str__(self):
        return str(self.value)


class LastName(Field):
    def __str__(self):
        return str(self.value)


class Email(Field):
    pass


class Phone(Field): 
    def __init__(self, value):
        super().__init__(value)
    
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if isinstance(new_value, int):
            self._value = new_value
        else:
            print("Only intiger numbers")


class Record:
    def __init__(self, name, last_name,  phones = None, emails = None, birthday = None):    
        self.name = Name(name)
        self.last_name = LastName(last_name)
        self.phones = [Phone(phone) for phone in (phones or [])]
        self.emails = [Email(email) for email in (emails or [])]
        self.birthday = birthday

    def __repr__(self):
        return f"({self.name}, {self.last_name}, {self.phones}, {self.emails})"
      
    
    def add_phone(self, phone):
        self.phones.append(Phone(phone))
    
    def add_email(self, email):
        self.emails.append(Email(email))


    def change_phone(self, old_phone, new_phone):
         for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = Phone(new_phone)
                break

    def change_email(self, old_email, new_email):
         for i, email in enumerate(self.emails):
            if email.value == old_email:
                self.emails[i] = Email(new_email)
                break


    def remove_phone(self, phone):                 
        new_phones = []
        if self.phones:
            for e in self.phones:
                if e.value != phone:
                    new_phones.append(e)
            self.phones = new_phones

    def remove_email(self, email):                  
        new_emails = []
        if self.emails:
            for e in self.emails:
                if e.value != email:
                    new_emails.append(e)
            self.emails = new_emails

    def days_to_birthday(self):     
        if self.birthday:
            today = datetime.now()
            next_bday = datetime(today.year, self.birthday.month, self.birthday.day)
            if today > next_bday:
                next_bday= datetime(today.year+1, self.birthday.month, self.birthday.day)
            days_left = (next_bday - today).days
            return days_left
        else:
            return None


class Birthday(): 
    def __init__(self,birthday):
        self._birthday = self.validate_birthday(birthday)

    @property
    def birthday(self):
        return self._birthday

    @birthday.setter
    def birthday(self, new_birthday):
        self._birthday = self.validate_birthday(new_birthday)

    def validate_birthday(self, new_birthday):
        if isinstance(new_birthday, date):
            return new_birthday
        else:
            raise ValueError("Błąd: new_birthdate musi być obiektem datetime.date.")


class AddressBook(UserDict):   
    def __init__(self, file_path="address_book.bin"):
        super().__init__()
        self.file_path = file_path
        self.load_from_file()

    def save_to_file(self):
        try:
            with open(self.file_path, "wb") as file:
                pickle.dump(self, file)
            print("Książka adresowa została pomyślnie zapisana.")
        except Exception as e:
            print(f"Błąd podczas zapisywania książki adresowej: {e}")

    def load_from_file(self):
        try:
            with open(self.file_path, "rb") as file:
                address_book = pickle.load(file)
                self.data = address_book.data
            print("Książka adresowa została pomyślnie wczytana.")
        except FileNotFoundError:
            print("Plik nie istnieje. Tworzenie nowej książki adresowej.")
        except Exception as e:
            print(f"Błąd podczas wczytywania książki adresowej: {e}")
    def __iter__(self):
        self.current_page = 0
        self.keys_list = list(self.data.keys())
        return self   
    
    def __next__(self):
        page_size = 2
        start = self.current_page * page_size
        end = min((self.current_page + 1) * page_size, len(self.keys_list))
        if start < end:
            records = [self.data[self.keys_list[i]] for i in range(start, end)]
            self.current_page += 1
            return records
        else:
            raise StopIteration
        
     
    def add_record(self, record: Record):
        key = record.name.value
        if key not in self.data:
            self.data[key] = []
        self.data[key].append(record)

    def find_record_by_name(self, name):            
        matching_records = []
        for record_list in self.data.values(): 
            for record in record_list:                 
                if name.lower() in record.name.value.lower():  
                    matching_records.append(record)         
        return matching_records
    
    def find_record_by_last_name(self, last_name):            
        matching_records = []
        for record_list in self.data.values(): 
            for record in record_list:                 
                if last_name.lower() in record.last_name.value.lower():  
                    matching_records.append(record)         
        return matching_records

    def find_record_by_phone_number(self, phone):   
        matching_records = []
        for record_list in self.data.values():
            for record in record_list:                  
                if any (phone in phone_number.value for phone_number in record.phones):        
                    matching_records.append(record)         
        return matching_records

    def find_record_by_email(self, email):          
        matching_records = []
        for record_list in self.data.values():
            for record in record_list:
                if any(email in email_field.value for email_field in record.emails):
                    matching_records.append(record)
        return matching_records
     



 

def main():    
    
    record_1 = Record(name="Alice", last_name="Smith", phones=["+111223344", "+111223344"], emails=["alice.smith@email.com"], birthday=datetime(year=2001, month=12, day=3))
    record_2 = Record(name="Bob", last_name="Johnson", phones=["999888777", "444333222"], emails=["bob.johnson@email.com"])
    record_3 = Record(name="Emily", last_name="Davis", phones=["777888999"], emails=["emily.davis@email.com"], birthday=datetime(year=1980, month=12, day=3))
    record_4 = Record(name="Michael", last_name="Miller", phones=["444523466"], emails=["michael.miller@email.com"], birthday=datetime(year=2001, month=11, day=6))
    record_5 = Record(name="Sophia", last_name="Anderson", phones=["222333444"], emails=["sophia.anderson@email.com"], birthday=datetime(year=1980, month=12, day=3))
    record_6 = Record(name="Daniel", last_name="White", phones=["555666777"], emails=["daniel.white@email.com"])
    record_7 = Record(name="Olivia", last_name="Brown", phones=["666777888"], emails=["olivia.brown@email.com"], birthday=datetime(year=1980, month=12, day=30))
    record_8 = Record(name="William", last_name="Taylor", phones=["333444555"], emails=["william.taylor@email.com"], birthday=datetime(year=1985, month=1, day=30))
    record_9 = Record(name="Emma", last_name="Jones", phones=["888999000", "444555666"], emails=["emma.jones@email.com"], birthday=datetime(year=1980, month=11, day=30))
    record_10 = Record(name="James", last_name="Wilson", phones=["123456789"], emails=["james.wilson@email.com", "j.wn@email.com"])

    address_book = AddressBook()
    address_book.add_record(record_1)
    address_book.add_record(record_2)
    address_book.add_record(record_3)
    address_book.add_record(record_4)
    address_book.add_record(record_5)
    address_book.add_record(record_6)
    address_book.add_record(record_7)
    address_book.add_record(record_8)
    address_book.add_record(record_9)
    address_book.add_record(record_10)
    

    address_book.save_to_file()
    loaded_address_book = AddressBook()
    loaded_address_book.load_from_file()

    
    print("Is loaded address book equal to the original one?",
          loaded_address_book.data == address_book.data)

    

#### TESTY ####
### Wyszukiwanie rekordów według kryteriów:
## po imieniu:
    # search_name = address_book.find_record_by_name("emm")
    # print(search_name)

## po nazwisku:  
    # search_last_name = address_book.find_record_by_last_name("Taylor")
    # print(search_last_name)

## po numerze telefonu:
    # search_phone1 = address_book.find_record_by_phone_number("44466")      
    # search_phone2 = address_book.find_record_by_phone_number("888999000")
    # print(search_phone1, search_phone2)

## po adresie email:
    # search_email = address_book.find_record_by_email("emma.jones@email.com")
    # print(search_email)


### Edycja opcjonalnych pól:
## Dodawanie kolejnego numeru telefonu:
    # print(record_2)
    # record_2.add_phone("0000")
    # print(record_2)

## Dodawanie kolejnego adresu mail:
    # print(record_2)
    # record_2.add_email("one@two.pl")
    # print(record_2)


## Zmiana numeru telefonu:
    # print(record_2)
    # record_2.change_phone("444333222", "1111111")
    # print(record_2)

## Zmiana adresu email:
    # print(record_2)
    # record_2.change_email("bob.johnson@email.com", "one@two.pl")
    # print(record_2)


## Usuwanie numeru telefonu:
    # print(record_2)
    # record_2.remove_phone("444333222")
    # print(record_2)

## Usuwanie adresu email:
    # print(record_10)
    # record_10.remove_email("james.wilson@email.com")
    # print(record_10)


    

### Wyświetlenie rekordów zawartych w książce adresowej
    # for record in address_book:
    #     print(record)



### Testowanie settera i gettera
    # phone_instance = Phone(777888999) # Tworzenie instancji
    # phone_instance.value = 42  # Ustawienie wartości za pomocą settera

    # phone_instance.value = "abc"  
    # print(phone_instance.value)  # Odczyt wartości za pomocą gettera

    # birthday_instance = Birthday(birthday=datetime(year=1980, month=12, day=3))  
    # birthday_instance.birthday = datetime(year=1990, month=5, day=15)
    
    # print(birthday_instance.birthday)
    # try:
    #     birthday_instance.birthday = "nie data"
    # except ValueError as e:
    #     print(e)                   


### Ilość dni do urodzin:
    # print(record_1)
    # days_left = record_1.days_to_birthday()
    # print(f"Do urodzin pozostało {days_left} dni.")

### Wyświetlanie N recordów na stronę
    # for records_batch in address_book:
    #     print(records_batch)



if __name__ == "__main__":
    main()
    