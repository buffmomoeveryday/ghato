from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from purchases.models import UnitOfMeasurements


@login_required()
def dashboard_index(request):
    context = {}

    return render(
        request=request,
        template_name="dashboard/dashboard-index.html",
        context=context,
    )


@login_required()
def add_uom(request):
    if request.method == "POST":
        uom = request.POST.get("UOM")
        unit_of_measurements = UnitOfMeasurements.objects.get_or_create(name="uom")
