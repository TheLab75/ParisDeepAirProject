# Paris DeepAir Project
------------------------------------------------

Le Wagon - Bootcamp Data Science - Full time
Batch #1002 - 03/10-09/12/2022

Projet de fin d'études présenté en groupe (4 personnes)

------------------------------------------------

**Démarches à faire :**
- Coller le dossier "data" dans le directory principal

**Setup de jupyter notebook à faire sur CLI :**

```shell
# install nbextensions
jupyter contrib nbextension install --user
jupyter nbextension enable toc2/main
jupyter nbextension enable collapsible_headings/main
jupyter nbextension enable spellchecker/main
jupyter nbextension enable code_prettify/code_prettify
```

------------------------------------------------

**Organisation des dossiers :**
- **autres** : data non-exploitée
- **data** : toute la data exploitée dans le cadre du projet

**Polluants :**
Unité de mesure pour tous les polluants : mg/m3

Polluants dans l'indice ATMO :
- **NO2** : dioxyde d'azote
- **O3** : ozone
- **PM 10** : particules
- **PM 2,5** : particules fines
- **SO2** : dioxyde de souffre

Polluants mesurés mais hors-indice ATMO - à dropper ?:
- **CO** : monoxyde de carbone
- **NO** : monoxyde d'azote
- **NOX** : oxydes d'azote
