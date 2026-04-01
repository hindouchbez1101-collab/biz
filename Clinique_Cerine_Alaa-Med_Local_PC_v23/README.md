# Clinique Cerine Alaa-Med — Logiciel (Local / Windows / PC)

Ce projet est une base **prête à installer** (backend + interface web PC) pour:
- Réception (patients, RDV, encaissement cash, reçus A5, analyses détaillées + packs)
- Gérant (recettes, dépenses, rapports)
- Administrateur (utilisateurs, listes, audit)

## 1) Installation (Windows 10/11 - Serveur local)

### Prérequis (à installer sur le PC Serveur)
1. **Python 3.12** (cocher "Add Python to PATH")
2. **PostgreSQL 16** (ou utiliser SQLite pour démarrer)
3. (Optionnel) **Git** si vous versionnez le projet

### Démarrage rapide (SQLite - pour test)
1. Double-cliquez: `start_dev_sqlite.bat`
2. Ouvrir: http://127.0.0.1:8080
3. Connexion:
   - admin: `admin`
   - mot de passe: `admin12345` (à changer)

### Installation PostgreSQL (recommandé en production locale)
1. Créez une base: `clinique`
2. Mettez les variables dans `.env` (voir `.env.example`)
3. Double-cliquez: `start_prod_postgres.bat`

## 2) Accès depuis les autres PC
- Donner une IP fixe au serveur (ex: 192.168.1.10)
- Autoriser le port 8080 dans le pare-feu Windows
- Depuis les autres PC: `http://192.168.1.10:8080`

## 3) Comptes & rôles
Le projet crée 3 groupes:
- RECEPTION
- GERANT
- ADMIN

## 4) Impression reçu A5
Le reçu est généré en HTML imprimable (format A5 CSS). Sur Windows: choisir A5.

## 5) Important
- Faire une sauvegarde quotidienne de la base de données.
- Changer les mots de passe par défaut.


## Dépannage (Windows)

### Erreur “Permission denied ... .venv\Scripts\python.exe”
- Déplacez le dossier du projet hors de **Downloads** (ex: `C:\CliniqueApp\`).
- Clic droit sur le dossier → Propriétés → décochez “Lecture seule” si actif.
- Ouvrez le .bat en **Administrateur** (clic droit → Exécuter en tant qu’administrateur).
- Si Windows Defender “Controlled folder access” est activé: autorisez `python.exe` ou désactivez-le pour ce dossier.

### Erreur “no such table: clinic_labtest”
- Cela arrive si les migrations du module clinic n’ont pas été appliquées.
- La version corrigée lance automatiquement:
  `makemigrations clinic` puis `migrate` avant `init_demo`.

## Nouveautés v3
- Bouton **Mode clair/sombre** (en haut).
- Encaissements avec détails: **Payeur** (Normal / CNAS-Chiffa / Militaire), **Docteur**, et **répartition** (Patient + Tiers).
- Reçu A5 affiche Payeur + Docteur + Patient/Tiers.

## Nouveautés v4
- Reçu A5 type “bon de paiement” (style tableau).
- **Montant total en toutes lettres** (FR).
- **Vrai code-barres CODE128** (basé sur N° de reçu uniquement).
