from django.shortcuts import render, get_object_or_404
from django.db.models import Count

from .models import (
    Company,
    Institute,
    Recruitment,
    Role,
    RecruitmentRole,
    Application,
    Student,
    StageSkill
)


def home(request):

    company_count = Company.objects.count()
    institute_count = Institute.objects.count()
    recruitment_count = Recruitment.objects.count()
    role_count = Role.objects.count()

    companies = Company.objects.all()

    context = {
        'company_count': company_count,
        'institute_count': institute_count,
        'recruitment_count': recruitment_count,
        'role_count': role_count,
        'companies': companies,
    }

    return render(request, 'home.html', context)


def companies(request):

    companies = Company.objects.all()

    context = {
        'companies': companies,
    }

    return render(request, 'companies.html', context)


def institutes(request):

    institutes = Institute.objects.all()

    context = {
        'institutes': institutes,
    }

    return render(request, 'institutes.html', context)


def opportunities(request):

    opportunities = RecruitmentRole.objects.select_related(
        'recruitment',
        'recruitment__company',
        'recruitment__institute',
        'role'
    ).all()

    context = {
        'opportunities': opportunities,
    }

    return render(request, 'opportunities.html', context)


def recruitment_detail(request, recruitment_role_id):

    opportunity = get_object_or_404(
        RecruitmentRole,
        id=recruitment_role_id
    )

    eligibility = opportunity.eligibility.all()

    stages = opportunity.selection_stages.prefetch_related(
        'skills__skill'
    ).order_by('stage_order')

    context = {
        'opportunity': opportunity,
        'eligibility': eligibility,
        'stages': stages,
    }

    return render(
        request,
        'recruitment_detail.html',
        context
    )


def applications(request):

    student = Student.objects.first()

    applications = Application.objects.filter(
        student=student
    ).select_related(
        'recruitment_role__recruitment__company',
        'recruitment_role__role'
    ).prefetch_related(
        'status_history__selection_stage'
    )

    context = {
        'student': student,
        'applications': applications,
    }

    return render(request, 'applications.html', context)


def analytics(request):

    company_count = Company.objects.count()
    institute_count = Institute.objects.count()
    opportunity_count = RecruitmentRole.objects.count()

    internship_count = Recruitment.objects.filter(
        recruitment_type='Internship'
    ).count()

    full_time_count = Recruitment.objects.filter(
        recruitment_type='Full-time'
    ).count()

    popular_skills = (
        StageSkill.objects
        .values('skill__name')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    context = {
        'company_count': company_count,
        'institute_count': institute_count,
        'opportunity_count': opportunity_count,
        'internship_count': internship_count,
        'full_time_count': full_time_count,
        'popular_skills': popular_skills,
    }

    return render(request, 'analytics.html', context)