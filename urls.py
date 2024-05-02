from django.contrib import admin
from django.urls import path
from app1 import views

urlpatterns = [
   path('admin/', admin.site.urls),
   path('', views.welcome, name='welcome'),
   
   path('home',views.home,name="home"),
   path('favorites/', views.favorite_products, name='favorite_products'),
   path('customreg', views.customreg, name='customreg'),
   path('log', views.login1, name='login1'),
   path('profile.html', views.profile, name='profile'),
   path('about.html', views.about, name='about'),
   path('contact.html', views.contact,name='contact'),

   
   
   path('cart.html', views.cart, name='cart'),
   path('viewcart',views.view_cart,name='viewcart'),
   path('add_cart/<int:product_id>',views.add_to_cart,name='add_to_cart'),
   path('remove_from_cart/<int:cart_item_id>/',views.remove_from_cart, name='remove_from_cart'),

   # path('changepassword', views.password_reset, name='password_reset'),
   path('add_to_favorites/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
   path('remove_from_favorites/<int:product_id>/', views.remove_from_favorites, name='remove_from_favorites'),
   path('category/<int:category_id>/', views.category, name='category'),
   path('product/<int:product_id>/', views.product, name='product'),
   # path('products', views.product_detail, name='product_detail'),
   path('logout/',views.logout,name="logout"),
   path('search/', views.search_view, name='search'),
   # path('product/<int:product_id>/', views.product, name='product'),
   path('checkout/', views.checkout, name='checkout'), 
   # path('checkout/', views.checkout, name='checkout'),
   path('view_orders/', views.view_orders, name='view_orders'),
   path('edit_profile/', views.edit_profile, name='edit_profile'),
   path('orders/', views.orders, name='orders'),
   path('changepassword.html',views.password_reset,name="password_reset"),
   path('checkout_success/', views.checkout_success, name='checkout_success'),

   path('alert_view',views.alert_view,name="alert_view"),
   path('alert_success',views.alert_success,name="alert_success")





]