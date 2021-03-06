from django.contrib import admin

from .models import Catalog, Section, Subsection, QuestionEntity, Question


class CatalogAdmin(admin.ModelAdmin):
    readonly_fields = ('uri', )


class SectionAdmin(admin.ModelAdmin):
    readonly_fields = ('uri', 'path')


class SubsectionAdmin(admin.ModelAdmin):
    readonly_fields = ('uri', 'path')


class QuestionEntityAdmin(admin.ModelAdmin):
    readonly_fields = ('uri', 'path')


class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ('uri', 'path')


admin.site.register(Catalog, CatalogAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Subsection, SubsectionAdmin)
admin.site.register(QuestionEntity, QuestionEntityAdmin)
admin.site.register(Question, QuestionAdmin)
