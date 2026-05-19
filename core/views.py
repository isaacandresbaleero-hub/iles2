from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import WeeklyLog, InternshipPlacement, Evaluation

# --- Weekly Logs ---
def weeklylog_list(request):
    logs = WeeklyLog.objects.all().values(
        'id', 'week_number', 'status', 'activities', 'challenges',
        'placement__student__username', 'created_at', 'submitted_at'
    )
    return JsonResponse(list(logs), safe=False)

def weeklylog_detail(request, id):
    try:
        log = WeeklyLog.objects.get(id=id)
        data = {
            'id': log.id,
            'week_number': log.week_number,
            'activities': log.activities,
            'challenges': log.challenges,
            'status': log.status,
            'student': log.placement.student.username,
            'company': log.placement.company_name,
            'created_at': log.created_at,
            'submitted_at': log.submitted_at,
        }
        return JsonResponse(data)
    except WeeklyLog.DoesNotExist:
        return JsonResponse({'error': 'WeeklyLog not found'}, status=404)

# --- Internship Placements ---
def placement_list(request):
    placements = InternshipPlacement.objects.all().values(
        'id', 'student__username', 'company_name', 'course',
        'Academic_supervisor__username', 'work_supervisor__username',
        'start_date', 'end_date', 'is_active'
    )
    return JsonResponse(list(placements), safe=False)

# --- Evaluations ---
def evaluation_list(request):
    evaluations = Evaluation.objects.all().values(
        'id', 'log__week_number', 'criteria__name', 'score',
        'supervisor__username', 'comments'
    )
    return JsonResponse(list(evaluations), safe=False)


# Create your views here.
