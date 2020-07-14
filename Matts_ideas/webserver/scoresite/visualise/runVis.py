import os
import webbrowser
from modeller import *
from modeller.scripts import complete_pdb
import urllib
import matplotlib
import matplotlib.cm as cm

class LoadModel:
    """
    Overarching class with methods common to all 3 sub classes
    """
    def __init__(self,pdb_code):
        self.pdb_code = pdb_code
        self.state = False
        self.url_warning=None

    def open_url(self,data_label=None,print_out=False,open_link=True):
        if not self.state:
            self.output_statefile(data_label=data_label,output_bool=False)
        url = f"https://www.ncbi.nlm.nih.gov/Structure/icn3d/full.html?divid=div0&pdbid={self.pdb_code}&command="
        for line in self.state:
            if "mmdb" not in line:
                url+=f"{line.replace(' ','%20')};"

        if open_link:
            if not self.url_warning:
                webbrowser.open(url)
            else:
                print(self.url_warning)

        if print_out:
            return(url)

    def output(self,lines,state_pref,state_suff):
        with open("%s%s%s" % (state_pref,self.pdb_code,state_suff),"w+") as f:
                for line in lines:
                    f.write(f"{line}\n")
                f.close()

class RepLabels(LoadModel):
    """
    A class to output iCn3D commands for surface labelling information
    """
    def __init__(self,pdb_code,labels):
        super().__init__(pdb_code)
        self.labels = self.get_labels(labels)


    def get_labels(self,labels):
        """Parse covalent labels and return residue ids"""
        mls = set()

        # print(labels)
        labels = labels.read().decode("utf-8")
        for line in str(labels).splitlines():
            ml = line.split('|')
            mls.add((int(ml[0]),ml[1]))

        return mls

    def output_statefile(self,data_label="",state_pref="./",state_suff="_state.txt",color="0FF",output_bool=True):
        lines = []

        lines.append(f"load mmdb {self.pdb_code}")

        for ml in self.labels:
            lines.append(f"select .{ml[1]}:{ml[0]}" )
            lines.append("style sidec ball and stick")
            lines.append(f"color {color}")

        if output_bool:
            self.output(lines,state_pref,state_suff)

        self.state = lines

class HDXRepr(LoadModel):
    """
    A class to output iCn3D commands for representing HDX information.
    HDX format is as gathered from start2fold database
    """
    def __init__(self,pdb_code,hdx_file):
        super().__init__(pdb_code)
        self.stability,self.folding = self.read_hdx(hdx_file)
        self.cols = {
            "EARLY":"green",
            "STRONG":"green",
            "INTERMEDIATE":"yellow",
            "MEDIUM":"yellow",
            "WEAK":"red",
            "LATE":"red"
        }

    def read_hdx(self,hdx_file):
        stability = {}
        folding = {}

        # with open(hdx_file) as f:
        #     g = f.read().splitlines()
        g = hdx_file.read().decode('utf-8')
        for line in [i for i in g.splitlines() if not i.startswith("#")]:
            state = line.split(';')[-1].strip()
            aa = int(line.split(';')[0].strip())
            if state in ["EARLY","INTERMEDIATE","LATE"]:
                folding[aa] = state
            else:
                stability[aa] = state
            # f.close()

        return stability, folding

    def output_statefile(self, data_label="stability", output_bool=True, state_pref="./",state_suff="_state.txt"):
        lines = []

        if data_label.lower() == "stability":
            d = self.stability
        elif data_label.lower() == "folding":
            d = self.folding
        else:
            print("Only stability and folding are allowed options.")
            print("No state file output.")
            return

        lines.append(f"load mmdb {self.pdb_code}")

        lines.append("color silver")

        for k,v in d.items():
            lines.append(f"select :{k}")
            lines.append(f"color {self.cols[v]}")

        if output_bool:
            self.output(lines,state_pref, state_suff)

        self.state = lines

class DOPE(LoadModel):
    """A class to output iCn3D commands for representing per-residue DOPE scores in"""
    def __init__(self,pdb_code,data,pdb_loc="."):
        super().__init__(pdb_code)
        self.pdb_loc = pdb_loc
        self.get_pdb()
        self.res_ids = self.get_res_ids()
        self.dope_scores = self.score_dope()
        self.url_warning = "DOPE scoring urls are too long to be accessed. Please output a state file and load into iCn3D."

    def get_pdb(self):
        try:
            os.mkdir(self.pdb_loc)
        except:
            pass

        urllib.request.urlretrieve(f"http://files.rcsb.org/download/{self.pdb_code}.pdb", f"{self.pdb_loc}/{self.pdb_code}.pdb")

    def get_res_ids(self):
        res_ids = set()
        with open(f"{self.pdb_loc}/{self.pdb_code}.pdb") as f:
            g = f.read().splitlines()
            for line in [i for i in g if i.startswith("ATOM")]:
                res_ids.add(int(line[22:28].strip()))
            f.close()

        return res_ids

    def score_dope(self):

        dope_scores = []

        env = environ()
        env.libs.topology.read(file='$(LIB)/top_heav.lib') # read topology
        env.libs.parameters.read(file='$(LIB)/par.lib') # read parameters

        mdl = complete_pdb(env, f"{self.pdb_loc}/{self.pdb_code}.pdb")

        # Assess with DOPE:
        s = selection(mdl)   # all atom selection
        s.assess_dope(output='ENERGY_PROFILE NO_REPORT', file=f"{self.pdb_loc}/{self.pdb_code}.profile",
                      normalize_profile=True, smoothing_window=15)

        with open(f"{self.pdb_loc}/{self.pdb_code}.profile") as f:
            g = f.read().splitlines()
            for line in [i for i in g[7:]]:
                dope_scores.append(float(line.split()[-1]))
            f.close()

        return {k:v for k,v in zip(self.res_ids,dope_scores)}

    def output_statefile(self, data_label="", output_bool=True, state_pref="./",state_suff="_state.txt"):
        lines = []

        lines.append(f"load mmdb {self.pdb_code}")

        lines.append("color silver")

        minima = min(self.dope_scores.values())
        maxima = max(self.dope_scores.values())
        norm = matplotlib.colors.Normalize(vmin=minima, vmax=maxima, clip=True)
        mapper = cm.ScalarMappable(norm=norm, cmap=cm.Reds_r)

        dope_colors = {k:matplotlib.colors.rgb2hex(mapper.to_rgba(v)) for k,v in self.dope_scores.items()}

#         print(dope_colors)

        for k,v in dope_colors.items():
            lines.append(f"select :{k}")
            lines.append(f"color {v}")

        if output_bool:
            self.output(lines,state_pref, state_suff)

        self.state = lines
