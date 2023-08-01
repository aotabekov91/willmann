from ubuntu:22.04

env LIBGL_ALWAYS_INDIRECT=1

run apt-get update && apt-get -y install libgl1
run apt-get -y install git
run apt-get -y install python3-pip  && apt-get -y install python3-pip
run git clone https://github.com/aotabekov91/plug
run cd plug && pip install -r requirements.txt -e . 

cmd ["python3", "-c", "import plug"]
