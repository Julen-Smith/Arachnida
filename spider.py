# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    spider.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jsmith <jsmith@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2022/07/22 16:30:19 by jsmith            #+#    #+#              #
#    Updated: 2022/07/22 18:57:23 by jsmith           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
from bs4 import *
import requests
import os
from PIL import Image

"""
El programa spider permitirá extraer todas las imágenes de un sitio web, de manera
recursiva, proporcionando una url como parámetro. Gestionarás las siguientes opciones
del programa
"""
# Opción -r : descarga de forma recursiva las imágenes en una URL recibida como parámetro.
# Opción -r -l [N] : indica el nivel profundidad máximo de la descarga recursiva. En caso de no indicarse, será 5.
# Opción -p [PATH] : indica la ruta donde se guardarán los archivos descargados. En caso de no indicarse, se utilizará ./data/.

jpg = "jpg"
jpeg = "jpeg"
png = "png"
gif = "gif"
bmp = "bmp"

def recursive_donwload(images, nbr , i):
	print("Entro aqui por "+ str(i) + " vez")
	if (i != nbr) :
		recursive_donwload(images,nbr,i + 1)
	print("Se ejecuta el launch numero " + str(i))
	try:
		try:
			image_link = images[i]["data-srcset"]
		except:
			try:
				image_link = images[i]["data-src"]
			except:
				try:
					image_link = images[i]["data-fallback-src"]
				except:
					try:
						image_link = images[i]["src"]
					except:
						pass
		del images[i]
		print("Numero de imagenes " + str(len(images)));
		w = requests.get(image_link).headers
		this_img = w['Content-Type']
		#contemplar dentro de los metadatos el valor de titulo de this img.
		new_str = this_img.split("/")
		print("La string nueva es : " + new_str[1])
		if new_str[1] != jpg and new_str[1] != jpeg and  new_str[1] != png and  new_str[1] != gif and  new_str[1] != bmp :
			recursive_donwload(images, nbr +1, i);
		r = requests.get(image_link).content
		try:
			r = str(r, 'utf-8')
		except UnicodeDecodeError:
			folder_name = "."
			with open(f"{folder_name}/images{i}." + new_str[1], "wb+") as f: 
				f.write(r) 
	except:
		pass


if __name__ == "__main__":
	if len(sys.argv ) > 3 :
		print ("Arg error")
	print("Request will be send to : " + sys.argv[2])
	req = requests.get(sys.argv[2])
	soup = BeautifulSoup (req.text, 'html.parser')
	images = soup.findAll('img')
	print("Succesfull " + str(len(images)) + " image/s found!")
	recursive_donwload(images,5,1)
