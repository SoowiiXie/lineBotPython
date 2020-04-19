import peewee #20200419

db = peewee.PostgresqlDatabase('daqfqhdshludoq',
                          user='tlnlkxrtnbepdl',
                          password='2a372ee7bedb7e93309cb56336a42fe8824885adb6a6509d27d86cdba914c5d3',
                          host='ec2-52-86-73-86.compute-1.amazonaws.com',
                          port=5432)

#db.connect()

#table
class GROUPER(peewee.Model):
    #col
    GRP_NO = peewee.CharField(null=True)
    MB_ID = peewee.CharField(null=True)
    LOC_NO = peewee.CharField(null=True)
    GRP_APPLYSTART = peewee.DateTimeField(null=True)
    GRP_APPLYEND = peewee.DateTimeField(null=True)
    GRP_START = peewee.DateTimeField(null=True)
    GRP_END = peewee.DateTimeField(null=True)
    GRP_NAME = peewee.CharField(null=True)
    GRP_CONTENT = peewee.CharField(null=True)
    GRP_PERSONMAX = peewee.IntegerField(null=True)
    GRP_PERSONMIN = peewee.IntegerField(null=True)
    GRP_PERSONCOUNT = peewee.IntegerField(null=True)
    GRP_STATUS = peewee.IntegerField(null=True)
    GRP_FOLLOW = peewee.IntegerField(null=True)
    
    #db
    class Meta:
        database = db

#table
class GRP_DETAIL(peewee.Model):
    #col
    participants = peewee.ForeignKeyField(GROUPER, backref='participatingGroups')
    GRP_NO = peewee.CharField(null=True)
    MB_ID = peewee.CharField(null=True)
    GRP_REGISTER = peewee.IntegerField(null=True)

    #db
    class Meta:
        database = db

#table
class ORDERS(peewee.Model):
    #col
    OD_NO = peewee.CharField(null=True)
    MB_ID = peewee.CharField(null=True)
    OD_STATUS = peewee.IntegerField(null=True)
    MB_LINE_ID = peewee.CharField(null=True)
    MB_LINE_PIC = peewee.CharField(null=True)
    MB_LINE_DISPLAY = peewee.CharField(null=True)
    MB_LINE_STATUS = peewee.CharField(null=True)

    #db
    class Meta:
        database = db
        
##creat_table()
#db.create_tables([ORDERS, GRP_DETAIL])
#db.close()

##drop_table()
#db.drop_tables([ORDERS, GRP_DETAIL])
#db.close()