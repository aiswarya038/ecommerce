from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.contrib.auth import authenticate, login
from .models import Customer,Category,Product,Orders,CartItem,wishlist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Sum
from django.http import JsonResponse




def welcome(request):
    return render(request, 'welcome.html')


# Create your views here.
def login1(request):
    if request.method=='POST':
        username=request.POST['uname']
        password=request.POST['psw']
        user=authenticate(request,username=username,password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return HttpResponseRedirect('/admin/')  

        elif Customer.objects.filter(username=username,password=password).exists():
            customer=Customer.objects.filter(username=username,password=password)
            for i in customer:
                request.session['customer_id']=i.id
                a=Category.objects.all()
                user=request.session['customer_id']
              
                customer=Customer.objects.get(id=user)
                items=Orders.objects.filter(customer=user)
                wishlist_items=wishlist.objects.filter(customer=user)
                wishlist_count=wishlist_items.count()
                user_cart_items=CartItem.objects.filter(customer=user)
                count=user_cart_items.count()
                return render(request,'home.html',{'categorys':a,'count':count,'customer':customer,'wishlist_count':wishlist_count,'check_items':items})
        # return redirect(alert_success)
    else:
         return render(request,'login.html')
    
def customreg(request):
    user_id = request.session.get('Customer_id', None)
    if request.method == 'POST':
        firstname = request.POST['fn']
        lastname = request.POST['ln']
        username = request.POST['un']
        phone = request.POST['ph']
        password = request.POST['psw']
        email = request.POST['em']
        customer = Customer.objects.create(Firstname=firstname, Lastname=lastname, username=username,
                                           phone=phone, email=email, password=password)
        return redirect(login1)
    category = Category.objects.all()
    if user_id:
        user = get_object_or_404(Customer, id=user_id)
        user_cart_items = CartItem.objects.filter(customer=user)
        count = user_cart_items.count()
        wishlist_items = wishlist.objects.filter(customer=user)
        wishlist_count = wishlist_items.count()
        customer = Customer.objects.get(id=user_id)
    else:
        count = 0
        wishlist_count = 0
        customer = None
    return render(request, 'customreg.html',
                  {'categorys': category, 'count': count, 'wishlist_count': wishlist_count, 'customer': customer})



def home(request):
    a=Category.objects.all()
    user=request.session['customer_id']
    customer=Customer.objects.get(id=user)
    cart_items=CartItem.objects.filter(customer=user)
    cart_count=cart_items.count()

    return render(request,'home.html',{'categories':a,'customer':customer ,'count':cart_count})



def add_products(request):
    return render(request,'add_products.html')

def search_view(request,category_id):
    category=Category.objects.get(pk=category_id)
    products=Product.objects.filter(category=category)
    return render(request,'search_result.html',{'products':products})

def shop(request):
    return render(request,'shop.html')

def detail(request):
    return render(request,'detail.html')

def cart(request):
    category=Category.objects.all()
    a=request.session['customer_id']
    customer=Customer.objects.get(id=a)
    cart_items=CartItem.objects.filter(customer=a)
    wishlist_items=wishlist.objects.filter(customer=a)
    count=cart_items.count()
    wishlist_count=wishlist_items.count()
    # user=request.session['customer_id']
    total_price = sum(item.product.Price * item.quantity for item in cart_items)
    product=Product.objects.all()
    if cart_items:
         return render(request,'cart1.html',{'cart_items':cart_items,'categorys':category,'count':count,'total':total_price,'wish_count':wishlist_count,'customer':customer})
    else:
        return render(request,'cart_empty.html',{'categorys':category,'customer':customer,'count':count,'wish_count':wishlist_count})

def view_cart(request):
    customer=Customer.objects.get(id=request.session.get('customer_id'))
    cart_items=CartItem.objects.filter(customer=customer)
    all_total_price=sum(item.product.Price*item.quantity for item in cart_items)

def checkout(request):
    if request.method=='POST':
        a=request.session['customer_id']
        customer=Customer.objects.get(id=a)
        cart_items=CartItem.objects.filter(customer=customer)
        addres=request.POST['address']
        phone=request.POST['Phone']
        for items in cart_items:

            quantity=items.quantity
            price=items.product.Price
    
            Orders.objects.create(
                customer=customer,
                product=items.product,
                Quantity=quantity,
                Price=price,
                Address=addres,
                Phone=phone
                )
        cart_items.delete()
        return render(request,'cart_empty.html')
    return render(request,'checkout.html')

def contact(request):
    return render(request,'contact.html')
def home1(request):
    categories = Category.objects.all()
    return render(request, 'home.html', {'categories': categories})

def product(request,product_id):
     p=Product.objects.get(id=product_id)
     a=Category.objects.all()
     user=request.session['customer_id']
     customer=Customer.objects.get(id=user)
     user_cart_items=CartItem.objects.filter(customer=user)
     count=user_cart_items.count()
     wish_items=wishlist.objects.filter(customer=user)
     wish_count=wish_items.count()

     return render(request,'product-detail.html',{'products':p,'categorys':a,'count':count,'cartitems':user_cart_items,'wish_count':wish_count,'customer':customer})



def cart(request):
    category=Category.objects.all()
    a=request.session['customer_id']
    cart_items=CartItem.objects.filter(customer=a)
    # user=request.session['customer_id']
    customer=Customer.objects.get(id=a)
  
    total_price = sum(item.product.Price * item.quantity for item in cart_items)

    count=cart_items.count()
    product=Product.objects.all()
    wishlist_items=wishlist.objects.filter(customer=a)
    wishlist_count=wishlist_items.count()
                     

    if cart_items:
         return render(request,'cart.html',{'cart_items':cart_items,'categorys':category,'count':count,'total':total_price,'wish_count':wishlist_count,'customer':customer})
    else:
        return render(request,'cart.html',{'categorys':category,'customer':customer,'count':count,'wish_count':wishlist_count})
    

def view_cart(request):
    customer=Customer.objects.get(id=request.session.get('customer_id'))
    cart_items=CartItem.objects.filter(customer=customer)
    all_total_price=sum(item.product.Price*item.quantity for item in cart_items)
    
    return render(request,'category.html',{'cart_items':cart_items,'total':all_total_price})



def about(request):
    return render(request,"about.html")

def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(id=product_id)
        customer_id = request.session.get('customer_id')
        if customer_id:
            customer = Customer.objects.get(id=customer_id)
            quantity = request.POST.get('qtn')

            if CartItem.objects.filter(customer=customer, product=product).exists():
                messages.info(request, "Item is already in the cart.")
            else:
                CartItem.objects.create(customer=customer, product=product, quantity=quantity)
                messages.success(request, "Item added to your cart.")

            return redirect('cart')
        else:
            messages.error(request, "You need to log in to add items to your cart.")
            return redirect('login')  # Redirect to the login page if the user is not logged in
    else:
        messages.error(request, "Invalid request method.")
        return redirect('cart') 
    


def remove_from_cart(request, cart_item_id):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id)
        cart_item.delete()
        messages.success(request, "Item removed from your cart.")
        return redirect('cart')
    except CartItem.DoesNotExist:
        messages.error(request, "The item you're trying to remove does not exist in your cart.")
        return redirect('cart')
    


