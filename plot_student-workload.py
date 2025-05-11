import numpy as np
import pandas as pd
import matplotlib as mpl
from matplotlib import pyplot as plt
plt.ion()
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
import streamlit as st

# st.write('matplotlib',mpl.__version__)
# st.write('numpy',np.__version__)
# st.write('pandas',pd.__version__)
# st.write('streamlit',st.__version__)

def year2level(year,yrtype="UG"):
    if yrtype=="PG":
        return 7
    else:
        return year+3

# Set student properties
academicYears=["2024/5","2025/6","2026/7"]
easterWeeks={"2024/5":11,"2025/6":8,"2026/7":9}
filenames={"2024/5":"AssessmentSchedule_2425.xlsx","2025/6":"AssessmentSchedule_2526.xlsx","2026/7":"AssessmentSchedule_2627.xlsx"}
coursetypes=["UG","PG"]
courses={"UG":["Physics","Astrophysics","Physics with Astronomy","Medical Physics","Show modules for all programmes"],
         "PG":["Physics", "Astrophysics", "Compound Semiconductor Physics","Show modules for all programmes"]}
years=[1,2,3,4]

columns={"UG":{"Physics":"Physics","Astrophysics":"Astro","Physics with Astronomy":"PhysAstro","Medical Physics":"MedPhys","Show modules for all programmes":"Physics"},
         "PG":{"Physics":"MScPhysics", "Astrophysics":"MScAstro","Compound Semiconductor Physics":"MScCSPhysics","Show modules for all programmes":"Physics"}}

st.header("Select your year and course")
academicYear = st.radio("Select your programme type:",academicYears)
studentCourseType = st.radio("Select your programme type:",coursetypes)
if studentCourseType=="UG":
    studentYear = st.radio("Select your year of study:",years)
else:
    studentYear=1
studentCourse = st.radio("Select your programme:",courses[studentCourseType])
studentLevel=year2level(studentYear,studentCourseType)

colName=columns[studentCourseType][studentCourse]
if studentCourse=="Show modules for all programmes":
    showAllProgs=True
    st.write(f"**Showing All modules for {studentCourseType} student in Year {studentYear} (Level {studentLevel}) of study**")
else:
    showAllProgs=False
    st.write(f"**You are a {studentCourseType} {studentCourse} student in Year {studentYear} (Level {studentLevel}) of study**")

# st.info(f"column {colName}")
# st.stop()
# Set core modules
fileIn=filenames[academicYear]
Modules=pd.read_excel(fileIn,"Modules")
if showAllProgs:
    coreMods=Modules[(Modules["Level"]==studentLevel)&(Modules["Source"]==studentCourseType[0])&(Modules["Credits"]>0)]
else:
    coreMods=Modules[(Modules[colName]=="C")&(Modules["Level"]==studentLevel)&(Modules["Source"]==studentCourseType[0])&(Modules["Credits"]>0)]

coreModList=coreMods["Module Code"].to_list()
selModList=coreModList

coreCredits=coreMods["Credits"].sum()
coreCreditsAutumn=coreMods[coreMods["Semester"]=="SEM1"]["Credits"].sum()+coreMods[coreMods["Semester"]=="SEMD"]["Credits"].sum()/2
coreCreditsSpring=coreMods[coreMods["Semester"]=="SEM2"]["Credits"].sum()+coreMods[coreMods["Semester"]=="SEMD"]["Credits"].sum()/2

nExamsAutumnCore=len(coreMods[(coreMods["Semester"]=="SEM1")&(coreMods["Exam Weight (%)"]>0)])
nExamsSpringCore=len(coreMods[(coreMods["Semester"]=="SEM2")&(coreMods["Exam Weight (%)"]>0)])

optCreditsAvail=120-coreCredits
optMods=Modules[(Modules[colName]=="O")&(Modules["Level"]==studentLevel)&(Modules["Source"]==studentCourseType[0])&(Modules["Credits"]>0)]
        
