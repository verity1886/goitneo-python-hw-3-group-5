from address_book import AddressBook, Record


def parse_input(user_input):
    cmd = ''
    try:
        cmd, *args = user_input.split()
    except ValueError:
        args = []
    cmd = cmd.strip().lower()
    return cmd, *args


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return 'Error: Contact is not found.'
        except ValueError as e:
            return 'Error: ' + str(e)

    return inner


@input_error
def handle_add_contact(args, address_book: AddressBook):
    if len(args) != 2:
        raise ValueError('Name & Phone arguments are required.')
    name, phone = args
    record = Record(name, phone)
    address_book.add_record(record)
    return 'Contact is added.'


@input_error
def handle_add_bday(args, address_book: AddressBook):
    if len(args) != 2:
        raise ValueError('Name & Phone arguments are required.')
    name, bday_str = args
    record: Record = address_book.find(name)
    record.add_birthday(bday_str)
    return 'Bday is added.'


@input_error
def handle_change_contact(args, address_book: AddressBook):
    if len(args) != 2:
        raise ValueError('Name & Birthday arguments are required.')
    name, phone = args
    record: Record = address_book.find(name)
    record.edit_phone(phone)
    return 'Contact is updated.'


@input_error
def handle_show_bday(args, address_book: AddressBook):
    if len(args) != 1:
        raise ValueError('Name is required argument.')
    name = args[0]
    record: Record = address_book.find(name)
    if not record.bday:
        raise ValueError('This record has no birthday set.')

    return 'Birthday: ' + str(record.bday)


@input_error
def handle_show_contact(args, address_book: AddressBook):
    if len(args) != 1:
        raise ValueError('Name is required argument.')
    name = args[0]
    record: Record = address_book.find(name)
    return str(record)


def handle_get_all(address_book: AddressBook):
    format_str = '{:<21}  {:<11} {:<10}'
    all = address_book.get_all()
    lines = [format_str.format(*item.values()) for item in all]
    output = ['=' * 42, format_str.format('Name:', 'Phone: ', 'Birthday: ')]
    output = output + lines + ['=' * 42]

    return '\n'.join(output)


contacts = [
    {"name": "Jhon", "phone": "0988285400", "birthday": '27.10.1955'},
    {"name": "Jack", "phone": "0988285401", "birthday": '22.10.1988'},
    {"name": "Odrey", "phone": "0988285402", "birthday": '25.10.1975'},
    {"name": "Bill", "phone": "0988285404", "birthday": '25.10.1975'},
    {"name": "Jaycob", "phone": "0988285404", "birthday": '28.10.1975'},
    {"name": "Lindon", "phone": "0988285405", "birthday": '26.10.1995'},
    {"name": "Tifany", "phone": "0988285406", "birthday": '27.10.1975'},
    {"name": "David", "phone": "0988285407", "birthday": '25.10.2003'},
    {"name": "Alex", "phone": "0988285408", "birthday": '29.10.1993'}
]


def main():
    address_book = AddressBook()

    for contact in contacts:
        rec = Record(contact['name'], contact['phone'])
        rec.add_birthday(contact['birthday'])
        address_book.add_record(rec)

    print(address_book)

    print('Welcome to the assistant bot!')
    while True:
        user_input = input('Enter a command: ')
        command, *args = parse_input(user_input)

        if command in ['close', 'exit']:
            print('Good bye!')
            break
        elif command == '':
            continue
        elif command == 'hello':
            print('How can I help you?')
        elif command == 'add-birthday':
            print(handle_add_bday(args, address_book))
        elif command == 'show-birthday':
            print(handle_show_bday(args, address_book))
        elif command == 'birthdays':
            print(address_book.get_birthdays_per_week())
        elif command == 'add':
            print(handle_add_contact(args, address_book))
        elif command == 'change':
            print(handle_change_contact(args, address_book))
        elif command == 'phone':
            print(handle_show_contact(args, address_book))
        elif command == 'all':
            print(handle_get_all(address_book))
        else:
            print('Invalid command.')


if __name__ == '__main__':
    main()
