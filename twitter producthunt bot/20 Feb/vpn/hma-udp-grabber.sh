#!/bin/bash
TEMP=/tmp/temp.$$
trap 'rm -f $TEMP; exit 0' 0 1 2 3 15

show_progress()
{
    while [ -r $TEMP ] ; do
        echo -n .
        sleep 2
    done
}

echo
echo "This script will download/update your HideMyAss OpenVPN configuration files."
echo
read -p "Are you sure you wish to continue? (y/n) " RESP

if [ "$RESP" = "y" ]; 
then
echo
# (1) prompt user, and read credentials from the command line
read -p "Your HMA! username: " username
stty echo
read -p "Your HMA! password: " password
stty echo
echo
# (2) download process begins
echo -n "\n""Downloading "
touch $TEMP
show_progress &

rm -r /etc/openvpn/*

# (3) write credentials to /etc/openvpn/hmauser.pass
echo "$username\n$password" > /etc/openvpn/hmauser.pass

cd /etc/openvpn
wget --quiet -r -A.ovpn -nd --no-parent https://www.hidemyass.com/vpn-config/UDP/
wget --quiet https://www.hidemyass.com/vpn-config/keys/ca.crt https://www.hidemyass.com/vpn-config/keys/hmauser.crt https://www.hidemyass.com/vpn-config/keys/hmauser.key

rm -f $TEMP

echo "Done! You can find the files in /etc/openvpn/" "\n"
echo
sleep 1
echo "Credentials stored in /etc/openvpn/hmauser.pass"
sleep 1
echo "Applying settings..."
sleep 4
# (4) edit all ovpn config files and make them read credentials from a file
sed -i 's/auth-user-pass/auth-user-pass hmauser.pass/g' /etc/openvpn/*
echo "All done!"

else
echo "\n""Good bye!"
fi

echo