st.divider()
st.header("Module Selection")
    # st.subheader("Select Optional Modules")
if showAllProgs:
    st.write("Available modules are:",coreMods[["Module Code","Module Title","Semester","Credits","Exam Weight (%)"]].to_html(index=False),unsafe_allow_html=True)
    st.write("Selecting all modules for all programmes")
    showAllMods=True
    optModSelCode=[]
elif coreCredits==120:
    st.write("Your core modules are:",coreMods[["Module Code","Module Title","Semester","Credits","Exam Weight (%)"]].to_html(index=False),unsafe_allow_html=True)
    st.write("You have no optional selections to make.")
    showAllMods=False
    optModSelCode=[]
    # optCreditSel=optMods[optMods["Module Code"].isin(optModSelCode)]["Credits"].sum()
else:
    st.subheader("Optional module selection")
    st.write("Remaining optional credits:",optCreditsAvail)
    st.write("Please consult SIMS for any further conditions of module selection.")
    # st.write("Optional modules",optMods[["Module Code","Module Title","Semester","Credits","Exam Weight (%)"]].to_html(index=False),unsafe_allow_html=True)
    
    optMods=Modules[(Modules[colName]=="O")&(Modules["Level"]==studentLevel)&(Modules["Source"]==studentCourseType[0])&(Modules["Credits"]>0)]
    
    showAllMods=st.checkbox("Select all available modules?")
    if showAllMods:
        st.write("**Warning: workload calculations are not possible when selecting all modules.**")

    # Select Autumn modules
    optModListSEM1=optMods[optMods["Semester"]=="SEM1"]["Module Code"].to_list()
    st.write("Core module credits (Autumn):", int(coreCreditsAutumn))
    if len(optModListSEM1)>0:
        st.write("Optional modules (Autumn Semester)",optMods[optMods["Semester"]=="SEM1"][["Module Code","Module Title","Semester","Credits","Exam Weight (%)"]].to_html(index=False),unsafe_allow_html=True)
        if showAllMods:
            optModSelCodeSEM1=optModListSEM1
            st.write("*Selecting all Autumn semester optional modules**")
        else:
            optModSelCodeSEM1=st.multiselect("Select your Autumn Semester optional modules:",optModListSEM1)
    else:
        st.write("You have no optional selections to make for Autumn semester")
        optModSelCodeSEM1=[]
    optCreditSelSEM1=optMods[optMods["Module Code"].isin(optModSelCodeSEM1)]["Credits"].sum()
    autumnCredits=optCreditSelSEM1 + coreCreditsAutumn
    nExamsAutumn=nExamsAutumnCore + len(optMods[(optMods["Module Code"].isin(optModSelCodeSEM1))&(optMods["Exam Weight (%)"]>0)])
    st.write("Autumn semester credits:",int(autumnCredits))
    st.write("Autumn semester exams:", nExamsAutumn)
    

    # Select Spring modules
    optModListSEM2=optMods[optMods["Semester"]=="SEM2"]["Module Code"].to_list()
    st.write("Core module credits (Spring):", int(coreCreditsSpring))
    if len(optModListSEM2)>0:
        st.write("Optional modules (Spring Semester)",optMods[optMods["Semester"]=="SEM2"][["Module Code","Module Title","Semester","Credits","Exam Weight (%)"]].to_html(index=False),unsafe_allow_html=True)
        if showAllMods:
            optModSelCodeSEM2=optModListSEM2
            st.write("**Selecting all Spring semester optional modules**")
        else:
            optModSelCodeSEM2=st.multiselect("Select your Spring Semester optional modules:",optModListSEM2)
    else:
        optModSelCodeSEM2=[]

    optCreditSelSEM2=optMods[optMods["Module Code"].isin(optModSelCodeSEM2)]["Credits"].sum()
    springCredits=optCreditSelSEM2 + coreCreditsSpring
    nExamsSpring=nExamsSpringCore + len(optMods[(optMods["Module Code"].isin(optModSelCodeSEM2))&(optMods["Exam Weight (%)"]>0)])
    st.write("Spring semester credits:",int(springCredits))
    st.write("Spring semester exams:", nExamsSpring)
    optModSelCode = optModSelCodeSEM1 + optModSelCodeSEM2
