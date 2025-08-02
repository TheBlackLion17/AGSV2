if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/TheBlackLion17/Wednesday_v1.git /Wednesday_v1
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /Wednesday_v1
fi
cd /KuttuBot
pip3 install -U -r requirements.txt
echo "Starting Bot...."
python3 bot.py
