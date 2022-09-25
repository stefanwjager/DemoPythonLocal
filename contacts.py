from cgi import print_arguments
from unicodedata import name


contacts = {
    'number': 4,
    'students':
        [
            {'name': 'assepoester', 'email': 'assepoester@efteling.com'},
            {'name': 'roodkapje', 'email': 'roodkapje@efteling.com'},
            {'name': 'bozewolf', 'email': 'bozewolf@efteling.com'},
            {'name': 'sneeuwwitje', 'email': 'sneeuwwitje@efteling.com'}
        ]
    }

for student in contacts ['students']:
    print (student)

for student in contacts['students']:
    print(student.get('email'))
    
    
for student in contacts['students']:
    print(student.get('name'))
    
    # drill down in dictionary
    # which has: list of dictionaries
    # and: acces values inside
    
print([contacts.get('number')])  #dict // blokhaak
print(contacts.get('number'))    #value
