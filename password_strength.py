import argparse


def load_data(path_to_file):
    with open(path_to_file, 'r', encoding='utf-8') as file:
        return file.read()


def find_password_symbol(string, password):
    found = False
    for symbol in string:
        find = password.find(symbol)
        if find >= 0:
            found = True
            break
    return found


def get_password_strength(password):
    assessment = 1
    len6 = False
    len9 = False
    birthday_error = False
    numbers = "0123456789"
    not_a_number = False
    lowercase_letters = "abcdefghijklmnopqrstuvwxyz"
    lowercase = find_password_symbol(lowercase_letters, password)
    uppercase_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    uppercase = find_password_symbol(uppercase_letters, password)
    special_characters = " !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    special_char = find_password_symbol(special_characters, password)
    blacklist = load_data("blacklist.txt").split()
    blacklist_bool = False
    counter = 0
    for symbol in password:
        for number in numbers:
            if symbol == number:
                counter += 1
    for pass_word in blacklist:
        if pass_word == password.lower():
            blacklist_bool = True
    if counter != len(password):
        not_a_number = True
    if len(password) > 6:
        len6 = True
        assessment += 1
    if len(password) > 9:
        len9 = True
        assessment += 1
    if not_a_number:
        if counter == 1:
            assessment += 1
        elif counter > 1:
            assessment += 2
    if lowercase:
        assessment += 1
    if uppercase:
        assessment += 1
    if special_char:
        assessment += 1
    elif not not_a_number:
        if len(password) == 6 or len(password) == 8:
            birthday_error = True
    return {'assessment': assessment, 'len6': len6, 'len9': len9,
            'not_a_number': not_a_number, 'uppercase': uppercase,
            'special_char': special_char, 'blacklist_bool': blacklist_bool,
            'birthday_error': birthday_error}


def add_parser():
    new_parser = argparse.ArgumentParser()
    new_parser.add_argument('password', help='your password')
    return new_parser.parse_args()


if __name__ == '__main__':
    args = add_parser()
    checked = get_password_strength(args.password)

    if not checked['len6'] or not checked['len9'] \
            or not checked['not_a_number'] or not checked['uppercase'] \
            or not checked['special_char'] or checked['blacklist_bool']:
        print("Strength of your password = {}.".format(checked['assessment']))
        if not checked['len6']:
            print("Length ERROR!")
        if not checked['not_a_number']:
            print("Only number ERROR!")
        if not checked['uppercase']:
            print("Lowercase only ERROR!")
        if not checked['special_char']:
            print("Have not special char ERROR!")
        if checked['blacklist_bool']:
            print("Blacklist ERROR!")
    else:
        print("Strength of your password = 10.")
        print("Your password have not errors.\n Your password is GREAT!")
