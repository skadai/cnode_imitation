# clone 代码到 /var/www/web23

# 换源
ln -f -s /var/www/web23/misc/sources.list /etc/apt/sources.list
mkdir -p /root/.pip
ln -f -s /var/www/web23/misc/pip.conf /root/.pip/pip.conf
apt-get update

# 系统设置
apt install -y  zsh curl ufw
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
ufw allow 22
ufw allow 80
ufw allow 443
ufw default deny incoming
ufw default allow outgoing
ufw status verbose
ufw -f enable

# 装依赖
apt install -y git supervisor nginx
add-apt-repository -y ppa:deadsnakes/ppa
apt update
apt install -y python3.6
curl https://bootstrap.pypa.io/get-pip.py > /tmp/get-pip.py
python3.6 /tmp/get-pip.py
pip3 install jinja2 flask gunicorn PyMySQL SQLAlchemy
pip3 install flask eventlet flask-socketio

# 删掉 nginx default 设置
rm -f /etc/nginx/sites-enabled/default
rm -f /etc/nginx/sites-available/default

# 建立一个软连接
ln -s -f /var/www/web23/web23.conf /etc/supervisor/conf.d/web23.conf
# 不要再 sites-available 里面放任何东西
ln -s -f /var/www/web23/web23.nginx /etc/nginx/sites-enabled/web23

echo 'succsss'
echo 'ip'
hostname -I