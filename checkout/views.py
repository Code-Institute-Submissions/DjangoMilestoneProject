from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MakePaymentForm, BillingForm, ShippingForm
from .models import OrderLineItem
from django.conf import settings
from django.utils import timezone
from products.models import Product
from accounts.forms import UserProfileForm, UserPaymentForm
from accounts.models import UserProfile, UserPayment
import stripe

# Create your views here.
stripe.api_key = settings.STRIPE_SECRET


@login_required()
def checkout(request):
    if request.method == "POST":
        billing_form = BillingForm(request.POST)
        shipping_form = ShippingForm(request.POST)
        payment_form = MakePaymentForm(request.POST)

        if billing_form.is_valid() and shipping_form.is_valid() and payment_form.is_valid():
            order = billing_form.save(commit=False)
            order.user = request.user
            order.date = timezone.now()
            order.save()

            cart = request.session.get('cart', {})
            total = 0
            for id, quantity in cart.items():
                product = get_object_or_404(Product, pk=id)
                total += quantity * product.price
                order_line_item = OrderLineItem(
                    order=order,
                    product=product,
                    quantity=quantity
                )
                order_line_item.save()
            
            try:
                customer = stripe.Charge.create(
                    amount=int(total * 100),
                    currency="EUR",
                    description=request.user.email,
                    card=payment_form.cleaned_data['stripe_id']
                )
            except stripe.error.CardError:
                messages.error(request, "Your card was declined!")
            
            if customer.paid:
                messages.error(request, "You have successfully paid")
                request.session['cart'] = {}
                return redirect(reverse('products'))
            else:
                messages.error(request, "Unable to take payment")
        else:
            print(payment_form.errors)
            messages.error(request, "We were unable to take a payment with that card!")
    else:
        profile = get_object_or_404(UserProfile, user=request.user)
        payment = get_object_or_404(UserPayment, user=request.user)

        payment_form = MakePaymentForm()
        # payment_form = UserPaymentForm(instance=payment)
        # billing_form = BillingForm()
        billing_form = UserProfileForm(instance=profile)
        # shipping_form = ShippingForm()
        shipping_form = UserProfileForm(instance=profile)
    
    return render(request, "checkout.html", {"billing_form": billing_form, "shipping_form": shipping_form, "payment_form": payment_form, "publishable": settings.STRIPE_PUBLISHABLE})