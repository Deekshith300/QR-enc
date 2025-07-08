from cryptography.fernet import Fernet
from datetime import datetime
import os

KEY_FILE = "secret.key"
NOTES_FILE = "notes.enc"

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)

def load_key():
    if not os.path.exists(KEY_FILE):
        generate_key()
    with open(KEY_FILE, "rb") as f:
        return f.read()

def encrypt_note(note, key):
    f = Fernet(key)
    return f.encrypt(note.encode())

def decrypt_note(token, key):
    f = Fernet(key)
    return f.decrypt(token).decode()

def add_note():
    key = load_key()
    note = input("Enter your note: ")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_note = f"[{timestamp}] {note}"
    encrypted = encrypt_note(full_note, key)
    with open(NOTES_FILE, "ab") as f:
        f.write(encrypted + b'\n')
    print("Note saved and encrypted.")

def list_notes():
    key = load_key()
    if not os.path.exists(NOTES_FILE):
        print("No notes found.")
        return
    with open(NOTES_FILE, "rb") as f:
        notes = [line.strip() for line in f if line.strip()]
    if not notes:
        print("No notes found.")
        return
    print("\nList of notes:")
    for idx, note in enumerate(notes, 1):
        try:
            preview = decrypt_note(note, key)[:30].replace('\n', ' ')
            print(f"{idx}. {preview}...")
        except Exception:
            print(f"{idx}. [Could not decrypt note]")

def view_note():
    key = load_key()
    if not os.path.exists(NOTES_FILE):
        print("No notes found.")
        return
    with open(NOTES_FILE, "rb") as f:
        notes = [line.strip() for line in f if line.strip()]
    if not notes:
        print("No notes found.")
        return
    try:
        idx = int(input(f"Enter note number (1-{len(notes)}): "))
        if 1 <= idx <= len(notes):
            print("\nNote content:")
            print(decrypt_note(notes[idx-1], key))
        else:
            print("Invalid note number.")
    except Exception:
        print("Invalid input or could not decrypt note.")

def delete_note():
    key = load_key()
    if not os.path.exists(NOTES_FILE):
        print("No notes found.")
        return
    with open(NOTES_FILE, "rb") as f:
        notes = [line.strip() for line in f if line.strip()]
    if not notes:
        print("No notes found.")
        return
    try:
        idx = int(input(f"Enter note number to delete (1-{len(notes)}): "))
        if 1 <= idx <= len(notes):
            del notes[idx-1]
            with open(NOTES_FILE, "wb") as f:
                for note in notes:
                    f.write(note + b'\n')
            print("Note deleted.")
        else:
            print("Invalid note number.")
    except Exception:
        print("Invalid input.")

def main():
    while True:
        print("\nEncrypted Notes CLI App")
        print("1. Add a note")
        print("2. List notes")
        print("3. View note")
        print("4. Delete note")
        print("5. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            add_note()
        elif choice == "2":
            list_notes()
        elif choice == "3":
            view_note()
        elif choice == "4":
            delete_note()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()