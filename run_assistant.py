import os
import re
from openai import OpenAI
import time

vector_store_id = "vs_67a82d9e83c881918e08f21f5249fca8"
assistant_id = "asst_I7XBBCb6syjNaUCponAV46iS"

# Directory containing PDF files
pdf_directory = "/Users/wenlongx/Desktop/litreviewpdfs/"
output_file = "output.csv"

# Set your OpenAI API key
client = OpenAI()

# Create a vector store caled "Financial Statements"
vector_store = client.beta.vector_stores.retrieve(vector_store_id)

# Themes and their associated descriptions, locations, and keywords
themes = {
    "Descriptions as stated in report/paper": ["abstract", "introduction", "background", "summary"],
    "Aim": ["aim", "objective", "purpose", "efficacy", "pragmatic"],
    # "Location in text or source (pg & /fig/table/other)": ["page", "paragraph", "figure", "table"],
    # "Design (e.g. parallel, crossover, non-RCT)": ["parallel", "crossover", "randomized", "non-RCT", "design"],
    # "Unit of allocation (by individuals, cluster/groups or body parts)": ["individuals", "clusters", "groups", "allocation", "body parts"],
    "Start date": ["start date", "commencement", "initiation date"],
    "End date": ["end date", "completion", "final date"],
    # "Duration of participation (from recruitment to last follow-up)": ["duration", "follow-up", "recruitment", "time frame"],
    # "Ethical approval needed/obtained for study": ["ethics", "approval", "institutional review board", "IRB", "ethical approval"],
    # "Notes": ["notes", "comments", "remarks", "observations"],
    # "Participants - Description": ["participants", "subjects", "volunteers"],
    # "Include comparative information for each intervention or comparison group if available": ["comparison", "intervention group", "control group"],
    # "Population description (from which study participants are drawn)": ["population", "cohort", "demographic"],
    # "Setting (including location and social context)": ["setting", "location", "context", "environment"],
    # "Inclusion criteria": ["inclusion criteria", "eligibility", "required criteria"],
    # "Exclusion criteria": ["exclusion criteria", "ineligible", "disqualifying criteria"],
    # "Method of recruitment of participants (e.g. phone, mail, clinic patients)": ["recruitment", "invitation", "enrollment method"],
    # "Informed consent obtained": ["informed consent", "consent form", "participant agreement"],
    # "Total no. randomized (or total pop. at start of study for NRCTs)": ["total participants", "randomized", "study population"],
    # "Clusters (if applicable, no., type, no. people per cluster)": ["clusters", "group size", "cluster allocation"],
    # "Baseline imbalances": ["baseline imbalance", "group differences", "initial imbalance"],
    # "Withdrawals and exclusions (if not provided below by outcome)": ["withdrawals", "dropouts", "exclusions"],
    # "Age": ["age", "years old", "age range"],
    # "Sex": ["sex", "gender", "male", "female"],
    # "Race/Ethnicity": ["race", "ethnicity", "cultural background"],
    # "Severity of illness": ["severity", "disease severity", "stage of illness"],
    # "Co-morbidities": ["co-morbidities", "comorbid conditions", "other illnesses"],
    # "Other relevant sociodemographics": ["sociodemographics", "education level", "income", "occupation"],
    # "Subgroups measure": ["subgroup measure", "subpopulation measure"],
    # "Subgroups reported": ["subgroup reported", "subpopulation reported"],
    # "Notes on participants": ["participant notes", "observations on participants", "participant feedback"],
    # "Intervention Group 1 - Description": ["intervention group", "group 1", "group description"],
    # "Group name": ["group name", "assigned group", "intervention identifier"],
    # "No. randomized to group (specify whether no. people or clusters)": ["randomized to group", "group size", "allocation count"],
    # "Theoretical basis (include key references)": ["theoretical basis", "theory", "underlying framework"],
    # "Description (include sufficient detail for replication, e.g. content, dose, components)": ["detailed description", "treatment details", "dose", "replication"],
    # "Duration of treatment period": ["treatment duration", "treatment period", "intervention length"],
    # "Timing (e.g. frequency, duration of each episode)": ["timing", "frequency", "treatment interval"],
    # "Delivery (e.g. mechanism, medium, intensity, fidelity)": ["delivery", "medium", "mechanism", "intensity"],
    # "Providers (e.g. no., profession, training, ethnicity etc. if relevant)": ["providers", "treatment staff", "intervention personnel"],
    # "Co-interventions": ["co-interventions", "combined interventions", "additional treatments"],
    # "Economic information (i.e. intervention cost, changes in other costs as result of intervention)": ["economic information", "intervention cost", "cost changes"],
    # "Resource requirements (e.g. staff numbers, cold chain, equipment)": ["resource requirements", "staff needed", "equipment"],
    # "Integrity of delivery": ["integrity", "treatment fidelity", "delivery monitoring"],
    # "Compliance": ["compliance", "adherence", "participant compliance"],
    # "Intervention Notes": ["intervention notes", "observations", "implementation feedback"],
    # "Outcome 1 - Description": ["outcome", "measured outcome", "result description"],
    # "Outcome name": ["outcome name", "measured variable", "endpoint"],
    # "Time points measured (specify whether from start or end of intervention)": ["time points measured", "measurement schedule"],
    # "Time points reported": ["time points reported", "reported measurements"],
    # "Outcome definition (with diagnostic criteria if relevant)": ["outcome definition", "diagnostic criteria", "criteria for outcome"],
    # "Person measuring/reporting": ["person measuring", "reporting individual", "measurement personnel"],
    # "Unit of measurement (if relevant)": ["unit of measurement", "measurement unit"],
    # "Scales: upper and lower limits (indicate whether high or low score is good)": ["scales", "upper limit", "lower limit", "score interpretation"],
    # "Is outcome/tool validated?": ["outcome validation", "validated tool", "validation status"],
    # "Imputation of missing data (e.g. assumptions made for ITT analysis)": ["imputation", "missing data", "data assumptions"],
    # "Assumed risk estimate (e.g. baseline or population risk noted in Background)": ["assumed risk", "baseline risk", "population risk"],
    # "Power (e.g. power & sample size calculation, level of power achieved)": ["power", "sample size", "power calculation"],
    # "Outcome Notes": ["outcome notes", "result observations", "notes on outcome"],
    # "Study funding sources (including role of funders)": ["funding", "funder role", "study funding"],
    # "Possible conflicts of interest (for study authors)": ["conflicts of interest", "study authors", "potential bias"],
    # "Other Notes": ["general notes", "additional observations", "study feedback"]
}

