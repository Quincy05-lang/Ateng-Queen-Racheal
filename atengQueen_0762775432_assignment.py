#Task 1
import re

contacts = []


def validate_phone(phone):
    """Return True when phone contains only digits, hyphens, and an optional leading plus."""
    if not phone:
        return False
    return bool(re.fullmatch(r'\+?[0-9-]+', phone))


def validate_email(email):
    """Return True when email is empty or contains both '@' and '.' characters."""
    if not email:
        return True
    return '@' in email and '.' in email


def add_contact():
    name = input('Enter contact name: ').strip()
    if not name:
        print('Error: Name cannot be blank.')
        return

    phone = input('Enter phone number: ').strip()
    if not validate_phone(phone):
        print('Error: Phone number may contain only digits, hyphens, and an optional leading \'+\'. Operation cancelled.')
        return

    email = input('Enter email (optional): ').strip()
    if email and not validate_email(email):
        print('Error: Email must contain an @ symbol and a period (.). Operation cancelled.')
        return

    contacts.append({'name': name, 'phone': phone, 'email': email})
    print('Contact added successfully.')


def update_contact():
    target_name = input('Enter the name of the contact to update: ').strip()
    for contact in contacts:
        if contact['name'].lower() == target_name.lower():
            phone = input(f'Enter new phone number [{contact["phone"]}]: ').strip()
            if not phone:
                phone = contact['phone']
            if not validate_phone(phone):
                print('Error: Phone number may contain only digits, hyphens, and an optional leading \'+\'. Operation cancelled.')
                return

            email = input(f'Enter new email [{contact.get("email", "")}]: ').strip()
            if not email:
                email = contact.get('email', '')
            if email and not validate_email(email):
                print('Error: Email must contain an @ symbol and a period (.). Operation cancelled.')
                return

            contact['phone'] = phone
            contact['email'] = email
            print('Contact updated successfully.')
            return

    print('Error: Contact not found.')


def list_contacts():
    if not contacts:
        print('No contacts available.')
        return

    print('\nContacts:')
    for index, contact in enumerate(contacts, start=1):
        print(f"{index}. {contact['name']} - {contact['phone']} - {contact['email']}")
    print()


def main():
    while True:
        print('\nContact Manager')
        print('1. Add contact')
        print('2. Update contact')
        print('3. List contacts')
        print('4. Search contacts')
        print('5. Exit')

        choice = input('Choose an option: ').strip()
        if choice == '1':
            add_contact()
        elif choice == '2':
            update_contact()
        elif choice == '3':
            list_contacts()
        elif choice == '4':
            search_contacts()
        elif choice == '5':
            print('Goodbye!')
            break
        else:
            print('Invalid option. Please try again.')


if __name__ == '__main__':
    main()

#Task 2

def display_search_results(results, query):
    if not results:
        print(f'No contacts matched "{query}".')
        return

    print(f'\nSearch results for "{query}":')
    for index, contact in enumerate(results, start=1):
        print(f"{index}. Name: {contact['name']}")
        print(f"   Phone: {contact['phone']}")
        print(f"   Email: {contact.get('email', 'N/A')}")
    print()


def search_contacts():
    query = input('Enter search query (name, phone, or email): ').strip().lower()
    if not query:
        print('Error: Search query cannot be blank.')
        return

    matched_contacts = [
        contact for contact in contacts
        if query in contact['name'].lower()
        or query in contact['phone'].lower()
        or query in contact.get('email', '').lower()
    ]

    display_search_results(matched_contacts, query)

#Task 3

