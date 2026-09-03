# Cardiff PHYSX Student workload model

Student workload, published via Streamlit at https://physx-student-workload.streamlit.app/

Streamlit page is based on plot_student-workload.py

# Data format

The data is loaded from an Excel file containing modules and assessments data.

## "Modules" sheet

List of modules with which degrees they are on.

* **Module Code**: Module code
* **Module Title**: Module title
* **Alternative Module Code**: alternative modules (parent/child modules)
* **Source**: UG/PGT. U = UG, P = PGT
* **Semester**: SEM1 = Semester 1, SEM2 = Semester 2, SEMD = Dual Semester
* **Level**: Module level (QAA level, so 4= year 1, etc.)
* **Credits**: Module credits
* **Parent**: Parent module code
* Module choices, with one column per programme.
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
* **Module Title**: Module Title
* **Contact type**: type of contact (Lecture / Workshop)
* Auto-complete columns (from Modules sheet):
  * **Credits**: Credits per module
  * **Semester**: Semester of module
  * **Nominal Hours**: typical contact hours per week
* **Autumn/Spring Week 1-12**: hours per week of contact time for that module and contact type
* **Total**: Auto-calculated total hours

### "Assessments" sheet

Details of assessments for modules, with one row for each "group" of assessments (of the same type)

* **Module Code**: Module Code
* **Module Title**: Module Title
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
* Auto-completed columns (from Modules sheet):
  * **CA Weight**: Weight of CA for whole module (in %)
  * **Credits**: module credits
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
