import numpy as np
import pandas as pd
import matplotlib as mpl
from matplotlib import pyplot as plt
plt.ion()
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
import streamlit as st
import os
from datetime import datetime, timedelta

def streamlit_cloud():
    """
    Checks if the Streamlit app is currently running on Streamlit Community Cloud.
    """
    # Streamlit Cloud sets the 'STREAMLIT_SERVER_PORT' environment variable
    # to a specific port (e.g., 8501).
    # When running locally, this variable might not be set or might be set differently.
    # Also, Streamlit Cloud often sets an environment variable like 'streamlit_cloud_config'.
    # st.write("HOSTNAME",os.environ.get("HOSTNAME"))
    # st.write("DEBUG os.environ",os.environ)
    return os.environ.get("HOSTNAME")=="streamlit"


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
if streamlit_cloud():
    st.info('Running on streamlit cloud.')
    academicYears=["2025/6"]
else:
    st.info('Running locally')
    academicYears=["2025/6","2024/5","2026/7 (TBC)"]
    # academicYears=["2025/6"]

easterWeeks={"2024/5":11,"2025/6":8,"2026/7 (TBC)":7}
startDates={"2024/5":{"Autumn":datetime(2024,9,30),"Spring":datetime(2025,1,27) },"2025/6":{"Autumn":datetime(2025,9,29),"Spring":datetime(2026,1,26)},"2026/7 (TBC)":{"Autumn":datetime(2026,10,5),"Spring":datetime(2027,2,1)}}
filenames={"2024/5":"AssessmentSchedule_2425.xlsx","2025/6":"AssessmentSchedule_2526_v2.xlsx","2026/7 (TBC)":"AssessmentSchedule_2627.xlsx"}
coursetypes=["UG","PG"]
courses={"UG":["Show modules for all programmes","Physics","Astrophysics","Physics with Astronomy","Medical Physics"],
         "PG":["Show modules for all programmes","Physics", "Astrophysics", "Data Intensive Physics", "Data Intensive Astrophysics","Compound Semiconductor Physics","CDT Compound Semiconductor Physics"]}
years=[1,2,3,4]

columns={"UG":{"Physics":"Physics","Astrophysics":"Astro","Physics with Astronomy":"PhysAstro","Medical Physics":"MedPhys","Show modules for all programmes":"AllUG"},
         "PG":{"Physics":"MScPhysics", "Astrophysics":"MScAstro",
               "Data Intensive Physics":"MScDataPhys",
               "Data Intensive Astrophysics":"MScDataAstro",
               "Compound Semiconductor Physics":"MScCSPhysics","CDT Compound Semiconductor Physics":"CDTCSPhysics",
               "Show modules for all programmes":"AllPG"}}



st.header("Select your year and course")
academicYear = st.radio("Select the academic year:",academicYears,index=0)
studentCourseType = st.radio("Select your programme type:",coursetypes)
if studentCourseType=="UG":
    studentYear = st.radio("Select your year of study:",years)
else:
    studentYear=1
studentCourse = st.radio("Select your programme:",courses[studentCourseType])
studentLevel=year2level(studentYear,studentCourseType)

if studentYear==4 and studentCourse=="Medical Physics":
    st.warning("ERROR: No Year 4 for Medical Physics")
    st.stop()

colName=columns[studentCourseType][studentCourse]
if studentCourse=="Show modules for all programmes":
    showAllProgs=True
    st.write(f"**Showing All modules for {studentCourseType} student in Year {studentYear} (Level {studentLevel}) of study**")
    st.write("If you would like to view your estimated workload profile, please select a specific course and (where appropriate), optional modules")
    shortCode=f'{academicYear.replace("/","-")}_{studentCourseType}_yr{studentYear}_All'
    if streamlit_cloud():
        savePlots="No"
    else:
        savePlots=st.radio("Save plots locally?",["Yes","No"],index=1)
else:
    showAllProgs=False
    st.write(f"**You are a {studentCourseType} {studentCourse} student in Year {studentYear} (Level {studentLevel}) of study**")
    shortCode=f'{academicYear.replace("/","-")}_{studentCourseType}_yr{studentYear}_{studentCourse}'
    savePlots="No"

# st.info(f"column {colName}")
# st.stop()
# Set core modules
fileIn=filenames[academicYear]
Modules=pd.read_excel(fileIn,"Modules")
try:
    if showAllProgs:
        coreMods=Modules[(Modules["Level"]==studentLevel)&(Modules["Source"]==studentCourseType[0])&(Modules["Credits"]>0)]
        coreModsAll=coreMods[coreMods[colName]=="C"]["Module Code"].to_list()
    else:
        coreMods=Modules[(Modules[colName]=="C")&(Modules["Level"]==studentLevel)&(Modules["Source"]==studentCourseType[0])&(Modules["Credits"]>0)]
        coreModsAll=coreMods[coreMods[colName]=="C"]["Module Code"].to_list()
except:
    st.error(f"ERROR reading data for {studentCourseType} {studentCourse} from {academicYear}")
    st.stop()

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

if not showAllProgs:
    showAllMods=st.checkbox("Show deadlines for all available modules?")
    if showAllMods:
        st.write("**Warning: workload calculations are not possible when selecting all modules.**")
else:
    showAllMods=True

