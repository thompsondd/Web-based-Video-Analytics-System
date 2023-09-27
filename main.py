import streamlit as st
from pytube import YouTube
from yolo import AI_see
import os, torch

# Pape setup
st.set_page_config(
    page_title="Video Analyse",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",

)

# GPU checking
device = (
            "cuda"
            if torch.cuda.is_available()
            else "mps"
            if torch.backends.mps.is_available()
            else "cpu"
        )

config = {
    "upload_folder": "./static/uploads",
    "model_folder": "./static/models"
}

if device == "cpu":
    # st.info('')
    # st.info('')
    notification1 = '''- **Please select short video (<15s) to see the processed video in the shorter time due to not finding GPU**'''
    notification2 = '''- **Note that you can select the longer one but it will take a long time to run!**'''
    st.markdown(notification1)
    st.markdown(notification2)


tab1, tab2 = st.tabs(["Upload a video","Get a video from URL"])

model, path, path_url = None, None, None
if model is not None:
    del model
    
with tab1:
    file = st.file_uploader("Upload video")
    if file != None:
        path_video = os.path.join(config["upload_folder"], "ignore_temp.mp4")
        with open(path_video,"wb+") as f:
            f.write(file.read())
        
        col1, col2 = st.columns(2)
        with col1:
            status = st.header('Uploaded Video', divider='rainbow')
            st.markdown(" ")
            st.markdown(" ")
            st.markdown(" ")
            st.video(path_video)

        with col2:
            st.header('Processed Video', divider='rainbow')
            with st.spinner('Wait for loading model'):
                model = AI_see(path_video,config["model_folder"])
            my_bar = st.progress(0.0, text="AI is working. Give model a few seconds!")
            file_url_done = model.create_video(my_bar)
            my_bar.progress(1.0, text="Done !")
            st.video(file_url_done)

with tab2:
    with st.form("my_form"):
        video_url = st.text_input("Youtube URL:")
        submitted = st.form_submit_button("Submit")
    if submitted:
        try:
            with st.spinner('Wait for loading video'):
                yt = YouTube(video_url)
                stream = yt.streams.get_highest_resolution()
                stream.download(config["upload_folder"],"ignore_url_temp.mp4")

            path_url = os.path.join(config["upload_folder"],"ignore_url_temp.mp4")
        except Exception as e:
            status = st.warning("Library error - The error is from the pytube library")
            status = st.warning("Please wait for finding the alternatives")
            
        try:
            col1, col2 = st.columns(2)
            with col1:
                status = st.header('Video from URL', divider='rainbow')
                st.markdown(" ")
                st.markdown(" ")
                st.markdown(" ")
                st.video(path_url)

            with col2:
                st.header('Processed Video', divider='rainbow')
                with st.spinner('Wait for loading model'):
                    model = AI_see(path_url, config["model_folder"])

                my_bar_url = st.progress(0.0, text="AI is working. Give model a few seconds!")
                file_url_done = model.create_video(my_bar_url)
                my_bar.progress(1.0, text="Done !")
                st.video(file_url_done)

        except Exception as e:
            status = st.warning("Please use valid URL!")