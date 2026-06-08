# GreenOps AI Dashboard

## Hurdle 0 Concept Check

### What is a Resource Group in Azure?
A Resource Group is a logical container used to organize and manage related Azure resources together.

### What is the difference between a virtual environment and a global Python installation?
A virtual environment is isolated to a specific project and prevents dependency conflicts. A global Python installation is shared across the entire system.

### Why is version control important from Day 1?
Version control tracks changes, enables collaboration, maintains project history, and allows recovery from mistakes.


## Hurdle 1 Concept Check

### What does CO2e mean and why is it used?
CO2e (Carbon Dioxide Equivalent) is a standardized unit used to compare the warming impact of different greenhouse gases by expressing them as an equivalent amount of CO2.

### Why separate emission factors by resource type?
Different resources consume energy differently. CPU compute, storage, and data transfer have different environmental impacts, so separate emission factors provide more accurate carbon accounting.

### What is the most carbon-intensive service type in the dataset?
Determined by grouping the dataset by service_type and comparing total CO2e emissions.



## Hurdle 2 Concept Check

### Blob Storage vs Azure SQL Database
Azure Blob Storage is used for unstructured files such as CSVs, images, logs, and model artifacts. Azure SQL Database is used for structured relational data that requires querying, indexing, and transactions.

### What is LRS?
Locally Redundant Storage (LRS) keeps multiple copies of data within a single Azure datacenter. It is cheaper but does not protect against regional outages like Geo-Redundant Storage (GRS).

### Why is hardcoding a connection string risky?
Anyone with access to the source code can access the storage account. Secrets should be stored in environment variables, .env files, or Azure Key Vault.


## Hurdle 3 Concept Check

### What is RMSE?
RMSE (Root Mean Squared Error) measures the average magnitude of prediction errors. Lower RMSE indicates better predictive accuracy.

### Why create lag features?
Lag features allow the model to learn how previous CO2e values influence future values. They capture temporal dependencies in time-series data.

### Risks of Linear Regression
Linear Regression assumes a linear relationship between inputs and outputs. It may fail to capture nonlinear trends, seasonality, and sudden spikes in carbon emissions.

