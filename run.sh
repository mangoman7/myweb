pip3 install -r requirements.txt
curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb && sudo dpkg -i cloudflared.deb
python3 api.py > log.txt 2>&1
cloudflared tunnel -url http://localhost:1777
