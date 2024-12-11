import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()
os.getenv("GROQ_API_KEY")

class Chain:
    def __init__(self):
        self.llm = ChatGroq(model="llama-3.1-70b-versatile",temperature=0,groq_api_key=os.getenv("GROQ_API_KEY"))

    def retrieve_job_postings_text(self, text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the 
            following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (WITH NO PREAMBLE):    
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={'data':text})
        print(res.content)
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Unable to parse job postings.")
        return res if isinstance(res, list) else [res]
    
    def write_mail(self, job, a_query):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}
            
            ### INSTRUCTION:
            You are Josh, a General Manager at Adobe. Adobe is a leading software company known for its innovative solutions that 
            empower individuals and businesses to create, manage, and deliver exceptional digital experiences. Your role involves 
            overseeing operations and driving strategic initiatives that enhance productivity and creativity across various sectors. 
            Your task is to write a cold email to a potential client, highlighting Adobe's capabilities in meeting their specific 
            needs with tailored solutions. Additionally, incorporate relevant examples from the following links to showcase Adobe's 
            portfolio: {link_list}. Remember, you are Josh, General Manager at Adobe.
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):
            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job), "link_list": a_query})
        return res.content


if __name__=="__main__":
    print("")