optModSel=optMods[optMods["Module Code"].isin(optModSelCode)]        
optCreditSel=optMods[optMods["Module Code"].isin(optModSelCode)]["Credits"].sum()
selModList=optModSelCode + coreModList

selMod=Modules[Modules["Module Code"].isin(selModList)].rename(columns={colName:"Core/Optional"})
autumnCredits=int(selMod[selMod["Semester"]=="SEM1"]["Credits"].sum()+selMod[selMod["Semester"]=="SEMD"]["Credits"].sum()/2)
springCredits=int(selMod[selMod["Semester"]=="SEM2"]["Credits"].sum()+selMod[selMod["Semester"]=="SEMD"]["Credits"].sum()/2)
selCredits=autumnCredits + springCredits

if not showAllMods:
    if optCreditSel<optCreditsAvail:
        st.write(f"Please select {optCreditsAvail-optCreditSel} more credits.")
    elif optCreditSel>optCreditsAvail:
        st.write(f"⚠️ ERROR: You can only select {optCreditsAvail} credits. {optCreditSel} selected")
        st.stop()
    else:
        st.write("👍 All credits selected.")
        if autumnCredits>70 or springCredits>70:
            st.error("⚠️ WARNING: Module choice is unbalanced between semesters")
    


# st.divider()
# st.subheader("Selected Modules:")
# st.write(selMod[["Module Code","Module Title","Semester","Credits","Core/Optional","Exam Weight (%)"]].to_html(index=False),unsafe_allow_html=True)

# st.write("Show All Mods",showAllMods)
st.divider()

if not showAllMods:
    st.header("Estimated Workload")
    st.write("The calculations below are all approximate, and based only on contact time and workload linked to summative assessments.")
    st.write("It assumes that all sessions with contact time are attended, and assessment workload is based on estimates.")
    if selCredits!=120:
        st.write(f"⚠️ WARNING: Module choice is only based on {selCredits} credits.")
    profiles=["Delta","Dist","Linear"]
    profilesDesc=["Work just before the deadline","Distribute the work evenly over the full period","Gradually increase work up to the deadline"]
    profileName=st.radio("How would you like to work?",profilesDesc)
    for p,prof in enumerate(profilesDesc):
        if profileName==prof:
            profileSel=profiles[p]
else:
    profileSel="Delta"


AssessDatesIn=pd.read_excel(fileIn,"Assessments")
AssessDatesIn.fillna(0)   

ContactTimeIn=pd.read_excel(fileIn,"ContactTime")
ContactTimeIn.fillna(0)
    
moduleList=Modules["Module Code"].values
### Add MSc modules to AssessDates 
# Step 1: Filter MSc-derived modules
msc_modules = Modules[(Modules["Source"] == "P") & (Modules["Alternative Module Code"].notna())]

# Step 2: Create duplicated assessment rows for each MSc module
msc_assessments = pd.DataFrame()

for _, row in msc_modules.iterrows():
    original_code = row["Alternative Module Code"]
    msc_code = row["Module Code"]

    # Find all assessment entries for the original module
    original_assessments = AssessDatesIn[AssessDatesIn["Module Code"] == original_code].copy()

    if not original_assessments.empty:
        # Replace Module Code with MSc Module Code
        original_assessments["Module Code"] = msc_code
        msc_assessments = pd.concat([msc_assessments, original_assessments], ignore_index=True)

# Step 3: Append the MSc assessments to the original table
AssessDatesAll = pd.concat([AssessDatesIn, msc_assessments], ignore_index=True)
# AssessDates.to_excel("assessments_with_msc_duplicates.xlsx", index=False)

