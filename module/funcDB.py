import peewee #20200418

db = peewee.PostgresqlDatabase('daqfqhdshludoq',
                          user='tlnlkxrtnbepdl',
                          password='2a372ee7bedb7e93309cb56336a42fe8824885adb6a6509d27d86cdba914c5d3',
                          host='ec2-52-86-73-86.compute-1.amazonaws.com',
                          port=5432)

db.connect()

##table
#class Person(peewee.Model):
#    #col
#    name = peewee.CharField()
#    birthday = peewee.DateField()
#    
#    #db
#    class Meta:
#        database = db
#
##table
#class Pet(peewee.Model):
#    #col
#    owner = peewee.ForeignKeyField(Person, backref='pets')
#    name = peewee.CharField()
#    animal_type = peewee.CharField()
#    
#    #db
#    class Meta:
#        database = db

##creat_table()
#db.create_tables([Person, Pet])
#
##insert-1
from datetime import date
#
#uncle_bob = Person(name='Bob', birthday=date(1960, 1, 15))
#uncle_bob.save() #return:1
#
##insert-2
grandma = Person.create(name='Grandma', birthday=date(1935, 3, 1))
#herb = Person.create(name='Herb', birthday=date(1950, 5, 5))
personDel = Person.create(name='personDel', birthday=date(1950, 5, 5))
##insert-pet
#bob_kitty = Pet.create(owner=uncle_bob, name='Kitty', animal_type='cat')
#herb_fido = Pet.create(owner=herb, name='Fido', animal_type='dog')
#herb_mittens = Pet.create(owner=herb, name='Mittens', animal_type='cat')
#herb_mittens_jr = Pet.create(owner=herb, name='Mittens Jr', animal_type='cat')

#update
print()
print("update--------------------------------------")
grandmaUpdate = Person.select().where(Person.name == 'Grandma').get()
print(type(grandmaUpdate))
grandmaUpdate.name = 'Grandma L.'
grandmaUpdate.save() #returns:1

#get one by key
print()
print("get one by key------------------------------")
herb = Person.select().where(Person.name == 'Herb').get()
print(herb.name, herb.birthday)
#get one by value
print()
print("--------------------------------------------")
grandma = Person.get(Person.name == 'Grandma L.')
print(grandma.name, grandma.birthday)

#get all
print()
print("--------------------------------------------")
print(type(Person.select())) #不是真的python的list

#delete
print()
print("delete--------------------------------------")
person = Person.get(Person.name=='personDel')
print(person.delete_instance()) #return number of rows deleted

#delete all
print()
query = Person.delete().where(Person.name=='Grandma L.')
query.execute() #return number of rows deleted

#使用select()，選取全部資料，再用迴圈一一列出
print()
print("--------------------------------------------")
for person in Person.select():
    print(person.id, person.name, person.birthday)

#使用更多SQL語句    
print()
print("--------------------------------------------")
query = Pet.select().where(Pet.animal_type == 'cat')

for pet in query:
    print("Pet's name: ", pet.name, ": ", "Owner's name: ", pet.owner.name)
    
#關閉連線
if db:
    db.close()