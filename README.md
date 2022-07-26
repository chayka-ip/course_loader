# Course parser

This program was build to collect information about programming courses 
and video download links available on certain resource.

The site requires authorisation to view detailed content for each lecture and dynamically generates page content.   
However, urls for these lectures where available for unauthorized users that had helped me to collect data faster. 

Overall process was divide on three stages to keep things simple.

### 1. Collect courses structure data from website

On this stage I sent request to the main page that represents information about available courses and their structure.   
This data gave me all necessary information to build absolute urls for each lecture page.

Result: lecture url lists were obtained for each course.

### 2. Obtain download links from the website

Authorisation is required to access lecture pages, so I logged into my account.   
Data from previous stage is used to navigate to page for each lecture to load it's content.   
Few simple .js scripts was build to automatically navigate to pages, 
search for download links and save output data to json file. 

Result: download links were obtained for each lecture

### 3. Process collected data to form structured json output

Once all download links are collected data from Stages 1 and 2 
is combined to form output shown in the folder data/courses_complete

Result: necessary data was collected and structured. 

P.S. All courses was paid by me. This task was made only for educational purposes.