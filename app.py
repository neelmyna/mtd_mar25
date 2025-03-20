from mongoengine import connect, Document, StringField
import mongoengine as me

# Define the Person document (collection)
class Person(me.Document):
   
    name = me.StringField(required=True, max_length=100)
    gender = me.StringField(required=True, choices=['Male', 'Female', 'Other'])
    location = me.StringField(required=True, max_length=200)   
   
    # Connect to MongoDB using the 'person_db' database
    Dbname = input("Enter Database name: ")
    me.connect( Dbname, host='localhost', port=27017)
    print(f"\nConnected to MongoDB using {Dbname} !!!")

def add_person():
    name = input("Enter Name: ")
    gender = input("Enter Gender (Male/Female/Other): ")
    location = input("Enter Location: ")
    person = Person(name=name, gender=gender, location=location)
    person.save()
    print("Person added successfully!\n")

def get_all_persons():
    persons = Person.objects()
    if not persons:
        print("No records found.\n")
    for person in persons:
        print(f"ID: {str(person.id):<20} Name: {str(person.name):<18} Gender: {str(person.gender):<6} Location: {str(person.location):<20}")
    print()

def get_person():
    person_id = input("Enter Person ID: ")
    person = Person.objects(id=person_id).first()
    if person:
        print(f"ID: {str(person.id):<20} Name: {str(person.name):<18} Gender: {str(person.gender):<6} Location: {str(person.location):<20}\n")
    else:
        print("Person not found.\n")

def update_person():
    person_id = input("Enter Person ID to update: ")
    person = Person.objects(id=person_id).first()
    if not person:
        print("Person not found.\n")
        return

    name = input("Enter New Name (leave blank to keep unchanged): ") or person.name
    gender = input("Enter New Gender (leave blank to keep unchanged): ") or person.gender
    location = input("Enter New Location (leave blank to keep unchanged): ") or person.location

    person.update(name=name, gender=gender, location=location)
    print("Person updated successfully!\n")

def delete_person():
    person_id = input("Enter Person ID to delete: ")
    person = Person.objects(id=person_id).first()
    if person:
        person.delete()
        print("Person deleted successfully!\n")
    else:
        print("Person not found.\n")

def menu():
    while True:
        print("\nMENU")
        print("1. Add Person")
        print("2. View All Persons")
        print("3. View Person by ID")
        print("4. Update Person")
        print("5. Delete Person")
        print("6. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            add_person()
        elif choice == '2':
            get_all_persons()
        elif choice == '3':
            get_person()
        elif choice == '4':
            update_person()
        elif choice == '5':
            delete_person()
        elif choice == '6':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice! Please enter a number between 1 and 6.\n")

if __name__ == "__main__":
    menu()
