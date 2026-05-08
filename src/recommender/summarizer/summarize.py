from transformers import pipeline

# This forces the pipeline to use a specific summarization model
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def generate_summary(text):
    # limit output to 50 tokens
    result = summarizer(text, max_length=50, do_sample=False)
    return result[0]['generated_text']