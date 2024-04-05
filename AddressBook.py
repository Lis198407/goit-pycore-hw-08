from collections import UserDict
from datetime import datetime
import re

class WrongRecord(Exception):                                         # Exception for problem with records in AdressBook
    def __init__(self, message="No such record in address book"):
        self.message = message
        super().__init__(self.message)

class WrongPhone(Exception):                                          # Exception for problem with phones in Records
    def __init__(self, message="Error in phone"):
        self.message = message
        super().__init__(self.message)

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
		pass

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value,"%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
    
    def __str__(self):
         date_str = self.value
         return date_str.strftime("%Y-%m-%d")

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.is_phone = self.__check_phone()                                 # Checking in auto mode Phone for 10 digits
  
    def __check_phone(self):
        pattern = r'^\d\s?(\d{3}\s?){2}\d{3}$'                             # pattern for 10 digits. for 12 digits with+ '^\+?\d{1,3}\s?(\d{3}\s?){2}\d{3}$'
        return bool(re.match(pattern, self.value))                         # Use re.match to check if the string matches the pattern

class Record:
    def __init__(self, name, birthday = None):
        self.name = Name(name)
        self.phones = []
        self.birthday = birthday

    def add_birthday(self, birthday_str:str):
        try:
            self.birthday =  Birthday(birthday_str)
        except Exception as ex:
            raise Exception (ex)
    
    def show_birthday(self):
        if self.birthday is not None:
            return f"{self.birthday}"
        else:
            return "There is no birthday in AddressBook"

    def __find_phone(self, phone_str:str)-> Phone:                         #find a Phone obj in record by phone in str
        return next((phone for phone in self.phones if phone.value == phone_str), None)
    
    def add_phone(self, phone_str:str):                                     #Adding phone from str
        try:
            phone_to_add = Phone(phone_str)          
            if not phone_to_add.is_phone:                                    #checking the phone vs rules (10 digit)
                raise WrongPhone (f"Phone {phone_str} must have 10 digits!") # if not - message via exception
            elif phone_to_add in self.phones:                                # checking for duplicates
                raise WrongPhone (f"Phone {phone_str} already exist in this record!") #if exist - message to user via exception
            else:
                self.phones.append(phone_to_add)                             # adding the phone if it's OK
        except Exception as ex:
            raise WrongPhone (ex)

    def remove_phone(self, phone_str: str):                                        #deleting phone from record
        try:
            phone_to_del = self.__find_phone(phone_str)                        #findind the Phone in Record by str of the phone
            if phone_to_del:
                self.phones.remove(phone_to_del)
            else:
                raise WrongPhone (f"No such phone {phone_str} in record!")  #if not found - raise a exception with message
        except Exception as ex:
            raise WrongPhone (ex)
    
    def edit_phone(self, old_phone_str:str, new_phone_str:str):              # Editing the phone by finding the phone by phone and changing to new one
        try:
            old_phone = self.__find_phone(old_phone_str)
            new_phone = Phone(new_phone_str)
            if old_phone and new_phone.is_phone:                             #checking if Phone to change in Record and weather new phone in Phone according to rules of 10 digits
                i = self.phones.index(old_phone)
                self.phones[i] = new_phone
            else:
                raise WrongPhone (f"Can't change phone {old_phone}. It's not in records, or {new_phone} not a phone")
        except Exception as ex:
            raise WrongPhone (ex)
    
    def show_phone(self):
        if len(self.phones)>1:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"    
        else:
            return "There are no phones in AddressBook"
   
    def __str__(self):
           return f"Contact name: {self.name.value}, birthday is {self.birthday}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    record_count = 0                                                          #Quantity of records in Adress Book
    
    def __init__(self,name=""):
        self.name = ""
        self.data = []
     
    def find(self, record_name: str) -> Record:                               #Finds Record by Name and returns Record if found
        return next((rec for rec in self.data if rec.name.value == record_name), None)
        
    def add_record(self, record:Record):                                             #adding the record to records in self.data
        try:
            if not self.find(record.name.value):                                    #checking for duplicates
                self.data.append(record)
                self.record_count +=1                                         #increasing Quantity of records in AdressBook                                
            else:
                raise WrongRecord(f"Record {record.name} already exist in phonebook {self.name}")
        except Exception as ex:
            raise WrongRecord (f"AddressBook Add record error: {ex}")

    def delete(self, rec_name: str):                                          #deleting the Record by record Name
        try:
            record = self.find(rec_name)
            if record:                                                        # if Record in records in self.data in AdressBook than Pop it
                self.data.remove(record)                
                self.record_count -=1
            else:
                raise WrongRecord(f"No such record {record.name} in phonebook {self.name}") #Raise the exception, that delete can't be made
        except Exception as ex:
            raise WrongRecord (f"AddressBook Delete record error:{ex}, record: {record.name}")

    def __str__(self):
        if self.record_count>0:
            message = f"in Adress Book '{self.name}' there are {self.record_count} contacts: \n"
            for record in self.data:
                    message += f"{record}\n"
            return message
        else:
            return "No records in AddressBook"
    
    def birthdays(self):
        now = datetime.now()
        i=0
        upcoming_birthday = {}
        for record in self.data:
            try:
                birthday_datetime = record.birthday.value
                greeting_date = birthday_datetime.replace(year = now.year)                                                        #changing the year to current
                weekdiff = greeting_date.isocalendar()[1]-now.isocalendar()[1]                                                    #difference in weeks between today and birthday date
                if upcoming_birthday.get(greeting_date.date().strftime("%d.%m.%Y")):                                              #if already in dict, than add name to the same day
                        str_temp = upcoming_birthday[greeting_date.date().strftime("%d.%m.%Y")]
                        upcoming_birthday[greeting_date.date().strftime("%d.%m.%Y")] = str_temp + ', '+ record.name.value
                elif weekdiff == 0 and greeting_date.isoweekday() in [6,7]:                                                       #if this week and SAT or SAN then MONDAY to greet
                    greeting_date = datetime(greeting_date.year,greeting_date.month,greeting_date.day+7-greeting_date.weekday())  # shift to next monday if weekend
                elif weekdiff == 1:                                                                                               #if next week than - date 
                    upcoming_birthday[greeting_date.date().strftime("%d.%m.%Y")] = record.name.value
            except Exception as ex:
                raise WrongRecord (f"birthdays: error message {ex}, record: {record}")
            i +=1
        return upcoming_birthday