if not showAllProgs and not showAllMods:
    st.subheader("Core modules")
    coreMods_display = coreMods.copy()
    coreMods_display["Semester"] = coreMods_display["Semester"].replace({"SEM1": "Autumn", "SEM2": "Spring", "SEMD": "Full Year"})
    coreMods_display["Exam Weight (%)"] = coreMods_display["Exam Weight (%)"].astype(int)  # Make integer

    st.write(coreMods_display[["Module Code","Module Title","Semester","Credits","Exam Weight (%)"]].to_html(index=False),unsafe_allow_html=True)
    # st.write("_SEM1=Autumn, SEM2=Spring, SEMD=Full Year_")

    # Create a DataFrame for display
    core_credits_df = pd.DataFrame({
        "Semester": ["Autumn", "Spring"],
        "Core Credits": [int(coreCreditsAutumn), int(coreCreditsSpring)],
        "# Core Exams": [nExamsAutumnCore, nExamsSpringCore]
    })

        
    st.write("Core Credits by Semester")
    st.write(core_credits_df.to_html(index=False),unsafe_allow_html=True)

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


    st.write("Total optional credits:",optCreditsAvail)
    st.write("Please consult SIMS, and the Module Catalogue for any further conditions of module selection.")
    # st.write("Optional modules",optMods[["Module Code","Module Title","Semester","Credits","Exam Weight (%)"]].to_html(index=False),unsafe_allow_html=True)
    
    optMods=Modules[(Modules[colName]=="O")&(Modules["Level"]==studentLevel)&(Modules["Source"]==studentCourseType[0])&(Modules["Credits"]>0)]
    

    # Select Autumn modules
    optModsSEM1 = optMods[optMods["Semester"]=="SEM1"]
    optModListSEM1_display = [f"{row['Module Code']} - {row['Module Title']}" for _, row in optModsSEM1.iterrows()]
    optModListSEM1_display.sort()  # Sort alphabetically by the display string
    optModListSEM1_codes = [item.split(" - ")[0] for item in optModListSEM1_display]  # Extract codes

    # st.write("Core module credits (Autumn):", int(coreCreditsAutumn))
    st.write("**Autumn Semester**")
    if len(optModListSEM1_display)>0:
        if showAllMods:
            optModSelCodeSEM1=optModListSEM1_codes
            st.write("**Showing all Autumn semester optional modules**")
        else:
            selected_display=st.multiselect("Select your Autumn Semester optional modules:",optModListSEM1_display)
            optModSelCodeSEM1 = [item.split(" - ")[0] for item in selected_display]  # Extract codes from selection
        
        optMods_display = optMods.copy()
        optMods_display["Selected"] = optMods_display["Module Code"].isin(optModSelCodeSEM1).map({True: "✔️", False: ""})
        optMods_display["Exam Weight (%)"] = optMods_display["Exam Weight (%)"].astype(int)  # Make integer
        st.write(optMods_display[optMods_display["Semester"]=="SEM1"][["Module Code", "Module Title", "Semester", "Credits", "Exam Weight (%)", "Selected"]].to_html(index=False), unsafe_allow_html=True)
        
        # st.write("Optional modules (Autumn Semester)",optMods[optMods["Semester"]=="SEM1"][["Module Code","Module Title","Semester","Credits","Exam Weight (%)"]].to_html(index=False),unsafe_allow_html=True)
    else:
        st.write("You have no optional selections to make for Autumn semester")
        optModSelCodeSEM1=[]
    optCreditSelSEM1=optMods[optMods["Module Code"].isin(optModSelCodeSEM1)]["Credits"].sum()
    autumnCredits=optCreditSelSEM1 + coreCreditsAutumn
    # st.write("Autumn semester credits:",int(autumnCredits))
    # st.write("Autumn semester exams:", nExamsAutumn)
    

    # Select Spring modules
    st.write("**Spring Semester**")
    optModsSEM2 = optMods[optMods["Semester"]=="SEM2"]
    optModListSEM2_display = [f"{row['Module Code']} - {row['Module Title']}" for _, row in optModsSEM2.iterrows()]
    optModListSEM2_display.sort()  # Sort alphabetically by the display string
    optModListSEM2_codes = [item.split(" - ")[0] for item in optModListSEM2_display]  # Extract codes
    # st.write("Core module credits (Spring):", int(coreCreditsSpring))
    if len(optModListSEM2_display)>0:
        if showAllMods:
            optModSelCodeSEM2=optModListSEM2_codes
            st.write("**Selecting all Spring semester optional modules**")
        else:
            selected_display=st.multiselect("Select your Spring Semester optional modules:",optModListSEM2_display)
            optModSelCodeSEM2 = [item.split(" - ")[0] for item in selected_display]  # Extract codes from selection
            
        optMods_display = optMods.copy()
        optMods_display["Selected"] = optMods_display["Module Code"].isin(optModSelCodeSEM2).map({True: "✔️", False: ""})
        optMods_display["Exam Weight (%)"] = optMods_display["Exam Weight (%)"].astype(int)  # Make integer
        st.write(optMods_display[optMods_display["Semester"]=="SEM2"][["Module Code", "Module Title", "Semester", "Credits", "Exam Weight (%)", "Selected"]].to_html(index=False), unsafe_allow_html=True)
        # st.write("**Spring Semester**",optMods[optMods["Semester"]=="SEM2"][["Module Code","Module Title","Semester","Credits","Exam Weight (%)"]].to_html(index=False),unsafe_allow_html=True)
    else:
        optModSelCodeSEM2=[]

    optCreditSelSEM2=optMods[optMods["Module Code"].isin(optModSelCodeSEM2)]["Credits"].sum()
    springCredits=optCreditSelSEM2 + coreCreditsSpring
    # st.write("Spring semester credits:",int(springCredits))
    # st.write("Spring semester exams:", nExamsSpring)
    optModSelCode = optModSelCodeSEM1 + optModSelCodeSEM2
