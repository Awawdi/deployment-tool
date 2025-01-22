# **FastAPI Deployment CLI Tool**

## **Project Overview**
This project is a containerized **FastAPI** application, accompanied by a **CLI tool** that automates deployment tasks using **Ansible** playbooks. The CLI supports deploying, updating, and rolling back the FastAPI application.

### **Features**
- **FastAPI Application**: A simple application containerized using Docker.
- **Ansible Playbooks**:
  - `deploy.yml`: Deploys the **BASE** image of the FastAPI application for the first time.
  - `update.yml`: Updates the deployment to the **LATEST** image.
  - `rollback.yml`: Reverts the deployment to the **BASE** image.
- **CLI Tool**: Automates deployment tasks by invoking the Ansible playbooks.

---

## **Prerequisites**
Before running the project, ensure the following tools are installed on your system:
1. **Python** (>= 3.9)
2. **Docker**
3. **Ansible**
4. **pip**

---

## **Setup Instructions**

### **1. Clone the Repository**
```bash
git clone <repository_url>
cd <repository_name>
```

### **2. Create a Virtual Environment**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### **3. Install Python Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Configure Ansible Playbooks**
Ensure the following Ansible playbooks are configured correctly:
- **deploy.yml**: Deploys the initial **BASE** image.
- **update.yml**: Deploys the updated **LATEST** image.
- **rollback.yml**: Reverts the deployment to the **BASE** image.

Place these playbooks under the `ansible/` directory in the project root.

### **5. Build Docker Images**
Ensure the **BASE** and **LATEST** Docker images are built locally.

```bash
# Build BASE image
docker build -t fastapi-app:base -f app/Dockerfile .

# Build LATEST image
docker build -t fastapi-app:latest -f app/Dockerfile .
```

---

## **Usage Instructions**

### **Run the CLI Tool**

The CLI tool provides commands to deploy, update, or rollback the application. Below are the usage details:

#### **1. Deploy the Application**
Deploy the FastAPI application using the **BASE** image.
```bash
python -m cli_tool.main --deploy --config ansible/deploy.yml --env <environment> --verbose
```

#### **2. Update the Deployment**
Update the deployment to the **LATEST** image.
```bash
python -m cli_tool.main --update --config ansible/update.yml --env <environment> --verbose
```

#### **3. Rollback the Deployment**
Rollback the deployment to the **BASE** image.
```bash
python -m cli_tool.main --rollback --config ansible/rollback.yml --env <environment> --verbose
```

#### **4. Additional Options**
- `--config <path>`: Path to the Ansible playbook.
- `--env <environment>`: Deployment environment (`development`, `staging`, or `production`).
- `--verbose`: Enable verbose output for debugging.
- `--log <path>`: Specify the path to the log file. Defaults to `app.log`.
- `--secret <secret>`: Optional secret key or token required for certain operations.

---

## **Project Structure**
```
.
├── app/                    # FastAPI application source code
│   ├── main.py             # FastAPI entry point
│   └── Dockerfile          # Dockerfile to containerize the app
├── ansible/                # Ansible playbooks
│   ├── deploy.yml          # Playbook to deploy the BASE image
│   ├── update.yml          # Playbook to deploy the LATEST image
│   └── rollback.yml        # Playbook to rollback to the BASE image
├── cli_tool/               # CLI tool source code
│   ├── main.py             # Entry point for the CLI tool
│   ├── operations.py       # Handles deploy, update, and rollback operations
│   ├── vault_cloud_api.py  # Interacts with Vault API for secrets management
│   └── logging_config.py   # Logging configuration module
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── .venv/                  # Virtual environment (ignored in `.gitignore`)
```

---

## **Assumptions**
1. **FastAPI Application**:
   - The application is containerized using Docker.
   - Two Docker images are built:
     - **BASE**: Initial deployment image.
     - **LATEST**: Updated image for deployment.

2. **Ansible Playbooks**:
   - `deploy.yml` deploys the **BASE** image for the first-time setup.
   - `update.yml` updates the application to the **LATEST** image.
   - `rollback.yml` rolls back the application to the **BASE** image.

3. **Secrets Management**:
   - The Vault API is used to retrieve sensitive credentials if `--secret` is provided.

---

## **Logs and Debugging**
- Logs are stored in `app.log` by default.
- Use the `--log <path>` flag to specify a custom log file path.
- Use the `--verbose` flag for detailed debugging output.

---

## **Future Enhancements**
- Add support for Kubernetes deployments.
- Integrate CI/CD pipelines for automated testing and deployment.
- Expand secrets management with HashiCorp Vault or other secure tools.
- Add unit tests for CLI and playbook integrations.

---