# Reduce to list of selected modules
AssessDates=AssessDatesAll[AssessDatesAll["Module Code"].isin(selModList)]
AssessDates["Core"]=AssessDates["Module Code"].isin(coreModList)
ContactTime=ContactTimeIn[ContactTimeIn["Module Code"].isin(selModList)]

AutumnWeeks=[]
SpringWeeks=[]
for a in AssessDates:
    if a.find('Autumn Week')>=0:
        AutumnWeeks.append(a)
    if a.find('Spring Week')>=0:
        SpringWeeks.append(a)

def l2y(level,yrtype="UG"):
    if yrtype=="PG":
        years={7:"Y1"}
    else:
        years={4:"Y1",5:"Y2",6:"Y3",7:"Y4"}
    assert(level in years)
    return(years[level])

profileAssess={"Autumn":np.zeros(len(AutumnWeeks)),"Spring":np.zeros(len(SpringWeeks))}
profileAssessCore={"Autumn":np.zeros(len(AutumnWeeks)),"Spring":np.zeros(len(SpringWeeks))}
profileContact={"Autumn":np.zeros(len(AutumnWeeks)),"Spring":np.zeros(len(SpringWeeks))}
nDeadlines={"Autumn":np.zeros(len(AutumnWeeks),dtype=int),"Spring":np.zeros(len(SpringWeeks),dtype=int)}
nDeadlinesBig={"Autumn":np.zeros(len(AutumnWeeks),dtype=int),"Spring":np.zeros(len(SpringWeeks),dtype=int)}
dlGrid={"Autumn":{},"Spring":{}}

for wA,weekA in enumerate(AutumnWeeks):
    conTime=ContactTime[weekA].sum()
    if conTime>0:
        profileContact["Autumn"][wA] = profileContact["Autumn"][wA] + conTime
for wS,weekS in enumerate(SpringWeeks):
    conTime=ContactTime[weekS].sum()
    if conTime>0:
        profileContact["Spring"][wS] = profileContact["Spring"][wS] + conTime

