from django.db import models
import datetime



#model for category
class Category(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name


#model for customer
class Customer(models.Model):
    Firstname=models.CharField(max_length=20)
    Lastname=models.CharField(max_length=20)
    username=models.CharField(max_length=20)
    phone=models.CharField(max_length=10)
    email=models.EmailField(max_length=20)
    password=models.CharField(max_length=20)
    new_password=models.CharField(max_length=20,default=12345)

    def __str__(self):
        return self.Firstname

#model for product
class Product(models.Model):
    Name=models.CharField(max_length=100)
    Price=models.IntegerField(default=0)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    Description=models.CharField(max_length=250, default='', blank=True, null= True)
    image=models.ImageField(upload_to='images/')

    def __str__(self):
        return self.Name



#model for orders
class Orders(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    Quantity=models.IntegerField(default=1)
    Price=models.IntegerField()
    Address=models.CharField(max_length=50)
    Phone=models.CharField(max_length=10)
    Date=models.DateField(default=datetime.datetime.today)
    Status=models.BooleanField(default=False)
    
class CartItem(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveBigIntegerField(default=1)
    # total=models.BigIntegerField(default=0)

    def total_amount(self):
         self.total = self.quantity * self.product.Price

    #    return self.quantity*self.product.Price
class wishlist(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
