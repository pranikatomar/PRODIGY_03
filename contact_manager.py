#!/usr/bin/env python3
"""
Contact Management System
==========================
A simple command-line application for storing and managing contacts.

Features:
    - Add a new contact (name, phone, email) with input validation
    - View all saved contacts in a formatted table
    - Search for a contact by name, phone, or email
    - Update an existing contact's details
    - Delete a contact (with confirmation)
    - Persistent storage using a local JSON file

Task-03 | ProDigy InfoTech Internship Program
"""

import json
import os
import re
import sys

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "contacts.json")


class Contact:
    """Represents a single contact record."""

    def __init__(self, contact_id, name, phone, email):
        self.id = contact_id
        self.name = name
        self.phone = phone
        self.email = email

    def to_dict(self):
        return {"id": self.id, "name": self.name, "phone": self.phone, "email": self.email}

    @staticmethod
    def from_dict(data):
        return Contact(data["id"], data["name"], data["phone"], data["email"])


class ContactManager:
    """Handles all contact operations and reads/writes the JSON data file."""

    def __init__(self, filepath=DATA_FILE):
        self.filepath = filepath
        self.contacts = []
        self._next_id_value = 1
        self.load_contacts()

    # ---------------------------------------------------------- persistence
    def load_contacts(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.contacts = [Contact.from_dict(c) for c in data.get("contacts", [])]
                self._next_id_value = data.get("next_id", self._compute_next_id())
            except (json.JSONDecodeError, KeyError, ValueError, AttributeError):
                print("Warning: contacts.json was unreadable. Starting with an empty list.")
                self.contacts = []
                self._next_id_value = 1
        else:
            self.contacts = []
            self._next_id_value = 1

    def save_contacts(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "next_id": self._next_id_value,
                    "contacts": [c.to_dict() for c in self.contacts],
                },
                f,
                indent=4,
            )

    # ------------------------------------------------------------- helpers
    def _compute_next_id(self):
        return max((c.id for c in self.contacts), default=0) + 1

    def _next_id(self):
        # IDs are never reused, even after a contact is deleted - the
        # counter is persisted to contacts.json alongside the data.
        value = self._next_id_value
        self._next_id_value += 1
        return value

    def get_contact(self, contact_id):
        for c in self.contacts:
            if c.id == contact_id:
                return c
        return None

    def all_contacts(self):
        return sorted(self.contacts, key=lambda c: c.id)

    # ------------------------------------------------------------- actions
    def add_contact(self, name, phone, email):
        contact = Contact(self._next_id(), name.strip(), phone.strip(), email.strip())
        self.contacts.append(contact)
        self.save_contacts()
        return contact

    def update_contact(self, contact_id, name=None, phone=None, email=None):
        contact = self.get_contact(contact_id)
        if not contact:
            return None
        if name:
            contact.name = name.strip()
        if phone:
            contact.phone = phone.strip()
        if email:
            contact.email = email.strip()
        self.save_contacts()
        return contact

    def delete_contact(self, contact_id):
        contact = self.get_contact(contact_id)
        if not contact:
            return False
        self.contacts.remove(contact)
        self.save_contacts()
        return True

    def search_contacts(self, keyword):
        keyword = keyword.strip().lower()
        return [
            c for c in self.contacts
            if keyword in c.name.lower()
            or keyword in c.phone.lower()
            or keyword in c.email.lower()
        ]


# --------------------------------------------------------------- validation
def is_valid_name(name):
    name = name.strip()
    return bool(name) and bool(re.match(r"^[A-Za-z\s.'-]+$", name))


def is_valid_phone(phone):
    return bool(re.match(r"^\+?[0-9\s-]{7,15}$", phone.strip()))


def is_valid_email(email):
    return bool(re.match(r"^[\w.+-]+@[\w-]+\.[\w.-]+$", email.strip()))


# ------------------------------------------------------------------ display
def truncate(text, width):
    text = str(text)
    return text if len(text) <= width else text[: width - 1] + "~"


def print_header(title):
    width = 70
    print("\n" + "=" * width)
    print(title.center(width))
    print("=" * width)


def print_menu():
    print_header("CONTACT MANAGEMENT SYSTEM")
    print(
        "\n"
        "  1. Add Contact\n"
        "  2. View All Contacts\n"
        "  3. Search Contact\n"
        "  4. Update Contact\n"
        "  5. Delete Contact\n"
        "  6. Exit\n"
    )


