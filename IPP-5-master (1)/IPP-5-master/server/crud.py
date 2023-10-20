import json
from typing import List, Optional

from mongoengine import connect
from pymongo import MongoClient

from models import Contact


class ContactsCRUD:

    def __init__(self):
        self.client: MongoClient = connect(db="contacts", host="mongo", port=27017, username="root", password="example")
        self.db = self.client["contacts"]

    def create(self, contact: Contact) -> dict:
        contact = contact.save()
        return self.__required_format(contact)

    def read(self, uid) -> Optional[dict]:
        try:
            contact = Contact.objects.get(id=uid)
            contact = self.__required_format(contact)
        except Contact.DoesNotExist:
            contact = None
        return contact

    def read_all(self) -> List[dict]:
        return [self.__required_format(c) for c in Contact.objects]

    def update(self, contact: Contact) -> Optional[dict]:
        try:
            old_contact = Contact.objects.get(id=contact.id)
        except Contact.DoesNotExist:
            old_contact = None
        if old_contact is not None:
            contact = contact.save()
            return self.__required_format(contact)
        else:
            return None

    def delete(self, uid) -> Optional[dict]:
        try:
            contact = Contact.objects.get(id=uid)
        except Contact.DoesNotExist:
            contact = None
        if contact is not None:
            contact.delete()
            return self.__required_format(contact)
        else:
            return None

    def delete_all(self) -> List[dict]:
        contacts = self.read_all()
        Contact.drop_collection()
        return contacts

    def __required_format(self, c):
        contact = json.loads(c.to_json())
        if contact.get("_id"):
            contact["id"] = contact["_id"]["$oid"]
            contact.pop("_id")
        return contact
