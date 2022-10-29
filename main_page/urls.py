from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page),
    path('products/', views.get_all_products),
    path('product/<str:pk>', views.get_exact_product),
    path('category/<int:pk>', views.get_exact_category),
    path('search', views.search_exact_product),
    path('search/<str:pk>', views.get_search_product),
    path('add_to_cart/<int:pk>', views.add_product_to_user),
    path('card', views.get_exact_card),
    path('delete_product/<int:pk>', views.delete_exact_user_cart),
    path('shopping', views.shopping_cart),
    path('follow', views.same_cart),
]
