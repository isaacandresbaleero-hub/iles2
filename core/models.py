from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'student_intern'),
        ('Acad_supervisor', 'academic supervisor'),
        ('work_supervisor', 'work supervisor'),
        ('admin', 'admin'),
    ]

    role = models.CharField(max_length=30, choices = ROLE_CHOICES, default='student')
    university_id = models.CharField(max_length = 20, blank=True, null= True)
    def __str__ (self):
        return f"{self.username} ({self.role})"

class InternshipPlacement(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                limit_choices_to = {'role': 'student'}, related_name = 'student_placements')
    Academic_supervisor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, 
                                limit_choices_to= {'role': 'Acad_supervisor'}, related_name = 'academic_supervisions')
    work_supervisor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, 
                                limit_choices_to= {'role': 'work_supervisor'}, related_name= 'work_supervisions' ) 
    company_name = models.CharField(max_length= 100)
    course = models.CharField(max_length= 100)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__ (self):
        return f"{self.student.username} - {self.company_name}"

class WeeklyLog(models.Model):
    placement = models.ForeignKey(InternshipPlacement, on_delete = models.CASCADE, related_name = 'weekly_logs')
    week_number = models.PositiveIntegerField()
    activities = models.TextField()
    challenges = models.TextField(blank = True, null = True)
    STATUS_CHOICES = [
        ('draft', 'draft'),
        ('submitted', 'submitted'),
        ('reviewed', 'reviewed'),
        ('approved', 'approved'),
        ('rejected', 'rejected'),
    ]
    status = models.CharField(max_length = 20, choices = STATUS_CHOICES, default = 'draft')
    created_at = models.DateTimeField(auto_now_add = True)
    submitted_at = models.DateTimeField(blank = True, null = True)

    def __str__ (self):
        return f"week {self.week_number} - {self.placement.student.username}"
    
class EvaluationCriteria(models.Model):
    name = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits = 5, decimal_places = 2)

    def __str__ (self):
        return f"{self.name} {self.weight}%"
    
class Evaluation(models.Model):
    log = models.ForeignKey(WeeklyLog, on_delete=models.CASCADE, related_name = 'evaluations')
    supervisor = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    criteria = models.ForeignKey(EvaluationCriteria, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    comments = models.TextField(blank = True, null = True)

    def __str__ (self):
        return f"{self.criteria.name} - {self.score} by {self.supervisor.username}"
    

    
    

    

    



