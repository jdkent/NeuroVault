from .models import Study, StatMap
from .forms import StudyFormSet#, StudyForm
from .forms2 import StudyForm
from django.http.response import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

@login_required
def edit_statmaps(request, study_id):
    study = Study.objects.get(pk=study_id)
    if request.method == "POST":
        formset = StudyFormSet(request.POST, request.FILES, instance=study)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(study.get_absolute_url())
    else:
        formset = StudyFormSet(instance=study)
        
    context = {"formset": formset}
    return render(request, "statmaps/edit_statmaps.html", context)

@login_required
def edit_study(request, study_id=None):
    page_header = "Add a new study"
    if study_id:
        study = Study.objects.get(pk=study_id)
        page_header = "Edit study"
        if study.owner != request.user:
            return HttpResponseForbidden()
    else:
        study = Study(owner=request.user)
    if request.method == "POST":
        form = StudyForm(request.POST, request.FILES, instance=study)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(study.get_absolute_url())
    else:

        form = StudyForm(instance=study)
        
    context = {"form": form, "page_header": page_header}
    return render(request, "statmaps/edit_study.html.haml", context)

def view_statmap(request, pk):
    #Tal put logic for reading and transforming Nifti to JSON here
    statmap = get_object_or_404(StatMap, pk=pk)
    #pass the JSON data here
    return render(request, 'statmaps/statmap_details.html.haml', {'statmap': statmap})

def view_statmaps_by_tag(request, tag):
    statmaps = StatMap.objects.filter(tags__name__in=[tag])
    context = {'statmaps': statmaps, 'tag': tag}
    return render(request, 'statmaps/statmaps_by_tag.html', context)
