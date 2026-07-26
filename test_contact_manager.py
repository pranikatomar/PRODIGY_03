"""
Unit tests for the Contact Management System.
Run with:  python3 -m unittest test_contact_manager.py -v
"""

import os
import tempfile
import unittest

from contact_manager import (
    ContactManager,
    is_valid_email,
    is_valid_name,
    is_valid_phone,
)


class TestValidation(unittest.TestCase):
    def test_valid_name(self):
        self.assertTrue(is_valid_name("Aarav Sharma"))
        self.assertFalse(is_valid_name(""))
        self.assertFalse(is_valid_name("John123"))

    def test_valid_phone(self):
        self.assertTrue(is_valid_phone("9876543210"))
        self.assertTrue(is_valid_phone("+91 9876543210"))
        self.assertFalse(is_valid_phone("12345"))
        self.assertFalse(is_valid_phone("abcdefghij"))

    def test_valid_email(self):
        self.assertTrue(is_valid_email("user@example.com"))
        self.assertFalse(is_valid_email("user@example"))
        self.assertFalse(is_valid_email("userexample.com"))


class TestContactManager(unittest.TestCase):
    def setUp(self):
        fd, path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        with open(path, "w", encoding="utf-8") as f:
            f.write('{"next_id": 1, "contacts": []}')
        self.path = path
        self.manager = ContactManager(filepath=self.path)

    def tearDown(self):
        os.unlink(self.path)

    def test_add_contact(self):
        c = self.manager.add_contact("Test User", "1234567890", "test@example.com")
        self.assertEqual(c.id, 1)
        self.assertEqual(len(self.manager.contacts), 1)

    def test_ids_increment_even_after_deletion(self):
        self.manager.add_contact("A", "1111111111", "a@example.com")
        b = self.manager.add_contact("B", "2222222222", "b@example.com")
        self.manager.delete_contact(b.id)
        c = self.manager.add_contact("C", "3333333333", "c@example.com")
        self.assertEqual(c.id, 3)

    def test_update_contact(self):
        c = self.manager.add_contact("Test User", "1234567890", "test@example.com")
        self.manager.update_contact(c.id, phone="9999999999")
        updated = self.manager.get_contact(c.id)
        self.assertEqual(updated.phone, "9999999999")
        self.assertEqual(updated.name, "Test User")  # unchanged fields stay intact

    def test_delete_contact(self):
        c = self.manager.add_contact("Test User", "1234567890", "test@example.com")
        self.assertTrue(self.manager.delete_contact(c.id))
        self.assertIsNone(self.manager.get_contact(c.id))

    def test_delete_nonexistent_contact_returns_false(self):
        self.assertFalse(self.manager.delete_contact(999))

    def test_search_contact(self):
        self.manager.add_contact("Alice Smith", "1112223333", "alice@example.com")
        self.manager.add_contact("Bob Jones", "4445556666", "bob@example.com")
        results = self.manager.search_contacts("alice")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Alice Smith")

    def test_persistence_across_instances(self):
        self.manager.add_contact("Persisted User", "1231231234", "persist@example.com")
        reloaded = ContactManager(filepath=self.path)
        self.assertEqual(len(reloaded.contacts), 1)
        self.assertEqual(reloaded.contacts[0].name, "Persisted User")


if __name__ == "__main__":
    unittest.main()
