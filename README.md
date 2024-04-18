# MPC Data Gathering

## Project Description
This project implements Multi-Party Computation (MPC) with a frontend interface and backend calculations to securely gather and analyze sensitive information about UNC students without revealing individual data. The system calculates various statistics about the student body, including the average year at university, financial aid, family income, GPA, and other relevant factors. Beyond simple averages, our implementation also computes the median, standard deviation, and performs linear regression analysis between selected variables. To ensure the confidentiality and integrity of the data, shares of the sensitive information are persisted in separate databases. This architecture guarantees that no individual party can access or deduce information about any single student, thereby preserving privacy and security.

## Project Update Document
[Project Update](https://github.com/adamdoyle630/comp590-mpc-final/blob/main/Project_Update_Template/project_template.tex)

## Functions
Linear Regression Cloud Function: https://us-central1-mpc-model.cloudfunctions.net/linReg
