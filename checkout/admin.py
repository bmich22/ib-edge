from django.contrib import admin
from .models import Purchase


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'package',
        'subject_choice',
        'customer_email',
        'purchased_on',
        'expires_on',
        'payment_status',
    )
    list_filter = (
        'payment_status',
        'package',
        'subject_choice',
        'purchased_on',
    )
    search_fields = (
        'user__username',
        'user__email',
        'customer_email',
        'stripe_payment_intent',
        'stripe_checkout_id',
    )
    ordering = ('-purchased_on',)