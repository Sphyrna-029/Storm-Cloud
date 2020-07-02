GO=/usr/local/go/bin/go
modcheck=go.mod
modinit="$GO mod init github.com/BuckarewBanzai/storm-cloud"

if [ ! -f "$modcheck" ]; then
    $modinit
fi

$GO build

docker build -t storm-cloud-api .
./control.sh stop
./control.sh start