optModSel=optMods[optMods["Module Code"].isin(optModSelCode)]        
optCreditSel=optMods[optMods["Module Code"].isin(optModSelCode)]["Credits"].sum()
selModList=optModSelCode + coreModList

selMod=Modules[Modules["Module Code"].isin(selModList)].rename(columns={colName:"Core/Optional"})
autumnCredits=int(selMod[selMod["Semester"]=="SEM1"]["Credits"].sum()+selMod[selMod["Semester"]=="SEMD"]["Credits"].sum()/2)
springCredits=int(selMod[selMod["Semester"]=="SEM2"]["Credits"].sum()+selMod[selMod["Semester"]=="SEMD"]["Credits"].sum()/2)
selCredits=autumnCredits + springCredits

if not showAllMods and not showAllProgs:
    st.subheader("**Selected credits**")
    all_credits_df = pd.DataFrame({
        "Semester": ["Autumn", "Spring"],
        "Credits": [autumnCredits, springCredits],
        "# Exams": [nExamsAutumn, nExamsSpring]
    })
    st.write(all_credits_df.to_html(index=False),unsafe_allow_html=True)

if not showAllMods:
    if optCreditSel<optCreditsAvail:
        st.error(f"⚠️ Please select {optCreditsAvail-optCreditSel} more optional credits.")
        st.stop()
    elif optCreditSel>optCreditsAvail:
        st.error(f"⚠️ ERROR: You can only select {optCreditsAvail} optional credits. {optCreditSel} selected")
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
    st.write("It assumes that all sessions with contact time are attended, and assessment workload is based on estimates, so are indicative only.")
    if selCredits!=120:
        st.write(f"⚠️ WARNING: Module choice is only based on {selCredits} credits.")
    profiles=["Delta","Dist","Linear"]
    profilesDesc=["Complete work in week of deadline","Distribute the work evenly over the full assessment duration","Gradually (linearly) increase work up to the deadline"]
    profileName=st.radio("How would you like to work?",profilesDesc,index=1)
    st.write("Actual workload depends on time management, with three 'models' available below. Assuming all work is before the deadline is distorted by large projects.")
    st.write("The 'assessment duration' is assumed to be from when it is set to when it is due, and measured in (integer) weeks. Reality will be somewhere between these three models.")
    for p,prof in enumerate(profilesDesc):
        if profileName==prof:
            profileSel=profiles[p]
else:
   st.write("If you select a specific programme and optional modules (if appropriate), then you will see an estimated workload profile based on contact time and assessment workload.")
   profileSel="Delta"


AssessDatesIn=pd.read_excel(fileIn,"Assessments")
AssessDatesIn.fillna(0)   

ContactTimeIn=pd.read_excel(fileIn,"ContactTime")
ContactTimeIn.fillna(0)
    
moduleList=Modules["Module Code"].values
### Add MSc modules to AssessDates and ContactTimeIn
# Step 1: Filter MSc-derived modules
msc_modules = Modules[(Modules["Source"] == "P") & (Modules["Alternative Module Code"].notna())]

# Step 2: Create duplicated assessment rows for each MSc module
msc_assessments = pd.DataFrame()
msc_contact = pd.DataFrame()

for _, row in msc_modules.iterrows():
    original_code = row["Alternative Module Code"]
    msc_code = row["Module Code"]

    # Find all assessment entries for the original module
    original_assessments = AssessDatesIn[AssessDatesIn["Module Code"] == original_code].copy()
    original_contact = ContactTimeIn[ContactTimeIn["Module Code"] == original_code].copy()

    if not original_assessments.empty:
        # Replace Module Code with MSc Module Code
        original_assessments["Module Code"] = msc_code
        original_contact["Module Code"] = msc_code
        msc_assessments = pd.concat([msc_assessments, original_assessments], ignore_index=True)
        msc_contact = pd.concat([msc_contact, original_contact], ignore_index=True)

# Step 3: Append the MSc assessments to the original table
AssessDatesAll = pd.concat([AssessDatesIn, msc_assessments], ignore_index=True)
ContactTimeIn = pd.concat([ContactTimeIn, msc_contact], ignore_index=True)
# AssessDates.to_excel("assessments_with_msc_duplicates.xlsx", index=False)

# Reduce to list of selected modules
AssessDates=AssessDatesAll[AssessDatesAll["Module Code"].isin(selModList)]
inCore=AssessDates["Module Code"].isin(coreModList)
AssessDates.loc[inCore,"Core"]=True
ContactTime=ContactTimeIn[ContactTimeIn["Module Code"].isin(selModList)]

