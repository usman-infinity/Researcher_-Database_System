from transformers import pipeline

# Load AI summarization model
summarizer = pipeline("summarization")

def generate_summary(text):

    result = summarizer(
        text,
        max_length=80,
        min_length=25,
        do_sample=False
    )

    return result[0]['summary_text']