import telebot
from django.shortcuts import render, redirect
from django.http import HttpResponse

from . import models

# Create your views here.
bot = telebot.TeleBot('5459935331:AAGVWpnqIK_bYMatPGDtqTWS8iPiWZgTJBc')


def home_page(request):
    all_category = models.Category.objects.all()

    return render(request, 'index.html',
                  {'all_categories': all_category})


def get_all_products(request):
    all_products = models.Product.objects.all()

    return render(request, 'product_index.html', {'all_products': all_products})


def get_exact_product(request, pk):
    current_product = models.Product.objects.get(product_name=pk)

    return render(request, 'get_exact_product_index.html', {'current_product': current_product})


def get_exact_category(request, pk):
    current_category = models.Category.objects.get(id=pk)
    category_products = models.Product.objects.filter(product_category = current_category)
    return render(request, 'get_exact_category_index.html', {'category_products': category_products})


def get_search_product(request, pk):
    current_product = models.Product.objects.get(product_name=pk)

    return render(request, 'search.html', {'current_product': current_product})


def search_exact_product(request):
    if request.method == 'POST':
        get_product = request.POST.get('search_product')

        try:
            models.Product.objects.get(product_name=get_product)

            return redirect(f'/search/{get_product}')
        except:
            return redirect('/')


def add_product_to_user(request, pk):
    if request.method == 'POST':
        checker = models.Product.objects.get(id=pk)
        if checker.product_count >= int(request.POST.get('pr_count')):
            models.UserCart.objects.create(user_id=request.user.id,
                                           user_product = checker,
                                           user_product_quantity = request.POST.get('pr_count')).save()

            return redirect(f'/products/')

        else:
            return redirect(f'/product/{checker.product_name}')


def get_exact_card(request):
    id = request.user.id
    all_card = models.UserCart.objects.filter(user_id = id)

    return render(request, 'user_card.html', {'all_card': all_card})


def delete_exact_user_cart(request, pk):
    product_to_delete = models.Product.objects.get(id = pk)

    models.UserCart.objects.filter(user_id=request.user.id,
                                user_product = product_to_delete).delete()

    return redirect('/card')


def shopping_cart(request):
    return render(request, 'registratsiya.html')


def same_cart(request):
    if request.method == 'POST':
        user_id = 1006779184
        total = 0
        user = models.UserCart.objects.filter(user_id = request.user.id)

        text = ' --------- xaridor ----'

        text += f'firstname :{request.POST.get("firstname")} \nlastname:{request.POST.get("lastname")}\n' \
                       f'Email :{request.POST.get("email")}\nManzil :{request.POST.get("address")}\n' \
                       f'Tolov turi :{request.POST.get("address_oplata")}\n'

        text += '----- products-----'

        for users in user:
            text += f'Tovar :{users.user_product.product_name} \n' \
                       f'Narxi:{users.user_product.product_price}\n' \
                       f'Soni :{users.user_product_quantity}\nZakaz qilingan sanasi :{users.cart_date}\n' \
                       f'Xaridor :{users.user_id}\n'
            total = int(users.user_product_quantity) * float(users.user_product.product_price) + total

        text += f'summa = {total}\n'

        bot.send_message(user_id, text)
        models.UserCart.objects.filter(user_id=request.user.id).delete()

        return redirect('/card')


