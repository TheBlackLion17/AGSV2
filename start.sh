apt update && apt upgrade -y

apt install git -y           
pip install -U pip  

if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/TheBlackLion17/AGSV2.git /AGSV2
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /AGSV2
fi
cd /AGSV2
pip3 install -U -r requirements.txt
echo "Starting Bot...."
python3 bot.py
