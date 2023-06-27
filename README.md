## Goal of the project
The goal is to have an automated test for medical EEG devices sold by OSG BV Belgium. The device needs to be plugged in, the test needs to be started, and everything else should work on its own. This project works with BrainRT, the software developed and used by OSG.

## Requirements
A server is required to run a database and some PHP scripts to start the tests and add new devices to the database. The database can be set up using setupDB.sql. There should be an environment variable called MYSQLUSER_OSG which contains your username in the database an environment variable called MYSQLPASSWORD_OSG which contains your password and an environment variable called MYSQLDATABASE_OSG which contains the name of the database. The IP address in Main.py on line 31.
The libraries needed can be found in requirements.txt.
Other installations needed on the default location are: NI VISA, tesseract and Wkhtmltopdf. When these are not on the default location, change the paths in settings.py.

The protocols in BrainRT need to have a few specific settings: 
- The vertical scaling should be set to 2000 uV
- The horizontal scaling should be set to 2 sec
- Horizontal scaling lines should be on at all times, set to 4000 uV
- Only 5 of the signals on channels should be visible at the same time, enough different protocols should exist to make sure that every channel is visible at least once (this is for the screenshot in the report the project makes)

when using the PHP scripts to start a test, move the PHP files to the server, when using XAMPP move the files to C:\xampp\htdocs. Generated errors from the main program will appear in a file named error.txt in the same folder.

## Setup
To help set up the database, there is a script to help finding coordinates. The script is called vindCoordinaten.py. Check if all the information needed is in the database and check if all settings in settings.py are correct for the specific set up. When adding a new relais card, don't forget to update the cards variable in settings.py.
