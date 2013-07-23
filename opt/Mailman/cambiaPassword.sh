#!/usr/bin/env sh


echo "Inserisci il nome della lista alla quale voi resettare la password di amministrazione: "

read lista

if [ "$lista" = "" ]
then

	exit 0

else

	/opt/Mailman/Mailman2.1.13-Debian6/Linux-amd64/bin/change_pw -l $lista

fi