for a,assess in AssessDates.iterrows():
    mod = assess["Module Code"]
    modCredits = Modules["Credits"][Modules["Module Code"]==mod].values[0]
    assSum=assess["Summative"]
    assCore=assess["Core"]
    assessType=assess["CA type"]
    assessName=assess["Description"]
    for wA in range(len(AutumnWeeks)):
        weekA=AutumnWeeks[wA]
        assessTime = assess[weekA] * modCredits*4
        if assessTime>0:
            if np.isfinite(assess["Hours"]):
                assessTime = assess["Hours"]
            assessWeeks = assess["Duration"]
            wR=np.arange(wA-assessWeeks,wA)+1
            wX0=np.min(wR)
            if assSum=="Y":
                nDeadlines["Autumn"][wA] = nDeadlines["Autumn"][wA] + 1
                if assessTime>=1:
                    nDeadlinesBig["Autumn"][wA] = nDeadlinesBig["Autumn"][wA] + 1
                if not mod in dlGrid["Autumn"]:
                    dlGrid["Autumn"][mod]={"grid":{},"semester":Modules["Semester"][Modules["Module Code"]==mod].values[0]}
                if not a in dlGrid["Autumn"][mod]["grid"]:
                    dlGrid["Autumn"][mod]["grid"][a]={"type":assessType,"name":assessName,"duration":assessWeeks,"weeks":[],"weights":[]}
                dlGrid["Autumn"][mod]["grid"][a]["weeks"].append(wA+1)
                dlGrid["Autumn"][mod]["grid"][a]["weights"].append(assess[weekA])
            if profileSel=="Delta":
                profileAssess["Autumn"][wA] = profileAssess["Autumn"][wA] + assessTime
                if assCore:
                    profileAssessCore["Autumn"][wA] = profileAssessCore["Autumn"][wA] + assessTime
            elif profileSel=="Dist":
                for wX in wR:
                    profileAssess["Autumn"][wX] = profileAssess["Autumn"][wX] + assessTime/assessWeeks
                    if assCore:
                        profileAssessCore["Autumn"][wX] = profileAssessCore["Autumn"][wX] + assessTime/assessWeeks
            elif profileSel=="Linear":       
                for wX in wR:
                    profileAssess["Autumn"][wX] = profileAssess["Autumn"][wX] + assessTime*(2*(wX-wX0+1)-1)/assessWeeks**2
                    if assCore:
                        profileAssessCore["Autumn"][wX] = profileAssessCore["Autumn"][wX] + assessTime*(2*(wX-wX0+1)-1)/assessWeeks**2
    for wS in range(len(SpringWeeks)):
        weekS=SpringWeeks[wS]
        # if AssessDates.loc[a,"Hours"]
        assessTime = assess[weekS] * modCredits*4
        if assessTime>0:
            if np.isfinite(assess["Hours"]):
                assessTime = assess["Hours"]
            assessWeeks = assess["Duration"]
            wR=np.arange(wS-assessWeeks,wS)+1
            wX0=np.min(wR)
            if assSum=="Y":
                nDeadlines["Spring"][wS] = nDeadlines["Spring"][wS] + 1
                if assessTime>=1:
                    nDeadlinesBig["Spring"][wS] = nDeadlinesBig["Spring"][wS] + 1
                if not mod in dlGrid["Spring"]:
                    dlGrid["Spring"][mod]={"grid":{},"semester":Modules["Semester"][Modules["Module Code"]==mod].values[0]}
                if not a in dlGrid["Spring"][mod]["grid"]:
                    dlGrid["Spring"][mod]["grid"][a]={"type":assessType,"name":assessName,"duration":assessWeeks,"weeks":[],"weights":[]}
                dlGrid["Spring"][mod]["grid"][a]["weeks"].append(wS+1)
                dlGrid["Spring"][mod]["grid"][a]["weights"].append(assess[weekS])
            if profileSel=="Delta":
                profileAssess["Spring"][wS] = profileAssess["Spring"][wS] + assessTime
                if assCore:
                    profileAssessCore["Spring"][wS] = profileAssessCore["Spring"][wS] + assessTime
            elif profileSel=="Dist":
                for wX in wR:
                    profileAssess["Spring"][wX] = profileAssess["Spring"][wX] + assessTime/assessWeeks
                    if assCore:
                        profileAssessCore["Spring"][wX] = profileAssessCore["Spring"][wX] + assessTime/assessWeeks
            elif profileSel=="Linear":       
                for wX in wR:
                    profileAssess["Spring"][wX] = profileAssess["Spring"][wX] + assessTime*(2*(wX-wX0+1)-1)/assessWeeks**2
                    if assCore:
                        profileAssessCore["Spring"][wX] = profileAssessCore["Spring"][wX] + assessTime*(2*(wX-wX0+1)-1)/assessWeeks**2

# st.stop()

semesters=["Autumn","Spring"]

