import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
plt.ion()
import datetime
from joypy import joyplot
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches

filterEB=False
checkAssess=False
# # Filter list of students if required
if filterEB:
    print('Reading datafile')
    df=pd.read_excel('student-data/Exam Board Report (Data).xlsx',sheet_name="Progression")

    # Step 1: Filter for academic year 2024/5
    df_2024 = df[df["AYR Academic Year"] == "2024/5"]

    # Step 2: Drop duplicate student-module combinations
    unique_modules = df_2024.drop_duplicates(subset=["SCE Student Course Join Code", "MOD Module code"])

    # Step 3: Group by student and sum unique credits
    credits_by_student = unique_modules.groupby("SCE Student Course Join Code")["SMR Credits Attempted"].sum().reset_index()
    credits_by_student = credits_by_student.rename(columns={"SMR Credits Attempted": "Total Unique Module Credits"})

    # Step 4: Filter to students with exactly 120 credits
    students_with_120 = credits_by_student[credits_by_student["Total Unique Module Credits"] == 120]

    # Step 5: Filter original unique_modules to include only these students
    filtered_students_df = unique_modules[unique_modules["SCE Student Course Join Code"].isin(students_with_120["SCE Student Course Join Code"])]

    # Step 6: Keep only the required columns
    columns_to_keep = [
        "CBK Course Block Course Code",
        "CBK Exam Board Code (UDF1)",
        "SCE Student Course Join Code",
        "PRG Programme code",
        "MOD Module code",
        "SMR Core or Optional Status Code"
    ]
    columns_to_keep = {
        "CBK Course Block Course Code": "Course Code",
        "CBK Exam Board Code (UDF1)": "Exam Board",
        "SCE Student Course Join Code": "Student ID",
        "PRG Programme code": "Programme",
        "MOD Module code": "Module Code",
        "SMR Core or Optional Status Code":"Module Status"
    }
    final_df = filtered_students_df[list(columns_to_keep.keys())].rename(columns=columns_to_keep)

    # Optional: Save to file
    final_df.to_excel("Student Module Enrolments.xlsx", index=False)

StudentModules = pd.read_excel("Student Module Enrolments.xlsx")

# Function to categorize course codes
def categorize_course(code):
    if pd.isna(code):
        return "Unknown"
    if "PSC" in code:
        return "Physics"
    elif "PMP" in code:
        return "MedPhys"
    elif "AST" in code or "PAS" in code:
        return "Astro"
    elif "MSP" in code:
        return "Physics"
    elif "MSA" in code:
        return "Astro"
    elif "MS" in code:
        return "OtherMSc"
    else:
        return "Other"

def categorize_year(eb):
    if pd.isna(eb):
        return "Unknown"
    if eb=="U1PHYSX":
        return "UG Year 1"
    elif eb=="U2PHYSX":
        return "UG Year 2"
    elif eb=="UFPHYSX":
        return "UG Year 3"
    elif eb=="UFPHYSXA":
        return "UG Year 4"
    elif eb=="PGPHYSX1":
        return "MSc"
    else:
        return "Other"

# Apply course category
StudentModules["Course Category"] = StudentModules["Course Code"].apply(categorize_course)
StudentModules["Year"] = StudentModules["Exam Board"].apply(categorize_year)

# Group by Exam Board and Course Category, and count unique students
StudentGroups = StudentModules.groupby(["Year", "Course Category"])["Student ID"].nunique().reset_index()
StudentGroups = StudentGroups.rename(columns={"Student ID": "Number of Students"})

module_counts = StudentModules.groupby("Module Code")["Student ID"].nunique().reset_index()
module_counts = module_counts.rename(columns={"Student ID": "Number of Students"})
module_counts.to_excel("module_student_counts.xlsx", index=False)


