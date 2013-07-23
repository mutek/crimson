#!/usr/bin/env sh
#
# Luca Cappelletti 2013
#
# GNU/GPL
#
# Popola cartella con il dump delle configurazioni di tutte le liste
#
#


for i in $(list_lists -b | sort)
do 

	config_list -o - $i > $i
	printf .

done

printf "\n"

ls
