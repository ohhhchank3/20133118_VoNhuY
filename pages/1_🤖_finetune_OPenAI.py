import json
import os
import re
import string
import webbrowser

import openai
import pandas as pd
import plotly.express as px
import requests
import streamlit as st


def get_finetuning_metrics_with_api(job_id, api_key):
    url = f"https://api.openai.com/v1/fine_tuning/jobs/{job_id}/events?limit=250"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        events_data = response.json()["data"]
        metrics = {"epochs": [], "train_loss": []}

        for event in events_data:
            if event["type"] == "metrics" and "train_loss" in event["data"]:
                metrics["epochs"].append(event["data"]["step"])
                metrics["train_loss"].append(event["data"]["train_loss"])

        return metrics

    return None


def create_finetuning_chart(job_id, api_key):
    metrics = get_finetuning_metrics_with_api(job_id, api_key)

    if metrics and metrics["epochs"]:
        fig = px.line(x=metrics["epochs"], y=metrics["train_loss"], title="Training Loss Over Epochs")
        fig.update_layout(xaxis_title="Epoch", yaxis_title="Train Loss")
        st.plotly_chart(fig)
    else:
        st.warning("No fine-tuning metrics available for the selected job.")


def main():
    st.set_page_config(page_title="ChatGPT Finetuning", page_icon=":smiley:", layout="wide")

    with st.sidebar:
        api_key = st.text_input('Enter your API key:', '')

    # If api_key is entered, read the contents and process the data
    if api_key.startswith('sk-'):
        openai.api_key = api_key
        st.title("ChatGPT Finetuning WebUI")
        
        st.subheader("Files")
        files = openai.File.list()
        st.table(pd.DataFrame(sorted(files.data, key=lambda k: -k['created_at'])))
        
        st.subheader("Jobs")
        jobs = openai.FineTuningJob.list()
        st.table(pd.DataFrame(sorted(jobs.data, key=lambda k: -k['created_at'])))
        
        st.subheader("Finetuned Models")
        models = openai.Model.list()
        st.table(pd.DataFrame([d for d in models.data if d["id"].startswith("ft")]))
        
        st.subheader("Debug Info")
        response_display = st.empty()

        with st.sidebar:
            file = st.file_uploader("Upload a file", accept_multiple_files=False)
            
            file_ids = [d["id"] for d in sorted(files.data, key=lambda k: -k['created_at'])]
            file_id = st.selectbox("Select a file", file_ids)
            
            job_ids = [d["id"] for d in sorted(jobs.data, key=lambda k: -k['created_at'])]
            job_id = st.selectbox("Select a job", job_ids)
            # Selectbox for choosing a model
            available_models = ["babbage-002", "davinci-002", "gpt-3.5-turbo-1106", "gpt-3.5-turbo-0613"]
            selected_model = st.selectbox("Select a model", available_models)

            n_epochs = st.number_input("Number of Epochs", min_value=1, max_value=100, value=3)
            
            if file:
                uploaded_file = openai.File.create(file=file, purpose='fine-tune', user_provided_filename=file.name)
                response_display.write(uploaded_file)

            if st.button("Delete File 🗑️") and file_id:
                deleted_file = openai.File.delete(file_id)
                response_display.write(deleted_file)

            if st.button("Create Fine-Tuning Job 🚀") and file_id:
                job = openai.FineTuningJob.create(training_file=file_id, model=selected_model, hyperparameters={"n_epochs": n_epochs})
                response_display.write(job)

            if st.button("Get Fine-Tuning Job Detail ℹ️") and job_id:
                job = openai.FineTuningJob.retrieve(job_id)
                response_display.write(job)

            if st.button("List Job Events 📋") and job_id:
                events = openai.FineTuningJob.list_events(id=job_id, limit=10)
                for event in events.data:
                    response_display.write(event)

            if st.button("Cancel Job 🚫") and job_id:
                cancelled_job = openai.FineTuningJob.cancel(job_id)
                response_display.write(cancelled_job)

        if st.button("Show Fine-Tuning Chart") and job_id:
               api_key = "sess-yfxI5na4mBBOQRJcsJrf17I9oTrPub3fS0RMHqhV"  # Note: Use your actual API key
               create_finetuning_chart(job_id, api_key)


if __name__ == "__main__":
    main()
