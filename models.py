from django.db import models

class Item(models.Model):
    item_name = models.CharField(max_length=200)
    item_desc = models.CharField(max_length=200)
    item_price = models.IntegerField()
    item_image = models.CharField(max_length=500,default='https://scontent.fktm6-1.fna.fbcdn.net/v/t1.6435-9/s526x395/241275850_107856911640929_5513469853399652353_n.jpg?_nc_cat=107&ccb=1-5&_nc_sid=09cbfe&_nc_ohc=z153lq4uI9EAX-y-0uP&_nc_ht=scontent.fktm6-1.fna&oh=42a1e3948a07df0d42e981bbaf656953&oe=61838A3A')
    

    def __str__(self) -> str:
        return self.item_name