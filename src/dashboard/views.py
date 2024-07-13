from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required()
def dashboard_index(request):
    context = {}

    return render(
        request=request,
        template_name="dashboard/dashboard-index.html",
        context=context,
    )
