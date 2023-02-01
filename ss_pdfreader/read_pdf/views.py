from django.shortcuts import render, redirect
from .forms import templateFrom, FieldFromSet, JobForm
from .models import DOMAIN_CHOICES, Fields, Jobs
from .models import template
import os
from django.conf import settings
import fitz
from django.forms import modelformset_factory
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


# Create your views here.

@login_required(login_url='/login/')
def create_template(request):
    engines = {"Engine 1": get_text1, "Engine 2": get_text2, "Engine 3": get_text3}
    a = template(author=request.user)
    form = templateFrom(request.POST or None, request.FILES or None, instance=a)
    print(form)
    context = {
        'form': form,
        "type": "form1",

    }
    if request.method == "POST" and request.POST["submit_button"] == "raw":
        if form.is_valid():
            form.initial = {"author": request.user, "status": "Sent for Approval"}
            rec = form.save()

        formset = FieldFromSet(queryset=Fields.objects.none())
        print(request.POST["engine"])
        print("%%%%%%%%%" * 10)
        text = engines[request.POST["engine"]](request.FILES["sample"].name)
        context["record"] = rec
        context["text"] = text
        context["type"] = "form2"
        context["formset"] = formset

    if request.method == "POST" and request.POST["submit_button"] != "raw":
        formset = FieldFromSet(data=request.POST)
        if formset.is_valid():
            formset.save()
            template.objects.filter(id=request.POST["pdf"]).update(status=request.POST["submit_button"])

            return render(request, "read_pdf/created.html", context={"message": "Template Created Successfully"})
        else:
            print(formset.errors)

    return render(request, "read_pdf/create_template.html", context)


@login_required(login_url='/login/')
def template_config(request):
    all_records = template.objects.all()
    context = {"records": all_records}
    return render(request, "read_pdf/template_config.html", context=context)


@login_required(login_url='/login/')
def edit_update(request, p_id):
    FormSetField = modelformset_factory(Fields, exclude=["pdf", ], extra=0)
    template_rec = template.objects.get(id=p_id)
    template_form = templateFrom(instance=template_rec)

    field_rec = Fields.objects.filter(pdf=p_id)
    print(list(field_rec))
    field_form = FormSetField(queryset=field_rec)

    context = {"tform": template_form, "formset": field_form, "show": "show",
               "formset_show": True if len(field_rec) > 0 else False}

    if request.method == "POST":
        print(request.POST)
        formset = FormSetField(data=request.POST)
        template_form = templateFrom(request.POST, request.FILES or None, instance=template_rec)
        if formset.is_valid():
            formset.save()

        if template_form.is_valid():
            template_form.save()
        else:
            print(template_form.errors)
        template.objects.filter(id=p_id).update(status=request.POST["submit_button"])
        return render(request, "read_pdf/created.html", context={"message": "Template Created Successfully"})

    return render(request, "read_pdf/edit_update.html", context=context)


@login_required(login_url='/login/')
def view_template(request):
    if request.method == "GET":
        all_records = template.objects.all()
        context = {"records": all_records, "type": "show"}
    # if request.method == "POST":
    #     id = request.POST["item_select"]
    #     record = template.objects.filter(id=id).first()
    #     text = get_text(record)
    #     print(record.sample.url)
    #     context = {"record": record, "type": "edit", "text": text}
    return render(request, "read_pdf/show.html", context)


def approve_template(request):
    templates = template.objects.filter(status="Approved")

    paginator = Paginator(templates, 10)
    try:
        page_number = request.GET.get('page')
    except:     
        page_number = 0
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj, "rec_count": True if len(templates) > 0 else False}
    if request.method == "POST":
        if request.POST.get("approve") and len(request.POST.getlist("approve_check")) > 0:
            print("approving")
            ll = template.objects.filter(
                id__in=request.POST.getlist("approve_check")).update(
                status="Approved")
        if request.POST.get("approve_all"):
            ll = template.objects.filter(status="Approved").update(status="Sent for Approval")
        return render(request, "read_pdf/approved.html", context={"count": ll, "user": request.user})
    return render(request, "read_pdf/approve.html", context=context)


def create_job(request):
    templates = template.objects.all()
    context = {"form": "first", "templates": templates}
    if request.method == "POST":
        if request.POST["form1"] == "Submit":
            t_id = request.POST["temp_select"]
            print(t_id)
            fields = Fields.objects.filter(pdf=t_id).values_list("field")
            fields = ", ".join([x[0] for x in fields])
            job_form = JobForm(initial={"file_fields": fields, "template": template.objects.get(id=t_id)})
            context["jobform"] = job_form
            context["form"] = "second"
            context["t_id"]=t_id

        else:
            print(request.POST)
            job_form = JobForm(request.POST)
            if job_form.is_valid():
                # obj = job_form.save(commit=False)
                # obj.template = request.POST.get('templ', False)
                # obj.save()
                job_form.save()
            else:
                print(job_form.as_p())
                print(job_form.errors)
            return render(request, "read_pdf/created.html", context={"message": "Job Created Successfully"})
    return render(request, "read_pdf/jobs.html", context=context)


def show_jobs(request):
    items = Jobs.objects.all()
    context = {"items": items}
    return render(request, "read_pdf/show_jobs.html", context=context)


def get_text1(record):
    print("Engine11111")
    doc = fitz.open(os.path.join(settings.MEDIA_ROOT, "pdfs", record))
    page = doc[0]
    text = page.get_text("text")
    return text


def get_text2(record):
    print("Engine22222")

    doc = fitz.open(os.path.join(settings.MEDIA_ROOT, "pdfs", record))
    page = doc[0]
    text = page.get_text("text")
    return text


def get_text3(record):
    print("Engine333333")
    doc = fitz.open(os.path.join(settings.MEDIA_ROOT, "pdfs", record))
    page = doc[0]
    text = page.get_text("text")
    return text


def logout_view(request):
    logout(request)
    return redirect('/')