if checkAssess:
    
    Modules=pd.read_excel('AssessmentSchedule_2425.xlsx',"Modules")
    
    ### Code to add PGT modules
    # nMod=len(Modules)
    # Modules["AssessTotal"]=[0]*len(Modules)

    # # Step 1: Filter modules with an MSc entry
    # msc_entries = Modules[Modules["MSc"].notna()].copy()

    # # Step 2: Create duplicated rows
    # msc_clones = msc_entries.copy()
    # msc_clones["Alternative Module Code"] = msc_clones["Module Code"]  # Keep original code
    # msc_clones["Module Code"] = msc_clones["MSc"]                   # Replace with MSc value
    # msc_clones["Level"] = 7                                         # Set Level to 7
    # msc_clones["Source"] = "P"                                      # Tag as MSc-added

    # # Step 3: Prepare original modules
    # original_trimmed = Modules.drop(columns=["MSc"]).copy()
    # original_trimmed["Alternative Module Code"] = None
    # original_trimmed["Source"] = "U"  # Tag as original

    # # Step 4: Drop MSc column from clones
    # msc_clones = msc_clones.drop(columns=["MSc"])

    # # Step 5: Combine both
    # Modules = pd.concat([original_trimmed, msc_clones], ignore_index=True)

    # # Optional: Save to Excel
    # Modules.to_excel("modules_with_msc_and_source_flag.xlsx", index=False)


    AssessDates=pd.read_excel('AssessmentSchedule_2425.xlsx',"Assessments")
    AssessDates.fillna(0)
    # Add sub-total column
    weeks=[]
    for a in AssessDates:
        if a.find('Week')>=0:
            weeks.append(a)

    AssessDates['Sub-total']=AssessDates[weeks].sum(axis=1)

    # Optional: Save to Excel
    updated_assessments.to_excel("assessments_with_msc_duplicates.xlsx", index=False)
    
    

    # Check tot assessment weight adds up
    
    for m in range(len(Modules)):
        mod=Modules["Module Code"][m]
        idx=np.where(AssessDates["Module Code"]==mod)
        # print(mod,idx)
        # print(AssessDates["Module Code"][idx[0]])
        # print(AssessDates["Sub-total"][idx[0]])
        # print(AssessDates["Sub-total"][idx[0]].sum(axis=0)*100)
        Modules.loc[Modules["Module Code"]==mod,"AssessTotal"]=AssessDates.loc[AssessDates["Module Code"]==mod,"Sub-total"].sum(axis=0)*100
    xltemp=pd.ExcelWriter('Assessments_temp.xlsx')
    Modules.to_excel(xltemp,"Modules",index=False)
    AssessDates.to_excel(xltemp,"Assessments",index=False)
    xltemp.close()


else:
    Modules=pd.read_excel('AssessmentSchedule_2425.xlsx',"Modules")
    AssessDates=pd.read_excel('AssessmentSchedule_2425.xlsx',"Assessments")
    AssessDates.fillna(0)   

ContactTime=pd.read_excel('AssessmentSchedule_2425.xlsx',"ContactTime")
ContactTime.fillna(0)
    
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
    original_assessments = AssessDates[AssessDates["Module Code"] == original_code].copy()

    if not original_assessments.empty:
        # Replace Module Code with MSc Module Code
        original_assessments["Module Code"] = msc_code
        msc_assessments = pd.concat([msc_assessments, original_assessments], ignore_index=True)

# Step 3: Append the MSc assessments to the original table
AssessDates = pd.concat([AssessDates, msc_assessments], ignore_index=True)
# AssessDates.to_excel("assessments_with_msc_duplicates.xlsx", index=False)


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

