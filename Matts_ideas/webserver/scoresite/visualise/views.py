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

            # if input_data["choice"]=="1":
                # print(request.FILES['data'].read())

            if 'data' not in request.FILES:
                request.FILES['data']=None

            obj = d_obj[input_data["choice"]](input_data['PDB'],request.FILES['data'])
            url = obj.open_url(open_link=False,print_out=True,data_label=input_data["hdx_opt"])
            # print(url)

            # elif input_data["choice"]=="2":
            #     obj = HDXRepr(input_data['PDB'],request.FILES['data'].read(),)

            print(len(url))

            context = {'state':"\n".join(obj.state)}

            try:
                req = urllib.request.urlopen(url)
                assert req.getcode()==200
                return HttpResponseRedirect(url)
            except:
                # return render(request,"visualise/redirect_out.html",context)
                # return HttpResponse("#The output url was too long.\n#Please copy and paste the below text into a txt file and load into iCn3D as a state file.\n" + "\n".join(obj.state),content_type='text/plain')
                filename = "%s_state.txt" % input_data['PDB']
                content = "\n".join(obj.state)
                response = HttpResponse(content, content_type='text/plain')
                response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
                return response
            # if len(url) <= 2500:
            #     return HttpResponseRedirect(url)
            # else:
            #     return HttpResponse("""
            #     #The URL generated was too long to open a window.\n
            #     #Please save this file as a txt and load print_out\n
            #     #iCn3D as a state file.\n\n
            #
            #     %s
            #     """ % '\n'.join(obj.state))

        return HttpResponse("Testing")
