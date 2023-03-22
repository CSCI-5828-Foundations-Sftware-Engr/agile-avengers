sudo python3 setup.py install
sudo pip3 install -e 
sudo pip3 install pillow jsonpickle

export FLASK_APP=app.py
#flask init-db
nohup flask run -h 0.0.0.0 &
