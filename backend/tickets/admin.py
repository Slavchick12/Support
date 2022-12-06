from django.contrib import admin

from .models import Ticket, TicketResponse


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('topic', 'descripion', 'file', 'status', 'user', 'date')
    search_fields = ('topic', 'date', 'user')
    list_filter = ('topic', 'date', 'user')
    empty_value_display = '-пусто-'


@admin.register(TicketResponse)
class TicketResponseAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'message', 'text', 'user')
    search_fields = ('ticket', 'message', 'user')
    list_filter = ('ticket', 'user')
    empty_value_display = '-пусто-'
