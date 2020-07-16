from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import PDBForm
from .runVis import LoadModel, DOPE, HDXRepr, RepLabels, CustomRes
import urllib

d_obj = {
    "1":RepLabels,
    "2":HDXRepr,
    "3":DOPE,
    "4":CustomRes
}

d_desc = {
    "1":"Selected residues are shown in red as ball and stick representation.",
    "2":{
    "folding":"Green: Early, Yellow: Intermediate, Red: Late.",
    "stability":"Green: Strong, Yellow: Medium, Red: Weak."
    },
    "3":"Lighter residues indicate better DOPE scoring regions.",
    "4":"Color gradient from white to dark red indicates low -> high scoring."
}

# Create your views here.
def index(request):

    if request.method == 'GET':
        context = {'form':PDBForm()}
        return render(request,"visualise/home.html",context)

    if request.method == 'POST':
        form = PDBForm(request.POST, request.FILES)

        print("Files")
        print(request.FILES)
        if form.is_valid():
            input_data = form.cleaned_data

            if 'data' not in request.FILES:
                request.FILES['data']=None

            obj = d_obj[input_data["choice"]](input_data['PDB'],request.FILES['data'])
            url = obj.open_url(open_link=False,print_out=True,data_label=input_data["hdx_opt"])

            print(len(url))

            context = {'state':"\n".join(obj.state)}

            if input_data["choice"] == "2":
                desc = d_desc["2"][input_data["hdx_opt"]]
            else:
                desc = d_desc[input_data["choice"]]

            try:
                req = urllib.request.urlopen(url)
                assert req.getcode()==200
                req.close()
                return render(request,"visualise/results.html",{'url':url,'desc':desc})
            except:
                filename = "%s_state.txt" % input_data['PDB']
                content = "\n".join(obj.state)
                # response = HttpResponse(content, content_type='text/plain')
                response = render(request,"visualise/results.html",{'url':'https://www.ncbi.nlm.nih.gov/Structure/icn3d/full.html','desc':desc})
                response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
                print(response)
                return response

        return HttpResponse("Testing")

def help(request):
    return render(request,"visualise/help.html")

def results(request):
    return render(request,"visualise/results.html",{'url':'https://www.ncbi.nlm.nih.gov/Structure/icn3d/full.html'})
