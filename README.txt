SMART CROP AI — WEB-READY PROTOTYPE

This version is prepared so the user only needs to open a website after the
prototype is hosted.

IMPORTANT:
A permanent public website cannot be created just by packaging the files.
The Streamlit app must be hosted on a computer/server or cloud service.
After hosting, Android/iPhone users only open the HTTPS website link.

For local testing:
1. Install Python 3.10+ on the host computer.
2. Open a terminal in this folder.
3. Run: pip install -r requirements.txt
4. Run: streamlit run app.py

For phone testing on the same Wi-Fi:
Use the host computer's network address, for example:
http://192.168.1.10:8501

Research warning:
The disease page currently demonstrates image upload only. Connect the trained
Version 3 crop models before collecting research predictions. Do not invent
accuracy values. The weather page currently uses sample values.
