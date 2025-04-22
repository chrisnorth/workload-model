import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
plt.ion()
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
import streamlit as st

def year2level(year,yrtype="UG"):
    if yrtype=="PG":
        return 7
    else:
        return year+3

# Set student properties
academicYears=["2024/5","2025/6","2026/7"]
filenames={"2024/5":"AssessmentSchedule_2425.xlsx","2025/6":"AssessmentSchedule_2526.xlsx","2026/7":"AssessmentSchedule_2627.xlsx"}
coursetypes=["UG","PG"]
courses={"UG":["Physics","Astrophysics","Physics with Astronomy","Medical Physics"],"PG":["Physics", "Astrophysics", "Compound Semiconductor Physics"]}
years=[1,2,3,4]

columns={"UG":{"Physics":"Physics","Astrophysics":"Astro","Physics with Astronomy":"PhysAstro","Medical Physics":"MedPhys"},
         "PG":{"Physics":"MScPhysics", "Astrophysics":"MScAstro","Compound Semiconductor Physics":"MScCSPhysics"}}

st.header("Select your year and course")
academicYear = st.radio("Select your programme type:",academicYears)
studentCourseType = st.radio("Select your programme type:",coursetypes)
studentCourse = st.radio("Select your programme:",courses[studentCourseType])
if studentCourseType=="UG":
    studentYear = st.radio("Select your year of study:",years)
else:
    studentYear=1
colName=columns[studentCourseType][studentCourse]

studentLevel=year2level(studentYear,studentCourseType)
st.write(f"**You are a {studentCourseType} {studentCourse} student in Year {studentYear} (Level {studentLevel}) of study**")
# st.info(f"column {colName}")
# st.stop()
# Set core modules
fileIn=filenames[academicYear]
Modules=pd.read_excel(fileIn,"Modules")
coreMods=Modules[(Modules[colName]=="C")&(Modules["Level"]==studentLevel)&(Modules["Source"]==studentCourseType[0])&(Modules["Credits"]>0)]

coreCredits=coreMods["Credits"].sum()
coreCreditsAutumn=coreMods[coreMods["Semester"]=="SEM1"]["Credits"].sum()+coreMods[coreMods["Semester"]=="SEMD"]["Credits"].sum()/2
coreCreditsSpring=coreMods[coreMods["Semester"]=="SEM2"]["Credits"].sum()+coreMods[coreMods["Semester"]=="SEMD"]["Credits"].sum()/2

optCreditsAvail=120-coreCredits

optMods=Modules[(Modules[colName]=="O")&(Modules["Level"]==studentLevel)&(Modules["Source"]==studentCourseType[0])&(Modules["Credits"]>0)]
st.divider()
st.header("Module Selection")
if coreCredits==120:
    st.write("You have no optional selections to make.")
    optModSelCode=[]
else:
    st.write("Your core modules are:",coreMods[["Module Code","Module Title","Semester","Credits","Exam Weight (%)"]].to_html(index=False),unsafe_allow_html=True)
    # st.subheader("Select Optional Modules")
    st.write("Core module credits (Autumn):",int(coreCreditsAutumn))
    st.write("Core module credits (Spring):",int(coreCreditsSpring))
    st.subheader("Optional module selection")
    st.write("Remaining optional credits:",optCreditsAvail)
    st.write("Please consult SIMS for any further conditions of module selection.")
    # st.write("Optional modules",optMods[["Module Code","Module Title","Semester","Credits","Exam Weight (%)"]].to_html(index=False),unsafe_allow_html=True)
    
    # Select Autumn modules
    optModListSEM1=optMods[optMods["Semester"]=="SEM1"]["Module Code"].to_list()
    if len(optModListSEM1)>0:
        st.write("Optional modules (Autumn Semester)",optMods[optMods["Semester"]=="SEM1"][["Module Code","Module Title","Semester","Credits","Exam Weight (%)"]].to_html(index=False),unsafe_allow_html=True)
        optModSelCodeSEM1=st.multiselect("Select your Autumn Semester optional modules:",optModListSEM1)
    else:
        optModSelCodeSEM1=[]
    optCreditSelSEM1=optMods[optMods["Module Code"].isin(optModSelCodeSEM1)]["Credits"].sum()
    autumnCredits=optCreditSelSEM1 + coreCreditsAutumn
    st.write("Autumn semester credits:",int(autumnCredits))


    # Select Spring modules
    optModListSEM2=optMods[optMods["Semester"]=="SEM2"]["Module Code"].to_list()
    if len(optModListSEM2)>0:
        st.write("Optional modules (Spring Semester)",optMods[optMods["Semester"]=="SEM2"][["Module Code","Module Title","Semester","Credits","Exam Weight (%)"]].to_html(index=False),unsafe_allow_html=True)
        optModSelCodeSEM2=st.multiselect("Select your Spring Semester optional modules:",optModListSEM2)
    else:
        optModSelCodeSEM2=[]
    optCreditSelSEM2=optMods[optMods["Module Code"].isin(optModSelCodeSEM2)]["Credits"].sum()
    springCredits=optCreditSelSEM2 + coreCreditsSpring
    st.write("Spring semester credits:",int(springCredits))

    optModSelCode = optModSelCodeSEM1 + optModSelCodeSEM2

optCreditSel=optMods[optMods["Module Code"].isin(optModSelCode)]["Credits"].sum()

optModSel=optMods[optMods["Module Code"].isin(optModSelCode)]
coreModList=coreMods["Module Code"].to_list()
selModList=optModSelCode + coreModList
selMod=Modules[Modules["Module Code"].isin(selModList)].rename(columns={colName:"Core/Optional"})
autumnCredits=int(selMod[selMod["Semester"]=="SEM1"]["Credits"].sum()+selMod[selMod["Semester"]=="SEMD"]["Credits"].sum()/2)
springCredits=int(selMod[selMod["Semester"]=="SEM2"]["Credits"].sum()+selMod[selMod["Semester"]=="SEMD"]["Credits"].sum()/2)
selCredits=autumnCredits + springCredits

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


st.divider()

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

# fig=plt.figure(figsize=(12,9),num=1)
fig,axes=plt.subplots(2,2,figsize=(8,8))
x_values=np.arange(0.5,13)
x_ticks=np.arange(1,13)
maxD=np.max([np.max(nDeadlines["Autumn"]),np.max(nDeadlines["Spring"])])+1
y_ticksN=np.arange(0,maxD+1,1,dtype=int)
semesters=["Autumn","Spring"]
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


# handles, labels = ax.get_legend_handles_labels()
# handlesN, labelsN = axN.get_legend_handles_labels()
# nText='# = Weekly deadlines'
# annotation_patch = mpatches.Patch(facecolor='none', edgecolor='none', label=nText)
# handles.append(annotation_patch)
# labels.append(nText)
plt.tight_layout(rect=[0, 0, 1, 0.9])
# fig.subplots_adjust(top=0.90)
# fig.legend(handles+handlesN, labels+labelsN, loc='upper center', bbox_to_anchor=(0.5, 0.95),ncol=len(labels))
st.pyplot(fig)

st.stop()

