# PRODIGY_03
# Contact Management System

A simple, menu-driven command-line application built in Python for storing and managing contacts. Every change is saved straight to a local JSON file, so your contacts are still there the next time you run the program.

> **Task-03** — ProDigy InfoTech Internship Program

## Features

- **Add Contact** — save a name, phone number, and email address, with input validation on every field
- **View Contacts** — see every saved contact in a clean, aligned table
- **Search Contact** — look up a contact by name, phone number, or email (partial matches work too)
- **Update Contact** — edit any field of an existing contact; leave a field blank to keep it unchanged
- **Delete Contact** — remove a contact, with a confirmation prompt so nothing is deleted by accident
- **Persistent Storage** — all data is automatically written to `contacts.json`; IDs are never reused, even after a deletion
- **Input Validation** — names, phone numbers, and email addresses are checked before being saved, with clear error messages

## Screenshots

**Main Menu**
![Main Menu](screenshots/01_main_menu.png)

**Adding a Contact** — with a validation error shown, then corrected
![Add Contact](screenshots/02_add_contact.png)

**Viewing All Contacts**
![View Contacts](screenshots/03_view_contacts.png)

**Searching for a Contact**
![Search Contact](screenshots/04_search_contact.png)

**Updating a Contact**
![Update Contact](screenshots/05_update_contact.png)

**Deleting a Contact**
![Delete Contact](screenshots/06_delete_contact.png)

**Contact List After the Changes Above**
![Final List](screenshots/07_final_list.png)

## Tech Stack

- Python 3 (standard library only — no external dependencies)
- JSON for persistent file storage

## Project Structure

```
Contact-Management-System/
│
├── contact_manager.py        # Main application
├── test_contact_manager.py   # Unit tests
├── contacts.json              # Sample data (auto-created if missing)
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
└── screenshots/
    ├── 01_main_menu.png
    ├── 02_add_contact.png
    ├── 03_view_contacts.png
    ├── 04_search_contact.png
    ├── 05_update_contact.png
    ├── 06_delete_contact.png
    └── 07_final_list.png
```

## Getting Started

### Prerequisites
- Python 3.7 or higher (no external packages required)

### Run it
```bash
git clone https://github.com/<your-username>/Contact-Management-System.git
cd Contact-Management-System
python3 contact_manager.py
```

The repo ships with three sample contacts in `contacts.json` so the menu isn't empty on first run — feel free to delete them from inside the app, or delete the file entirely and it will be recreated automatically.

### Run the tests
```bash
python3 -m unittest test_contact_manager.py -v
```

## How It Works

1. Run the program — a menu with six numbered options appears.
2. Enter a number to add, view, search, update, or delete a contact.
3. Every change is saved immediately to `contacts.json`, so nothing is lost if you close the terminal.
4. Choose option 6 at any time to exit.

## Possible Enhancements

- Contact groups / categories (family, work, etc.)
- Export contacts to CSV or vCard
- A graphical interface (Tkinter) or web interface (Flask)
- Duplicate-contact detection when adding

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

## Author

Submitted as part of the ProDigy InfoTech Internship Program.
