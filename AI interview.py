import streamlit as st

st.set_page_config(
    page_title="LLM",
    layout="centered"
)

st.title("AI Interview")
st.caption("Practice and Prepare for your placement")
st.caption("launched by Athiya firdose")

try:
    from groq import Groq

except ImportError:
    st.error("Groq package is not installed.")
    st.info("Add groq to your requirements.txt file and redeploy.")
    st.stop()

try:
    client = Groq(
        api_key=st.secrets["GROQ_API_KEY"]
    )

except (KeyError, FileNotFoundError):
    st.error("API key is missing. Add it in Streamlit Secrets.")
    st.stop()

st.success("Groq API connected successfully!")

st.write("Welcome to your AI Interview Assistant.")
role =st.selectbox("Job Title", ["Machine Learning Engineer", "Senior Software Engineering","data analysis","cyber security","software develovper","Others"])

if role =="Others":
    st.text_input("Enter your Job Title","XXXXXX")
model = st.selectbox(
    "choose your model",
[
"openai/gpt-oss-120b"
"openai/gpt-oss-20b"
]
)
level = st.selectbox(
    "choose your level",
    [
        "begginer","intermideate","advanced"
    ]
)
mode= st.radio("Activity",["Generate Questions","Generate Code Questions","Evaluate Answers","Improve answers"])
if mode =="Generate Question" :
    count = st.slider("Number Of Questions",1,10,5)
elif mode =="Generate code Questions" :
    topic = st.selectbox( "Select Topic",
                         [ "Python", "C++", "C", "DSA", "Aptitude","Java"])
    count= st.slider("Number of Questions",1,10,5)
else:
    question = st.text_area("Enter Interview Question Here")
    answer = st.text_area("Enter Your Answer", height=160)
   if st.button("Generate AI Response",type = "primary"):
        if mode == ["Evaluate Answer","Improve Answer"] and (not question.strip()):
            st.warning("please enter a valid Question and Answer")
            st.stop()
            topics = "Topic is" + topic +"Difficulty is" +level
    if mode == "Generate Question" :
        task = "Generate" + str(count) +"Frequently asked Interview question 3 situation based questions as well as 2 theory questions"
    elif mode == "Generate Code Questions":
        task="Generate" +str(count) + "Frequently asked Coding or technical questions for the topics"+ topic + "and give me the hints with accurate performance."
    elif mode == "Evaluate Answers":
        task = "Question:"+ question + "Answer: "+answer+"Evaluate the answer based on the question and identify the drawbacks ."
    elif mode == "Improve Answer" :
        task = "Question:" = question + "Answer: " + answer + "Improve the answer based on the result and highligth the important points."
          try:

        with st.spinner("Generating AI Response..."):

            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Act as an expert Technical Interviewer "
                            "and HR professional. Provide accurate, "
                            "clear, and helpful interview guidance."
                        )
                    },
                    {
                        "role": "user",
                        "content": background + task
                    }
                ],
                temperature=0.7,
                max_tokens=1800
            )

            output = response.choices[0].message.content

      
        st.subheader("AI Response")
        st.markdown(output)

        
        st.download_button(
            label="Download Response",
            data=output,
            file_name="Interview_Response.txt",
            mime="text/plain"
        )

    except Exception as e:

        st.error(f"API connection was unsuccessful: {e}")
        st.info("Please check your API key, model availability, and rate limits.")
st.caption("Powered by Streamlit and Groq LLM API")
