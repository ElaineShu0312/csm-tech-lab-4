from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    section = models.ForeignKey("Section", on_delete=models.CASCADE)
    course = models.ForeignKey("Course", on_delete=models.CASCADE)

    active = models.BooleanField()
    banned = models.BooleanField()


class Mentor(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    course = models.ForeignKey("Course", on_delete=models.CASCADE)


class Section(models.Model):
    mentor = models.OneToOneField("Mentor", on_delete=models.CASCADE)

    capacity = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=100)


class Course(models.Model):
    name = models.CharField(max_length=20)


# Create an Attendance model, which stores the attendance of a student on a given date.
class Attendance(models.Model):
    class Presence(models.TextChoices):
        PRESENT = "PR", "Present"
        UNEXCUSED_ABSENCE = "UN", "Unexcused absence"
        EXCUSED_ABSENCE = "EX", "Excused absence"

    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    date = models.DateField()
    presence = models.CharField(max_length=2,choices=Presence.choices, blank=True)