from sys import exception
from youtube_transcript_api import YouTubeTranscriptApi
import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda


st.title("🎬 YouTube Transcript Chatbot")
video_id = st.text_input("Paste Video URL Here")
check_transcript = st.button("Check Transcript Availability")
question = st.chat_input("Ask your Question")



def extract_id(video_id):
    if("v=" in video_id):
        return video_id.split("v=")[-1].split("&")[0]
    elif("youtu.be/"in video_id):
        return video_id.split("youtu.be/")[-1].split("?")[0]    
    return video_id    
def get_transcript(transcript):
                transcript_list = []
                for i in transcript:
                    transcript_list.append(i['text'])
                return " ".join(transcript_list)


if check_transcript and video_id:
    with st.spinner("processing"):
        try:
            video_id = extract_id(video_id)
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
            final_transcript = get_transcript(transcript)
            if final_transcript:
                st.success("✅ Transcript is available for this video.")
            else:
                st.error("🚨 No transcript found.") 
        except Exception as e:
            st.error(f"🚨 Error: {str(e)}")

if video_id and question:
    with st.spinner("Processing"):
            video_id = extract_id(video_id)
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
            final_transcript = get_transcript(transcript)

            ##Text Splitter

            splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
            chunks = splitter.split_text(final_transcript)

            ##Vector Store



            embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

            vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings)
            vectorstore.save_local("faiss_index")

            ## Reteiever

            retriever = vectorstore.as_retriever(search_type = "mmr", search_kwargs= {"k": 3})

            ## Chat Groq Model



            model = ChatGroq(model= "llama3-8b-8192",api_key=os.getenv("GROQ_API_KEY"))

            ##Prompt Template



            prompt = ChatPromptTemplate.from_template(
                """
                You are a helpful and detailed assistant.
            Your task is to answer the user's question based SOLELY on the provided YouTube video transcript context.
            If the context does not contain enough information to answer the question, state clearly that you don't have enough information from the transcript.
            Do not use any outside knowledge.
            When summarizing, prioritize the core content and main discussion points of the video.
            If asked for main points, provide a concise list.

            Transcript Context:
            {context}

            Question: {question}
            """)

            ##Parser



            parser = StrOutputParser()

            ## Function for joining docs

            def format_docs(retriever):
                context = "\n\n".join(doc.page_content for doc in retriever)
                return context


            ##Chains



            parallel_chain = RunnableParallel({
                "context": RunnableLambda(lambda x: x["question"])|retriever| RunnableLambda(format_docs),
                "question": RunnablePassthrough()
            })  

            ##Query and Results

            final_chain = parallel_chain|prompt|model|parser

            if question:
                with st.spinner("Thinking..."):
                    result = final_chain.invoke({"question": question})
                    st.success("Answer:")
                    st.write(result)

