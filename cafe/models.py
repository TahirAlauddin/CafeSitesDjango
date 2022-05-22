from django.db import models
import uuid

class Table(models.Model):
    id = models.IntegerField(primary_key=True)
    guid = models.CharField(max_length=50, unique=True)
    top = models.IntegerField(default=0)
    left = models.IntegerField(default=0)
    label = models.CharField(max_length=50)
    color = models.CharField(max_length=50,
                            default='unselected-color')
    cafe = models.ForeignKey("Cafe", on_delete=models.CASCADE,
                            related_name='tables')

    def __str__(self):
        return str(self.cafe) + " " + self.label 
    
    def delete(self, *args, **kwargs):
        for record in self.records.all():
            record.deleted_table = f"cafe={str(self.cafe)} label={self.label} id={self.id}"
            record.save()
        super().delete(*args, **kwargs)


class Cafe(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='cafe', default='default.jpg')

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=255)
    selected = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Record(models.Model):
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True,
                                related_name='records')
    date_time = models.DateTimeField()
    allocated = models.BooleanField(default=False)
    deleted_table = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        if self.table:
            return str(self.date_time.date()) + " " + str(self.table)

        return str(self.date_time.date()) + str(self.deleted_table)


    @classmethod
    def get_data_for_specific_date(cls, date):
        # date -> 2000-12-30
        queryset = cls.objects.filter(date_time__contains=date)
        return list(queryset)


# class Record(models.Model):
    # tables = models.ManyToManyField(Table)
    # date_time = models.DateTimeField()

    # def __str__(self):
    #     tables = list(self.tables.all())
    #     print(tables)
    #     return str(self.date_time.date()) + " ".join([str(table) for table in tables])
    

    # @classmethod
    # def get_data_for_specific_date(cls, date):
    #     # date -> 2000-12-30
    #     queryset = cls.objects.filter(date_time__contains=date)
    #     return list(queryset)
        