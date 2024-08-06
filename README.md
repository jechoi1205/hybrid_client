# hybrid_client

# client program setting



## [git 내려받기]
```
git clone https://github.com/jechoi1205/hybrid_client.git
* username: jechoi1205
* password: 
```


## [패키지 설치]
```
pip install -r requirements.txt
```


## [.env 파일 수정]
```
SERVER_URL과 RABBITMQ_HOST 부분에 API server의 IP address 입력하기

* SERVER_URL=http://192.168.0.5:8001
* RABBITMQ_HOST="192.168.0.5"
```

## [팝업창을 위한 python tkinter 설치]
```
[MacOS]
brew install tcl-tk@python3.11

export PATH="/usr/local/opt/tcl-tk/bin:$PATH"
export LDFLAGS="-L/usr/local/opt/tcl-tk/lib"
export CPPFLAGS="-I/usr/local/opt/tcl-tk/include"
export PKG_CONFIG_PATH="/usr/local/opt/tcl-tk/lib/pkgconfig"

source .zshrc

[Ubuntu]
sudo apt-get update
sudo apt-get install python3-tk

[CentOS]
sudo yum install python3-tkinter
```