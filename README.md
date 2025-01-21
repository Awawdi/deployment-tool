# Deployment CLI Tool

## Setup
1. Clone the repository.
2. Create a virtual environment and install dependencies.
3. Add your secret key in `.env`.
4. Run the CLI tool using `python cli_tool/main.py`.

## Commands
- `--deploy`: Deploy the web application.
- `--update`: Update the existing deployment.
- `--rollback`: Rollback to the previous version.

## Examples
Deploy the application:
```bash
python cli_tool/main.py --deploy --env production --secret mysecret
