# FROM python:alpine3.17

# # Set the working directory inside the container
# WORKDIR /app

# # Copy the Python requirements file and install the dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the Python code to the container
# COPY . .

# # Set the default command to run when the container starts
# CMD ["python3","app.py"]

FROM nats:alpine

COPY nats.conf ws.conf

CMD [ "-c", "ws.conf" ]
