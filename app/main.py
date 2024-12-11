import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from skills_portfolio import SkillsPortfolio
from utils import clean_text
from chains import Chain

def streamlit_app(llm,skills_portfolio,clean_text):
    st.title("📨 WarmUpMailer")
    input_url = st.text_input("Enter a URL:", value="https://flutterjobs.com/jobs/349-mobile-developer-flutter-sii-poland")
    submit = st.button("Submit Button")

    if submit:
        try:
            web_loader = WebBaseLoader([input_url])
            page_data = clean_text(web_loader.load().pop().page_content)
            skills_portfolio.load_skills_portfolio()
            job_listings = llm.retrieve_job_postings_text(page_data)
            if job_listings:
                for job in job_listings:
                    required_skills = job.get('skills', [])
                    a_query = skills_portfolio.query(required_skills)
                    email_content = llm.write_mail(job, a_query)
                    if email_content:
                        st.code(email_content, language='markdown')
                    else:
                        st.warning("Email content could not be generated")
            else:
                st.warning("No job listings found")
        except Exception as error:
            st.error(f"An Error Occurred: {error}")


if __name__=="__main__":
    chain = Chain()
    skills_portfolio = SkillsPortfolio()
    st.set_page_config(layout="wide", page_title="  WarmUpMailer",page_icon="📨")
    streamlit_app(chain, skills_portfolio, clean_text)