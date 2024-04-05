from AddressBook import AddressBook, Record
from functools import wraps
from pathlib import Path
import pickle

def get_AddressBook(file_path:Path)->AddressBook:                                   #reads names and phones from file to list of dictionary
    try:
        with open(file_path, "rb") as file:
            book = pickle.load(file)
        print("Data successfully fetched!")
        return book
    except Exception as ex:
        return f"unable to fetch data from file {file_path.name}. Error:{ex}"

def save_AddressBook(book:AddressBook, file_path:Path):                              #writes database to file
    try:
        with open(file_path, "wb") as file:
            pickle.dump(book,file)
        return f"AddressBook {book.name} saved successfully to {file_path.name}"
    except Exception as ex:
        return f"unable to fetch save to file {file_path.name}. Error:{ex}"

def input_error(func):                                                                #decorator for main chat-bot functions
    @wraps(func)
    def inner(*args):
        name=''
        phone=''
        try:                                                                          #parsing arguments from command promt to variables
            if func.__name__ == 'parse_input':
                user_input = args[0]
            else:
                if type (args[0]) is AddressBook: 
                    book = args[0]
                else:
                    raise TypeError ("Wrong AddressBook")
                name = args[1][0]
                data = args[1][1]
        except (IndexError, ValueError, TypeError):
            pass                                                                      #in case of mistake doing nothing. all checks will be in block Match
        
        match func.__name__:                                                          #for different function differenet input arguments and feedback for user 
            case "add_contact":
                try:
                   return func(book, name, data)
                except Exception as ex:
                    return f"Unable to add contact. Error: {ex}"
            case "change_contact":                                                    #for different function - differenet messages and bot function calls
                try:
                    new_phone = input("Enter new phone to change phone {data} for contact {name}")
                    return func(book, name, data, new_phone)
                except Exception as ex:
                    return f"Unable to change contact. Error: {ex}"
            case "delete_contact":
                try:
                   return func(book, name)
                except Exception as ex:
                    return f"Unable to delete contact. Error: {ex}"         
            case "show_phone":
                try:
                    return func(book, name)
                except Exception as ex:
                    return f"Unable to show phone number. Error: {ex}"
            case "show_all":
                try:
                    return func(book)
                except Exception as ex:
                    return f"Unable to show all database. Error: {ex}"

            case "add_birthday":
                try:
                    return func(book, name,data)
                except Exception as ex:
                    return f"Unable to add birthday. Error: {ex}"
            case "show_birthday":
                try:
                    return func(book, name)
                except Exception as ex:
                    return f"Unable to show birthday. Error: {ex}"
            case "birthdays":
                try:
                    return func(book)
                except Exception as ex:
                    return f"Unable to show upgoing birthdays. Error: {ex}"
            case "parse_input":
                try:
                    return func(*args)
                except Exception as ex:
                    return f"Unable to parse parameters from command prompt. please use 'help' for help. Error: {ex}"
            case _:
                return "no such function"
    return inner

@input_error
def add_contact(book:AddressBook,name_to_add:str,phone_to_add:str)->str:                       #adds new line: name and phone to the list of dictionaries or new phone to exsistng phone
    record = book.find(name_to_add)
    if not record:
        record = Record(name_to_add)
        record.add_phone(phone_to_add)
        book.add_record(record)
    else:
        record.add_phone(phone_to_add)
    return f"data added: {record}"

@input_error
def change_contact(book:AddressBook,name_to_change:str,old_phone:str, new_phone:str)->str:       #change concrete phone by name (if more than 1 phone)
    record = book.find(name_to_change)
    record.edit_phone(old_phone, new_phone)
    return f"data for {record} updated"

@input_error
def delete_contact(book:AddressBook,name_to_del:str)->str:                              #delete contact by name
    book.delete(name_to_del)
    return f"Contact {name_to_del} was deleted from AddressBook"

@input_error
def show_phone(book:AddressBook, name_to_find:str)->str:                               #shows phone by name
    record = book.find(name_to_find)
    return f"phones in AdressBook {book.name} {record.show_phone()}"