# Function to query OpenAI GPT for additional insights
def query_chatgpt(prompt):
    response = client.chat.completions.create(
        engine="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )
    return response.choices[0].text.strip()

def clean_text(text_input):
    ret = text_input.strip().strip("`").strip('csv').strip()
    return ret

def write_csv(rows):
    output_file_path = pdf_directory + output_file
    with open(output_file_path, 'w') as f:
        print(f"Writing output to {output_file_path}")
        f.writelines(rows)

# Main function to iterate over PDFs and extract thematic information
def main():

    prompt_theme_str = ""
    for theme, subthemes in themes.items():
        prompt_theme_str += "Theme: " + theme
        prompt_theme_str += "\n"
        for subtheme in subthemes:
            prompt_theme_str += "\tSubtheme: " + subtheme + "\n"
    

    # Create a thread and attach the file to the message
    example_theme = {
        "example_theme_1": ["example_subtheme_a", "example_subtheme_b"],
        "example_theme_2": ["example_subtheme_c"]
    }
    example_theme_output = "source_pdf, example_theme_1:example_subtheme_a, example_theme_1:example_subtheme_b, example_theme_2:example_subtheme_c,"
    msg_instruction = f"""
    For each PDF in the knowledge store, analyze the following themes and subthemes from the experiments and research described in the PDF:
        {prompt_theme_str}
    Parse information out of the PDFs and output a CSV object for each distinct PDF, with the CSV column headers being of the format 'theme: subtheme'. The first column should be the name of the source PDF.
    For example, for the given themes and subthemes:
        {example_theme}
    The column headers should look like:
        {example_theme_output}
    Do not return any system message, only return the CSV. Make sure the column keys are sorted in alphabetical order.
    """
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": msg_instruction,
            }
        ],
    )
    
    global_instructions = "You are a data cleaner research assistant. Use the knowledge base of PDFs to transform PDF data into cleaned, summarized information."

    print("Running prompt")
    print(msg_instruction)
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant_id,
        instructions=global_instructions
    )

    start = time.time()
    print("Starting to wait for prompt to complete")
    while run.status != "completed":
        print("Waiting for run to complete for {:.2f} seconds".format(time.time() - start))
        if time.time() - start > 300:
            print("Aborting, took over 5 minutes")
            exit(1)
        time.sleep(5)

    print("Finished prompt, starting to parse messages")
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )

    rows = []
    idx = 0
    for message in messages:
        try:
            print(f"Processing message {idx}")
            for blob in message.content:
                data = clean_text(blob.text.value)
                rows.append(data)
        except Exception as e:
            # ignore any errors
            print(e)
            pass
        finally:
            idx += 1
    
    print("Writing out to file")
    write_csv(rows[:-1])

if __name__ == "__main__":
    main()
