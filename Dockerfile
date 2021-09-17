# base-image for python on any machine using a template variable,
# see more about dockerfile templates here: https://www.balena.io/docs/learn/develop/dockerfile/
FROM python:3

# use `install_packages` if you need to install dependencies,
# for instance if you need git, just uncomment the line below.
# RUN install_packages git

# Set our working directory
WORKDIR /app

# Copy requirements.txt first for better cache on later pushes
COPY requirements.txt requirements.txt

# pip install python deps from requirements.txt on the resin.io build server
RUN pip3 install -r requirements.txt
RUN python -m dostoevsky download fasttext-social-network-model
# This will copy all files in our root to the working  directory in the container
COPY . ./

# Enable udevd so that plugged dynamic hardware devices show up in our container.
ENV UDEV=1

EXPOSE 5000:5000

# main.py will run when container starts up on the device
CMD ["python","-u","app.py"]