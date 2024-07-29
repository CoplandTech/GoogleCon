import os
import json
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Указываем разрешения, включая refresh token
SCOPES = ["https://www.googleapis.com/auth/contacts.readonly", "https://www.googleapis.com/auth/userinfo.profile", "offline"]

def fetch_contacts(scopes):
    xml_book_contacts = []
    https_book_contacts = []
    other_contacts = []

    # Получаем абсолютный путь к файлам credentials.json и token.json
    credentials_path = os.path.join(os.path.dirname(__file__), "auth", "credentials.json")
    token_path = os.path.join(os.path.dirname(__file__), "auth", "token.json")

    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, scopes)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, scopes)
            creds = flow.run_console()
            # Сохраняем refresh token
            with open(token_path, "w") as token:
                token.write(creds.to_json())

    try:
        service = build("people", "v1", credentials=creds)
        results = (
            service.people()
            .connections()
            .list(
                resourceName="people/me",
                pageSize=1000,  # Increase page size to fetch all contacts
                personFields="names,emailAddresses,phoneNumbers,memberships,organizations",
            )
            .execute()
        )
        connections = results.get("connections", [])
        all_contacts = []
        for person in connections:
            all_contacts.append(person)
        
        for contact in all_contacts:
            memberships = contact.get("memberships", [])
            group_ids = [membership.get("contactGroupMembership", {}).get("contactGroupId") for membership in memberships]
            if "4742592e8b960a62" in group_ids:  # ID ГРУППЫ из GOOGLE CONTACT
                xml_book_contacts.append(contact)
            if "f1351030eedda16" in group_ids: # ID ГРУППЫ из GOOGLE CONTACT
                https_book_contacts.append(contact)
            if not any(group_id in ["4742592e8b960a62", "f1351030eedda16"] for group_id in group_ids): # ID ГРУПП из GOOGLE CONTACT
                other_contacts.append(contact)
        
        return xml_book_contacts, https_book_contacts, other_contacts
    
    except HttpError as err:
        print(f"An error occurred: {err}")

if __name__ == "__main__":
    xml_contacts, https_contacts, other_contacts = fetch_contacts(SCOPES)
    print("XML Book Contacts:", xml_contacts)
    print("HTTPS Book Contacts:", https_contacts)
    print("Other Contacts:", other_contacts)
