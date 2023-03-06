import json
import threading
import time
import dict2xml
from django.http import HttpResponse
from json2html import *
from django.shortcuts import render, redirect
from .forms import templateFrom, FieldFromSet, JobForm, FileModelForm
from .models import DOMAIN_CHOICES, Fields, Jobs, Jobpdf
from .models import template
import os
from django.conf import settings
import fitz
from django.forms import modelformset_factory
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import pdfplumber


@login_required(login_url='/login/')
def create_template(request):
    engines = {"Engine 1": get_text1, "Engine 2": get_text2, "Engine 3": get_text1}
    a = template(author=request.user)
    form = templateFrom(request.POST or None, request.FILES or None, instance=a)
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
        text = engines[request.POST["engine"]](os.path.join("pdfs", request.FILES["sample"].name))
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
    all_records = template.objects.filter(status__in=["Sent for Approval", "Approved", "Draft"]).order_by('-id')
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
        all_records = template.objects.filter(status__in = ["Sent for Approval", "Approved", "Draft"]).order_by('-id')
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
    context = {"page_obj": page_obj, "rec_c ount": True if len(templates) > 0 else False}
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
            # templateFrom(request.POST or None, request.FILES or None, instance=a)
            job_form = JobForm(initial={"file_fields": fields, "template": template.objects.get(id=t_id)})
            context["jobform"] = job_form
            context["form"] = "second"
            context["t_id"] = t_id
            context["fileform"] = FileModelForm

        else:
            print(request.POST)
            job_form = JobForm(request.POST or None, request.FILES or None)
            fileform = FileModelForm(request.POST or None, request.FILES or None)
            files = request.FILES.getlist('input')
            if job_form.is_valid() and fileform.is_valid():
                # obj = job_form.save(commit=False)
                # obj.template = request.POST.get('templ', False)
                # obj.save()
                jbf = job_form.save()
                for f in files:
                    print(f">>>>>>>>{f}<<<<<<<<<")
                    file_instance = Jobpdf(input=f, job=jbf)
                    file_instance.save()
            else:
                print(request.FILES.getlist('input'))
                # print(job_form.as_p())
                print(job_form.errors)
                print(fileform.errors)
                print("###########")
            return render(request, "read_pdf/created.html", context={"message": "Job Created Successfully"})
    return render(request, "read_pdf/jobs.html", context=context)


def show_jobs(request):
    items = Jobs.objects.all()
    context = {"items": items}
    return render(request, "read_pdf/show_jobs.html", context=context)


def get_text1(record):
    print("GET TEXT1")
    doc = fitz.open(os.path.join(settings.MEDIA_ROOT, record))
    text = ""
    for page in doc:
        text += page.get_text("text")
    return text


def get_text2(record):
    print("GET TEXT 2")
    text = ""
    with pdfplumber.open(os.path.join(settings.MEDIA_ROOT, record)) as pdf:
        pages = pdf.pages
        for i in range(0, len(pages)):
            page = pages[i]
            text1 = page.extract_text(x_tolerance=3, y_tolerance=3)
            text += text1
    return text


def logout_view(request):
    logout(request)
    return redirect('/')


def execute(request, j_id):
    job = Jobs.objects.get(id=j_id)
    fields = Fields.objects.filter(pdf=job.template)
    items = Jobpdf.objects.filter(job=j_id)
    job.status = "Running"
    job.save()
    t = threading.Thread(target=extract_data,
                         args=(job, items, fields))
    t.daemon = True
    t.start()

    # data = extract_data(job, items, fields)
    # data = json2html.convert(json=json.dumps(data))
    # context = {"data": data}
    return redirect(show_jobs)
    # return render(request, "read_pdf/show_output.html", context)

    
def extract_data(job, items, fields):
    engines = {"Engine 1": get_text1, "Engine 2": get_text2, "Engine 3": get_text1}

    for item in items:
        dd = {}
        text = engines[job.template.engine](item.input.name)
        # text = text.replace("\n", " ")
        for f in fields:
            try:
                dd[f.field] = text.split(f.start)[1].split(f.end)[0].strip()
            except:
                dd[f.field] = ""
        item.status = True
        item.result = json.dumps(dd)
        item.save()
    job.status = "Completed"
    job.save()


def view_result(request, j_id):
    items = Jobpdf.objects.filter(job=j_id, status=True)
    data_dict = {}
    count = 0
    for i in items:
        count += 1
        if count > 5:
            break
        d = json.loads(i.result)
        print(i.id, i.job, d)
        data_dict[i.input.name.split("/")[1].split(".pdf")[0]] = d
    data = json2html.convert(json=json.dumps(data_dict))
    context = {"data": data, "job_id": j_id}
    return render(request, "read_pdf/show_output.html", context)


def download_file(request, j_id):
    job = Jobs.objects.get(id=j_id)
    filename = f"{job.output_filename}.{job.output_format}"
    path = os.path.join(settings.MEDIA_ROOT, "temp", filename)
    items = Jobpdf.objects.filter(job=j_id,status=True)
    data = {}
    for item in items:
        data[item.input.name.split("/")[1].split(".pdf")[0]] = json.loads(item.result)

    with open(path,"w+") as f:
        if job.output_format == "XML":
            xml = dict2xml(data)
            f.write(xml)
        elif job.output_format == "JSON":
            json_data = json.dumps(data, indent=4)
            f.write(json_data)
    resp = HttpResponse('')
    with open(path, 'r') as tmp:
        # filename = tmp.name.split('/')[-1]
        resp = HttpResponse(tmp, content_type='application/text;charset=UTF-8')
        resp['Content-Disposition'] = "attachment; filename=%s" % filename
    return resp
