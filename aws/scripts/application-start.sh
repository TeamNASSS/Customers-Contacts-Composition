cd /home/ec2-user/Customers-Contacts-Composition
sudo fuser -k 5012/tcp || true
python3 main.py > app.out.log 2> app.err.log < /dev/null &