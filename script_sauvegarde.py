#!/usr/bin/env python
# -*-coding:Latin-1 -*


import os

import sys

import time

import tarfile

import pysftp

import paramiko

import time

from datetime import datetime

import subprocess

import pipes

cnopts = pysftp.CnOpts()

cnopts.hostkeys = None
#--------------------------------------------------------------------------

dossier_sauvegarde = "/home/adminsys/sauvegardes/"

dossier_sauvegarde_wp = "/home/adminsys/sauvegardes/wordpress/"

dossier_sauvegarde_mysql = "/home/adminsys/sauvegardes/mysql/"

dossier_config_wp = "/var/www/html/"

utilisateur_mysql = "adminsys"

mdp_sql = "Moudies7"

nom_db_sql = "wordpress"

ip_serveur = "192.168.0.254"

id_serveur = "adminsys"

mdp_serveur = "Moudies7"

ftp_serveur = "/home/adminsys/ftp/"

#--------------------------------------------------------------------------
def sauvegarde_wordpress():

	if os.path.exists(dossier_sauvegarde_wp) and os.path.exists(dossier_config_wp):
		os.system("tar -zcvf " +dossier_sauvegarde_wp+"wordpress.tar.gz "+dossier_config_wp)
		print("[SUCCES] Configuration de wordpress sauvegardée avec succes")
	else:
		print("[ERROR] Dossier de sauvegarde et/ou de configuration Wordpress introuvable")
		sys.exit(1)

def sauvegarde_sql():
	if os.path.exists(dossier_sauvegarde_mysql):

		os.system("mysqldump -u "+utilisateur_mysql+" -p"+mdp_sql+ nom_db_sql+" > "+dossier_sauvegarde_mysql+nom_db_sql+".sql")
		print("[SUCCES] Base de donnees wordpress sauvegardée avec succes")
	else:
		print("[ERROR] Dossier de sauvegarde de la base de données introuvable")
		sys.exit(1)
def transfert_sftp():

	try:
		with pysftp.Connection(host = ip_serveur, username = id_serveur, password = mdp_serveur, cnopts=cnopts) as sftp:
			print("Connexion au serveur distant établie avec succès...")
			localFilePath = dossier_sauvegarde
			remoteFilePath = ftp_serveur
			sftp.put_r(localFilePath, remoteFilePath)
			print("[SUCCES] Configuration de wordpress transferée sur le serveur distant avec succes")
			l = open("logs_sauvegarde.txt","a")
			l.write("[SUCCES]")
			l.close()
			sys.exit(0)

	except paramiko.SSHException:
		print("Echec de connexion avec le serveur distant")
		l = open("logs_sauvegarde.txt","a")
		l.write("[ERROR]")
		l.close()
		sys.exit(1)



sauvegarde_wordpress()

sauvegarde_sql()

transfert_sftp()
