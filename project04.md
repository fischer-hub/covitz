Freie Universität Berlin, Robert-Koch Institute

Practical course: SARS-2 Bioinformatics & Data Science

Max von Kleist, Martin Hölzer

# Project 4

## Genome-based SARS-CoV-2 incidence estimation and case ascertainment

**Deadline**: 29.09.2023, 14:00

*The project should be worked out in groups of two or three students. Students should document their progress and present their work on Friday; 29.09.2023; 14:30am to the lecturers and students. The talk should be about 30-40 min, and allowing for 10-15min of questions.*

**a) The presentation should be uploaded via whiteboard as `Project4.pdf`, no later than the above stated deadline.**

An exemplary structure of the talk: 
*	Title including group composition (possibly a link to the code repository)
*	Short background (what is this good for?) & description of task
*	Methods: A step-by-step explanation of what has been done; troubleshooting
*	Results: A summary of the outcomes and analysis
*	Discussion of results; aspects that were unclear; how the workflow could be improved 
*	Outlook

**b) Codes for conducting the project tasks should be zipped into `Project4.zip` and uploaded either via whiteboard or made accessible via GitHub or GitLab.** In the latter case, a link to the repo should be provided on the slides and the repo must be accessible to the lecturers.

**Detailed Tasks:**

1) Install `GInPipe` [https://github.com/KleistLab/GInPipe](https://github.com/KleistLab/GInPipe) and `covsonar` [https://github.com/rki-mf1/covsonar](https://github.com/rki-mf1/covsonar)
2) If not done already in the hands-on session, analyse the dataset for Germany from 2022 with GInPipe. The dataset can be found here: [https://osf.io/hxk5m](https://osf.io/hxk5m)
3) Download the following data as well:
  * [A CoVsonar databse](https://osf.io/uchtg)
  * [reported cases table for France](https://osf.io/jptkw)
4) Export and explore data:
  * Extract entries that fall into the time period between 2022-01-01 and 2022-07-01 and originate in France from the covsonar database. Note: the location is stored in field ***collection***
  * Plot a histogram of the amount of entries per day for the extracted data set
  * Note that the reported cases for France were recorded once a week. Pick a method and obtain the (average) daily number of reported cases before running the pipeline.
5) Analyse the extracted France dataset using `GInPipe``:
  * Configure (see course notes or README in the GInPIpe repository) and run the pipeline
6) Discuss the France results and compare with results for Germany.