hasDays="Day of Week" in AssessDates.columns

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
hasOldDeadline=False

# Track workload by CA type
nDeadlinesByType={"Autumn":{},"Spring":{}}
profileAssessByType={"Autumn":{},"Spring":{}}
caTypes=set()

# First pass: collect all CA types
for a,assess in AssessDates.iterrows():
    assessType = assess["CA type"]
    if pd.notna(assessType):
        caTypes.add(assessType)

# Initialize dictionaries for each CA type
for caType in caTypes:
    profileAssessByType["Autumn"][caType] = np.zeros(len(AutumnWeeks))
    profileAssessByType["Spring"][caType] = np.zeros(len(SpringWeeks))
    nDeadlinesByType["Autumn"][caType] = np.zeros(len(AutumnWeeks), dtype=int)
    nDeadlinesByType["Spring"][caType] = np.zeros(len(SpringWeeks), dtype=int)
    
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
    try:
        assessDay=assess["Day of Week"]
    except:
        assessDay=""
    for wA in range(len(AutumnWeeks)):
        weekA=AutumnWeeks[wA]
        assessTime = assess[weekA] * modCredits*4
        if assessTime>0:
            if np.isfinite(assess["Hours"]):
                assessTime = assess["Hours"]
            assessWeeks = assess["Duration"]
            wR=np.arange(wA-assessWeeks,wA,dtype=int)+1
            wX0=np.min(wR)

            ### add to deadlines counter
            if assSum=="Y":
                nDeadlines["Autumn"][wA] = nDeadlines["Autumn"][wA] + 1
                if pd.notna(assessType) and assessType in nDeadlinesByType["Autumn"]:
                    nDeadlinesByType["Autumn"][assessType][wA] += 1
                if assessTime>=1:
                    nDeadlinesBig["Autumn"][wA] = nDeadlinesBig["Autumn"][wA] + 1
            
            ### add modules to grid object
            if not mod in dlGrid["Autumn"]:
                dlGrid["Autumn"][mod]={"grid":{},"semester":Modules["Semester"][Modules["Module Code"]==mod].values[0]}
            
            ### add to deadlines grid for that assessment
            if assSum=="Y" or assSum=="N":
                if not a in dlGrid["Autumn"][mod]["grid"]:
                    dlGrid["Autumn"][mod]["grid"][a]={"type":assessType,"name":assessName,"duration":assessWeeks,"day":assessDay,"weeks":[],"weights":[]}
                dlGrid["Autumn"][mod]["grid"][a]["weeks"].append(wA+1)
            if assSum=="Y":
                dlGrid["Autumn"][mod]["grid"][a]["weights"].append(assess[weekA])
            elif assSum=="N":
                dlGrid["Autumn"][mod]["grid"][a]["weights"].append(0)
            
            ### set workload
            if profileSel=="Delta":
                profileAssess["Autumn"][wA] = profileAssess["Autumn"][wA] + assessTime
                if pd.notna(assessType) and assessType in profileAssessByType["Autumn"]:
                        profileAssessByType["Autumn"][assessType][wA] += assessTime
                if assCore:
                    profileAssessCore["Autumn"][wA] = profileAssessCore["Autumn"][wA] + assessTime
            elif profileSel=="Dist":
                for wX in wR:
                    profileAssess["Autumn"][wX] = profileAssess["Autumn"][wX] + assessTime/assessWeeks
                    if pd.notna(assessType) and assessType in profileAssessByType["Autumn"]:
                        profileAssessByType["Autumn"][assessType][wX] += assessTime/assessWeeks
                    if assCore:
                        profileAssessCore["Autumn"][wX] = profileAssessCore["Autumn"][wX] + assessTime/assessWeeks
            elif profileSel=="Linear":       
                for wX in wR:
                    profileAssess["Autumn"][wX] = profileAssess["Autumn"][wX] + assessTime*(2*(wX-wX0+1)-1)/assessWeeks**2
                    if pd.notna(assessType) and assessType in profileAssessByType["Autumn"]:
                        profileAssessByType["Autumn"][assessType][wX] += assessTime*(2*(wX-wX0+1)-1)/assessWeeks**2
                    if assCore:
                        profileAssessCore["Autumn"][wX] = profileAssessCore["Autumn"][wX] + assessTime*(2*(wX-wX0+1)-1)/assessWeeks**2
        elif assessTime<0:
            if not mod in dlGrid["Autumn"]:
                dlGrid["Autumn"][mod]={"grid":{},"semester":Modules["Semester"][Modules["Module Code"]==mod].values[0]}
            if assSum=="Y" or assSum=="N":
                if not a in dlGrid["Autumn"][mod]["grid"]:
                    dlGrid["Autumn"][mod]["grid"][a]={"type":assessType,"name":assessName,"duration":assessWeeks,"day":assessDay,"weeks":[],"weights":[]}
                dlGrid["Autumn"][mod]["grid"][a]["weeks"].append(wA+1)
            if assSum=="Y":
                dlGrid["Autumn"][mod]["grid"][a]["weights"].append(assess[weekA])
            elif assSum=="N":
                dlGrid["Autumn"][mod]["grid"][a]["weights"].append(0)
    for wS in range(len(SpringWeeks)):
        weekS=SpringWeeks[wS]
        # if AssessDates.loc[a,"Hours"]
        assessTime = assess[weekS] * modCredits*4
        if assessTime>0:
            if np.isfinite(assess["Hours"]):
                assessTime = assess["Hours"]
            assessWeeks = assess["Duration"]
            wR=np.arange(wS-assessWeeks,wS,dtype=int)+1
            wX0=np.min(wR)

            ### add to deadlines counter
            if assSum=="Y":
                nDeadlines["Spring"][wS] = nDeadlines["Spring"][wS] + 1
                if pd.notna(assessType) and assessType in nDeadlinesByType["Spring"]:
                    nDeadlinesByType["Spring"][assessType][wS] += 1
                if assessTime>=1:
                    nDeadlinesBig["Spring"][wS] = nDeadlinesBig["Spring"][wS] + 1
            
            ### add modules to grid object
            if not mod in dlGrid["Spring"]:
                dlGrid["Spring"][mod]={"grid":{},"semester":Modules["Semester"][Modules["Module Code"]==mod].values[0]}
            
            ### add to deadlines grid for that assessment
            if assSum=="Y" or assSum=="N":
                if not a in dlGrid["Spring"][mod]["grid"]:
                    dlGrid["Spring"][mod]["grid"][a]={"type":assessType,"name":assessName,"duration":assessWeeks,"day":assessDay,"weeks":[],"weights":[]}
                dlGrid["Spring"][mod]["grid"][a]["weeks"].append(wS+1)
            if assSum=="Y":
                dlGrid["Spring"][mod]["grid"][a]["weights"].append(assess[weekS])
            elif assSum=="N":
                dlGrid["Spring"][mod]["grid"][a]["weights"].append(0)
            if profileSel=="Delta":
                profileAssess["Spring"][wS] = profileAssess["Spring"][wS] + assessTime
                if pd.notna(assessType) and assessType in profileAssessByType["Spring"]:
                    profileAssessByType["Spring"][assessType][wS] += assessTime
                if assCore:
                    profileAssessCore["Spring"][wS] = profileAssessCore["Spring"][wS] + assessTime
            elif profileSel=="Dist":
                for wX in wR:
                    profileAssess["Spring"][wX] = profileAssess["Spring"][wX] + assessTime/assessWeeks
                    if pd.notna(assessType) and assessType in profileAssessByType["Spring"]:
                        profileAssessByType["Spring"][assessType][wX] += assessTime/assessWeeks
                    if assCore:
                        profileAssessCore["Spring"][wX] = profileAssessCore["Spring"][wX] + assessTime/assessWeeks
            elif profileSel=="Linear":       
                for wX in wR:
                    profileAssess["Spring"][wX] = profileAssess["Spring"][wX] + assessTime*(2*(wX-wX0+1)-1)/assessWeeks**2
                    if pd.notna(assessType) and assessType in profileAssessByType["Spring"]:
                        profileAssessByType["Spring"][assessType][wX] += assessTime*(2*(wX-wX0+1)-1)/assessWeeks**2
                    if assCore:
                        profileAssessCore["Spring"][wX] = profileAssessCore["Spring"][wX] + assessTime*(2*(wX-wX0+1)-1)/assessWeeks**2
        elif assessTime<0:
            hasOldDeadline=True
            if not mod in dlGrid["Spring"]:
                dlGrid["Spring"][mod]={"grid":{},"semester":Modules["Semester"][Modules["Module Code"]==mod].values[0]}
            if assSum=="Y" or assSum=="N":
                if not a in dlGrid["Spring"][mod]["grid"]:
                    dlGrid["Spring"][mod]["grid"][a]={"type":assessType,"name":assessName,"duration":assessWeeks,"day":assessDay,"weeks":[],"weights":[]}
                dlGrid["Spring"][mod]["grid"][a]["weeks"].append(wS+1)
            if assSum=="Y":
                dlGrid["Spring"][mod]["grid"][a]["weights"].append(assess[weekS])
            elif assSum=="N":
                dlGrid["Spring"][mod]["grid"][a]["weights"].append(0)

