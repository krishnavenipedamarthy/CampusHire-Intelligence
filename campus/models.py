from django.db import models


class Institute(models.Model):
    INSTITUTE_TYPES = [
        ('IIT', 'IIT'),
        ('NIT', 'NIT'),
    ]

    name = models.CharField(max_length=150, unique=True)
    institute_type = models.CharField(max_length=10, choices=INSTITUTE_TYPES)
    location = models.CharField(max_length=100)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=150, unique=True)
    industry = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Branch(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Role(models.Model):
    ROLE_TYPES = [
        ('Internship', 'Internship'),
        ('Full-time', 'Full-time'),
    ]

    title = models.CharField(max_length=150)
    role_type = models.CharField(max_length=20, choices=ROLE_TYPES)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Recruitment(models.Model):
    RECRUITMENT_TYPES = [
        ('Internship', 'Internship'),
        ('Full-time', 'Full-time'),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='recruitments'
    )

    institute = models.ForeignKey(
        Institute,
        on_delete=models.CASCADE,
        related_name='recruitments'
    )

    recruitment_type = models.CharField(
        max_length=20,
        choices=RECRUITMENT_TYPES
    )

    academic_year = models.CharField(max_length=20)

    recruitment_date = models.DateField(null=True, blank=True)

    application_deadline = models.DateField(null=True, blank=True)

    source = models.URLField(blank=True)

    def __str__(self):
        return f"{self.company.name} - {self.institute.name} - {self.academic_year}"


class RecruitmentRole(models.Model):
    recruitment = models.ForeignKey(
        Recruitment,
        on_delete=models.CASCADE,
        related_name='roles'
    )

    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name='recruitment_roles'
    )

    minimum_cgpa = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True
    )

    stipend_or_ctc = models.CharField(
        max_length=100,
        blank=True
    )

    openings = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.recruitment.company.name} - {self.role.title}"


class Eligibility(models.Model):
    recruitment_role = models.ForeignKey(
        RecruitmentRole,
        on_delete=models.CASCADE,
        related_name='eligibility'
    )

    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name='eligibilities'
    )

    graduation_year = models.IntegerField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.recruitment_role} - {self.branch.name}"


class SelectionStage(models.Model):
    STAGE_TYPES = [
        ('Application', 'Application'),
        ('Review', 'Application Review'),
        ('OA', 'Online Assessment'),
        ('Technical', 'Technical Interview'),
        ('HR', 'HR Interview'),
        ('Final', 'Final Selection'),
        ('Offer', 'Offer'),
        ('Internship', 'Internship'),
    ]

    recruitment_role = models.ForeignKey(
        RecruitmentRole,
        on_delete=models.CASCADE,
        related_name='selection_stages'
    )

    stage_name = models.CharField(max_length=100)

    stage_type = models.CharField(
        max_length=30,
        choices=STAGE_TYPES
    )

    stage_order = models.PositiveIntegerField()

    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.recruitment_role} - {self.stage_name}"


class Skill(models.Model):
    CATEGORIES = [
        ('Programming', 'Programming'),
        ('DSA', 'DSA'),
        ('Database', 'Database'),
        ('Frontend', 'Frontend'),
        ('Backend', 'Backend'),
        ('Server', 'Server'),
        ('Cloud', 'Cloud'),
        ('Data', 'Data'),
        ('ML', 'Machine Learning'),
        ('Core', 'Core Engineering'),
        ('Aptitude', 'Aptitude'),
        ('HR', 'HR/Behavioral'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=100, unique=True)

    category = models.CharField(
        max_length=30,
        choices=CATEGORIES
    )

    def __str__(self):
        return self.name


class StageSkill(models.Model):
    selection_stage = models.ForeignKey(
        SelectionStage,
        on_delete=models.CASCADE,
        related_name='skills'
    )

    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name='selection_stages'
    )

    importance = models.CharField(
        max_length=20,
        choices=[
            ('High', 'High'),
            ('Medium', 'Medium'),
            ('Low', 'Low'),
        ],
        default='Medium'
    )

    def __str__(self):
        return f"{self.selection_stage} - {self.skill.name}"


class Student(models.Model):
    name = models.CharField(max_length=150)

    email = models.EmailField(unique=True)

    institute = models.ForeignKey(
        Institute,
        on_delete=models.CASCADE,
        related_name='students'
    )

    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name='students'
    )

    graduation_year = models.IntegerField()

    cgpa = models.DecimalField(
        max_digits=4,
        decimal_places=2
    )

    def __str__(self):
        return self.name


class Application(models.Model):
    STATUS_CHOICES = [
        ('Applied', 'Applied'),
        ('Under Review', 'Under Review'),
        ('Shortlisted', 'Shortlisted'),
        ('Rejected', 'Rejected'),
        ('Selected', 'Selected'),
        ('Offer Accepted', 'Offer Accepted'),
        ('Withdrawn', 'Withdrawn'),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='applications'
    )

    recruitment_role = models.ForeignKey(
        RecruitmentRole,
        on_delete=models.CASCADE,
        related_name='applications'
    )

    application_date = models.DateField(auto_now_add=True)

    current_status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='Applied'
    )

    def __str__(self):
        return f"{self.student.name} - {self.recruitment_role}"


class ApplicationStatusHistory(models.Model):
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='status_history'
    )

    selection_stage = models.ForeignKey(
        SelectionStage,
        on_delete=models.CASCADE,
        related_name='application_statuses'
    )

    status = models.CharField(max_length=50)

    updated_at = models.DateTimeField(auto_now=True)

    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.application} - {self.selection_stage} - {self.status}"