profileDelta={"Y1":{},"Y2":{},"Y3":{},"Y4":{}}
profileDist={"Y1":{},"Y2":{},"Y3":{},"Y4":{}}
profileContact={"Y1":{},"Y2":{},"Y3":{},"Y4":{}}
profileLin={"Y1":{},"Y2":{},"Y3":{},"Y4":{}}
nDeadlines={"Y1":{},"Y2":{},"Y3":{},"Y4":{}}
courses={"Physics":{"filter":{"Physics":"C"}},
         "Astro":{"filter":{"Astro":"C"}},
         "MedPhys":{"filter":{"MedPhys":"C"}},
         "MScPhysics":{"filter":{"MScPhysics":"C"}},
         "MScAstro":{"filter":{"MScAstro":"C"}}
}
for y in profileDelta:
    for f in courses:
        profileDelta[y][f]={}
        profileDelta[y][f]["Autumn"]=np.zeros(len(AutumnWeeks))
        profileDelta[y][f]["Spring"]=np.zeros(len(SpringWeeks))
        profileDist[y][f]={}
        profileDist[y][f]["Autumn"]=np.zeros(len(AutumnWeeks))
        profileDist[y][f]["Spring"]=np.zeros(len(SpringWeeks))
        profileLin[y][f]={}
        profileLin[y][f]["Autumn"]=np.zeros(len(AutumnWeeks))
        profileLin[y][f]["Spring"]=np.zeros(len(SpringWeeks))
        profileContact[y][f]={}
        profileContact[y][f]["Autumn"]=np.zeros(len(AutumnWeeks))
        profileContact[y][f]["Spring"]=np.zeros(len(SpringWeeks))
        nDeadlines[y][f]={}
        nDeadlines[y][f]["Autumn"]=np.zeros(len(AutumnWeeks),dtype=int)
        nDeadlines[y][f]["Spring"]=np.zeros(len(SpringWeeks),dtype=int)

def modType(mod,course):
    return Modules[course][Modules["Module Code"]==mod].item()

for c in range(len(ContactTime)):
    mod=ContactTime["Module Code"][c]
    modLevel = Modules["Level"][Modules["Module Code"]==mod].values[0]
    modYear=l2y(modLevel)
    for wA in range(len(AutumnWeeks)):
        weekA=AutumnWeeks[wA]
        conTime=ContactTime.loc[c,weekA].item()
        if conTime>0:
            for course in courses:
                if modType(mod,course)=="C":
                    profileContact[modYear][course]["Autumn"][wA] = profileContact[modYear][course]["Autumn"][wA] + conTime
    for wS in range(len(SpringWeeks)):
        weekS=SpringWeeks[wS]
        conTime=ContactTime.loc[c,weekS].item()
        if conTime>0:
            for course in courses:
                if modType(mod,course)=="C":
                    profileContact[modYear][course]["Spring"][wS] = profileContact[modYear][course]["Spring"][wS] + conTime