# st.stop()

caTypesList = sorted(list(caTypes))
def caType2Label(caType):
    """
    Converts a CA type to a more readable label.
    """
    if pd.isna(caType):
        return "Unknown"
    caType = caType.strip().upper()
    if caType == "CT":
        return "Class Test"
    elif caType == "CW":
        return "Coursework"
    elif caType == "PJ":
        return "Project"
    elif caType == "PR":
        return "Presentation"
    elif caType == "PO":
        return "Portfolio"
    elif caType == "QU":
        return "Quiz"
    elif caType == "OA":
        return "Oral Assessment"
    elif caType == "LB":
        return "Lab diary"
    else:
        return caType.capitalize()

caTypeColorMap = {
        "CT": 0,    # Class Test - red
        "CW": 1,    # Coursework - blue  
        "PJ": 2,    # Project - green
        "PR": 3,    # Presentation - purple
        "PO": 4,    # Portfolio - orange
        "QU": 5,    # Quiz - brown
        "OA": 6,    # Oral Assessment - pink
        "LB": 7,    # Lab diary - gray
    }
colors = plt.cm.Set1(np.linspace(0, 1, 9))  # Get 9 colors from Set1
caTypeColors = {}

for caType in caTypesList:
    if pd.isna(caType):
        # Use the last color for unknown types
        caTypeColors[caType] = colors[8]
    else:
        caType_clean = caType.strip().upper()
        if caType_clean in caTypeColorMap:
            caTypeColors[caType] = colors[caTypeColorMap[caType_clean]]
        else:
            # For any other types, use a default color
            caTypeColors[caType] = colors[8]  # Gray for unknown types
