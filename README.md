## Goal of the project
The goal is to have an automated test for medical EEG devices sold by OSG BV Belgium. The device needs to be plugged in, the test needs to be started, everything else should work on it's own. This project works with BrainRT, the software developped and used by OSG.

## Requirements
A server is required to run a database and some php scripts to start the tests and add new devices to the database. The database can be set up using setupDB.sql. 
The librairies needed can be found in requirements.txt
The protocols in BrainRT need to have a few specific settings: 
- The vertical scaling should be set to 2000 uV
- The horizontal scaling should be set to 2 sec
- Horizontal scaling lines should be on at all times, set to 4000 uV
- Only 5 of the signals on channels should be visible at the same time, enough different protocols should exist to make sure that every channel is visible at least once (this is for the screenshot in the report the project makes)
