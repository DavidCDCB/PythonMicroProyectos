#! /usr/bin/python3
# _*_ coding: utf8 _*_

import pynput.keyboard
from os import system as exc
import sys

def press(key):
	print(key)
	if(key == key.left):
		return False

def unpress(key):
	pass
	
def convert(key):
	pass

def main():

	with pynput.keyboard.Listener(on_press=press,on_release=unpress) as listen:
		listen.join()

if __name__ == "__main__":
	main()
