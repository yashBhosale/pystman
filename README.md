# Pystman

## A Python websocket test client with support for HTTP Basic Access Authentication

How to set up:

```
pip install -r requirements.txt
python3 pystman.py
```   

How to use:
- Put the url (with the port) in the top bar, e.g. `ws://localhost:80`
- If you're using HTTP Basic Access Auth, put the username and password into the next two text boxes.
- Hit connect
- While connected:
  - put in your input in the text box at the bottom
  - responses will show up in the text box above your input text box
  - To disconnect, hit disconnect. 

Goals for this project
- Move from PyQt to Kivy
- automated testing
- Http requests
