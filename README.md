# MPC Data Gathering

## Project Description
This project implements Multi-Party Computation (MPC) with a frontend interface and backend calculations to securely gather and analyze sensitive information about UNC students without revealing individual data. The system calculates various statistics about the student body, including the average year at university, financial aid, family income, GPA, and other relevant factors. Beyond simple averages, our implementation also computes the correlation and standard deviation of selected variables. To ensure the confidentiality and integrity of the data, shares of the sensitive information are persisted in separate databases. This architecture guarantees that no individual party can access or deduce information about any single student, thereby preserving privacy and security.

## Project Update Document
[Project Update](https://github.com/adamdoyle630/comp590-mpc-final/blob/main/Project_Update_Template/project_template.tex)

# API Overview

Below is an overview of the API endpoints implemented in this application. 
Base URL: https://us-east1-outstanding-map-421217.cloudfunctions.net

## Insert Data
Takes various data points and divides them into shares among parties.

### Endpoint
`POST /insert_data`

### Request Body
JSON object must follow the below format. Valid values for each field must be a number or decimal value.

```json
{
     "gpa": 3.5,
	 "age": 18,
     "financial_aid": 5000
}
```

### Response
A successful response will return the number of data points entered and the number of parties. 

```json
{
	"data_points": 3,
	"parties": 3
}
```

## Calculate Mean
Calculates the mean of a specified statistic using MPC calculations.

### Endpoint
`POST /calculate_mean`

### Request Body
JSON object must follow the below format. Valid values for the "statistic" field are `"gpa"`, `"age"`, and `"financial_aid"`.

```json
{
    "statistic": "gpa"
}
```

### Response

A successful response will make the MPC calculations and return the mean for the specified statistic.

```json
{
    "mean": 3.5
}
```

## Calculate Standard Deviation
Calculates the standard deviation of a specified statistic using MPC calculations.

### Endpoint
`POST /calculate_standard_deviation`

### Request Body
JSON object must follow the below format. Valid values for the "statistic" field are `"gpa"`, `"age"`, and `"financial_aid"`.

```json
{
    "statistic": "gpa"
}
```

### Response

A successful response will make the MPC calculations and return the mean for the specified statistic.

```json
{
    "sd": 1.0
}
