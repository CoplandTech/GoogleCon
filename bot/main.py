import os.path
import files_operations 
import google_api


SCOPES = ["https://www.googleapis.com/auth/contacts.readonly"]

# Глобальные переменные для контактов
xml_book_contacts = []
https_book_contacts = []
other_contacts = []

xml_book_contacts, https_book_contacts, other_contacts = google_api.fetch_contacts(SCOPES)

def main():
    backup_dir = "ПУТЬ К ДИРЕКТОРИИ ДЛЯ БЕКАПОВ, СОЗДАЮЩИХСЯ РАЗ В СУТКИ КРОМЕ СБ. И ВС."
    contacts_xml_path = "ПУТЬ К ДИРЕКТОРИИ ДЛЯ СОЗДАНИЯ XML с именем файла: contacts.xml"
    https_contacts_json_path = "ПУТЬ К ДИРЕКТОРИИ ДЛЯ СОЗДАНИЯ JSON с именем файла: contacts.json"

    files_operations.create_backup(contacts_xml_path, backup_dir)
    files_operations.create_backup(https_contacts_json_path, backup_dir)

    files_operations.create_xml(xml_book_contacts, contacts_xml_path)
    files_operations.create_json_https(https_book_contacts, https_contacts_json_path)
    
    print("\nXML Book Contacts:")
    for contact in xml_book_contacts:
        print(contact)
    
    print("\nHTTPS Book Contacts:")
    for contact in https_book_contacts:
        print(contact)
    
    print("\nOther Contacts:")
    for contact in other_contacts:
        print(contact)

if __name__ == "__main__":
    main()