def favorite_products(request):

    user=request.session['customer_id']
    customer=Customer.objects.get(id=user)
    category=Category.objects.all()
    wishlist_items=wishlist.objects.filter(customer=user)
    wishlist_count=wishlist_items.count()
    cart_items=CartItem.objects.filter(customer=user)
    cart_count=cart_items.count()
    if wishlist_items:
            return render(request,
                          'whishlist.html',
                          {'wishlist_items':wishlist_items,
                           'categorys':category,
                           'wishlist_count':wishlist_count,
                           'cart_count':cart_count,
                           'customer':customer}
                           )
    else:
        return render(request,'whishlist.html')
    

def profile(request):
    user=request.session['customer_id']
    customer=Customer.objects.get(id=user)
    category=Category.objects.all()
    wishlist_items=wishlist.objects.filter(customer=user)
    wishlist_count=wishlist_items.count()
    cart_items=CartItem.objects.filter(customer=user)
    cart_count=cart_items.count()

    # items=Orders.objects.filter(customer=user)
    return render(request,'profile.html',{'customer':customer,'categorys':category,'wish_count':wishlist_count,'count':cart_count})



def edit_profile(request):
    if request.method == 'POST':
        firstname = request.POST['fname']
        lastname = request.POST['lname']
        username = request.POST['uname']
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['psw']
        customer_id = request.session.get('customer_id')
        if customer_id:
            customer = Customer.objects.get(id=customer_id)
            customer.Firstname = firstname
            customer.Lastname = lastname
            customer.username = username
            customer.phone = phone
            customer.email = email
            customer.password = password
            customer.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
        else:
            messages.error(request, "User not logged in.")
            return redirect('login')  
    else:
        customer_id = request.session.get('customer_id')
        if customer_id:
            customer = Customer.objects.get(id=customer_id)
            return render(request, 'edit_profile.html', {'customer': customer})
        else:
            messages.error(request, "User not logged in.")
            return redirect('login')
        

def search_view(request):
    query = request.GET.get('q')
    products = None
    
    if query:
        products = Product.objects.filter(Name__icontains=query) | Product.objects.filter(Description__icontains=query)
        
    return render(request, 'product.html', {'query': query, 'products': products})
        