def print_contacts_table(contacts):
    if not contacts:
        print("\n  No contacts to display.\n")
        return
    print(f"\n  {'ID':<4}{'Name':<20}{'Phone':<16}{'Email':<28}")
    print("  " + "-" * 68)
    for c in contacts:
        print(
            f"  {c.id:<4}{truncate(c.name, 18):<20}"
            f"{truncate(c.phone, 14):<16}{truncate(c.email, 26):<28}"
        )
    print()


def prompt(text):
    return input(text).strip()


# ------------------------------------------------------------------ actions
def action_add(manager):
    print_header("ADD NEW CONTACT")

    name = prompt("  Name  : ")
    while not is_valid_name(name):
        print("  Error: Please enter a valid name (letters and spaces only).")
        name = prompt("  Name  : ")

    phone = prompt("  Phone : ")
    while not is_valid_phone(phone):
        print("  Error: Please enter a valid phone number (7-15 digits).")
        phone = prompt("  Phone : ")

    email = prompt("  Email : ")
    while not is_valid_email(email):
        print("  Error: Please enter a valid email address.")
        email = prompt("  Email : ")

    contact = manager.add_contact(name, phone, email)
    print(f"\n  Contact '{contact.name}' added successfully with ID {contact.id}.\n")


def action_view(manager):
    print_header("ALL CONTACTS")
    print_contacts_table(manager.all_contacts())


def action_search(manager):
    print_header("SEARCH CONTACT")
    keyword = prompt("  Enter name, phone or email to search: ")
    results = manager.search_contacts(keyword)
    if results:
        print(f"\n  Found {len(results)} matching contact(s):")
        print_contacts_table(results)
    else:
        print("\n  No matching contacts found.\n")


def action_update(manager):
    print_header("UPDATE CONTACT")
    print_contacts_table(manager.all_contacts())
    if not manager.contacts:
        return

    raw_id = prompt("  Enter contact ID to update: ")
    if not raw_id.isdigit():
        print("  Error: Please enter a valid numeric ID.\n")
        return

    contact = manager.get_contact(int(raw_id))
    if not contact:
        print("  Error: No contact found with that ID.\n")
        return

    print("\n  Leave a field blank to keep its current value.")

    print(f"  Current Name  : {contact.name}")
    name = prompt("  New Name      : ")
    if name and not is_valid_name(name):
        print("  Error: Invalid name entered. Keeping the current value.")
        name = None

    print(f"  Current Phone : {contact.phone}")
    phone = prompt("  New Phone     : ")
    if phone and not is_valid_phone(phone):
        print("  Error: Invalid phone entered. Keeping the current value.")
        phone = None

    print(f"  Current Email : {contact.email}")
    email = prompt("  New Email     : ")
    if email and not is_valid_email(email):
        print("  Error: Invalid email entered. Keeping the current value.")
        email = None

    manager.update_contact(contact.id, name or None, phone or None, email or None)
    print(f"\n  Contact ID {contact.id} updated successfully.\n")


def action_delete(manager):
    print_header("DELETE CONTACT")
    print_contacts_table(manager.all_contacts())
    if not manager.contacts:
        return

    raw_id = prompt("  Enter contact ID to delete: ")
    if not raw_id.isdigit():
        print("  Error: Please enter a valid numeric ID.\n")
        return

    contact = manager.get_contact(int(raw_id))
    if not contact:
        print("  Error: No contact found with that ID.\n")
        return

    confirm = prompt(f"  Delete '{contact.name}'? This cannot be undone. (y/n): ").lower()
    if confirm == "y":
        manager.delete_contact(contact.id)
        print(f"\n  Contact '{contact.name}' deleted successfully.\n")
    else:
        print("\n  Deletion cancelled.\n")


MENU_ACTIONS = {
    "1": action_add,
    "2": action_view,
    "3": action_search,
    "4": action_update,
    "5": action_delete,
}


def main():
    manager = ContactManager()
    while True:
        print_menu()
        choice = prompt("  Enter your choice (1-6): ")
        if choice == "6":
            print("\n  Thank you for using Contact Management System. Goodbye!\n")
            sys.exit(0)
        action = MENU_ACTIONS.get(choice)
        if action:
            action(manager)
        else:
            print("\n  Invalid choice. Please enter a number between 1 and 6.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Program interrupted. Goodbye!\n")
        sys.exit(0)
