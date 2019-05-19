from django.contrib import admin

from .models import Thread, ChatMessage


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.TabularInline):
    pass


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessage]
