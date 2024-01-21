from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from backend.models import User, Section, Student, Mentor
from backend.serializers import (
    UserSerializer,
    StudentSerializer,
    MentorSerializer,
    SectionSerializer,
    AttendanceSerializer,
    CourseSerializer,
)


@api_view(["GET"])
def users(request):
    """Return all users in the database"""
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def sections(request):
    """Return all sections in the database"""
    sections = Section.objects.all()
    serializer = SectionSerializer(sections, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def section_students(request, section_id):
    """Return all students currently enrolled in a section"""
    section = Section.objects.get(id=section_id)
    students = section.student_set.filter(active=True)
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
def section_details(request, section_id):
    """
    GET: Return section details
    POST: Update section details
        - format: { "capacity": int, "description": str }
    """
    if request.method == "GET":
        section = Section.objects.get(id=section_id)
        serializer = SectionSerializer(section)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        section = Section.objects.get(id=section_id)
        capacity = request.data.get("capacity")
        description = request.data.get("description")
        if capacity is not None:
            section.capacity = capacity
        if description is not None:
            section.description = description
        section.save()
        return Response(status=status.HTTP_201_CREATED)


@api_view(["GET"])
def student_details(request, student_id):
    """
    GET: Return student details
    """
    if request.method == "GET":
        student = Student.objects.get(id=student_id)
        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Theoretically gets the Course for a student's section, given student ID
@api_view(["GET"])
def student_course(request, student_id):
    try:
        student = Student.objects.get(id=student_id)
        course_id = student.section.course
        return Response({"course_id": course_id}, status=status.HTTP_200_OK)
    except Student.DoesNotExist:
        return Response({"error": "Student not found"},status=status.HTTP_404_NOT_FOUND)


# Theoretically gets the mentor of a student's section, given student ID
@api_view(["GET"])
def student_mentor(request, student_id):
    """
    GET: Return student's mentor
    """
    try:
        student = Student.objects.get(id=student_id)
        mentor = student.section.mentor
        serializer = MentorSerializer(mentor)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Student.DoesNotExist:
        return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
    except Mentor.DoesNotExist:
        return Response({"error": "Mentor not found for the student's section"}, status=status.HTTP_404_NOT_FOUND)
    

# Theoretically gets all of a student's attendances, given student ID
@api_view(["GET", "PUT"])
def student_attendances(request, student_id):
    """
    GET: Return all attendance objects associated with a student
    PUT: Update student attendance (PR - present, UN - unexcused absence, EX - excused absence)
    """
    if request.method == "GET":
        student = Student.objects.get(id=student_id)
        attendances = student.attendance_set.all()
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        student = Student.objects.get(id=student_id)
        attendances = student.attendance_set.all()
        for attendance in attendances:
            date = attendance.date
            presence = request.data.get(str(date))
            if presence is not None:
                attendance.presence = presence
                attendance.save()
        return Response(status=status.HTTP_200_OK)

