# Use an official Python runtime as a parent image
FROM python:3.9-slim

COPY . /app
# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Install spaCy and Streamlit
RUN pip install --no-cache-dir spacy

# Download the English model
RUN python -m spacy download en_core_web_sm

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run app.py when the container launches
CMD ["streamlit", "run", "main.py"]