from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone
import os
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import TextLoader
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from langchain.prompts import PromptTemplate
from langchain.chains import (
    StuffDocumentsChain, LLMChain, ConversationalRetrievalChain
)
import json
from dotenv import load_dotenv
load_dotenv()


def initialize():
    pinecone.init(
        api_key=os.environ['PINECONE_API_KEY'],
        environment= 'asia-southeast1-gcp-free')
    index = pinecone.Index('coursecrafter')
    embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])
    vectordb = Pinecone.from_documents(documents='', embedding=embeddings, index_name='coursecrafter')

    # retriever = vectordb.as_retriever(k=10)

    template = '''I'm trying to run cosine similarity on a user-generated text input against a number of course descriptions. To do this, I will need to convert the user-generated text input into a course description. Using your own knowledge of the content of computer science classes as well as the examples below, you will create the course description. Your description should be a little bit longer and more verbose than the examples.

    Here are some examples of course descriptions:

    Course Title: CSCE 411 Design and Analysis of Algorithms, Description: Credits 3.  3 Lecture Hours.       Study of computer algorithms for numeric and non-numeric problems; design paradigms; analysis of time and space requirements of algorithms; correctness of algorithms; NP-completeness and undecidability of problems. Prerequisite:  Grade of C or better in CSCE 221 and CSCE 222/ECEN 222; junior or senior classification or approval of instructor.
    Course Title: CSCE 412 Cloud Computing, Description: Credits 3.  3 Lecture Hours.       Operating system and distributed systems fields that form the basis of cloud computing such as virtualization, key-value storage solutions, group membership, failure detection, peer to peer systems, datacenter networking, resource management and scalability; popular frameworks such as MapReduce and HDFS and case studies on failure determination. Prerequisite:  Grade of C or better in CSCE 315 or CSCE 331.
    Course Title: CSCE 413 Software Security, Description: Credits 3.  3 Lecture Hours.       Basic principles of design and implementation of defect-free software, code reviews including tool-assisted review by static and dynamic analysis, risk analysis and management and methods for software security testing. Prerequisites:  Grade of C or better in CSCE 315 or CSCE 331; or approval of instructor.

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

def find_similar_courses(index, llm_response):
    vectorizer = TfidfVectorizer()
    dict = {}
    for i in index:
        tfidf_matrix = vectorizer.fit_transform([llm_response, i])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        dict[similarity[0][0]] = i[20:23]
        # print(similarity[0][0], i[20:23])

    dict = sorted(dict.items(), reverse=True)
    # print(dict)
    max_value = max(item[0] for item in dict)
    scaled_vals = [(item[0], item[1], (item[0] / max_value) * 100) for item in dict]
    # print(scaled_vals)

    scaled_vals = [{"val": i[0], "course_number": i[1], "scaled_val": i[2]} for i in scaled_vals]
    json_string = json.dumps(scaled_vals, indent=4)
    # print(json_string)

    return(json_string)

def rate_difficulty_courses():
    # TODO
    pass


def main():
    llm_chain = initialize()
    llm_response = run(llm_chain=llm_chain)
    file_path = 'Data_Files/Catalog.txt'
    index = create_index_from_file(file_path)
    json_string = find_similar_courses(index=index, llm_response=llm_response)
    print(json_string)

main()