from django.contrib import admin
from faqs.models import Faqs


@admin.register(Faqs)
class FaqAdminModel(admin.ModelAdmin):
    list_filter = ('is_deleted',)
    search_fields = ('question_body', 'answer')
    list_display = ('question', 'answer')

    def question(self, obj):
        if len(obj.question_body) > 50:
            return f"{obj.question_body[:50]}{'.' * 10}"

        return obj.__str__()

    def answer(self, obj):
        if len(obj.answer) > 50:
            return f"{obj.answer[:50]}{'.' * 10}"

        return obj.answer
