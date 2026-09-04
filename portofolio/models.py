from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to='projects/gallery/')
    description = models.CharField(max_length=300, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.project.title} image {self.order + 1}'


class Profile(models.Model):
    name = models.CharField(max_length=100)
    headline = models.CharField(max_length=200)
    subheadline = models.CharField(max_length=300)
    bio = models.TextField()
    avatar = models.ImageField(upload_to='profile/', blank=True)
    email = models.EmailField(blank=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    tiktok = models.URLField(blank=True)
    cv_file = models.FileField(upload_to='cv/', blank=True)

    def __str__(self):
        return self.name


class ProfileImage(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to='profile/gallery/')
    description = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']


class Experience(models.Model):
    company = models.CharField(max_length=150)
    role = models.CharField(max_length=150)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f'{self.role} at {self.company}'


class ExperienceImage(models.Model):
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to='experience/')
    description = models.CharField(max_length=300, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']


class Certification(models.Model):
    name = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=200)
    issue_date = models.DateField(blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)
    credential_id = models.CharField(max_length=150, blank=True)
    credential_url = models.URLField(blank=True)
    image = models.ImageField(upload_to='certifications/', blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-issue_date', 'name']

    def __str__(self):
        return self.name


class Language(models.Model):
    PROFICIENCY_CHOICES = (
        ('Native or bilingual proficiency', 'Native or bilingual proficiency'),
        ('Full professional proficiency', 'Full professional proficiency'),
        ('Professional working proficiency', 'Professional working proficiency'),
        ('Limited working proficiency', 'Limited working proficiency'),
        ('Elementary proficiency', 'Elementary proficiency'),
    )
    name = models.CharField(max_length=80)
    proficiency = models.CharField(max_length=60, choices=PROFICIENCY_CHOICES)

    def __str__(self):
        return f'{self.name} - {self.proficiency}'


class Organization(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=150, blank=True)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)
    image = models.ImageField(upload_to='organizations/', blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['-start_date', 'name']

    def __str__(self):
        return self.name


class Education(models.Model):
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=150)
    field = models.CharField(max_length=150)
    year = models.CharField(max_length=30)
    score = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['-year']

    def __str__(self):
        return f'{self.degree} - {self.institution}'


class Message(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.subject or "No subject"}'