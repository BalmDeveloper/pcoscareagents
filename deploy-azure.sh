#!/bin/bash

# Set your Azure resource group and app name
RESOURCE_GROUP="pcos-care-resources"
APP_NAME="pcos-care-app"

# Login to Azure
az login

# Create a resource group
az group create --name $RESOURCE_GROUP --location eastus

# Create an App Service plan
az appservice plan create --name $APP_NAME-plan --resource-group $RESOURCE_GROUP --sku B1 --is-linux

# Create the web app
az webapp create --resource-group $RESOURCE_GROUP --plan $APP_NAME-plan --name $APP_NAME --runtime "PYTHON|3.9" --startup-file "gunicorn -w 4 -k uvicorn.workers.UvicornWorker preview_server:app"

# Configure the web app
az webapp config appsettings set --resource-group $RESOURCE_GROUP --name $APP_NAME --settings SCM_DO_BUILD_DURING_DEPLOYMENT=1

# Deploy the code
az webapp up --resource-group $RESOURCE_GROUP --name $APP_NAME --sku B1 --runtime "PYTHON|3.9"

echo "Deployment complete! Your app is available at: https://$APP_NAME.azurewebsites.net"