for a in range(len(AssessDates)):
    mod = AssessDates["Module Code"][a]
    modLevel = Modules["Level"][Modules["Module Code"]==mod].values[0]
    modCredits = Modules["Credits"][Modules["Module Code"]==mod].values[0]
    assSum=AssessDates.loc[a,"Summative"]
    # physChoice=Modules["Physics"][Modules["Module Code"]==mod].item()
    # astroChoice=Modules["Astro"][Modules["Module Code"]==mod].item()
    # medPhysChoice=Modules["MedPhys"][Modules["Module Code"]==mod].item()
    # MscPhysChoice=Modules["MScPhysics"][Modules["Module Code"]==mod].item()
    # MscAstroChoice=Modules["MScAstro"][Modules["Module Code"]==mod].item()
    assessType=AssessDates.loc[a,"CA type"]
    modYear=l2y(modLevel)
    for wA in range(len(AutumnWeeks)):
        weekA=AutumnWeeks[wA]
        assessTime = AssessDates.loc[a,weekA].item() * modCredits*4
        if assessTime>0:
            if np.isfinite(AssessDates.loc[a,"Hours"]):
                assessTime = AssessDates.loc[a,"Hours"].item()
            assessWeeks = AssessDates.loc[a,"Duration"].item()
            wR=np.arange(wA-assessWeeks,wA)+1
            wX0=np.min(wR)
            for course in courses:
                if modType(mod,course)=="C":
                    profileDelta[modYear][course]["Autumn"][wA] = profileDelta[modYear][course]["Autumn"][wA] + assessTime
                    if assSum=="Y":
                        nDeadlines[modYear][course]["Autumn"][wA] = nDeadlines[modYear][course]["Autumn"][wA] + 1
                    for wX in wR:
                        profileDist[modYear][course]["Autumn"][wX] = profileDist[modYear][course]["Autumn"][wX] + assessTime/assessWeeks
                        profileLin[modYear][course]["Autumn"][wX] = profileLin[modYear][course]["Autumn"][wX] + assessTime*(2*(wX-wX0+1)-1)/assessWeeks**2
    for wS in range(len(SpringWeeks)):
        weekS=SpringWeeks[wS]
        # if AssessDates.loc[a,"Hours"]
        assessTime = AssessDates.loc[a,weekS].item() * modCredits*4
        if assessTime>0:
            if np.isfinite(AssessDates.loc[a,"Hours"]):
                assessTime = AssessDates.loc[a,"Hours"].item()
            assessWeeks = AssessDates.loc[a]["Duration"].item()
            wR=np.arange(wS-assessWeeks,wS)+1
            wX0=np.min(wR)
            # linWork=(2 * (wR-np.min(wR)+1)-1)/len(wR)**2
            # if MscPhysChoice=="C":
            #     print(mod,modYear,weekS,assessType,assessTime,int(assessWeeks),assessTime/assessWeeks,wS,wR)
            for course in courses:
                if modType(mod,course)=="C":
                    profileDelta[modYear][course]["Spring"][wS] = profileDelta[modYear][course]["Spring"][wS] + assessTime
                    if assSum=="Y":
                        nDeadlines[modYear][course]["Spring"][wS] = nDeadlines[modYear][course]["Spring"][wS] + 1
                    for wX in wR:
                        profileDist[modYear][course]["Spring"][wX] = profileDist[modYear][course]["Spring"][wX] + assessTime/assessWeeks
                        profileLin[modYear][course]["Spring"][wX] = profileLin[modYear][course]["Spring"][wX] + assessTime*(2*(wX-wX0+1)-1)/assessWeeks**2

plots={"AutumnUG":{"num":1,"semester":"Autumn","cohort":"UG"},
       "SpringUG":{"num":2,"semester":"Spring","cohort":"UG"},
       "AutumnPG":{"num":3,"semester":"Autumn","cohort":"PG"},
       "SpringPG":{"num":4,"semester":"Spring","cohort":"PG"}
       }
