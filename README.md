# ☕ Coffee Analytics — Data Engineering & BI Project

![Project](https://img.shields.io/badge/Project-Coffee%20Analytics-blue)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![Docker](https://img.shields.io/badge/Docker-Container-blue)

---

## ✅ Badges

| Status | Description |
|--------|-------------|
| ![Build](https://img.shields.io/badge/build-passing-brightgreen) | CI build |
| ![Tests](https://img.shields.io/badge/tests-passing-brightgreen) | Pytest |
| ![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen) | Code coverage |

> ⚠️ Les badges sont **exemples**. Ils doivent être reliés à ton GitHub Actions une fois le repo pushé.

---

# 🎯 Objectif du projet

Ce projet a pour objectif de :

- Intégrer des données brutes de consommation de café (CSV)
- Nettoyer, transformer et charger les données dans PostgreSQL (ETL)
- Créer un **modèle en étoile (Star Schema)** pour BI
- Construire un dashboard BI moderne (Power BI + FastAPI + Plotly)
- Automatiser le pipeline avec Docker
- Fournir une API pour exposer les données

---

# Structure du projet

Data-Analytic/
├─ api/
│ ├─ main.py
│ ├─ templates/
│ │ └─ dashboard.html
├─ etl/
│ ├─ etl_coffee.py
│ └─ quality_checks.py
├─ sql/
│ ├─ schema.sql
│ └─ views.sql
├─ tests/
│ └─ test_quality.py
├─ data/
│ └─ Coffee.csv
├─ docker/
│ ├─ Dockerfile
│ └─ docker-compose.yml
├─ powerbi/
│ └─ coffee_dashboard.pbix
├─ requirements.txt
└─ README.md


![CI](https://github.com/<USER>/<REPO>/actions/workflows/ci-cd.yml/badge.svg)