semesters=["Autumn","Spring"]

if not showAllMods:
    # fig=plt.figure(figsize=(12,9),num=1)
    fig,axes=plt.subplots(2,2,figsize=(8,8))
    x_values=np.arange(0.5,13)
    x_ticks=np.arange(1,13)
    x_tick_positions=np.arange(0.5,12.5)  # Position tick marks between weeks
    maxW=np.max([np.max(profileContact["Autumn"]+profileAssess["Autumn"]),np.max(profileContact["Spring"]+profileAssess["Spring"])])+1
    maxD=np.max([np.max(nDeadlines["Autumn"]),np.max(nDeadlines["Spring"])])+1
    y_ticksN=np.arange(0,maxD+1,1,dtype=int)
    
    # # Define colors for different CA types
    # caTypesList = sorted(list(caTypes))
    # colors = plt.cm.Set1(np.linspace(0, 1, len(caTypesList)))
    # caTypeColors = dict(zip(caTypesList, colors))
    
    for s,sem in enumerate(semesters):
        dataContact=profileContact[sem]
        y_Contact=np.concatenate([[dataContact[0]],dataContact])
        dataAssess=profileAssess[sem]
        y_Assess=np.concatenate([[dataAssess[0]],dataAssess])
        dataAssessCore=profileAssessCore[sem]
        y_AssessCore=np.concatenate([[dataAssessCore[0]],dataAssessCore])

        ax=axes[0,s]

        # Create stacked bar chart for assessment types
        bottom = y_Contact.copy()
        width = 1.0
        x_bar = np.arange(1, 13)
        
        for caType in caTypesList:
            if caType in profileAssessByType[sem]:
                data = profileAssessByType[sem][caType]
                ax.bar(x_bar, data, width, bottom=bottom[1:], 
                      color=caTypeColors[caType], alpha=0.7, label=caType2Label(caType))
                bottom[1:] += data
        
        # Plot contact time as baseline
        ax.plot(x_values,y_Contact,"k",linestyle=":",drawstyle="steps-pre",label="Contact Time")
        ax.fill_between(x_values,y_Contact,color="gray",alpha=0.3,step="pre")
        
        # Plot total workload line
        ax.plot(x_values,y_Assess+y_Contact,"b",drawstyle="steps-pre",linewidth=2,label="Total Workload")

        
        ax.grid(True, axis='y', linestyle='--', color='grey', alpha=0.6)
        
        # Set custom x-axis grid lines between weeks
        ax.set_xticks(x_ticks)  # Labels at week centers
        ax.tick_params(axis='x', length=0,labelsize=8)  # Hide the default tick marks
        
        # Add custom grid lines between weeks
        for x_pos in x_tick_positions:
            ax.axvline(x_pos, color='grey', linestyle='--', alpha=0.6, linewidth=0.5)
        
        # Add top x-axis with dates
        ax_top = ax.twiny()
        ax_top.set_xlim(0.5,12.5)
        ax_top.tick_params(axis='x', length=0,labelsize=8)  # Hide the default tick marks
        ax_top.set_xticks(x_ticks)
        ax_top.set_xlabel(f"{sem} Semester Week")
   

        ax.set_ylim(0,maxW+10)
        ax.set_xlim(0.5,12.5)
        # ax.set_xlabel(f"{sem} Semester Week")
        ax.set_ylabel("Estimated Workload (Hours)")
        if s==0:
            ax.axvline(11.5,color="gray",lw=6,alpha=0.5)
            ax.annotate("Vacation",(11.75,ax.get_ylim()[1]),rotation="vertical",va="top")
        if s==1:
            legW=ax.legend(loc="upper left", bbox_to_anchor=(1.05, 1),fontsize='small')
            eW=easterWeeks[academicYear]+0.5
            ax.axvline(eW,color="gray",lw=6,alpha=0.5)
            ax.annotate("Vacation",(eW+0.25,ax.get_ylim()[1]),rotation="vertical",va="top")
        

        ### PLOT N Deadlines plot
        dataNDeadlines=nDeadlines[sem]
        y_NDeadlines=np.concatenate([[dataNDeadlines[0]],dataNDeadlines])
        dataNDeadlinesBig=nDeadlinesBig[sem]
        y_NDeadlinesBig=np.concatenate([[dataNDeadlinesBig[0]],dataNDeadlinesBig])
        axN=axes[1,s]

        bottom_dl = np.zeros(12)
        
        for caType in caTypesList:
            if caType in nDeadlinesByType[sem]:
                data_all = nDeadlinesByType[sem][caType]
                
                # Stack all deadlines
                axN.bar(x_bar, data_all, width, bottom=bottom_dl, 
                       color=caTypeColors[caType], alpha=0.6, label=caType2Label(caType))
                bottom_dl += data_all
                
        

        axN.plot(x_values,y_NDeadlines,"g",drawstyle="steps-pre",label="All Deadlines")
        # axN.plot(x_values,y_NDeadlinesBig,"r",drawstyle="steps-pre",label="Workload >=1hr")
        axN.grid(True, axis='y', linestyle='--', color='grey', alpha=0.6)
        
        # Same treatment for the deadlines plot
        axN.set_xticks(x_ticks)
        axN.tick_params(axis='x', length=0,labelsize=8)
        
        # Add custom grid lines between weeks
        for x_pos in x_tick_positions:
            axN.axvline(x_pos, color='grey', linestyle='--', alpha=0.6, linewidth=0.5)
        
        axN.set_xlim(0.5,12.5)
        axN.set_ylim(0,maxD)
        axN.set_yticks(y_ticksN)
        axN.set_xlabel(f"{sem} Semester Week")
        axN.set_ylabel("# Deadlines")
        if s==0:
            axN.axvline(11.5,color="gray",lw=6,alpha=0.5)
            axN.annotate("Vacation",(11.75,axN.get_ylim()[1]),rotation="vertical",va="top")
        if s==1:
            legN=axN.legend(loc="upper left", bbox_to_anchor=(1.05, 1),fontsize='small')
            eW=easterWeeks[academicYear]+0.5
            axN.axvline(eW,color="gray",lw=6,alpha=0.5)
            axN.annotate("Vacation",(eW+0.25,axN.get_ylim()[1]),rotation="vertical",va="top")

    plt.tight_layout(rect=[0, 0, 1, 0.8])
    st.pyplot(fig)
    if savePlots=="Yes":
        try:
            fileOutPng=f'plots/png/workload_{shortCode}.png'
            fileOutPdf=f'plots/pdf/workload_{shortCode}.pdf'
            plt.savefig(fileOutPng)
            plt.savefig(fileOutPdf)
            st.info('Plot saved to',fileOutPng)
            st.info('Plot saved to',fileOutPdf)
        except:
            st.info('Unable to save plot')

