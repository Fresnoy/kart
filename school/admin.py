from django.contrib import admin
from .models import Student, Promotion


class StudentAdmin(admin.ModelAdmin):
    """ Admin model for Student.
    """
    list_display = ('stud_display',)
    search_fields = ['user__first_name', 'user__last_name']
    # filter_horizontal = ('websites',)

    def stud_display(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name} (Promo {obj.promotion.name})"

    stud_display.short_description = 'Student'

    def firstname(self, obj):
            return obj.user.first_name

    def lastname(self, obj):
        return obj.user.last_name


class PromoAdmin(admin.ModelAdmin):
    """ Admin model for Promotion.
    """

    list_display = ('promo_display', 'stud_counter')

    def promo_display(self, obj):
        '''Display the name of the promotion and its corresponding years.'''

        return f"Promotion {obj.name} ({obj.starting_year}-{obj.ending_year})"

    promo_display.short_description = 'Promotion'

    def stud_counter(self, obj):
        '''Display the number of students per promotion.'''

        students = Student.objects.all().filter(pk=obj.pk)
        return(len(students))

# Model registration
admin.site.register(Student, StudentAdmin)
admin.site.register(Promotion, PromoAdmin)
