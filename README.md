# Cardiff PHYSX Student workload model

Student workload, published via Streamlit at [https://physx-student-workload.streamlit.app/](https://physx-student-workload.streamlit.app/)

Streamlit page is based on plot_student-workload.py

It runs in "developer mode" when run locally, or when dev=1 is set in URL query (e.g. [physx-student-workload.streamlit.app?dev=1]([physx-student-workload.streamlit.app](https://physx-student-workload.streamlit.app/)?dev=1))

Use URL queries to affect settings:

* **school**: (currently only PHYSX)
* **dev**: (0 or blank for none, >0 for dev, ), and default years
* **type**: student type (UG/PG)
* **year**: student year (1-4))

# Config file

Configuration is read from a config file in JSON format. The structure is:

* dev_updates: "dev" versions of any of the sections below, used in dev mode<updates to any of the below when in dev mode></updates>
* defaults: default parameters
  * academicYear
  * courseType
  * studentYear
* academicYears: list of academic years
* easterWeeks: dict of week of Spring semester for Easter break (by academic year)
* startDates: dict of start dates (by semesters) in dd/mm/yyyy format
  * Autumn: "dd/mm/yyyy",
  * Spring: "dd/mm/yyyy",
* filenames: dict of filenames containing assessment data (by academic year)
* courseTypes: list of course types (e.g. ["UG", "PG"])
* courses: list of courses for each courseType. Must include "Show modules for all programmes" as one entry
* years: list of years for students for each courseType. Blank list for no options
* columns: dict of column names in assessments file (by course)

# Data format

The data is loaded from an Excel file containing modules and assessments data. Autu-calculated of look-up columns are shaded grey.

## "Modules" sheet

List of modules with which degrees they are on.

* **Module Code**: Module code
* **Module Title**: (auto-completed) Module title
* **Alternative Module Code**: alternative modules (Used for PGT child modules of UG modules)
* **Source**: UG/PGT. U = UG, P = PGT
* **Semester**: SEM1 = Semester 1, SEM2 = Semester 2, SEMD = Dual Semester
* **Level**: Module level (QAA level, so 4= year 1, etc.)
* **Credits**: Module credits
* **Parent**: Parent module code (used for parent/child modules within UG/PGT)
* Module choices columns, with one column per programme. Column names must match config file.
  * Columns must include
    * "AllUG" (for when showing all UG programmes)
    * "AllPG" (for when showing all PG programmes)
  * Format is C = Core, O = Optional.  A suffics of "[N]" links to a footnote, which is included as a "dummy module" at the bottom of the table
* **Contact Time**: Typical contact hours per week
* **Exam Weight (%):** Exam weight for the module
* Auto-calculated modules:
  * **CA Weight**: (100- Exam weight)
  * **CA Check**: Check column with Assessments data

### "ContactTime" sheet

Weekly contact time for modules

* **Module Code**: Module Code (excluding child modules)
* Auto-complete columns (from Modules sheet):

  * **Module Title**: Module Title
  * **Credits**: Credits per module
  * **Semester**: Semester of module
  * **Nominal Hours**: typical contact hours per week
* ****Contact type**: type of contact (Lecture / Workshop / Lab)**
* **Autumn/Spring Week 1-12**: hours per week of contact time for that module and contact type
* **Total**: Auto-calculated total hours

### "Assessments" sheet

Details of assessments for modules, with one row for each "group" of assessments (of the same type)

* **Module Code**: Module Code
* Auto-completed columns (from Modules sheet):
* * **Module Title**: Module Title
  * **CA Weight**: Weight of CA for whole module (in %)
  * **Credits**: module credits
* **CA type**: Type of assessment.

  * CT = Class Test
  * CW = Written Coursework
  * LB = Laboratory assessment
  * OA = Oral Assessment
  * PJ = Project
  * PO = Portfolio
  * PR = Presentation
  * QU = Quiz
  * RP = Report
* **Description**: (short) Description of assessment. Can include line breaks. "(*)" means in-class assessment. "(P)" means single portfolio of multiple assessments
* **Summative**: Flag to indicate summative/formative. Y = Summative, N = Formative, W = Workshop/Project work
* **Day of Week**: Day of week of assessment. Mo/To/We/Th/Fi. Can be "TBC" or "N/A"
* **Duration**: Number of weeks for assessment (i.e. weeks between release and submission)
* **Nominal hours**: (auto-calculated) Nominal number of hours per assessment, assuming 4 hours per 10% of 10 credit module. Used if "Hours" column is blank
* **Hours**: estimated hours per assessment
* **Autumn Week 1-12 ,** **Spring Week 1-12**: assessment weight (as proportion of whole module) in that week
* Auto-calculated columns:

  * **Sub-total**: sub-total of assessment weighting (propotion of total module assessment) for assessments(s) in row
  * **Total hours**: Sub-total of hours for assessment(s) in row)
