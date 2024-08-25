# Système d'Alarme avec Détection de Mouvement

Ce projet consiste en la création d'un système d'alarme utilisant un capteur PIR pour la détection de mouvement. Le système est contrôlé par un Raspberry Pi, avec une interface en Python pour gérer les événements d'alarme.

## Fonctionnalités

- **Détection de Mouvement** : Le système utilise un capteur PIR pour détecter les mouvements. Lorsqu'un mouvement est détecté, le système demande l'entrée d'un code d'accès via un clavier numérique pour désactiver l'alarme.
- **Indicateurs Visuels** : Deux LED (rouge et verte) sont utilisées pour indiquer l'état du système d'alarme (activé ou désactivé).
- **Affichage des Informations** : Un écran LCD est utilisé pour afficher les messages relatifs à l'état du système, comme les demandes de code d'accès ou les notifications d'activation/désactivation.
- **Avertisseur Sonore** : Un buzzer est utilisé pour signaler une tentative d'accès invalide.
- **Gestion des Événements** : Les événements du système (activation, désactivation, accès valide/invalide) sont enregistrés avec l'heure et la date complètes.

## Structure du Code

Le code est organisé selon le modèle MVC (Modèle-Vue-Contrôleur).

### Modèle

Le modèle gère les données et la logique métier du système d'alarme. Il inclut les interactions avec la base de données et les capteurs.

### Vue

La vue est responsable de l'interface utilisateur. Elle utilise Tkinter pour afficher les boutons, les listes et les étiquettes, ainsi que pour gérer l'affichage sur l'écran LCD.

### Contrôleur

Le contrôleur gère les interactions entre le modèle et la vue. Il reçoit les entrées de l'utilisateur via la vue (comme le code d'accès entré sur le clavier numérique), met à jour le modèle, et rafraîchit la vue en conséquence.

## Prérequis

- **Matériel** : Raspberry Pi, capteur PIR, LED (rouge et verte), buzzer, clavier numérique, écran LCD.
- **Logiciel** : Python, modules Python pour gérer le matériel connecté (GPIO).

## Installation

Cloner le dépôt du projet :
   ```bash
   git clone https://github.com/votre-utilisateur/systeme-alarme.git