if not showAllMods:
    # fig=plt.figure(figsize=(12,9),num=1)
    fig,axes=plt.subplots(2,2,figsize=(8,8))
    x_values=np.arange(0.5,13)
    x_ticks=np.arange(1,13)
    maxD=np.max([np.max(nDeadlines["Autumn"]),np.max(nDeadlines["Spring"])])+1
    y_ticksN=np.arange(0,maxD+1,1,dtype=int)
    
    for s,sem in enumerate(semesters):
        dataContact=profileContact[sem]
        y_Contact=np.concatenate([[dataContact[0]],dataContact])
        dataAssess=profileAssess[sem]
        y_Assess=np.concatenate([[dataAssess[0]],dataAssess])
        dataAssessCore=profileAssessCore[sem]
        y_AssessCore=np.concatenate([[dataAssessCore[0]],dataAssessCore])

        ax=axes[0,s]
        ax.plot(x_values,y_Assess+y_Contact,"b",drawstyle="steps-pre",label="Total Workload")
        ax.fill_between(x_values,y_Assess+y_Contact,color="b",alpha=0.3,step="pre")
        # ax.plot(x_values,y_AssessCore+y_Contact,"r",drawstyle="steps-pre",label="Core Workload")
        ax.plot(x_values,y_Contact,"k",linestyle=":",drawstyle="steps-pre",label="Contact Time")
        

        # y_text=dataAssess + dataContact + 1
        # for t in range(len(nDeadlines[sem])):
        #     ax.annotate(nDeadlines[sem][t],(t+1,y_text[t]),ha="center")
        ax.grid(True, axis='y', linestyle='--', color='grey', alpha=0.6)
        ax.set_xticks(x_ticks)
        ax.set_ylim(0,50)
        ax.set_xlim(0.5,12.5)
        # ax.set_xlabel(f"{sem} Semester Week")
        ax.set_ylabel("Workload (Hours)")
        if s==0:
            ax.legend(loc="upper left")
            ax.axvline(11.5,color="gray",lw=6,alpha=0.5)
            ax.annotate("Vacation",(11.75,ax.get_ylim()[1]),rotation="vertical",va="top")
        if s==1:
            eW=easterWeeks[academicYear]+0.5
            ax.axvline(eW,color="gray",lw=6,alpha=0.5)
            ax.annotate("Vacation",(eW+0.25,ax.get_ylim()[1]),rotation="vertical",va="top")
                        
        dataNDeadlines=nDeadlines[sem]
        y_NDeadlines=np.concatenate([[dataNDeadlines[0]],dataNDeadlines])
        dataNDeadlinesBig=nDeadlinesBig[sem]
        y_NDeadlinesBig=np.concatenate([[dataNDeadlinesBig[0]],dataNDeadlinesBig])
        axN=axes[1,s]
        axN.plot(x_values,y_NDeadlines,"g",drawstyle="steps-pre",label="All Deadlines")
        axN.fill_between(x_values,y_NDeadlines,color="g",alpha=0.3,step="pre")
        axN.plot(x_values,y_NDeadlinesBig,"r",drawstyle="steps-pre",label="Deadlines (1 Hour+)")
        axN.fill_between(x_values,y_NDeadlinesBig,color="r",alpha=0.3,step="pre")
        axN.grid(True, axis='y', linestyle='--', color='grey', alpha=0.6)
        axN.set_xticks(x_ticks)
        axN.set_xlim(0.5,12.5)
        axN.set_ylim(0,maxD)
        axN.set_yticks(y_ticksN)
        axN.set_xlabel(f"{sem} Semester Week")
        axN.set_ylabel("# Deadlines")
        if s==0:
            axN.legend(loc="upper left")
            axN.axvline(11.5,color="gray",lw=6,alpha=0.5)
            axN.annotate("Vacation",(11.75,axN.get_ylim()[1]),rotation="vertical",va="top")
        if s==1:
            eW=easterWeeks[academicYear]+0.5
            axN.axvline(eW,color="gray",lw=6,alpha=0.5)
            axN.annotate("Vacation",(eW+0.25,axN.get_ylim()[1]),rotation="vertical",va="top")

    plt.tight_layout(rect=[0, 0, 1, 0.9])
    st.pyplot(fig)

# st.write(dlGrid)

if showAllProgs:
    title=f"All Deadlines for {studentCourseType} student in Year {studentYear} (all modules)"
elif showAllMods:
    title=f"All Deadlines for {studentCourseType} {studentCourse} student in Year {studentYear} (all modules)"
else:
    title=f"Deadlines for {studentCourseType} {studentCourse} student in Year {studentYear}"

nMods=len(selMod)
if nMods>20:
    figh=20
if nMods>10:
    figh=15
else:
    figh=8

