# Use the official Python 3.9 image as the base image
FROM python:3.9

# Set the working directory within the container
WORKDIR /usr/src/app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application files into the container
COPY . .

EXPOSE 8000
CMD ["python", "-m", "chainlit", "run", "app.py", "--port" ,"8000"]