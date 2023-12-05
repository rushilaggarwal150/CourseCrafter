from langchain.chat_models import ChatOpenAI
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from langchain.prompts import PromptTemplate
from langchain.chains import (
    StuffDocumentsChain, LLMChain, ConversationalRetrievalChain
)
import json
# from flask import Flask, request, jsonify
# from flask_cors import CORS
import streamlit as st
import plost
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

# app = Flask(__name__)
# CORS(app)

def initialize():

    template = '''I'm trying to run cosine similarity on a user-generated text input against a number of course descriptions. To do this, I will need to convert the user-generated text input into a course description. Using your own knowledge of the content of computer science classes as well as the examples below, you will create the course description. Your description should be a little bit longer and more verbose than the examples.

    Here are some examples of user inputs and relevant course descriptions:
    User: "I'm interested in low-level languages"
    Assistant: "Principles of embedded system architecture and programming; fundamentals and theoretical foundations of wireless communication systems; hands-on experiences of how an embedded system could be used to solve problems in biomedical engineering; projects on wireless sensors and imaging for medical devices. Programming language translation; functions and general organization of compiler design and interpreters; theoretical and implementation aspects of lexical scanners; parsing of context free languages; code generation and optimization; error recovery. Security principles; common security features and flaws in day-to-day embedded systems; security analysis, vulnerability exploits and security fixes for embedded systems."


    User: "I like Big Data and want to work in the cloud one day"
    Assistant: "Operating system and distributed systems fields that form the basis of cloud computing such as virtualization, key-value storage solutions, group membership, failure detection, peer to peer systems, datacenter networking, resource management and scalability; popular frameworks such as MapReduce and HDFS and case studies on failure determination. Theoretical foundations, algorithms and methods of data analytics for cybersecurity; study of data analytics including cluster analysis, supervised machine learning, anomaly detection, and visualization applied to cyber attacks, anomaly detection, vulnerability analysis, strategic manipulation, propaganda and other topics. Representation of, storage of and access to very large multimedia document collections; fundamental data structures and algorithms of current information storage and retrieval systems and relates various techniques to design and evaluation of complete retrieval systems."


    User: "Machine learning"
    Assistant: "Theoretical foundations of machine learning, pattern recognition and generating predictive models and classifiers from data; includes methods for supervised and unsupervised learning (decision trees, linear discriminants, neural networks, Gaussian models, non-parametric models, clustering, dimensionality reduction, deep learning), optimization procedures and statistical inference. Theoretical foundations, algorithms and methods of data analytics for cybersecurity; study of data analytics including cluster analysis, supervised machine learning, anomaly detection, and visualization applied to cyber attacks, anomaly detection, vulnerability analysis, strategic manipulation, propaganda and other topics. Fundamental concepts and techniques of intelligent systems; representation and interpretation of knowledge on a computer; search strategies and control; active research areas and applications such as notational systems, natural language understanding, vision systems, planning algorithms, intelligent agents and expert systems."

    Convert the following user-generated string into a course description. Do not include anything other than the description in your response. Here is the user-generated string:
    {user}'''

    prompt = PromptTemplate(
        input_variables=["adjective"], template=template
    )
    llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.01, verbose=True)
    llm_chain = LLMChain(llm=llm, prompt=prompt, verbose=True)

    return llm_chain

def run(llm_chain):
    llm_response = llm_chain.run('''I'm really interested in low-level programming. I would love to work for a company that would allow me to work on operating systems or on embedded devices. Using a language like C would be great.''')

    # print(llm_response)
    return llm_response


def create_index_from_file(file_path):
    index = []
    with open(file_path, 'r') as file:
        for line in file:
            cleaned_line = line.strip()
            index.append(cleaned_line)
    return index

def find_name_by_number(courses, course_number):
    for course in courses:
        if course["Course Number"] == course_number:
            return course["Course Name"]
    return None

def find_desc_by_number(courses, course_number):
    for course in courses:
        if course["Course Number"] == course_number:
            return course["Description"]
    return None

def find_diff_by_number(courses, course_number):
    for course in courses:
        if course["Course Number"] == course_number:
            return course["Difficulty"]
    return None


# @app.route('/process_user_input', methods=['POST'])
def process_user_input():
    # Load course data
    file_path = 'updated_courses_data.json'

    with open(file_path, 'r') as file:
        data = json.load(file)
    courses = data['courses']

    # user_input = request.json.get('user_input')
    user_input = st.text_input("What are your computer science interests or career goals?")

    llm_chain = initialize()
    llm_response = llm_chain.run(user_input)

    file_path = 'Data_Files/CatalogWithProfessors.txt'
    index = create_index_from_file(file_path)


    # Calculate similarities
    vectorizer = TfidfVectorizer()
    similarity_dict = {}
    for course in courses:
        course_desc = course["Description"]
        tfidf_matrix = vectorizer.fit_transform([llm_response, course_desc])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

        similarity_dict[similarity[0][0]] = i[19:22]

    # Sort and scale values
    sorted_similarities = sorted(similarity_dict.items(), reverse=True)
    max_value = max(item[0] for item in sorted_similarities)
    scaled_vals = [{"val": item[0], "course_number": item[1], "relevance": item[0] * 100} for item in sorted_similarities]

    # Add course name and description
    for item in scaled_vals:
        print(item["course_number"], "HELP")
        number = item["course_number"]

        item["course_name"] = find_name_by_number(courses, number)
        item["description"] = find_desc_by_number(courses, number)
        item["difficulty"] = find_diff_by_number(courses, number)


    return json.dumps(scaled_vals, indent=4)


if __name__ == '__main__':
    # app.run(host='0.0.0.0', debug=True)
    print("Started")

    st.title("CourseCrafter")
    
    # llm_chain = initialize()
    # llm_response = run(llm_chain=llm_chain)
    # file_path = 'Data_Files/Catalog.txt'
    # index = create_index_from_file(file_path)
    # json_string = find_similar_courses(index=index, llm_response=llm_response)
    # data = json.loads(json_string)
    # print(json_string)
    # df = pd.DataFrame(data)

    json_data = process_user_input()
    if isinstance(json_data, str):
        data = json.loads(json_data)
        print("1")
    else:
        data = json_data
        print("2")
    df = pd.DataFrame(data)
    # df['difficulty'] = pd.to_numeric(df['difficulty'])
    # df['scaled_val'] = pd.to_numeric(df['scaled_val'])
    print(df)
    print(len(df))
    print(json_data)

    plost.scatter_chart(
        df,
        x="difficulty",
        y="scaled_val",
        opacity="course_number",
        size="course_number"
    )
    
    
    for index, row in df.iterrows():
        if index >= 5:
            break
        st.write("CSCE", row["course_number"], "-", row["course_name"], "-", row["course_desc"])
        st.write("Difficulty:", row["difficulty"], "Relevance:", str(round(row["scaled_val"], 2)))
        st.write()