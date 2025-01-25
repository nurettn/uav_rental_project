from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .constants import TEAM_PART_MAPPING, TeamEnum
from .forms import PartForm
from .models import Aircraft, Assembly, Part


@login_required
def dashboard(request):
    user_team = request.user.personnel.team.name
    context = {
        "team": user_team,
    }
    return render(request, "rental/dashboard.html", context)


@login_required
def part_list(request):
    user_team = request.user.personnel.team

    if user_team is None or user_team.name == TeamEnum.NOTEAM.value:
        messages.error(request, "You do not belong to any team and cannot manage parts.")
        return redirect("dashboard")

    if user_team.name == TeamEnum.ASSEMBLY.value:
        parts = Part.objects.all()
    else:
        parts = Part.objects.filter(team=user_team)

    context = {
        "parts": parts,
        "team": user_team.name,
    }

    return render(request, "rental/part_list.html", context)


@login_required
def part_create(request):
    user_team = request.user.personnel.team
    if user_team is None or user_team.name == TeamEnum.NOTEAM.name:
        messages.error(
            request, "You are not assigned to any team and cannot create parts. Please contact the administrator."
        )
        return redirect("dashboard")

    allowed_part_types = TEAM_PART_MAPPING.get(user_team.name, [])
    if not allowed_part_types:
        messages.error(request, "Your team does not manage any parts.")
        return redirect("dashboard")

    if request.method == "POST":
        form = PartForm(request.POST, user_team=user_team)
        if form.is_valid():
            part = form.save(commit=False)
            part.team = user_team
            part.save()
            messages.success(request, "Part created successfully.")
            return redirect("part_list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PartForm(user_team=user_team)
    return render(request, "rental/part_form.html", {"form": form})


@login_required
def part_update(request, pk):
    user_team = request.user.personnel.team

    if user_team is None or user_team.name == TeamEnum.NOTEAM.value:
        messages.error(request, "You do not belong to any team and cannot edit parts.")
        return redirect("dashboard")

    part = get_object_or_404(Part, pk=pk)

    # Disallow Assembly Team from deleting any parts
    if user_team.name == TeamEnum.ASSEMBLY.value:
        messages.error(request, "Assembly Team members are not authorized to delete parts.")
        return redirect("part_list")

    # Ensure team members can only edit their own parts
    if user_team.name != TeamEnum.ASSEMBLY.value and part.team != user_team:
        messages.error(request, "You are not authorized to edit this part.")
        return redirect("part_list")

    allowed_part_types = TEAM_PART_MAPPING.get(user_team.name, [])
    if part.part_type not in allowed_part_types and user_team.name != TeamEnum.ASSEMBLY.value:
        messages.error(request, "You are not authorized to edit this part type.")
        return redirect("part_list")

    if request.method == "POST":
        form = PartForm(request.POST, instance=part, user_team=user_team)
        if form.is_valid():
            form.save()
            messages.success(request, "Part updated successfully.")
            return redirect("part_list")
    else:
        form = PartForm(instance=part, user_team=user_team)
    return render(request, "rental/part_form.html", {"form": form})


@login_required
def part_delete(request, pk):
    user_team = request.user.personnel.team

    if user_team is None or user_team.name == TeamEnum.NOTEAM.value:
        messages.error(request, "You do not belong to any team and cannot delete parts.")
        return redirect("dashboard")

    part = get_object_or_404(Part, pk=pk)

    # Disallow Assembly Team from deleting any parts
    if user_team.name == TeamEnum.ASSEMBLY.value:
        messages.error(request, "Assembly Team members are not authorized to delete parts.")
        return redirect("part_list")

    # Ensure team members can only edit their own parts
    if user_team.name != TeamEnum.ASSEMBLY.value and part.team != user_team:
        messages.error(request, "You are not authorized to delete this part.")
        return redirect("part_list")

    allowed_part_types = TEAM_PART_MAPPING.get(user_team.name, [])
    if part.part_type not in allowed_part_types and user_team.name != TeamEnum.ASSEMBLY.value:
        messages.error(request, "You are not authorized to delete this part type.")
        return redirect("part_list")

    if request.method == "POST":
        part.delete()
        messages.success(request, "Part deleted successfully.")
        return redirect("part_list")
    return render(request, "rental/part_confirm_delete.html", {"part": part})


@login_required
def assembly_list(request):
    user_team = request.user.personnel.team
    if user_team.name != "Assembly":
        messages.error(request, "You do not have permission to access this page. You're not an Assembly team member.")
        return redirect("dashboard")
    assemblies = Assembly.objects.all()
    return render(request, "rental/assembly_list.html", {"assemblies": assemblies})


@login_required
def assemble_aircraft(request):
    user_team = request.user.personnel.team
    if user_team.name != TeamEnum.ASSEMBLY.value:
        messages.error(
            request, "You do not have permission to perform this action. You're not an Assembly team member."
        )
        return redirect("dashboard")
    if request.method == "POST":
        aircraft_id = request.POST.get("aircraft")
        aircraft = get_object_or_404(Aircraft, id=aircraft_id)

        # Fetch required parts
        required_parts = {
            "Wing": None,
            "Fuselage": None,
            "Tail": None,
            "Avionics": None,
        }

        # Check and assign parts
        try:
            with transaction.atomic():
                for part_type in required_parts.keys():
                    part = (
                        Part.objects.select_for_update()
                        .filter(part_type=part_type, aircraft=aircraft, stock__gt=0)
                        .first()
                    )
                    if not part:
                        raise ValueError(f"{part_type} is missing for {aircraft}.")
                    required_parts[part_type] = part
                    # Decrease stock
                    part.stock -= 1
                    part.save()

                # Create assembly
                assembly = Assembly.objects.create(
                    aircraft=aircraft,
                    wings=required_parts["Wing"],
                    fuselages=required_parts["Fuselage"],
                    tails=required_parts["Tail"],
                    avionics=required_parts["Avionics"],
                )
                messages.success(request, f"{aircraft} assembled successfully.")
                return redirect("assembly_list")
        except ValueError as e:
            messages.error(request, str(e))
    aircrafts = Aircraft.objects.all()
    return render(request, "rental/assemble_aircraft.html", {"aircrafts": aircrafts})
