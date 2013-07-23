#!/usr/bin/env sh

input=$1

if [ "$input" == "" ]
then

    exit 1;

else
:
fi

nome_file=ALIASES_$input

touch $nome_file
echo "" > $nome_file
echo "## lista $input" >> $nome_file 
echo "$input:              \"|/opt/Mailman/Mailman2.1.13-Debian6/Linux-amd64/mail/mailman post $input\"" >> $nome_file
echo "$input-admin:        \"|/opt/Mailman/Mailman2.1.13-Debian6/Linux-amd64/mail/mailman admin $input\"" >> $nome_file
echo "$input-bounces:      \"|/opt/Mailman/Mailman2.1.13-Debian6/Linux-amd64/mail/mailman bounces $input\"" >> $nome_file
echo "$input-confirm:      \"|/opt/Mailman/Mailman2.1.13-Debian6/Linux-amd64/mail/mailman confirm $input\"" >> $nome_file
echo "$input-join:         \"|/opt/Mailman/Mailman2.1.13-Debian6/Linux-amd64/mail/mailman join $input\"" >> $nome_file
echo "$input-leave:        \"|/opt/Mailman/Mailman2.1.13-Debian6/Linux-amd64/mail/mailman leave $input\"" >> $nome_file
echo "$input-owner:        \"|/opt/Mailman/Mailman2.1.13-Debian6/Linux-amd64/mail/mailman owner $input\"" >> $nome_file
echo "$input-request:      \"|/opt/Mailman/Mailman2.1.13-Debian6/Linux-amd64/mail/mailman request $input\"" >> $nome_file
echo "$input-subscribe:    \"|/opt/Mailman/Mailman2.1.13-Debian6/Linux-amd64/mail/mailman subscribe $input\"" >> $nome_file
echo "$input-unsubscribe:  \"|/opt/Mailman/Mailman2.1.13-Debian6/Linux-amd64/mail/mailman unsubscribe $input\"" >> $nome_file

echo $nome_file" generato"
cat $nome_file
