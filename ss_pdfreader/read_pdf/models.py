from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField

Engine_choice = [
    ("Engine 1", "Engine 1"),
    ("Engine 2", "Engine 2"),
    # ("Engine 3", "Engine 3"),
]

DOMAIN_CHOICES = (
    ('Invoice', (
        ("Electricity", "Electricity"),
        ('Shopping', 'Shopping'),
    )
     ),
    ('Purchase order', (
        ('PO Subdomain', 'PO Subdomain'),
    )
     ),
    ('Healthcare', (
        ('hospital', 'hospital'),
        ('clinic', 'clinic'),
    )
     ),
)
regex_choice = [("Custom", "Custom"),
                ("Decimal numbers", "Decimal numbers"),
                ("Numeric", "Numeric"),
                ("Alphanumeric", "Alphanumeric"),
                ("All characters, except newline or line terminator",
                 "All characters, except newline or line terminator"),
                ("String beginning with", "String beginning with"),
                ("Alphabet", "Alphabet"),
                ("Special Characters", "Special Characters"),
                ("Alphanumberic with special characters ASCII Characters",
                 "Alphanumberic with special characters ASCII Characters")]

status_choice = [("Sent for Approval", "Sent for Approval"),
                 ("Approved", "Approved"),
                 ("Draft", "Draft")]
NODE_CHOICES = [("Machine 1", "Machine 1"),
                ("Machine 2", "Machine 2"),
                ("Machine 3", "Machine 3"),
                ("Machine 4", "Machine 4")]

INPUT_CHOICES = [("Network/Local", "Network/Local"), ("Email", "Email")]
NOTIFICATION_CHOICES = [("Email", "Email"), ("SMS", "SMS"), ("IVR", "IVR")]
OUTPUT_CHOICES = [("JSON", "JSON"), ("XML", "XML"), ("CSV", "CSV"), ("EXCEL", "EXCEL")]


class template(models.Model):
    name = models.CharField(max_length=100)
    domain = models.CharField(max_length=50, choices=DOMAIN_CHOICES)
    engine = models.CharField(max_length=50, choices=Engine_choice)
    sample = models.FileField(upload_to="pdfs/")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=100)
    comments = models.CharField(max_length=500)
    status = models.CharField(max_length=500, choices=status_choice)

    def __str__(self):
        return str(self.id)


class Fields(models.Model):
    pdf = models.ForeignKey(to=template, on_delete=models.CASCADE, related_name="pdf")
    field = models.CharField(max_length=50)
    start = models.CharField(max_length=200)
    end = models.CharField(max_length=200)
    occurance = models.IntegerField()
    regex_type = models.CharField(max_length=100, choices=regex_choice, null=True)
    regex = models.CharField(max_length=100, null=True)

    class Meta:
        verbose_name_plural = "Fields"


class Jobs(models.Model):
    # execution = models.CharField(max_length=100,
    #                              choices=[("Immediate", "Immediate"), ("Frequency Based", "Frequency Based")])
    template = models.ForeignKey(to=template, on_delete=models.CASCADE, related_name="job")
    name = models.CharField(max_length=100)
    # node = models.CharField(max_length=100, choices=NODE_CHOICES)
    # engine = models.CharField(max_length=100, choices=Engine_choice)
    # input = models.FileField(upload_to="job_pdfs/")
    file_fields = models.TextField()
    # Notification = models.CharField(max_length=50, choices=NOTIFICATION_CHOICES)
    output_format = models.CharField(max_length=50, choices=OUTPUT_CHOICES)
    output_filename = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default="Pending")
    start = models.DateTimeField()
    end = models.DateTimeField()

    class Meta:
        verbose_name_plural = "Jobs"
    def __str__(self):
        return str(self.id)

class Jobpdf(models.Model):
    input = models.FileField(upload_to="job_pdfs")
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    result = JSONField(null=True)