# st.write(dlGrid)
st.divider()
st.header("Deadline Grids")
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

def weight2sizecolorlabel(w,portfolio=False):
    if w<-0.1:
        return {'ms':100,'ec':'orange','lw':0,'fc':'yellow','lab':"24/25 deadline",'textcol':'grey','alpha':0}
        # return {'ms':0  ,'ec':'orange','lw':0,'fc':'yellow','lab':'','textcol':'white','alpha':0}
    elif w<0:
        return {'ms':30,'ec':'orange','lw':0,'fc':'yellow','lab':"24/25 deadline",'textcol':'grey','alpha':1}
        # return {'ms':0,'ec':'orange','lw':0,'fc':'yellow','lab':"",'textcol':'white','alpha':0}
    elif w==0:
        return {'ms':25,'ec':'grey','lw':1,'fc':'white','lab':"Formative",'textcol':'grey','alpha':1}
    elif w<=0.05:
        return {'ms':25,'ec':'blue','lw':1,'fc':'white','lab':"<5%",'textcol':'black','alpha':1}
    elif w<=0.1:
        return {'ms':30,'ec':'green','lw':0,'fc':'green','lab':"5-10%",'textcol':'black','alpha':1}
    elif w<=0.3:
        return {'ms':80,'ec':'red','lw':1,'fc':'white','lab':"10-30%",'textcol':'black','alpha':1}
    else:
        return {'ms':100,'ec':'red','lw':0,'fc':'red','lab':">30%",'textcol':'black','alpha':1}
    