@input_error
def show_all(book:AddressBook)->str:                                                   #shows all contacts
    return f"Your contact database: \n {book}"

@input_error
def add_birthday(book:AddressBook, name_to_find:str, birthday: str):                   ##adds birthday to the contact
    record = book.find(name_to_find)
    record.add_birthday(birthday)
    return f"brthday {birthday} added"
    
@input_error
def show_birthday(book:AddressBook, name_to_find:str):                                 #shows contact birthday
    record = book.find(name_to_find)
    return f"The birthday of {name_to_find} is {record.show_birthday()}"

@input_error
def birthdays(book:AddressBook):                                                        
    return f"Upcoming birtdays is: {book.birthdays()}"

@input_error
def parse_input(user_input):                                                            #parses input
    cmd, *args = user_input.split(' ')
    cmd = cmd.strip().lower()
    args = [arg.strip() for arg in args]                                                # Strip spaces from each argument
    return cmd, args

def main():
    print("Welcome to the assistant bot!")
    file_path = Path("AddressBook.svf")
    # adr_book = AddressBook()
    adr_book = get_AddressBook(file_path)
    while True:                                                                         # execution of commands to bot
        message = ""
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)                                         #parsing command promt in format <command> <-argumument1> <-argument2>...
        command = command.lower()
       
        match command:                                                                  # case for bot commands
            case "close"|"exit":                                                        # close або exit: Закрити програму.
                print("Good bye!")
                break
            case "hello":                   print("How can I help you? print 'help' for all commands") # hello: Отримати вітання від бота.
            case "get from file"|"get":     adr_book = get_AddressBook(file_path)       # get data from file
            case "add"|"add-contact":       print(add_contact(adr_book, args))          # add [ім'я] [телефон]: Додати або новий контакт з іменем та телефонним номером, або телефонний номер к контакту який вже існує.
            case "delete"|"delete-contact": print(delete_contact(adr_book,args))        # deletes contact by name from AddressBook 
            case "change-contact"|"change": print(change_contact(adr_book, args))       # change [ім'я] [новий телефон]: Змінити телефонний номер для вказаного контакту.
            case "show-contacts"|"all":     print(show_all(adr_book))                   # all: Показати всі контакти в адресній книзі.
            case "show-phone"|"phone":      print(show_phone(adr_book, args))           # phone [ім'я]: Показати телефонний номер для вказаного контакту.
            case "add-birthday":            print(add_birthday(adr_book, args))         # add-birthday [ім'я] [дата народження]: Додати дату народження для вказаного контакту.
            case "show-birthday":           print(show_birthday(adr_book, args))        # show-birthday [ім'я]: Показати дату народження для вказаного контакту.
            case "birthdays":               print(birthdays(adr_book))                  # birthdays: Показати дні народження, які відбудуться протягом наступного тижня.
            case "save to file"|"save":     print(save_AddressBook(adr_book,file_path)) # save data to file   

            case "help"|"?"|"/?":
                print("""available command of bot is:  
                      "hello" - to say hello to bot   
                      "close" or "exit" - to stop bot
                      commands for contacts: 
                          "get-from-file" or "get" - import contacts from file
                          "add-contact" or "add" with arguments "Name" and "Phone" will add contact to database (DB). for example add NewName NewPhone
                          "change-contact" or "change" with arguments "Name" and "Phone" will change contact in DB
                          "show-contacts" or "all" - to show all contacts in DB
                          "show-phone" or "phone" - with argument "Name" will show the phone of contact
                          "add-birthday" -  add-birthday "Name" "Date" will add Date to contact. Date format should be DD.MM.YYYY
                          "show-birthday" - show-birthday "Name" will show the birthday date of contact
                          "birthdays": will shows all contacts with birthdays during ongoing week
                          "save-to-file" or "save" - save names and phones to file
                    """)
            case _:                
                print("Invalid command. if you need assistance please enter: help")
    print(save_AddressBook(adr_book,file_path))

if __name__ == "__main__":
    main()