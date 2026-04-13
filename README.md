
# How to install our project <br/>

First, clone this repository and create a virtual environment using:
```
python -m venv venv
```
Activate the virtual environment:
```
./venv/Scripts/activate
```
Install the required packages using: <br/>
```
pip install -r requirements.txt
```

Create an Authy Application and grab your API Key https://www.twilio.com/console/authy/applications <br/>
Edit `config.py` and update the API key with your application key. Create a secret key for managing sessions. <br/>

`cd` to the location of the cloned repository and run the command:
```
python run.py
```
Copy `http://127.0.0.1:5000/` and paste it in the address bar of a browser.

# Working of our Website 
The front-end portion of the web application has been developed using **HTML, CSS & JavaScript** while the backend portion has been developed using **Flask & SQLite**. The information regarding the users, food items, tables and orders are stored in a database created using **SQLite**. Through the use of **Flask**, the web app interacts with the database. To verify the user's phone number, we have used **Twilio Authy API** and the delivery tracking has been implemented using **Google Maps Javascript API** and **Google Directions API**

