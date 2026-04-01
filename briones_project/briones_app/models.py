from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# ─────────────────────────────────────────────
#  PROFILE
# ─────────────────────────────────────────────

class Profile(models.Model):
    """
    Stores all personal/hero information shown on the Home page.
    Only one record should exist — enforced via save().
    """
    full_name       = models.CharField(max_length=150)
    tagline         = models.CharField(max_length=255, help_text="Short headline shown below your name.")
    profile_photo   = models.ImageField(upload_to='profile/', blank=True, null=True)

    class Meta:
        verbose_name        = 'Profile'
        verbose_name_plural = 'Profile'

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        """Singleton — only one Profile row allowed."""
        if not self.pk and Profile.objects.exists():
            raise ValueError("Only one Profile record is allowed. Edit the existing one.")
        super().save(*args, **kwargs)


# ─────────────────────────────────────────────
#  ABOUT
# ─────────────────────────────────────────────

class About(models.Model):
    """
    Detailed personal background, bio, and career goals shown on the About page.
    Only one record should exist — enforced via save().
    """
    short_bio       = models.TextField(blank=True, null=True)
    full_bio        = models.TextField(blank=True, null=True)
    career_goals    = models.TextField(blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'About'
        verbose_name_plural = 'About'

    def __str__(self):
        return f"About — last updated {self.updated_at:%Y-%m-%d}"

    def save(self, *args, **kwargs):
        """Singleton — only one About row allowed."""
        if not self.pk and About.objects.exists():
            raise ValueError("Only one About record is allowed. Edit the existing one.")
        super().save(*args, **kwargs)

    def bio_paragraphs(self):
        """Split full_bio on blank lines for easy template rendering."""
        return [p.strip() for p in self.full_bio.split('\n\n') if p.strip()]


# ─────────────────────────────────────────────
#  CONTACT  (social links + incoming messages)
# ─────────────────────────────────────────────

class ContactInfo(models.Model):
    """
    Public contact details and social links shown on the Contact page.
    Only one record should exist — enforced via save().
    """
    email           = models.EmailField()
    phone           = models.CharField(max_length=30, blank=True,
                                        help_text="Optional — leave blank to hide.")
    github_url      = models.URLField(blank=True)
    linkedin_url    = models.URLField(blank=True)
    twitter_url     = models.URLField(blank=True)
    facebook_url    = models.URLField(blank=True)
    instagram_url   = models.URLField(blank=True)
    contact_note    = models.TextField(
        blank=True,
        help_text="Short blurb shown above the contact form, e.g. 'Always open to new projects…'"
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Contact Info'
        verbose_name_plural = 'Contact Info'

    def __str__(self):
        return f"Contact Info — {self.email}"

    def save(self, *args, **kwargs):
        """Singleton — only one ContactInfo row allowed."""
        if not self.pk and ContactInfo.objects.exists():
            raise ValueError("Only one ContactInfo record is allowed. Edit the existing one.")
        super().save(*args, **kwargs)


class ContactMessage(models.Model):
    """
    Incoming messages submitted through the contact form.
    """
    STATUS_CHOICES = [
        ('new',      'New'),
        ('read',     'Read'),
        ('replied',  'Replied'),
        ('archived', 'Archived'),
    ]

    name        = models.CharField(max_length=100)
    email       = models.EmailField()
    subject     = models.CharField(max_length=200)
    message     = models.TextField()
    status      = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')
    sent_at     = models.DateTimeField(auto_now_add=True)
    admin_notes = models.TextField(
        blank=True,
        help_text="Internal notes — not visible to the sender."
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering        = ['-sent_at']
        verbose_name    = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f"[{self.get_status_display()}] {self.name} — {self.subject}"

    @property
    def is_new(self):
        return self.status == 'new'


# ─────────────────────────────────────────────
#  PROJECT
# ─────────────────────────────────────────────

class Project(models.Model):
    title       = models.CharField(max_length=200)
    description = models.TextField()
    tools       = models.CharField(max_length=300,
                                   help_text="Comma-separated list of tools/technologies.")
    github_link = models.URLField(blank=True, null=True)
    live_link   = models.URLField(blank=True, null=True)
    image       = models.ImageField(upload_to='projects/', blank=True, null=True)
    order       = models.PositiveIntegerField(default=0)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    def tools_list(self):
        return [t.strip() for t in self.tools.split(',')]


# ─────────────────────────────────────────────
#  EDUCATION
# ─────────────────────────────────────────────

class Education(models.Model):
    school      = models.CharField(max_length=200)
    degree      = models.CharField(max_length=200)
    program     = models.CharField(max_length=200, blank=True)
    year_start  = models.CharField(max_length=4)
    year_end    = models.CharField(max_length=4, blank=True,
                                   help_text="Leave blank if still ongoing.")
    description = models.TextField(blank=True)
    order       = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-year_start']

    def __str__(self):
        return f"{self.degree} — {self.school}"

    def year_range(self):
        return f"{self.year_start} – {self.year_end}" if self.year_end \
               else f"{self.year_start} – Present"


# ─────────────────────────────────────────────
#  SKILL
# ─────────────────────────────────────────────

class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('language',  'Programming Languages'),
        ('framework', 'Frameworks & Libraries'),
        ('database',  'Databases'),
        ('tool',      'Tools & Platforms'),
        ('other',     'Other'),
    ]
    name        = models.CharField(max_length=100)
    category    = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    proficiency = models.PositiveIntegerField(
        default=80,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Percentage 0–100"
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['category', 'order', 'name']

    def __str__(self):
        return self.name

class Owner(models.Model):
    name     = models.CharField(max_length=100)
    email    = models.EmailField()
    location = models.CharField(max_length=150)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Singleton — only one Owner allowed."""
        if not self.pk and Owner.objects.exists():
            raise ValueError("Only one Owner record is allowed.")
        super().save(*args, **kwargs)