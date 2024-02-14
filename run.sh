
#!/bin/bash
# aws s3 cp --recursive $CODE_BUCKET/databricksapp ~/
sudo yum install python3
sudo yum install pip
python3 -m venv /home/ec2-user/venv
source /home/ec2-user/venv/bin/activate
pip install streamlit
pip install boto3
sudo chmod -R a+rwx ~/venv

# pip install requirements.txt
python3 -m streamlit run app.py --server.port 8080

# REQUIRES SECURITY GROUP THAT ALLOWS TCP TRAFFIC
# IAM ROLE MUST BE ABLE TO READ FROM S3 BUCKETS.... AND WRITE TO YOUR S3 BUCKET

# OTHER VARS REQUIRED
EXPORT S3_BUCKET=s3://streamlit-sample-bucket
EXPORT CODE_BUCKET=s3://streamlit-sample-bucket

