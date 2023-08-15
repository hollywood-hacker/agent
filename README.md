# Hollywood Agent

### Install (Automated)
```
curl https://gist.githubusercontent.com/flynnemon/bac4d03bf0bfced6d3d6dde6c0d177b2/raw/c7ae882ea956a9a7f541653661270686b13235e3/gistfile1.txt | bash
```

### Install (Manual)
```
git clone https://github.com/hollywood-hacker/agent.git ./hollywood-agent
cd hollywood-agent
pip3 install -r requirements.txt
pip3 install -e .
```

### Run
```
usage: hollywood-agent start [-h] [-i IP] [-p PORT] [-si REMOTE_IP]

optional arguments:
  -h, --help            show this help message and exit
  -i IP, --ip IP        IP address of the agent
  -p PORT, --port PORT  Port number of the agent
  -si REMOTE_IP, --server-ip REMOTE_IP
                        IP address or hostname of the manager application
```

example `hollywood-agent start -i 0.0.0.0 -si hollywood-macbook-air.local`

### Development
```
make virtualenv
source .venv/bin/activate
```

