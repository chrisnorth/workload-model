import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
plt.ion()
import datetime
import string

# StudentFilters
# Levels: U1PHYSX, U2PHYSX, UFPHYSX, UFPHYSXA, PGPHYSX1
Cohort="U1PHYSX"
Semester="SEM1"
StartAutumn=pd.Timestamp(2024,9,30)
StartSpring=pd.Timestamp(2025,1,27)

AssessDates=pd.read_excel('AssessmentSchedule_2425.xlsx',"Assessments")
AssessDates.fillna(0)
weeks=[]
AutumnWeeks=[]
SpringWeeks=[]
for a in AssessDates:
    if a.find('Week')>=0:
        weeks.append(a)
    if a.find('Autumn Week')>=0:
        AutumnWeeks.append(a)
    if a.find('Spring Week')>=0:
        SpringWeeks.append(a)
AssessDates['Sub-total']=AssessDates[weeks].sum(axis=1)

Modules=pd.read_excel('AssessmentSchedule_2425.xlsx',"Modules",)

nMod=len(Modules)
# Modules["CA Weight"]=100-Modules["Exam Weight"]
Modules["AssessTotal"]=[0]*len(Modules)
for m in range(len(Modules)):
    mod=Modules["Module Code"][m]
    idx=np.where(AssessDates["Module Code"]==mod)
    # print(mod,idx)
    # print(AssessDates["Module Code"][idx[0]])
    # print(AssessDates["Sub-total"][idx[0]])
    # print(AssessDates["Sub-total"][idx[0]].sum(axis=0)*100)
    Modules.loc[Modules["Module Code"]==mod,"AssessTotal"]=AssessDates.loc[AssessDates["Module Code"]==mod,"Sub-total"].sum(axis=0)*100
xltemp=pd.ExcelWriter('Assessments_temp.xlsx')
Modules.to_excel(xltemp,"Modules")
AssessDates.to_excel(xltemp,"Assessments")
xltemp.close()

def l2y(level):
    years={4:"Y1",5:"Y2",6:"Y3",7:"Y4"}
    assert(level in years)
    return(years[level])

profileDelta={"Y1":{"level":4},"Y2":{"level":5},"Y3":{"level":6},"Y4":{"level":7}}
profileDist={"Y1":{"level":4},"Y2":{"level":5},"Y3":{"level":6},"Y4":{"level":7}}
for y in profileDelta:
    profileDelta[y]["PhysCore"]={"Autumn":[0]*len(AutumnWeeks),"Spring":[0]*len(SpringWeeks)}
    profileDelta[y]["AstroCore"]={"Autumn":[0]*len(AutumnWeeks),"Spring":[0]*len(SpringWeeks)}
    profileDelta[y]["MedPhysCore"]={"Autumn":[0]*len(AutumnWeeks),"Spring":[0]*len(SpringWeeks)}
    profileDist[y]["PhysCore"]={"Autumn":[0]*len(AutumnWeeks),"Spring":[0]*len(SpringWeeks)}
    profileDist[y]["AstroCore"]={"Autumn":[0]*len(AutumnWeeks),"Spring":[0]*len(SpringWeeks)}
    profileDist[y]["MedPhysCore"]={"Autumn":[0]*len(AutumnWeeks),"Spring":[0]*len(SpringWeeks)}

