# AIR QUALITY FORECAST PROJECT
[![Data pipeline](https://github.com/Nell87/air-quality-monitoring/actions/workflows/data_pipeline.yml/badge.svg)](https://github.com/Nell87/air-quality-monitoring/blob/main/.github/workflows/data_pipeline.yml)
[![ML pipeline](https://github.com/Nell87/air-quality-monitoring/actions/workflows/ml_pipeline.yml/badge.svg)](https://github.com/Nell87/air-quality-monitoring/blob/main/.github/workflows/ml_pipeline.yml)

## Table of Contents
- [Objective](#objective)
- [Project structure](#project-structure)
- [Architecture](#architecture)
- [To do list](#to-do-list)

## Objective
The objective of the project is to build an end-to-end machine learning project that aims to predict air quality across various cities. 

## Project structure
- **Data Pipeline**: Automatically collects data hourly from the API and stores it in Supabase, triggered every 30 minutes via GitHub Actions.
- **ML Pipeline**: Automatically retrieves and preprocesses database data, trains an LSTM network for predictions, and saves outcomes back to the database.

## Architecture
<a href="https://files.fm/u/djguyqe3h7#/view/air_quality_project.drawio.png"><img src="https://files.fm/thumb_show.php?i=56pz4reshw"></a>

## To do list
- [ ] Dockerize the project for containerization
- [ ] Implement GitHub Actions for CI/CD
- [ ] Use Evidently AI for data monitoring
- [ ] Adopt Poetry for managing dependencies
- [ ] MLFlow for tracking experiments and managing model registry
- [ ] Hopsworks as Feature Store
- [ ] Improve the LSTM network's benchmark model
- [ ] Write unit tests and integration tests
- [ ] Use Pylint for code analysis
