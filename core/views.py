from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import WeeklyLog, InternshipPlacement, Evaluation, EvaluationCriteria, CustomUser

# --- Helper: role check ---
def user_has_role(user, allowed_roles):
    """
    Checks if an authenticated user possesses one of the allowed roles 
    or has superuser privileges. Returns False if user is not logged in.
    """
    if not user.is_authenticated:
        return False
    return user.role in allowed_roles or user.is_superuser


# ==========================================
# --- WeeklyLogs Endpoints ---
# ==========================================

@csrf_exempt
def weeklylog_create(request):
    """
    POST endpoint: allows authenticated students to submit a new WeeklyLog.
    """
    if request.method == "POST":
        # 1. Authentication Check
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)

        # 2. Authorization (Role) Check
        if not user_has_role(request.user, ["student", "admin"]):
            return JsonResponse({"error": "Permission denied"}, status=403)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON payload"}, status=400)

        required_fields = ["placement_id", "week_number", "activities"]
        if not all(field in data for field in required_fields):
            return JsonResponse({"error": "Missing required fields"}, status=400)

        try:
            placement = InternshipPlacement.objects.get(id=data["placement_id"])
        except InternshipPlacement.DoesNotExist:
            return JsonResponse({"error": "Placement not found"}, status=404)

        log = WeeklyLog.objects.create(
            placement=placement,
            week_number=data["week_number"],
            activities=data["activities"],
            challenges=data.get("challenges", ""),
            status="submitted"
        )
        return JsonResponse({"id": log.id, "message": "WeeklyLog created"}, status=201)

    return JsonResponse({"error": "Method not allowed. Use POST."}, status=405)


def weeklylog_list(request):
    """
    GET endpoint: returns a list of all weekly logs.
    """
    if request.method == "GET":
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)
            
        logs = WeeklyLog.objects.all().values(
            'id', 'week_number', 'status', 'activities', 'challenges',
            'placement__student__username', 'created_at', 'submitted_at'
        )
        return JsonResponse(list(logs), safe=False)
    return JsonResponse({"error": "Method not allowed. Use GET."}, status=405)


def weeklylog_detail(request, id):
    """
    GET endpoint: returns data for a specific weekly log.
    """
    if request.method == "GET":
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)

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
            return JsonResponse({'error': 'Weekly log not found'}, status=404)
            
    return JsonResponse({"error": "Method not allowed. Use GET."}, status=405)


@csrf_exempt
def weeklylog_update_status(request, id):
    """
    PATCH/PUT endpoint: allows supervisors to update the status of a WeeklyLog.
    """
    if request.method in ["PATCH", "PUT"]:
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)

        if not user_has_role(request.user, ["acad_supervisor", "work_supervisor", "admin"]):
            return JsonResponse({"error": "Permission denied"}, status=403)

        try:
            data = json.loads(request.body)
            log = WeeklyLog.objects.get(id=id)
            log.status = data.get("status", log.status)
            log.save()
            return JsonResponse({"id": log.id, "status": log.status})
        except WeeklyLog.DoesNotExist:
            return JsonResponse({"error": "WeeklyLog not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Method not allowed. Use PATCH or PUT."}, status=405)


# ==========================================
# --- Placements Endpoints ---
# ==========================================

def placement_list(request):
    """
    GET endpoint: lists all internship placements.
    """
    if request.method == "GET":
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)

        placements = InternshipPlacement.objects.all().values(
            'id', 'student__username', 'company_name', 'course',
            'Academic_supervisor__username', 'work_supervisor__username',
            'start_date', 'end_date', 'is_active'
        )
        return JsonResponse(list(placements), safe=False)
    return JsonResponse({"error": "Method not allowed. Use GET."}, status=405)


# ==========================================
# --- Evaluations Endpoints ---
# ==========================================

def evaluation_list(request):
    """
    GET endpoint: lists all evaluations submitted.
    """
    if request.method == "GET":
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)

        evaluations = Evaluation.objects.all().values(
            'id', 'log__week_number', 'criteria__name', 'score',
            'supervisor__username', 'comments',
        )
        return JsonResponse(list(evaluations), safe=False)
    return JsonResponse({"error": "Method not allowed. Use GET."}, status=405)


@csrf_exempt
def evaluation_create(request):
    """
    POST endpoint: allows supervisors to grade a WeeklyLog against criteria.
    """
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)

        if not user_has_role(request.user, ["acad_supervisor", "work_supervisor", "admin"]):
            return JsonResponse({"error": "Permission denied"}, status=403)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON payload"}, status=400)

        required_fields = ["log_id", "criteria_id", "supervisor_id", "score"]
        if not all(field in data for field in required_fields):
            return JsonResponse({"error": "Missing required fields"}, status=400)

        try:
            log = WeeklyLog.objects.get(id=data["log_id"])
            criteria = EvaluationCriteria.objects.get(id=data["criteria_id"])
            supervisor = CustomUser.objects.get(id=data["supervisor_id"])
            
            evaluation = Evaluation.objects.create(
                log=log,
                criteria=criteria,
                supervisor=supervisor,
                score=data["score"],
                comments=data.get("comments", "")
            )
            return JsonResponse({"id": evaluation.id, "message": "Evaluation created"}, status=201)
        except (WeeklyLog.DoesNotExist, EvaluationCriteria.DoesNotExist, CustomUser.DoesNotExist):
            return JsonResponse({"error": "Invalid references (Log, Criteria, or Supervisor not found)"}, status=404)

    return JsonResponse({"error": "Method not allowed. Use POST."}, status=405)