figh={"Autumn":len(dlGrid["Autumn"].keys()),"Spring":len(dlGrid["Spring"].keys())}
# figG,axesG=plt.subplots(2,1,figsize=(8,figh))
figG=[]
axesG=[]
figGA=plt.figure(figsize=(8,figh["Autumn"]),edgecolor='k',frameon=True)
figG.append(figGA)
axesG.append(plt.gca())
figGS=plt.figure(figsize=(8,figh["Spring"]))
figG.append(figGS)
axesG.append(plt.gca())

assessColours=[]
assessTypes=set()
available_colors = ['red', 'blue', 'green', 'purple', 'orange', 'cyan', 'magenta', 'yellow', 'black']
col_idx=0
for s,sem in enumerate(semesters):
    for m,mod in enumerate(dlGrid[sem].keys()):
        for a,an in enumerate(dlGrid[sem][mod]["grid"].keys()):
            aType=dlGrid[sem][mod]["grid"][an]["type"]
            if aType not in assessTypes:
                assessTypes.add(aType)
                assessColours.append(available_colors[col_idx % len(available_colors)])
                col_idx +=1

def weight2sizecolorlabel(w):
    if w<=0.05:
        return {'ms':25,'ec':'blue','lw':1,'fc':'white','lab':"<5%"}
    elif w<=0.1:
        return {'ms':30,'ec':'green','lw':0,'fc':'green','lab':"5-10%"}
    elif w<=0.3:
        return {'ms':80,'ec':'red','lw':1,'fc':'white','lab':"10-30%"}
    else:
        return {'ms':100,'ec':'red','lw':0,'fc':'red','lab':">30%"}

