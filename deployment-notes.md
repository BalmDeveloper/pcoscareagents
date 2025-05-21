# Azure Deployment Guide for PCOS Care Application

## Prerequisites
1. Azure CLI installed on your local machine
2. Azure account with sufficient permissions
3. Git installed

## Deployment Steps

### 1. Login to Azure
```bash
az login
```

### 2. Run the deployment script
```bash
chmod +x deploy-azure.sh
./deploy-azure.sh
```

### 3. Configure Environment Variables
After deployment, set your environment variables in the Azure Portal:
1. Go to your App Service
2. Navigate to Configuration > Application settings
3. Add your environment variables (e.g., API keys, database URLs)

### 4. Access Your Application
Your application will be available at: `https://<your-app-name>.azurewebsites.net`

## Manual Deployment (Alternative)

### 1. Create a resource group
```bash
az group create --name pcos-care-resources --location eastus
```

### 2. Create an App Service plan
```bash
az appservice plan create --name pcos-care-plan --resource-group pcos-care-resources --sku B1 --is-linux
```

### 3. Create the web app
```bash
az webapp create --resource-group pcos-care-resources --plan pcos-care-plan --name <your-app-name> --runtime "PYTHON|3.9" --startup-file "gunicorn -w 4 -k uvicorn.workers.UvicornWorker preview_server:app"
```

### 4. Deploy your code
```bash
az webapp up --resource-group pcos-care-resources --name <your-app-name> --sku B1 --runtime "PYTHON|3.9"
```

## Troubleshooting

### View logs
```bash
az webapp log tail --resource-group pcos-care-resources --name <your-app-name>
```

### Check application settings
```bash
az webapp config appsettings list --resource-group pcos-care-resources --name <your-app-name>
```