assessSeen={"Autumn":set(),"Spring":set()}
handles={}
labels={}
for s,sem in enumerate(semesters):
    extra_artists=[]
    axG=axesG[s]
    yticks=[]
    ylabels=[]
    mods=list(dlGrid[sem].keys())
    mods.sort(key=lambda x:dlGrid[sem][x]["semester"])
    for m,mod in enumerate(mods):
        nassess=len(dlGrid[sem][mod]["grid"])
        coreMod= mod in coreModsAll
        if coreMod:
            coreRect=mpatches.Rectangle((0.5,m-0.5),12,1,facecolor='lightgray',alpha=0.5)
            axG.add_patch(coreRect)
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
            alphas=[]
            edgecolors=[]
            facecolors=[]
            linewidths=[]
            labs=[]
            textcols=[]
            for w,wt in enumerate(weights):
                sizes.append(weight2sizecolorlabel(wt)["ms"])
                alphas.append(weight2sizecolorlabel(wt)["alpha"])
                edgecolors.append(weight2sizecolorlabel(wt)["ec"])
                facecolors.append(weight2sizecolorlabel(wt)["fc"])
                linewidths.append(weight2sizecolorlabel(wt)["lw"])
                labs.append(weight2sizecolorlabel(wt)["lab"])
                textcols.append(weight2sizecolorlabel(wt)["textcol"])
            # st.write(m,mod,nassess,a,dlGrid[sem][mod]["grid"][an]["type"],yass[0],len(dlGrid[sem][mod]["grid"][an]["weeks"]))
            # axG.scatter(dlGrid[sem][mod]["grid"][an]["weeks"],yplot,s=np.array(sizes),
            #             edgecolor=edgecolors,facecolor=facecolors,linewidth=linewidths)
            if hasDays:
                for w,week in enumerate(dlGrid[sem][mod]["grid"][an]["weeks"]):
                    if dlGrid[sem][mod]["grid"][an]["day"]==" " or dlGrid[sem][mod]["grid"][an]["day"]=="":
                        axG.scatter(dlGrid[sem][mod]["grid"][an]["weeks"][w],yplot[w],s=np.array(sizes)[w],
                            edgecolor=edgecolors[w],facecolor=facecolors[w],linewidth=linewidths[w],alpha=alphas[w])
                    else:
                        axG.scatter(dlGrid[sem][mod]["grid"][an]["weeks"][w]-0.25,yplot[w],s=np.array(sizes)[w],
                            edgecolor=edgecolors[w],facecolor=facecolors[w],linewidth=linewidths[w],alpha=alphas[w])
                        axG.text(week-0.15*(1-sizes[w]/100),yass,dlGrid[sem][mod]["grid"][an]["day"],ha="left",va="center_baseline",
                            fontsize=8,color=textcols[w],alpha=alphas[w])
            else:
                 for w,week in enumerate(dlGrid[sem][mod]["grid"][an]["weeks"]):
                    axG.scatter(dlGrid[sem][mod]["grid"][an]["weeks"][w],yplot[w],s=np.array(sizes)[w],
                        edgecolor=edgecolors[w],facecolor=facecolors[w],linewidth=linewidths[w],alpha=alphas[w])
            yticks.append(yass)
            ylabels.append(aName)
        if coreMod:
            modtxt=axG.text(-2,m,f'{mod}\n(Core)',ha="center",va="center",rotation="vertical",fontsize=10)
        else:
            modtxt=axG.text(-2,m,f'{mod}\n(Optional)',ha="center",va="center",rotation="vertical",fontsize=10)
        extra_artists.append(modtxt)
    # st.write('types',assessTypes,'colors',assessColours)
    # axG.set_yticks(np.arange(len(mods)))
    # axG.set_yticklabels(mods)
    axG.set_yticks(yticks)
    axG.set_yticklabels(ylabels,fontsize=8)
    axG.set_ylim(-0.5,len(mods)-0.5)
    axG.set_xlabel(f"{sem} Semester Week ({academicYear})")
    axG.set_xticks(np.arange(13))
    startDate=startDates[academicYear][sem]
    xticklabels=[]
    axG.set_xticks(np.arange(13))
    for w in range(13):
        if (sem=="Autumn" and w<=11) or sem=="Spring" and w-1<easterWeeks[academicYear]:
            wkbeg=startDate+timedelta(weeks=w-1)
        else:
            wkbeg=startDate+timedelta(weeks=w-1+3)
        xticklabels.append(f'{w}\n'+wkbeg.strftime("%d/%m"))
    axG.set_xticklabels(xticklabels)
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
    axG.set_title(f"{title}\n{sem} Semester {academicYear}")
    
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
    if hasOldDeadline:
        legendWeights=[-0.5,0,0.05,0.1,0.3,0.5]
    else:
        legendWeights=[0,0.05,0.1,0.3,0.5]
    legendMarkers=[]
    for w,wt in enumerate(legendWeights):
        alpha=weight2sizecolorlabel(wt)["alpha"]
        size=weight2sizecolorlabel(wt)["ms"]
        edgecolor=weight2sizecolorlabel(wt)["ec"]
        facecolor=weight2sizecolorlabel(wt)["fc"]
        linewidth=weight2sizecolorlabel(wt)["lw"]
        lab=weight2sizecolorlabel(wt)["lab"]
        textcol=weight2sizecolorlabel(wt)["textcol"]
        legendMarkers.append(axG.scatter(0.5,0.5,s=size,
                            label=lab,edgecolor=edgecolor,facecolor=facecolor,linewidth=linewidth,alpha=alpha))
    legend=axesG[s].legend(loc='upper right',bbox_to_anchor=(1.25,1),title="Weighting")
    
    for t,text in enumerate(legend.get_texts()):
        text.set_color(weight2sizecolorlabel(legendWeights[t])["textcol"])
        text.set_alpha(weight2sizecolorlabel(legendWeights[t])["alpha"])

    #Add deadline date key
    if hasDays:
        axesG[s].text(12.6,len(mods)-0.5,"Deadlines:\nMo/Tu/We/Th/Fr\n\n(*)=In-session\n       assessment\n(P)=Portfolio or\n       component" ,va="bottom",ha="left")
    for l,lm in enumerate(legendMarkers):
        lm.remove()
    extra_artists.append(legend)
    axesG[s].set_position([0.2,0.2,0.8,figh[sem]/(figh[sem]+1)])
    st.pyplot(figG[s])
    if savePlots=="Yes":
        try:
            fileOutPng=f'plots/png/deadlines_{shortCode}_{sem}.png'
            fileOutPdf=f'plots/pdf/deadlines_{shortCode}_{sem}.pdf'
            figG[s].savefig(fileOutPng,bbox_inches="tight")
            figG[s].savefig(fileOutPdf,bbox_inches="tight")
            st.write('Plot saved to',fileOutPng)
            st.write('Plot saved to',fileOutPdf)
        except:
            st.info('Unable to save plot')
    
            
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

