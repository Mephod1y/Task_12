from Task_12_classes import AddressBook, Record

contacts_dict = AddressBook()

def input_error(function):
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except KeyError:
            return 'Wrong name'
        except ValueError as exception:
            return exception.args[0]
        except IndexError:
            return 'Enter name and number'
        except TypeError:
            return 'Wrong command'
    return wrapper

@input_error
def hello():
    return 'How can I help you?'

@input_error
def exit_func():
    return "Good bye"

@input_error
def show_all():  # функція повертає всі записи в словнику AddressBook
    contacts = "All data in AddressBook:"
    for name in contacts_dict:
        contacts += f'\n{name}: '
        for phone in contacts_dict[name].phones:
            contacts += f"{phone.value}"
        contacts += f" {contacts_dict[name].birthday.value}"
    return contacts

@input_error
def add_name_phone(data):  # функція додає ведене ім'я телефон до екземляру класу Record
    new_data = data.strip().split(" ")
    name = new_data[0]
    phones = new_data[1]
    if name in contacts_dict:
        raise ValueError('This contact already exist.')
    record = Record(name)
    record.put_phone_list(phones)
    contacts_dict.add_record(record)
    return f'You added new contact: {name} with this {phones}'

@input_error
def change_phone(user_input):  # функція змінює телефон по ключу в словнику AddressBook
    user_input = user_input.split()
    name = user_input[0]
    current_phone = user_input[1]
    new_phone = user_input[2]
    return contacts_dict[name].change(current_phone, new_phone)

@input_error
def show_phone(user_input): # функція повертає телефон по ключу в словнику AddressBook
    phones = ""
    user_input = user_input.split()
    name = user_input[0]
    for phone in (contacts_dict[name]).phones:
        phones += f"{phone.value} "
    return phones

@input_error
def add_birth(user_input):
    user_input = user_input.split()
    name = user_input[0]
    birthday = user_input[1]
    return contacts_dict[name].add_birthday(birthday)

@input_error
def show_birth(user_input):
    user_input = user_input.split()
    name = user_input[0]
    return contacts_dict[name].days_to_birthday()

@input_error
def search(user_input):
    user_input = user_input.split()
    pattern = user_input[0]
    return contacts_dict.search(pattern)

def save():
    return contacts_dict.save_to_file()

def read():
    return contacts_dict.read_from_file()

functions = {
    'hello': hello,
    'add': add_name_phone,
    'change': change_phone,
    'phone': show_phone,
    'show all': show_all,
    'exit': exit_func,
    'close': exit_func,
    'good bye': exit_func,
    'birth': add_birth,
    'day': show_birth,
    'search': search,
    'save': save,
    'read': read
}

def parser_input(user_input):
    new_input = user_input
    data = ''
    for key in functions:
        if user_input.strip().lower().startswith(key):
            new_input = key
            data = user_input[len(new_input):]
            break
    if data:
        return reaction_func(new_input)(data)
    return reaction_func(new_input)()

def reaction_func(reaction):
    return functions.get(reaction, break_func)

def break_func():
    return 'Wrong command'

def main():
    read()
    while True:
        user_input = input('Enter command: ')
        result = parser_input(user_input)
        print(result)
        if result == 'Good bye':
            break
    save()

if __name__ == "__main__":
    main()
