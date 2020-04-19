import peewee #20200418

db = peewee.PostgresqlDatabase('daqfqhdshludoq',
                          user='tlnlkxrtnbepdl',
                          password='2a372ee7bedb7e93309cb56336a42fe8824885adb6a6509d27d86cdba914c5d3',
                          host='ec2-52-86-73-86.compute-1.amazonaws.com',
                          port=5432)

db.connect()

print("VO------------------------------------------")
#table
class Person(peewee.Model):
    #col
    name = peewee.CharField(null=True)
    birthday = peewee.DateField(null=True)
    
    #db
    class Meta:
        database = db

#table
class Pet(peewee.Model):
    #col
    owner = peewee.ForeignKeyField(Person, backref='pets')
    name = peewee.CharField(null=True)
    animal_type = peewee.CharField(null=True)
    
    #db
    class Meta:
        database = db

#creat_table()
#db.create_tables([GROUPER, GRP_DETAIL])
#db.drop_tables([GROUPER, GRP_DETAIL])
print("DAO-----------------------------------------")
print("insert-1------------------------------------")
from datetime import date
import datetime
#
#uncle_bob = Person(name='Bob', birthday=date(1960, 1, 15))
#uncle_bob.save() #return:1
#
print()
print("insert-2------------------------------------")
grandma = Person.create(name='Grandma', birthday=date(1935, 3, 1))
#herb = Person.create(name='Herb', birthday=date(1950, 5, 5))
peopleDel = Person.create(name='PeopleDel', birthday=date(1950, 5, 5))
peopleDel2 = Person.create(name='PeopleDel', birthday=date(1957, 7, 7))
##insert-pet
#bob_kitty = Pet.create(owner=uncle_bob, name='Kitty', animal_type='cat')
#herb_fido = Pet.create(owner=herb, name='Fido', animal_type='dog')
#herb_mittens = Pet.create(owner=herb, name='Mittens', animal_type='cat')
#herb_mittens_jr = Pet.create(owner=herb, name='Mittens Jr', animal_type='cat')

print()
print("#update-------------------------------------")
grandmaUpdate = Person.select().where(Person.name == 'Grandma').get()
print(type(grandmaUpdate))
grandmaUpdate.name = 'Grandma L.'
print(grandmaUpdate.save(),'#returns:1')

print()
print("#get one by key-----------------------------")
herb = Person.select().where(Person.name == 'Herb').get()
print(herb.name, herb.birthday)

print()
print("#get one by value---------------------------")
grandma = Person.get(Person.name == 'Grandma L.')
print(grandma.name, grandma.birthday)
aDateString='2020-04-18T12:49'
print(aDateString[0:4],aDateString[5:7],aDateString[8:10])
print(datetime.datetime.strptime(aDateString, '%Y-%m-%dT%H:%M'))
print(datetime.datetime(1957, int('7'), 7, 14, 25))

print()
print("#get all------------------------------------")
print(type(Person.select()),'#不是真的python的list') 
print(type(GROUPER.select()),'#不是真的python的list')      

print()
print("#delete-------------------------------------")
person = Person.get(Person.name=='Grandma L.')
print(person.delete_instance(),'#return number of rows deleted')

print()
print("#delete all---------------------------------")
query = Person.delete().where(Person.name=='PeopleDel')
print(query.execute(),'#return number of rows deleted')

print()
print("#使用select()，選取全部資料，再用迴圈列出------")
for person in Person.select():
    print(person.id, person.name, person.birthday)
for GROUPER in GROUPER.select():
    print(GROUPER.LOC_NO)

print()
print("#使用更多SQL語句 ----------------------------")
query = Pet.select().where(Pet.animal_type == 'cat')
for pet in query:
    print("Pet's name: ", pet.name, ": ", "Owner's name: ", pet.owner.name)

print()
print("#關閉連線------------------------------------")
#if db:
#    db.close()