assessSeen={"Autumn":set(),"Spring":set()}
handles={}
labels={}
for s,sem in enumerate(semesters):
    axG=axesG[s]
    yticks=[]
    ylabels=[]
    mods=list(dlGrid[sem].keys())
    mods.sort(key=lambda x:dlGrid[sem][x]["semester"])
    for m,mod in enumerate(mods):
        nassess=len(dlGrid[sem][mod]["grid"])
        for a,an in enumerate(dlGrid[sem][mod]["grid"].keys()):
            aType=dlGrid[sem][mod]["grid"][an]["type"]
            aName=dlGrid[sem][mod]["grid"][an]["name"]
            if type(aName)==float:
                aName="CA"
            color=assessColours[list(assessTypes).index(aType)]
            yass=m-0.5+(a+1)/(nassess+1)
            yplot=[yass]*len(dlGrid[sem][mod]["grid"][an]["weeks"])
            weights=dlGrid[sem][mod]["grid"][an]["weights"]
            sizes=[]
            edgecolors=[]
            facecolors=[]
            linewidths=[]
            labs=[]
            for w,wt in enumerate(weights):
                sizes.append(weight2sizecolorlabel(wt)["ms"])
                edgecolors.append(weight2sizecolorlabel(wt)["ec"])
                facecolors.append(weight2sizecolorlabel(wt)["fc"])
                linewidths.append(weight2sizecolorlabel(wt)["lw"])
                labs.append(weight2sizecolorlabel(wt)["lab"])
            # st.write(m,mod,nassess,a,dlGrid[sem][mod]["grid"][an]["type"],yass[0],len(dlGrid[sem][mod]["grid"][an]["weeks"]))
            axG.scatter(dlGrid[sem][mod]["grid"][an]["weeks"],yplot,s=np.array(sizes),
                        edgecolor=edgecolors,facecolor=facecolors,linewidth=linewidths)
            yticks.append(yass)
            ylabels.append(aName)
        axG.text(-2,m,mod,ha="center",va="center",rotation="vertical",fontsize=10)
    # st.write('types',assessTypes,'colors',assessColours)
    # axG.set_yticks(np.arange(len(mods)))
    # axG.set_yticklabels(mods)
    axG.set_yticks(yticks)
    axG.set_yticklabels(ylabels,fontsize=8)
    axG.set_ylim(-0.5,len(mods)-0.5)
    axG.set_xlabel(f"{sem} Semester Week")
    axG.set_xticks(np.arange(13))
    axG.set_xlim(0.5,12.5)
    # axG.legend(loc="upper left")
    # st.write(type(axG))
    handles[sem],labels[sem]=axG.get_legend_handles_labels()
    
    if s==0:
        axG.axvline(11.5,color="gray",lw=6,alpha=0.5)
        # axG.annotate("Vacation",(11.625,axG.get_ylim()[0]),rotation="vertical",va="top")
    if s==1:
        eW=easterWeeks[academicYear]+0.5
        axG.axvline(eW,color="gray",lw=6,alpha=0.5)
        # axG.annotate("Vacation",(eW+0.125,axG.get_ylim()[0]),rotation="vertical",va="top")

    axG.invert_yaxis()
    axG.tick_params(axis="both",length=0)
    axG.set_title(f"{title}\n{sem} Semester")
    
    # Create grid lines
    axGx=axG.twiny()
    axGx.set_xticks(np.arange(0.5,12.5))
    axGx.set_xticklabels([])
    axGx.grid(True, axis='x', linestyle='--', color='grey', alpha=0.6)
    axGx.set_xlim(axG.get_xlim()[0],axG.get_xlim()[1])
    axGx.tick_params(axis="both",length=0)
    axGy=axG.twinx()
    axGy.set_yticks(np.arange(0.5,len(mods)+0.5))
    axGy.set_yticklabels([])
    axGy.set_ylim(axG.get_ylim()[0],axG.get_ylim()[1])
    axGy.grid(True, axis='y', linestyle='--', color='grey', alpha=0.6)
    axGy.tick_params(axis="both",length=0)
    
    # Create manual legend
    legendWeights=[0.05,0.1,0.3,0.5]
    legendMarkers=[]
    for w,wt in enumerate(legendWeights):
        size=weight2sizecolorlabel(wt)["ms"]
        edgecolor=weight2sizecolorlabel(wt)["ec"]
        facecolor=weight2sizecolorlabel(wt)["fc"]
        linewidth=weight2sizecolorlabel(wt)["lw"]
        lab=weight2sizecolorlabel(wt)["lab"]
        legendMarkers.append(axG.scatter(0.5,0.5,s=size,
                            label=lab,edgecolor=edgecolor,facecolor=facecolor,linewidth=linewidth))
    axesG[s].legend(loc='upper right',bbox_to_anchor=(1.25,1),title="Weighting")
    for l,lm in enumerate(legendMarkers):
        lm.remove()

    axesG[s].set_position([0,0,0.8,figh[sem]/(figh[sem]+1)])
    st.pyplot(figG[s])

# # Old method for legends
# unique_handles = []
# unique_labels = []
# seen_labels = set()
# allHandles=handles["Autumn"]+handles["Spring"]
# allLabels=labels["Autumn"]+labels["Spring"]
# for handle, label in zip(allHandles, allLabels):
#     if label not in seen_labels:
#         unique_handles.append(handle)
#         unique_labels.append(label)
#         seen_labels.add(label)
# plt.tight_layout(rect=[0.1, 0, 1, 0.9])

# for s,sem in enumerate(semesters):
    # axesG[s].legend(handles=unique_handles, labels=unique_labels,loc='upper right',bbox_to_anchor=(1.25,1),title="Weighting")
    # figG[s].subplots_adjust(right=0.8,top=0.9)
    # axesG[s].set_position([0,0,0.8,figh[sem]/(figh[sem]+1)])
    # figG[s].patches.extend([plt.Rectangle((0, 0), 1, 1, fill=None, edgecolor='red',transform=figG[s].transFigure)])
    # figG[s].patches.extend([plt.Rectangle((0, 0), 0.8, figh[sem]/(figh[sem]+1), fill=None, edgecolor='blue',transform=figG[s].transFigure)])
    # st.pyplot(figG[s])

st.stop()