for p in plots:
    if plots[p]["cohort"]=="UG":
        core_subjects = ['Physics', 'Astro', 'MedPhys']
        years = ['Y1', 'Y2', 'Y3', 'Y4']
    elif plots[p]["cohort"]=="PG":
        core_subjects = ['MScPhysics', 'MScAstro']
        years = ['Y4']
    if len(years)>1:
        figsize=(12,9)
    else:
        figsize=(12,6)
    fig=plt.figure(figsize=figsize,num=plots[p]["num"])
    fig.clf()
    fig,axes=plt.subplots(len(years),len(core_subjects),sharex=False,sharey=False,num=plots[p]["num"])
    fig.subplots_adjust(top=0.90)
    fig.suptitle(f'{plots[p]["semester"]} - {plots[p]["cohort"]}', fontsize=16)
    plots[p]["fig"]=fig
    plots[p]["axes"]=axes
    plots[p]["file"]=f"plots/{p}_core-workload.png"

    
    x_values=np.arange(0.5,13)
    x_ticks=np.arange(1,13)
    for px, year in enumerate(years):
        for py,subject in enumerate(core_subjects):
            if len(years)>1 and len(core_subjects)>1:
                ax=plots[p]["axes"][px,py]
            elif len(years)>1:
                ax=plots[p]["axes"][px]
            else:
                ax=plots[p]["axes"][py]
            
            dataContact=profileContact[year][subject][plots[p]["semester"]]
            y_Contact=np.concatenate([[dataContact[0]],dataContact])
            dataDelta=profileDelta[year][subject][plots[p]["semester"]]
            y_Delta=np.concatenate([[dataDelta[0]],dataDelta])
            dataDist=profileDist[year][subject][plots[p]["semester"]]
            y_Dist=np.concatenate([[dataDist[0]],dataDist])
            dataLin=profileLin[year][subject][plots[p]["semester"]]
            y_Lin=np.concatenate([[dataLin[0]],dataLin])
            ax.plot(x_values,y_Delta+y_Contact,"b",drawstyle="steps-pre",label="Last-minute Work")
            ax.fill_between(x_values,y_Delta+y_Contact,color="b",alpha=0.3,step="pre")
            ax.plot(x_values,y_Dist+y_Contact,"r",drawstyle="steps-pre",label="Distributed Work")
            ax.fill_between(x_values,y_Dist+y_Contact,color="r",alpha=0.3,step="pre")
            ax.plot(x_values,y_Lin+y_Contact,"g",drawstyle="steps-pre",label="Linearly Increase Work")
            ax.fill_between(x_values,y_Lin+y_Contact,color="g",alpha=0.3,step="pre")
            ax.plot(x_values,y_Contact,"k",linestyle=":",drawstyle="steps-pre",label="Contact Time")

            y_text=np.amax([dataDist,dataDelta,dataLin],axis=0) + dataContact + 1
            for t in range(len(nDeadlines[year][subject][plots[p]["semester"]])):
                ax.annotate(nDeadlines[year][subject][plots[p]["semester"]][t],(t+1,y_text[t]),ha="center")
            ax.text(0.02, 0.95, f'{subject} - {year}', transform=ax.transAxes, fontsize=10, verticalalignment='top')
            ax.set_xticks(x_ticks)
            ax.grid(True, axis='y', linestyle='--', color='grey', alpha=0.6)
            ax.set_ylim(0,50)
            ax.set_xlim(0.5,12.5)
            if px==len(years)-1:
                ax.set_xlabel("Week of Semester")
            if py==0:
                ax.set_ylabel(f"{year} workload (Hours)")
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    handles, labels = ax.get_legend_handles_labels()
    nText='# = Weekly deadlines'
    annotation_patch = mpatches.Patch(facecolor='none', edgecolor='none', label=nText)
    handles.append(annotation_patch)
    labels.append(nText)
    fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 0.95),ncol=len(labels))
    plt.show()
    plt.savefig(plots[p]["file"])

sadfsafs

### Cycle over students
years=["UG Year 1","UG Year 2","UG Year 3","UG Year 4","MSc"]
courses=["Physics","Astro","MedPhys"]
# years=["UG Year 4"]
# courses=["Astro"]

# cmap = cm.get_cmap('viridis',len(cohortWL[semester]))
cmap= plt.get_cmap('tab20')