for a in range(len(AssessDates)):
    mod = AssessDates["Module Code"][a]
    modLevel = Modules["Level"][Modules["Module Code"]==mod].values[0]
    modCredits = Modules["Credits"][Modules["Module Code"]==mod].values[0]
    physChoice=Modules["Physics"][Modules["Module Code"]==mod].item()
    astroChoice=Modules["Astro"][Modules["Module Code"]==mod].item()
    medPhysChoice=Modules["MedPhys"][Modules["Module Code"]==mod].item()
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
            if medPhysChoice=="C":
                print(mod,weekA,assessType,assessTime,int(assessWeeks),assessTime/assessWeeks,wA,wR)
            if physChoice=="C":
                profileDelta[modYear]["PhysCore"]["Autumn"][wA] = profileDelta[modYear]["PhysCore"]["Autumn"][wA] + assessTime
                for wX in wR:
                    profileDist[modYear]["PhysCore"]["Autumn"][wX] = profileDist[modYear]["PhysCore"]["Autumn"][wX] + assessTime/assessWeeks
            if astroChoice=="C":
                profileDelta[modYear]["AstroCore"]["Autumn"][wA] = profileDelta[modYear]["AstroCore"]["Autumn"][wA] + assessTime
                for wX in wR:
                    profileDist[modYear]["AstroCore"]["Autumn"][wX] = profileDist[modYear]["AstroCore"]["Autumn"][wX] + assessTime/assessWeeks
            if medPhysChoice=="C":
                profileDelta[modYear]["MedPhysCore"]["Autumn"][wA] = profileDelta[modYear]["MedPhysCore"]["Autumn"][wA] + assessTime
                for wX in wR:
                    profileDist[modYear]["MedPhysCore"]["Autumn"][wX] = profileDist[modYear]["MedPhysCore"]["Autumn"][wX] + assessTime/assessWeeks
    for wS in range(len(SpringWeeks)):
        weekS=SpringWeeks[wS]
        assessTime = AssessDates.loc[a,weekS].item() * modCredits*4
        if assessTime>0:
            if np.isfinite(AssessDates.loc[a,"Hours"]):
                assessTime = AssessDates.loc[a,"Hours"].item()
            assessWeeks = AssessDates.loc[a]["Duration"].item()
            wR=np.arange(wS-assessWeeks,wS)+1
            if medPhysChoice=="C":
                print(mod,modYear,weekS,assessType,assessTime,int(assessWeeks),assessTime/assessWeeks,wS,wR)
            if physChoice=="C":
                profileDelta[modYear]["PhysCore"]["Spring"][wS] = profileDelta[modYear]["PhysCore"]["Spring"][wS] + assessTime
                for wX in wR:
                    profileDist[modYear]["PhysCore"]["Spring"][wX] = profileDist[modYear]["PhysCore"]["Spring"][wX] + assessTime/assessWeeks
            if astroChoice=="C":
                profileDelta[modYear]["AstroCore"]["Spring"][wS] = profileDelta[modYear]["AstroCore"]["Spring"][wS] + assessTime
                for wX in wR:
                    profileDist[modYear]["AstroCore"]["Spring"][wX] = profileDist[modYear]["AstroCore"]["Spring"][wX] + assessTime/assessWeeks
            if medPhysChoice=="C":
                profileDelta[modYear]["MedPhysCore"]["Spring"][wS] = profileDelta[modYear]["MedPhysCore"]["Spring"][wS] + assessTime
                for wX in wR:
                    profileDist[modYear]["MedPhysCore"]["Spring"][wX] = profileDist[modYear]["MedPhysCore"]["Spring"][wX] + assessTime/assessWeeks


plots={"DeltaAutumn":{"data":profileDelta,"num":1,"semester":"Autumn","type":"No CA distribution"},
       "DistAutumn":{"data":profileDist,"num":2,"semester":"Autumn","type":"CA distribution"},
       "DeltaSpring":{"data":profileDelta,"num":3,"semester":"Spring","type":"Duration=1 week"},
       "DistSpring":{"data":profileDist,"num":4,"semester":"Spring","type":"CA distribution"}
       }
for p in plots:
    fig=plt.figure(figsize=(12,6),num=plots[p]["num"])
    fig.clf()
    fig,axes=plt.subplots(3,3,sharex=False,sharey=False,num=plots[p]["num"])
    fig.subplots_adjust(top=0.90)
    fig.suptitle(f'{plots[p]["semester"]} - {plots[p]["type"]}', fontsize=16)
    plots[p]["fig"]=fig
    plots[p]["axes"]=axes

    core_subjects = ['PhysCore', 'AstroCore', 'MedPhysCore']
    years = ['Y1', 'Y2', 'Y3']
    x_values=np.arange(1,13)
    for px, year in enumerate(years):
        for py,subject in enumerate(core_subjects):
            ax=plots[p]["axes"][px,py]
            ax.bar(x_values,plots[p]["data"][year][subject][plots[p]["semester"]])
            ax.text(0.02, 0.95, f'{subject} - {year}', transform=ax.transAxes, fontsize=10, verticalalignment='top')
            ax.set_xticks(x_values)
            ax.grid(True, axis='y', linestyle='--', color='grey', alpha=0.6)
            if px==2:
                ax.set_xlabel("Week of Semester")
            if py==0:
                ax.set_ylabel("Hours")
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    plt.show()
