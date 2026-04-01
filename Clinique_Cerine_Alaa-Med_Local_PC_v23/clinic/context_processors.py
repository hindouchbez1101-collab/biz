def nav_context(request):
    user = request.user
    groups = set()
    if user.is_authenticated:
        groups = set(user.groups.values_list("name", flat=True))
    return {"USER_GROUPS": groups, "CLINIC_NAME": "Clinique Cerine Alaa-Med"}