fignum=5
studentWorkload={}
for year in years:
    for course in courses:
        studentWorkload[f'{course}:{year}']={"year":year,"course":course}
        cohortWL={}
        StudentModulesFilt = StudentModules[(StudentModules["Course Category"] == course) & (StudentModules["Year"] == year)]
        StudentList=StudentModulesFilt["Student ID"].unique().tolist()
        if len(StudentList)==0:
            print(f'skipping {course} {year}')
            continue
        else:
            print(f'plotting {course} {year}')

        cohortWL["studentList"]=[]
        cohortWL["Autumn"]=[]
        cohortWL["Spring"]=[]
        for stu in StudentList:
            cohortWL["studentList"].append(stu)
            stuModules = StudentModulesFilt[StudentModulesFilt["Student ID"] == stu]["Module Code"].dropna().unique().tolist()
            stuWLAutumn=[0]*len(AutumnWeeks)
            stuWLSpring=[0]*len(SpringWeeks)
            for mod in stuModules:
                if not mod in moduleList:
                    print(f'skipping {mod}')
                    continue
                modAssess=AssessDates[AssessDates["Module Code"]==mod].reset_index()
                modCredits = Modules["Credits"][Modules["Module Code"]==mod].values[0]
                for a in range(len(modAssess)):
                    for wA in range(len(AutumnWeeks)):
                        weekA=AutumnWeeks[wA]
                        assessTime = modAssess.loc[a,weekA].item() * modCredits*4
                        if assessTime>0:
                            if np.isfinite(modAssess.loc[a,"Hours"]):
                                assessTime = modAssess.loc[a,"Hours"].item()
                            assessWeeks = modAssess.loc[a,"Duration"].item()
                            wR=np.arange(wA-assessWeeks,wA)+1
                            # print(mod,weekA,assessTime,assessWeeks,wR)
                            for wX in wR:
                                stuWLAutumn[wX]=stuWLAutumn[wX] + assessTime/assessWeeks
                            # print(mod,weekA,assessTime,assessWeeks,wR,stuWLAutumn[wA])
                    for wS in range(len(SpringWeeks)):
                        weekS=SpringWeeks[wS]
                        assessTime = modAssess.loc[a,weekS].item() * modCredits*4
                        if assessTime>0:
                            if np.isfinite(modAssess.loc[a,"Hours"]):
                                assessTime = modAssess.loc[a,"Hours"].item()
                            assessWeeks = modAssess.loc[a,"Duration"].item()
                            wR=np.arange(wS-assessWeeks,wS)+1
                            for wX in wR:
                                stuWLSpring[wX]=stuWLSpring[wX] + assessTime/assessWeeks
            cohortWL["Autumn"].append(stuWLAutumn)
            cohortWL["Spring"].append(stuWLSpring)
        
        for semester in ["Autumn","Spring"]:
            ### Plot using 
            plt.figure(figsize=(12,9))
            plt.clf()
            plt.title(f"Weekly Workload {course} {year} ({semester})")
            ax=plt.gca()
            y_offset=20
            for s in range(len(cohortWL[semester])):
                dataDist=cohortWL[semester][s]
                y_Dist=np.concatenate([[dataDist[0]],dataDist]) + s*y_offset
                # ax.plot(x_values,y_Dist,"r",drawstyle="steps-pre",label="Distributed")
                x_Dist=np.arange(1,13)
                y_Dist=np.array(dataDist) + s*y_offset
                ax.plot(x_Dist,y_Dist,color=cmap(s % cmap.N))
            y_ticks_values=np.arange(0,len(cohortWL["studentList"]))*y_offset
            ax.set_yticks(y_ticks_values,cohortWL["studentList"])
            ax.set_xticks(x_ticks)
            plt.ylabel("Student")
            plt.xlabel(f"{semester} week")
            plt.show()
            plt.savefig(f'student-data/plots/{course}_{year}_{semester}.png')
            plt.close()


            # ## Plot using Joyplot
            # # Convert to DataFrame: rows = students, columns = weeks
            # pltDf=pd.DataFrame(cohortWL[semester],index=StudentList)
            # if semester=="Autumn":
            #     pltDf.columns=AutumnWeeks
            # elif semester=="Spring":
            #     pltDf.columns=SpringWeeks
            # # Melt the DataFrame so it's long-form: needed by joypy
            # df_long = pltDf.reset_index().melt(id_vars='index', var_name='Week', value_name='Workload')
            # df_long = df_long.rename(columns={'index': 'Student'})
            # # Create the ridgeline plot
            # fig, axes = joyplot(
            #     data=df_long,
            #     by="Student",
            #     column="Workload",
            #     fill=False,
            #     overlap=1,
            #     figsize=(9,9),
            #     linewidth=1.2,
            #     bw_method=0.1,  # Less smoothing
            #     colormap=plt.cm.viridis
            # )           

            # ax=plt.gca()
            # ax.grid(True, color='grey', linestyle='--', linewidth=0.5)
            # plt.xlim(0,12)
            # plt.xticks(np.arange(0,13))
            # plt.title(f"Weekly Workload {course} {year} ({semester})")
            # plt.ylabel("Student")
            # plt.xlabel(f"{semester} week")
            # plt.yticks([])
            # plt.subplots_adjust(top=0.95)
            # # plt.show()
            # plt.savefig(f'student-data/joyplots/{course}_{year}_{semester}.png')
            # plt.close()
