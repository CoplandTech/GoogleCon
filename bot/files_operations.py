import os
import xml.etree.ElementTree as ET
import json
import re
import shutil
from datetime import datetime
from department_numbers import department_numbers

def create_backup(file_path, backup_dir):
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    timestamp = datetime.now().strftime("%d-%m-%Y")
    base_name = os.path.basename(file_path)
    backup_file = os.path.join(backup_dir, f"{timestamp}_{base_name}")
    
    shutil.copy2(file_path, backup_file)
    print(f"Копия создана: {backup_file}")
    
    backups = sorted([f for f in os.listdir(backup_dir) if base_name in f])
    if len(backups) > 4:
        for old_backup in backups[:-4]:
            os.remove(os.path.join(backup_dir, old_backup))
            print(f"Старая копия удалена: {old_backup}")

def format_phone_number(phone_number):
    # Удаляем все символы, кроме цифр
    digits = re.sub(r'\D', '', phone_number)
    # Проверяем, что номер состоит из 11 цифр и начинается с 8 или 7
    if len(digits) == 11 and (digits[0] == '8' or digits[0] == '7'):
        # Заменяем первую цифру на 8
        digits = '8' + digits[1:]
        # Форматируем номер
        formatted_number = f"{digits[0]} {digits[1:4]} {digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
        return formatted_number
    else:
        return phone_number  # Возвращаем оригинальный номер, если он не соответствует ожиданиям

def normalize_phone_number(phone_number):
    phone_number = re.sub(r'[\s()]', '', phone_number)
    phone_number = re.sub(r'^\+7', '8', phone_number)
    phone_number = re.sub(r'\D', '', phone_number)
    return phone_number

def create_xml(contact_list, xml_filename):
    root = ET.Element("YealinkIPPhoneBook")
    title_element = ET.SubElement(root, "Title")
    title_element.text = "Yealink"

    menu_elements = {}

    for contact in contact_list:
        department = contact.get("organizations", [{}])[0].get("department")
        if department:
            # Если департамент еще не был добавлен, добавьте его.
            if department not in menu_elements.keys():
                menu_element = ET.SubElement(root, "Menu")
                menu_element.set("Name", department)
                if department in department_numbers:
                    for number in department_numbers[department]:
                        menu_element.set("Number", number)
                menu_elements[department] = menu_element
            else:
                menu_element = menu_elements[department]

            names = contact.get("names", [])
            if names:
                surname = names[0].get("familyName", "")
                first_name = names[0].get("givenName", "")
                middle_name = names[0].get("middleName", "")
                full_name = f"{surname} {first_name}"
                unit_element = ET.SubElement(menu_element, "Unit")
                unit_element.set("Name", full_name)
                unit_element.set("Middle", middle_name)
                phone_numbers = contact.get("phoneNumbers", [])
                email = contact.get("emailAddresses", [{}])[0].get("value", "")
                jobTitle = contact.get("organizations", [{}])[0].get("title", "")
                phone1_number = ""
                phone2_number = ""
                for phone_number_data in phone_numbers:
                    phone_number = phone_number_data.get("value", "")
                    phone_type = phone_number_data.get("type", "").lower()
                    if phone_type == "короткий":
                        phone1_number = phone_number
                    elif phone_type == "корпоративный":
                        phone2_number = phone_number
                unit_element.set("Phone1", format_phone_number(phone1_number))
                unit_element.set("Phone2", format_phone_number(phone2_number))
                unit_element.set("Phone3", "")
                unit_element.set("Email", email)
                unit_element.set("JobTitle", jobTitle)
                unit_element.set("default_photo", "Resource:")
    
    tree = ET.ElementTree(root)
    tree.write(xml_filename, encoding="utf-8", xml_declaration=True)
        
def create_json_https(contact_list, json_filename):
    data = []
    for contact in contact_list:
        contact_data = {}
        names = contact.get("names", [])
        if names:
            surname = names[0].get("familyName", "")
            first_name = names[0].get("givenName", "")
            middle_name = names[0].get("middleName", "")
            full_name = f"{surname} {first_name} {middle_name}"
            contact_data["Name"] = full_name
            phone_numbers = contact.get("phoneNumbers", [])
            contact_data["PhoneNumbers"] = [phone.get("value", "") for phone in phone_numbers]
            data.append(contact_data)

    with open(json_filename, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def get_contacts_by_phone():
    with open('ПУТЬ К ДИРЕКТОРИИ ДЛЯ ЧТЕНИЯ JSON с именем файла: contacts.json', 'r', encoding='utf-8') as json_file:
        https_book_contacts = json.load(json_file)

    contacts_list = []
    
    for contact in https_book_contacts:
        name = contact.get("Name", "")
        phone_numbers = contact.get("PhoneNumbers", [])

        surname = ""
        first_name = ""
        middle_name = ""
        if name:
            parts = name.split()
            if len(parts) > 2:
                surname = parts[0]
                first_name = parts[1]
                middle_name = parts[2]
            elif len(parts) == 2:
                surname = parts[0]
                first_name = parts[1]
            elif len(parts) == 1:
                surname = parts[0]

        all_phone_numbers = [phone_data for phone_data in phone_numbers]

        contact_info = {
            "Name": f"{surname} {first_name} {middle_name}",
            "PhoneNumbers": all_phone_numbers
        }
        
        contacts_list.append(contact_info)
    
    return contacts_list