def add_to_favorites(request,product_id):
        product=Product.objects.get(id=product_id)
        a=request.session['customer_id']
        customer=Customer.objects.get(id=a)
        if wishlist.objects.filter(customer=customer,product=product).exists():
            messages.success(request,"item is alredy in your wishlist")
            return redirect(favorite_products)

            
            # messages.error(request,"item is already in your wishlist")
        else:
            wishlist.objects.create(customer=customer,product=product,quantity=1)
            all_wishlist_items=wishlist.objects.all()
            count=all_wishlist_items.count()
            count=count+1
            
        return redirect(favorite_products)
       
def remove_from_favorites(request,product_id):
    wishlist.objects.get(id=product_id).delete()
    return redirect(favorite_products)
        
def checkout(request):
    if request.method == 'POST':
        if 'customer_id' not in request.session:
            messages.error(request, "You need to log in to proceed with the checkout.")
            return redirect('log')  
        
        user_id = request.session['customer_id']

        try:
            customer = Customer.objects.get(id=user_id)
        except Customer.DoesNotExist:
            messages.error(request, "User not found. Please log in again.")
            return redirect('log') 
        
        cart_items = CartItem.objects.filter(customer=customer)
        if not cart_items.exists():
            messages.error(request, "Your cart is empty. Add items to your cart before checking out.")
            return redirect('cart') 
        
        address = request.POST.get('address')
        phone = request.POST.get('Phone')

        for item in cart_items:
            Orders.objects.create(
                customer=customer,
                product=item.product,
                Quantity=item.quantity,
                Price=item.product.Price,
                Address=address,
                Phone=phone
            )

        cart_items.delete()
        return redirect('orders')  # Redirect to the orders page after successfully placing the order

    else:
        # Retrieve cart items, total quantity, and total amount
        user_id = request.session.get('customer_id')
        if not user_id:
            messages.error(request, "You need to log in to proceed with the checkout.")
            return redirect('log')  
        
        customer = Customer.objects.get(id=user_id)
        cart_items = CartItem.objects.filter(customer=customer)
        total_quantity = cart_items.aggregate(Sum('quantity'))['quantity__sum']
        total_amount = sum(item.product.Price * item.quantity for item in cart_items)
        
        # Pass the data to the template context
        context = {
            'cart_items': cart_items,
            'total_quantity': total_quantity,
            'total_amount': total_amount
        }
        return render(request, 'checkout.html', context)


def logout(request):
    return redirect(login1)

def password_reset(request):
    if request.method == 'POST':
        user_id = request.session.get('customer_id')
        if user_id:
            customer = Customer.objects.get(id=user_id)
            new_password = request.POST.get('newpass')
            customer.password = new_password
            customer.save()
            messages.success(request, 'Your password has been successfully updated!')
            return redirect('home')  # Redirect to the home page or any other desired page
        else:
            messages.error(request, 'User not logged in.')
            return redirect('login')  # Redirect to the login page if the user is not logged in
    else:
        return render(request, 'changepassword.html')


def view_orders(request):
    category=Category.objects.all()

    user=request.session['customer_id']

    customer=Customer.objects.get(id=user)
    cart_items=CartItem.objects.filter(customer=user)
    count=cart_items.count()
    wishlist_items=wishlist.objects.filter(customer=user)
    wishlist_count=wishlist_items.count()
    order_items=Orders.objects.filter(customer=user)
    return render(request,'orders.html',{'orders':order_items,'count':count,'wishlist_count':wishlist_count,'customer':customer,'categorys':category})



def orders(request):
   user_id = request.session.get('customer_id')
   customer = Customer.objects.get(id=user_id)
   orders = Orders.objects.filter(customer=customer)
   return render(request, 'orders.html', {'orders': orders, 'customer': customer})

def category(request, category_id):
    category = Category.objects.get(pk=category_id)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    user_id = request.session.get('customer_id', None)
    customer = Customer.objects.get(id=user_id) if user_id else None
    user_cart_items = CartItem.objects.filter(customer=user_id) if user_id else None
    count = user_cart_items.count() if user_cart_items else 0
    wishlist_items = wishlist.objects.filter(customer=user_id) if user_id else None
    wishlist_count = wishlist_items.count() if wishlist_items else 0
    product_count = products.count()
    
    return render(request, 'product.html', 
                  {'category': category, 
                   'products': products,
                   'categories': categories,
                   'count': count,
                   'wishlist_count': wishlist_count,
                   'wishlist': wishlist_items,
                   'customer': customer,
                   'product_count': product_count})


def checkout_success(request):
    return render(request, 'checkout_success.html')

def alert_view(request):
    response_content = """
        <script>
            alert("invalid username or password");
        </script>
    """
    return HttpResponse(response_content)

def alert_success(request):
    response_content = """
        <script>
            alert("successfully registerd");
        </script>
    """
    return HttpResponse(response_content)
