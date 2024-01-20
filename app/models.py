from django.db import models
from django.utils import timezone
from .utils.file_helpers import custom_file_name
import string
import random

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class role(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(role, self).save(*args, **kwargs)

class staff(BaseModel):
    DIR_NAME = 'staff'
    staff_id = models.CharField(max_length=10, unique=True, editable=False)
    role = models.ForeignKey(role, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True, blank=False)
    mobile = models.CharField(max_length=50, null=True)
    password = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    otp = models.CharField(max_length=20, default='123456')

    def __str__(self):
        return f"{self.staff_id} - {self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.staff_id:
            # Generate the custom ID if it doesn't exist
            last_id = staff.objects.all().order_by('-id').first()
            if last_id:
                last_id = last_id.staff_id
                last_id = last_id.replace('HP', '')
                last_id = int(last_id)
                new_id = f'HP{str(last_id + 1).zfill(4)}'
            else:
                new_id = 'HP0001'
            self.staff_id = new_id

        if not self.password:
            # Generate a random password
            password_characters = string.ascii_letters + string.digits + '@#_!'
            random_password = ''.join(random.choice(password_characters) for i in range(8))
            self.password = random_password.upper()

        super(staff, self).save(*args, **kwargs)


class Doctor(models.Model):
    DIR_NAME = 'doctors-profile'
    FILENAME_WORD = 'dp'
    firstname = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    age = models.IntegerField()  # Changed to IntegerField
    address = models.TextField()  # Removed duplicate line
    total_patient = models.IntegerField(default=0)
    summary = models.TextField()
    profile_pic = models.ImageField(upload_to=custom_file_name, default='default_images/doctor-profile.png')

    def __str__(self):
        return f"{self.firstname} - {self.last_name}"


class Patient(models.Model):
    firstname = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    age = models.IntegerField()  # Changed to IntegerField
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    address = models.CharField(max_length=150)
