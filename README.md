Calcul de la DSR
================

Ce programme calcule une partie de la dotation de solidarité rurale (DSR), partie des dotations globales de fonctionnement (DGR).

Ce programme a été réalisé dans le cadre du hackathon Datafin 2020 organisé au Sénat les 24 et 25 janvier 2020 ; il est à l’état de prototype pour démontrer la faisabilité du défi.

## Utilisation

Lancement du serveur :

```sh
python3 server.py
```

Appel de l’API :

```sh
curl -X POST 'http://127.0.0.1/simul' -d '{}' > dsr.json
jq . dsr.json
```

Cet appel va retourner deux fois la même législation (initiale).
