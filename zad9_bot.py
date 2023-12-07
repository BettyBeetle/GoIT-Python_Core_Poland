import sys

def input_error(function):
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except KeyError:
            return f"Contact does not exist in contacs."
        except ValueError:
            return f" The command is incorrect.\n The correct syntax of command is e.g. Mark Smith 123456 or Tom 123456"
        except IndexError:
            return "Enter name and phone number separately."
    return wrapper


def get_handler(command):
    return COMMANDS[command]

def exit():
    sys.exit()

def good_bye():
    sys.exit("Good bye")

def hello():
    return "How can I help you?"


@input_error
def add(data):
    
    data = data.removeprefix("add").strip()
    name, phone = data.rsplit(" ", maxsplit=1)
    name = name.title()
    if name in CONTACTS:
        return f"The contact is already in contacts."
    CONTACTS[name] = phone
    return f"Contact {name} added to contacts."


@input_error
def change(data):

    data = data.removeprefix("change").strip()
    name, phone = data.rsplit(" ", maxsplit=1)
    name = name.title()
    if name in CONTACTS:
        CONTACTS[name] = phone
        return f"I've changed {name} phone number"
    return f"{name} is not found in contacts."


def show_all():
    contact_list = [f"{name}: {phone}" for name, phone in CONTACTS.items()]
    return contact_list
        

@input_error
def phone(data):
    name = data.removeprefix("phone").strip().capitalize()
    return CONTACTS[name] 

    
COMMANDS = {
    ".": exit,
    "good bye": good_bye,
    "close": good_bye,
    "exit": good_bye,
    "hello": hello,
    "add ": add,
    "change ": change,
    "show all": show_all,
    "phone ": phone,
}

CONTACTS = {}

def main(): 

    while True:
        user_input_org = input(">>: ")
        user_input = user_input_org.lower().strip()
    
        known_command = False
        for key in COMMANDS.keys():
            if user_input.startswith(key):
                known_command = True
                handler = get_handler(key)
                match key:
                    case "." | "good bye" | "close" | "exit" | "hello":
                        print(handler())
                    case "show all":
                        for info in show_all():
                            print(info)
                    case "add " | "change " | "phone ":
                        print(handler(user_input))
                break
        if not known_command:
            print(f"The command {user_input_org} is incorrect.")
    

main() 