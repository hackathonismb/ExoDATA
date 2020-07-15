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

            try:
                req = urllib.request.urlopen(url)
                assert req.getcode()==200
                return HttpResponseRedirect(url)
            except:
                filename = "%s_state.txt" % input_data['PDB']
                content = "\n".join(obj.state)
                response = HttpResponse(content, content_type='text/plain')
                response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
                return response

        return HttpResponse("Testing")

def help(request):
    return render(request,"visualise/help.html")
