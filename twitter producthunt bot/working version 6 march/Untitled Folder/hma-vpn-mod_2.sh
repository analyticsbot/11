#!/bin/bash

cd `dirname $0`

curl=`which curl`
if [ "$curl" == "" ]; then
  curl=`which wget`
  if [ "$curl" == "" ]; then
    echo <<EOF
Error: Please install curl or wget for this script to work.
You can try any of the following commands:
apt-get install wget
yum install wget
apt-get install curl
yum install curl
EOF
    exit 1
  else
    curl="$curl -T 5 -O - "
  fi
else
  curl="$curl --connect-timeout 5 -s"
fi

openvpn=`which openvpn`
if [ "$openvpn" == "" ] ; then
    cat <<EOF
Error: Please install openvpn for this script to work.
You can try any of the following commands:
apt-get install openvpn
yum install openvpn
EOF
    exit 1
fi

proto=
list=0
while getopts "lp:" parm
do
	case $parm in
	l)
		list=1
		;;
	p)
		proto="$OPTARG"
		;;
	?)	echo "unknown $parm / $OPTARG"
	esac
done

shift $(( $OPTIND - 1 ))
grep="$*"
names=( )
ips=( )
tcps=( )
udps=( )

count=0

echo "Obtaining list of servers..."
$curl https://www.securenetconnection.com/vpnconfig/servers-cli.php 2>/dev/null| grep -i -e "$grep" | grep -i -e "$proto" > /tmp/hma-servers
exec < /tmp/hma-servers
rm /tmp/hma-servers
	while read server
	do
		: $(( count++ ))
		ips[$count]=`echo "$server"|cut -d '|' -f 1`
		udps[$count]=`echo "$server"|cut -d '|' -f 5`
		tcps[$count]=`echo "$server"|cut -d '|' -f 4`
		names[$count]=`echo "$server"|cut -d '|' -f 2`

	done

if [ "$count" -lt 1 ] ; then
	echo "No matching servers to connect: $grep"
	exit
else
	echo "$count servers matched"
fi

if [ $list -eq 1 ]; then
	for i in `seq 1 $count`; do
		echo -e "${names[$i]}\t${ips[$i]}\t${tcps[$i]}\t${udps[$i]}"
	done
	exit
fi


i=$(( $RANDOM%$count + 1 ))
echo "Connecting to:"
echo -e "${names[$i]}\t${ips[$i]}"
if [ "$proto" == "" ]; then
	if [ "$udps[$i]" != "" ]; then
		proto=udp
	else
		proto=tcp
	fi
fi

if [ "$proto" == "tcp" ]; then
	port=443
else
	port=53
fi

echo "Loading configuration..."
$curl "https://securenetconnection.com/vpnconfig/openvpn-template.ovpn" > /tmp/hma-config.cfg 2>/dev/null

echo "remote ${ips[$i]} $port" >> /tmp/hma-config.cfg
echo "proto $proto" >> /tmp/hma-config.cfg

#sudo $openvpn --config /tmp/hma-config.cfg
#rm /tmp/hma-config.cfg
cat <<EOF > /tmp/hma-routeup.sh
#!/bin/sh
cat <<EOEO >> /tmp/hma-ipcheck.txt
 *******************************************
*                                           *
*   You are now connected to HMA Pro! VPN   *
*                                           *
 *******************************************

Checking new IP address...
EOEO
nohup /tmp/hma-ipcheck.sh >/dev/null 2>&1 &
rm /tmp/hma-routeup.sh
EOF

cat <<EOF > /tmp/hma-ipcheck.sh
#!/bin/sh
ip=""
attempt=0
while [ "\$ip" = "" ]; do
	attempt=\$((\$attempt+1))
	ip="\`$curl http://geoip.hidemyass.com/ip/ 2>/dev/null\`"
	if [ "\$ip" != "" ]; then
	        echo "Your IP is \$ip" >> /tmp/hma-ipcheck.txt
	fi
	if [ \$attempt -gt 3 ]; then
		echo "Failed to load IP address." >> /tmp/hma-ipcheck.txt
		exit
	fi
done

EOF
echo "" > /tmp/hma-ipcheck.txt
tail -f /tmp/hma-ipcheck.txt &
chmod 755 /tmp/hma-ipcheck.sh
chmod 755 /tmp/hma-routeup.sh
/tmp/hma-ipcheck.sh
sleep 1


# MODIFICATION BY PETE

#!/bin/bash

pwfile="password.txt"

if [ -f "$pwfile" ]
then
echo "Login details found in password.txt"
else
echo "No Login details found. Please enter:" 

read -p "Username: " vpnuser < /dev/tty
echo $vpnuser > password.txt

read -p "Password: " vpnpass < /dev/tty
echo $vpnpass >> password.txt

fi

sleep 1

# adding to config file that password.txt should be used
sed -i 's/auth-user-pass/auth-user-pass password.txt/g' /tmp/hma-config.cfg

# END OF MODIFICATIONS





sudo $openvpn --script-security 3 --route-up /tmp/hma-routeup.sh --verb 2 --config /tmp/hma-config.cfg
rm /tmp/hma-config.cfg
rm /tmp/hma-ipcheck.sh
rm /tmp/hma-routeup.sh 2>/dev/null
rm /tmp/hma-ipcheck.txt
