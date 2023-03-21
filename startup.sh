
sudo apt-get update
sudo apt-get install -y python3 python3-pip git
git clone git@github.com:CSCI-5828-Foundations-Sftware-Engr/AgileAvengers.git
#cd flask-tutorial
sudo python3 setup.py install
sudo pip3 install -e 
sudo pip3 install pillow jsonpickle

export FLASK_APP=app.py
#flask init-db
nohup flask run -h 0.0.0.0 &