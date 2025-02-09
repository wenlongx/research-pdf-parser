# Setup Instructions

Create the virtualenv if you haven't already (if you have, skip this step)
```
python3 -m virtualenv /Users/angelinawei/pdfproject
```

Activate the virtualenv
```
source /Users/angelinawei/pdfproject
```

If this is the first time running code, then install the packages you need (only openai)
```
pip3 install openai
```

# Initial setup (run only once to create the vector db once)
Set the API keys
```
export OPENAI_API_KEY="your_api_key_here"
```

Run the setup script to (1) create a vector store, (2) upload files to your vector store (PDFs), (3) create an assistant that makes use of this vector store.
The output should show something like this:

Run
```
python3 setup.py
```

Output
```
(pdfproject) wenlongx:~/Desktop/research-pdf-parser > python3 setup.py
Begin file upload
Uploading files: ['/Users/wenlongx/Desktop/litreviewpdfs/A Case of Bartonella Quintana Culture-Negative Endocarditis.pdf', '/Users/wenlongx/Desktop/litreviewpdfs/A national survey of dental hygienists_ infection control attitudes and practices.pdf']
Waiting for file uploads ...
Succeeded
Finished uploading files!
Vector store ID is: vs_67a83077634481919faa2564a45aff2b
Assistant ID is: asst_TikL4iprP1yH8Y0nQtDaBXqF
```

Keep track of these vector store ID + assistant ID for the next step

# Run the assistant and make them generate a CSV file
Modify the script `run_assistant.py` to include the vector store id and assistant id.
```
  1 import os
  2 import re
  3 from openai import OpenAI
  4 import time
  5
  6 vector_store_id = "vs_67a82d9e83c881918e08f21f5249fca8"
  7 assistant_id = "asst_I7XBBCb6syjNaUCponAV46iS"
  8
```

Run the assistant python script:
```
python3 run_assistant.py
```

It should output a file and tell you where that CSV is located:
```
(pdfproject) wenlongx:~/Desktop/research-pdf-parser > python3 run_assistant.py
Running prompt

    For each PDF in the knowledge store, analyze the following themes and subthemes from the experiments and research described in the PDF:
        Theme: Descriptions as stated in report/paper
	Subtheme: abstract
	Subtheme: introduction
	Subtheme: background
	Subtheme: summary
Theme: Aim
	Subtheme: aim
	Subtheme: objective
	Subtheme: purpose
	Subtheme: efficacy
	Subtheme: pragmatic
Theme: Start date
	Subtheme: start date
	Subtheme: commencement
	Subtheme: initiation date
Theme: End date
	Subtheme: end date
	Subtheme: completion
	Subtheme: final date

    Parse information out of the PDFs and output a CSV object for each distinct PDF, with the CSV column headers being of the format 'theme: subtheme'. The first column should be the name of the source PDF.
    For example, for the given themes and subthemes:
        {'example_theme_1': ['example_subtheme_a', 'example_subtheme_b'], 'example_theme_2': ['example_subtheme_c']}
    The column headers should look like:
        source_pdf, example_theme_1:example_subtheme_a, example_theme_1:example_subtheme_b, example_theme_2:example_subtheme_c,
    Do not return any system message, only return the CSV. Make sure the column keys are sorted in alphabetical order.



Starting to wait for prompt to complete
Finished prompt, starting to parse messages
Processing message 0
Processing message 1
Writing out to file
Writing output to /Users/wenlongx/Desktop/litreviewpdfs/output.csv
```

The output CSV should look like this:
```
source_pdf,aim:aim,aim:efficacy,aim:objective,aim:purpose,aim:pragmatic,background:          background,introduction:introduction,summary:summary,theme:start date,start date:          commencement,start date:initiation date,theme:end date,end date:completion,end date:       final date
A Case of Bartonella Quintana Culture-Negative Endocarditis.pdf,The purpose of this study    was to present a case of culture-negative Bartonella quintana endocarditis diagnosed       using a multidisciplinary approach.,The efficacy of the combined approach was supported    by the positive results of nucleic acid testing.,To investigate the role of Bartonella     quintana in culture-negative endocarditis.,The objective was to establish a diagnosis      using various methods including clinical evaluation and testing.,The pragmatic aspect      involved integrating multiple diagnostic tools for effective patient management.,          Bartonella quintana and Bartonella henselae are commonly associated with culture-          negative endocarditis..,This study highlights the increasing incidence of culture-         negative endocarditis and the challenges involved in its diagnosis.,This case report       illustrates timely intervention is crucial for patient survival after diagnosis.,Not       stated,Not stated,Not stated,Not stated,Not stated,Not stated,Not stated
A national survey of dental hygienists_ infection control attitudes and practices.pdf,To     summarize the infection control attitudes and practices of dental hygienists regarding     infectious diseases.,This study aims to evaluate the effect of professional affiliation    on infection control practices.,To investigate the knowledge, attitudes, and practices     of dental hygienists regarding infection control measures.,To determine compliant          practices with recommended infection control procedures.,The pragmatic aim is to improve   infection control practices through better education of dental hygienists.,Background      emphasizes the importance of proper infection control to prevent disease transmission in   dental settings.,The introduction discusses hypothesis on knowledge and attitudes of       hygienists toward infected patients.,A summary of findings shows current compliance        levels and ongoing issues in infection control practices.,Survey conducted between 1998    and 2005.,Initiated study to build a representative data set across the United States      for analysis.,Intro of study began early 2005. The actual survey was conducted soon        after.,Study completed in the spring of 2005, reflecting compliance at that period.,End    of study reflects significant changes or lack in infection control practices over time..
```

# Cleanup
We created the vector store, the assistant, and uploaded some files. However, these all cost $$ to keep around, so we should clean it up when we're done.

```
python3 delete_assistants.py
python3 delete_files.py
```

You need to delete the vector stores manually, in the UI:
`https://platform.openai.com/storage/vector_stores/`
