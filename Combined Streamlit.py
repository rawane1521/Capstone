#importing libraries
import streamlit as st
import numpy as np
import pandas as pd 
import os
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import spacy
from spacy.matcher import PhraseMatcher
import skillNer
import plotly
import plotly.graph_objs as go
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
plt.style.use("seaborn-whitegrid")
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings("ignore")
from plotly import tools
import matplotlib.pyplot as plt



im = Image.open("Forward-MENA-logo.png")

st.set_page_config(
    page_title="ForasTech Skilling Tools",
    page_icon=im,
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)


#Navigation Bar
Menu = option_menu(None, ["Home", "Scraping","Skills Extraction","Score Matching"],icons=['house','pen','search',"code"],menu_icon="cast", default_index=0, orientation="horizontal", styles={"container": {"padding": "0!important", "background-color": "#B0C4DE"},"icon": {"color": "black", "font-size": "25px"}, "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},"nav-link-selected": {"background-color": "#4F6272"},})



#Setting Conditions 
video_file = open('FMQ_Digital-World_Music-only-2.mp4', 'rb')
video_bytes = video_file.read()
if Menu == "Home": st.video(video_bytes)
if Menu == "Home": st.title("FIND OUT ABOUT THE TOP SKILLS NEEDED IN THE MARKET TODAY!")
if Menu == "Home":st.write("77% believe there is a gap between the job requirementsand the university graduate qualifications. As the world moves at a rapid pace towards digitalization, the gap  is exponentially growing. Accordingly, we have taken on the role of filling this gap.")
if Menu == "Home":st.write("We will help you learn about the most in-demand careers, assess your skills, get certified and find the right job. To do so, please surf our offered tools to go through a career aspiration path.")

if Menu== "Scraping": 
    import time
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from webdriver_manager.chrome import ChromeDriverManager

    job_descriptions, job_titles, Positions = [], [], []

    # function to run code based on input
    def scrapeWeb(query, website):
        driver = webdriver.Chrome(ChromeDriverManager().install())
        if dropdown_value == "Bayt.com":
            # code A logic
            base_url = "https://www.bayt.com/en/"
            # web page url
            driver.get(base_url)
            time.sleep(1)
            # input search query
            ## look for search bar location
            search_bar = driver.find_element(By.ID, "text_search")
            ## enter text
            search_bar.send_keys(query)
            time.sleep(1)
            ## look for search button loacation
            search_button = driver.find_element(By.ID, "search_icon_submit")
            ## click button
            search_button.click()
            time.sleep(1)
            # get job urls
            job_urls = driver.find_elements(By.XPATH, "//a[@data-js-aid='jobID']")
            job_urls = [elem.get_attribute("href") for elem in job_urls]

            # loop over urls
            
            for url in job_urls:
                # open url
                driver.get(url)
                
                try:
                    # get job description
                    job_description = driver.find_element(By.XPATH, "//div[@class='card-content is-spaced']")
                    job_description = job_description.text
                except:
                    break
                
                # get job title
                job_title = driver.find_element(By.ID, "job_title")
                job_title = job_title.text

                # append to list
                job_descriptions.append(job_description)

                # append to list
                job_titles.append(job_title)


                # append to list
                Positions.append(query)

                # sleep
                time.sleep(1)
                
                
            output_data = pd.DataFrame(data={"Positions":Positions, "job title":job_titles, "job description":job_descriptions})
            
            return output_data
            
        elif dropdown_value == "DaleelMadani.com":
                # code B logic
            base_url = "https://daleel-madani.org/jobs/"
            
            driver.get(base_url)
            time.sleep(1)
        
            # input search query
            ## look for search bar location
            search_bar = driver.find_element(By.ID, "edit-search-api-views-fulltext")
            ## enter text
            search_bar.send_keys(query)
            time.sleep(1)
            ## look for search button loacation
            search_button = driver.find_element(By.ID, "edit-submit-jobs-index-dm-jobs")
            ## click button
            search_button.click()
            time.sleep(1)

            # get job urls
            job_urls = driver.find_elements(By.XPATH, "//div[@class='field-item even']//h4//a")
            job_urls = [elem.get_attribute("href") for elem in job_urls]

            # loop over all jobs

            for url in job_urls:
                # open url
                driver.get(url)

                # get job description
                job_description = driver.find_element(By.XPATH, "//div[@class='field field-name-body field-type-text-with-summary field-label-above']")
                job_description = job_description.text

                # get job title
                job_title = driver.find_element(By.XPATH, "//div[@class='field-item even']//h1")
                job_title = job_title.text

                # append to list
                job_descriptions.append(job_description)

                # append to list
                job_titles.append(job_title)

                # append to list
                Positions.append(query)

                # sleep
                time.sleep(1)

            output_data = pd.DataFrame(data={"Positions":Positions, "job title":job_titles, "job description":job_descriptions})
            return output_data
        
        elif dropdown_value == "jobsforlebanon.com":
            base_url = "https://www.jobsforlebanon.com"
            driver.get(base_url)
            time.sleep(1)

            # input search query
            ## look for search bar location
            search_bar = driver.find_element(By.ID, "ui-search-terms")
            ## enter text
            search_bar.send_keys(query)
            time.sleep(1)
            ## look for search button loacation
            search_button = driver.find_element(By.XPATH, "//input[@type='submit']")
            ## click button
            search_button.click()
            time.sleep(1)

            # get job urls
            job_urls = driver.find_elements(By.XPATH, "//div[@class='catalogue-job']")
            job_urls = [elem.get_attribute("data-href") for elem in job_urls]
            
            for url in job_urls:
                # open url
                driver.get(url)

                # get job description
                job_description = driver.find_element(By.XPATH, "//div[@itemprop='description']")
                job_description = job_description.text

                # get job title
                job_title = driver.find_element(By.XPATH, "//main[@class='jobad-main job']//h1")
                job_title = job_title.text

                # append to list
                job_descriptions.append(job_description)

                # append to list
                job_titles.append(job_title)

                # append to list
                Positions.append(query)

                # sleep
                time.sleep(1)
            
            output_data = pd.DataFrame(data={"Positions":Positions, "job title":job_titles, "job description":job_descriptions})
            
            return output_data

        else:
            return None

    # set up streamlit app
    st.title('ForasTech Job Scraping Tool:')

    # dropdown for user to choose code
    dropdown_value = st.selectbox('Select a website to scrape:', ['Bayt.com', 'DaleelMadani.com', 'jobsforlebanon.com'])

    # input text box for user to enter input
    input_text = st.text_input('Enter Job Position:')

    # Create a button to download the output file
    from io import BytesIO
    def download_button(df):
        output = BytesIO()
        excel_writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(excel_writer, sheet_name='Sheet1', index=False)
        excel_writer.save()
        processed_data = output.getvalue()
        return processed_data

    # search button to run code
    if st.button('Search'):
        # run code and display output
        output_data = scrapeWeb(input_text, dropdown_value)
        if output_data is not None:
            st.dataframe(output_data)
            processed_data = download_button(output_data)
            st.download_button(label='Download Results',
                        data=processed_data,
                        file_name='output.xlsx',
                        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


if Menu == "Skills Extraction": 

    # load default skills data base
    from skillNer.general_params import SKILL_DB
    # import skill extractor
    from skillNer.skill_extractor_class import SkillExtractor
    # init params of skill extractor
    nlp = spacy.load("en_core_web_lg")
    # init skill extractor
    skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)

    st.title("ForasTech Skills Extraction Tool:")
    #enter the job description
    job_description = st.text_area('Enter the job description:')

    if st.button('Run'):
        annotations = skill_extractor.annotate(job_description)
        doc_node_values = [match['doc_node_value'] for match in annotations['results']['ngram_scored']]
        unique_skills = list(set(doc_node_values))
        st.write(f"Skills Extracted: {unique_skills}")
        
        # Create a WordCloud object
        wordcloud = WordCloud(width=800, height=800, background_color='white', colormap='inferno', max_words=50).generate_from_text(' '.join(unique_skills))

        # Plot the WordCloud image
        st.set_option('deprecation.showPyplotGlobalUse', False)
        plt.figure(figsize=(8,8))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        st.pyplot()    


if Menu == "Score Matching": 
    # Load data from CSV file
    df = pd.read_excel('ExtractedSkills.xlsx')

    # Create list of unique job names
    job_names = df["Original JT"].unique().tolist()
    job_names.sort()

    # Sidebar widgets for selecting job name
    selected_job = st.sidebar.selectbox("Select a job", [job.title() for job in job_names])

    # Filter DataFrame based on selected job
    job_df = df[df["Original JT"] == selected_job.lower()]

    # Get the top 5 SS and top 5 HS repeated or counted skills in the DataFrame of the selected job
    ss_skills = job_df[job_df["type"] == "ss"]["OrgSkill"].value_counts().sort_values(ascending=False).index.tolist()
    hs_skills = job_df[job_df["type"] == "hs"]["OrgSkill"].value_counts().sort_values(ascending=False).index.tolist()

    # Dictionary to map proficiency level to multiplication factor
    proficiency_mapping = {"Beginner": 1/3, "Intermediate": 2/3, "Proficient": 1}

    # Sidebar widgets for selecting SS and HS skills with proficiency level
    select_ss_skills = st.sidebar.multiselect("Select the Soft Skills you acquire:", ss_skills, format_func=lambda x: x.title())
    ss_proficiency = {}
    for skill in select_ss_skills:
        proficiency = st.sidebar.radio(f"Select your proficiency level in  '{skill.title()}':", ["Beginner", "Intermediate", "Proficient"])
        ss_proficiency[skill] = proficiency

    select_hs_skills = st.sidebar.multiselect("Select the Hard Skills you acquire:", hs_skills, format_func=lambda x: x.title())
    hs_proficiency = {}
    for skill in select_hs_skills:
        proficiency = st.sidebar.radio(f"Select your proficiency level in  '{skill.title()}':", ["Beginner", "Intermediate", "Proficient"])
        hs_proficiency[skill] = proficiency

    # Calculate matching score
    total_ss_skills = len(ss_skills)
    total_hs_skills = len(hs_skills)
    total_skills = total_ss_skills + total_hs_skills
    matching_score = 0

    # Calculate score for selected SS skills
    for skill in select_ss_skills:
        proficiency = ss_proficiency[skill]
        if skill in ss_skills[:5]:
            matching_score += 0.08 * proficiency_mapping[proficiency]
        else:
            matching_score += (20 / (total_skills - 10) / 100) * proficiency_mapping[proficiency]

    # Calculate score for selected HS skills
    for skill in select_hs_skills:
        proficiency = hs_proficiency[skill]
        if skill in hs_skills[:5]:
            matching_score += 0.08 * proficiency_mapping[proficiency]
        else:
            matching_score += (20 / (total_skills - 10) / 100) * proficiency_mapping[proficiency]

    # Round matching score to 2 decimal places
    matching_score = round(matching_score * 100, 2)

    # Display job name as title and matching score in the center of the screen
    st.title("ForasTech Matching Score Calculation Tool:")
    st.header(f"Matching score for {selected_job} is: {matching_score}%")

    if matching_score <= 65:
        st.write("To enhance your skills in this field, you can start a learning path course or training on our website and get certified!")
    else:
        st.write("Continue learning more skills to gain competitive edge! The sky is the limit.")
