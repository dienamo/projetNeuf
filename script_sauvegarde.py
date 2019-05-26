#!/usr/bin/env python
# -*-coding:Latin-1 -*



# importation des modules os et sys afin d'ecrire des commandes bash et sortir du programme proprement

import os

import sys

# importation du module tarfile afin de faire les sauvegardes

import tarfile

# importation du module pysftp afin de transferer les donnees en ftp securise

import pysftp

# importation du module paramiko afin de tester la connexion SSH

import paramiko

# importation du module datetime afin d'horodater les executions

from datetime import datetime

#--------------------------------------------------------------------------

#Assignation des variables

cnopts = pysftp.CnOpts()

cnopts.hostkeys = None

date = datetime.now()

date = str(date)

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
# creation de la fonction de sauvegarde de wordpress
def sauvegarde_wordpress():
	# verification de l'existance des dossiers
	if os.path.exists(dossier_sauvegarde_wp) and os.path.exists(dossier_config_wp):
		# tar du dossier de configuration dans le dossier de sauvegarde wordpress
		os.system("tar zcvf " + dossier_sauvegarde_wp + "wordpress.tar.gz " + dossier_config_wp)
		print("************************************************************************")
		print("[SUCCES] Configuration de wordpress sauvegardée avec succes: " + date)
		print("************************************************************************")
		# renseignement de l'operation dans un fichier de logs
		l = open("logs_sauvegarde.txt","a")
                l.write("[SUCCES] configuration de wordpress sauvegardée avec succes: " + date + "\n")
                l.close()
	# levee d'une erreur en cas d'abscence d'un ou des dossiers
	else:
		print("**************************************************************************************")
		print("[ERROR] Dossier de sauvegarde et/ou de configuration Wordpress introuvable: " + date)
		print("**************************************************************************************")
		l = open("logs_sauvegarde.txt","a")
                l.write("[ERROR] echec de la sauvegarde configuration wordpress: " + date + "\n")
                l.close()
		# sortie du programme
		sys.exit(1)

# creation de la fonction de sauvegarde de la base de donnees
def sauvegarde_sql():
	# verification de l'existance du dossier de savegarde mysql
	if os.path.exists(dossier_sauvegarde_mysql):
		# dump de la base de donnees
		os.system("mysqldump -u "+utilisateur_mysql+" -p"+mdp_sql+ nom_db_sql+" > "+dossier_sauvegarde_mysql+nom_db_sql+".sql")
		print("*****************************************************************")
		print("[SUCCES] Base de donnees wordpress sauvegardée avec succes: "+ date)
		print("*****************************************************************")
		# renseignement de l'operation dans un fichier de logs
		l = open("logs_sauvegarde.txt","a")
                l.write("[SUCCES] base de données sauvegardée avec succes: " + date + "\n")
                l.close()

	# levee d'une erreur en cas d'abscence d'un dossier
	else:
		print("************************************************************************")
		print("[ERROR] Dossier de sauvegarde de la base de données introuvable: " + date)
		print("************************************************************************")
		# renseignement de l'operation dans un fichier de logs
		l = open("logs_sauvegarde.txt","a")
                l.write("[ERROR] dossier de sauvegarde de la base de données introuvable: " + date + "\n")
                l.close()
		# sortie du programme
		sys.exit(1)

# creation de la fonction de transfere en FTP des donnees
def transfert_sftp():
	# creation d'un bloc try afin de levee une exception en cas de probleme de connexion au serveur
	try:
		# connexion au serveur
		with pysftp.Connection(host = ip_serveur, username = id_serveur, password = mdp_serveur, cnopts=cnopts) as sftp:
			print("***************************************************")
			print("Connexion au serveur distant établie avec succès...")
			print("***************************************************")
			print("Transfert en cours...")
			print("*********************")
			localFilePath = dossier_sauvegarde
			remoteFilePath = ftp_serveur
			# transfere du dossier de sauvegarde vers le serveur ftp
			sftp.put_r(localFilePath, remoteFilePath)
			print("****************************************************************************************")
			print("[SUCCES] Configuration de wordpress transferée sur le serveur distant avec succes: "+date)
			print("****************************************************************************************")
			# renseignement de l'operation dans un fichier de logs
			l = open("logs_sauvegarde.txt","a")
			l.write("[SUCCES] configuration de wordpress transferée sur le serveur distant: " + date + "\n")
			l.close()
			# sortie du programme
			sys.exit(0)
	# levee d'une exception en cas de probleme de connexion au serveur
	except paramiko.SSHException:
		print("*******************************************")
		print("Echec de connexion avec le serveur distant.")
		print("*******************************************")
		# renseignement de l'operation dans un fichier de logs
		l = open("logs_sauvegarde.txt","a")
		l.write("[ERROR] echec de la connexion avec le serveur distant: " + date + "\n")
		l.close()
		# sortie du programme
		sys.exit(1)



sauvegarde_wordpress()

sauvegarde_sql()

transfert_sftp()
