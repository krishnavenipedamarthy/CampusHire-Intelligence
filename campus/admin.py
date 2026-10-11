from django.contrib import admin

from .models import (
    Institute,
    Company,
    Branch,
    Role,
    Recruitment,
    RecruitmentRole,
    Eligibility,
    SelectionStage,
    Skill,
    StageSkill,
    Student,
    Application,
    ApplicationStatusHistory,
)

admin.site.register(Institute)
admin.site.register(Company)
admin.site.register(Branch)
admin.site.register(Role)
admin.site.register(Recruitment)
admin.site.register(RecruitmentRole)
admin.site.register(Eligibility)
admin.site.register(SelectionStage)
admin.site.register(Skill)
admin.site.register(StageSkill)
admin.site.register(Student)
admin.site.register(Application)
admin.site.register(ApplicationStatusHistory)