class ContactManager:
    def __init__(self):
        self.contacts = []

    def validate_phone(self, phone):
        return bool(re.fullmatch(r'\+?[0-9-]+', phone))

    def validate_email(self, email):
        return not email or ('@' in email and '.' in email)

    def find_contact(self, name):
        name_lower = name.lower()
        for contact in self.contacts:
            if contact['name'].lower() == name_lower:
                return contact
        return None

    def add_contact(self, name, phone, email):
        if not name:
            return False, 'Name cannot be blank.'
        if not self.validate_phone(phone):
            return False, 'Phone number may contain only digits, hyphens, and an optional leading +.'
        if email and not self.validate_email(email):
            return False, 'Email must contain an @ symbol and a period (.).'

        self.contacts.append({'name': name, 'phone': phone, 'email': email})
        return True, 'Contact added successfully.'

    def view_contact(self, name):
        return self.find_contact(name)

    def update_contact(self, name, phone=None, email=None):
        contact = self.find_contact(name)
        if not contact:
            return False, 'Contact not found.'

        if phone:
            if not self.validate_phone(phone):
                return False, 'Phone number may contain only digits, hyphens, and an optional leading +.'
            contact['phone'] = phone

        if email is not None:
            if email and not self.validate_email(email):
                return False, 'Email must contain an @ symbol and a period (.).'
            contact['email'] = email

        return True, 'Contact updated successfully.'

    def delete_contact(self, name):
        contact = self.find_contact(name)
        if not contact:
            return False, 'Contact not found.'
        self.contacts.remove(contact)
        return True, 'Contact deleted successfully.'

    def search_contacts(self, query):
        query = query.lower()
        return [
            contact for contact in self.contacts
            if query in contact['name'].lower()
            or query in contact['phone'].lower()
            or query in contact.get('email', '').lower()
        ]

    def list_contacts(self):
        return list(self.contacts)

    def format_contact(self, contact):
        return (
            f"Name: {contact['name']}\n"
            f"Phone: {contact['phone']}\n"
            f"Email: {contact.get('email') or 'N/A'}"
        )

    def display_contacts(self, contacts, title='Contacts'):
        if not contacts:
            print(f'No contacts found for {title}.')
            return

        print(f'\n=== {title} ===')
        for index, contact in enumerate(contacts, start=1):
            print(f'{index}. {self.format_contact(contact)}')
            print()


def main():
    manager = ContactManager()

    while True:
        print('\n=== Contact Manager Menu ===')
        print('1. Add Contact')
        print('2. View Contact')
        print('3. Update Contact')
        print('4. Delete Contact')
        print('5. Search Contacts')
        print('6. List All Contacts')
        print('7. Exit')

        choice = input('Choose an option (1-7): ').strip()

        if choice == '1':
            name = input('Enter contact name: ').strip()
            phone = input('Enter phone number: ').strip()
            email = input('Enter email (optional): ').strip()
            success, message = manager.add_contact(name, phone, email)
            print(message)

        elif choice == '2':
            name = input('Enter name to view: ').strip()
            contact = manager.view_contact(name)
            if contact:
                print('\n' + manager.format_contact(contact))
            else:
                print('Contact not found.')

        elif choice == '3':
            name = input('Enter name of the contact to update: ').strip()
            contact = manager.view_contact(name)
            if not contact:
                print('Contact not found.')
                continue

            phone = input(f'Enter new phone number [{contact["phone"]}]: ').strip()
            email = input(f'Enter new email [{contact.get("email", "N/A")}]: ').strip()
            phone = phone or contact['phone']
            email = email if email != '' else contact.get('email', '')
            success, message = manager.update_contact(name, phone=phone, email=email)
            print(message)

        elif choice == '4':
            name = input('Enter name of the contact to delete: ').strip()
            success, message = manager.delete_contact(name)
            print(message)

        elif choice == '5':
            query = input('Search by name, phone, or email: ').strip()
            if not query:
                print('Error: Search query cannot be blank.')
                continue
            results = manager.search_contacts(query)
            manager.display_contacts(results, title=f'Search Results for "{query}"')

        elif choice == '6':
            manager.display_contacts(manager.list_contacts(), title='All Contacts')

        elif choice == '7':
            print('Goodbye!')
            break

        else:
            print('Invalid option. Please choose a number between 1 and 7.')


if __name__ == '__main__':
    main()

