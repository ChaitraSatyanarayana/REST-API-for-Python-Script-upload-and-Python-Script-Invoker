->POST request will upload a file to the server
->server stores that file and send the id created for that file to the client
->GET request will invoke the python script whose id is specified in the request

Below are the steps to run the server.py

1) Export flask APP for the server.py
    $ export FLASK_APP=server.py

2) run the flask application by assigning port 8000 to it
    $ python -m flask run --port=8000

The destination folder is wrt to the author's machine.If you wish to change,
To change the destination folder (where server saves the posted files)
    change the variable 'Destination_folder' in server.py to the target folder path
  
