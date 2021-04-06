# aws audit
This a simple script to audit an aws account for security certain security issues.
Specifically, this script checks for public objects in s3 buckets and "old" (configurable age) Access Keys

## Setup
This script reuires python3 and a number of python libraries.
The best way to run this script localy is to setup a virtual environment with the required dependencies.
Additionally, this script relies on existing aws client configuration and proper credentials in it's runtime enviornment
using any of the usual methods (config files, env variables or possibly an iam role if running on an ec2 instance).
### Local setup instructions
```sh
git clone git@github.com:andreyzax/aws_audit.git
cd aws_audit
python -mvenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
