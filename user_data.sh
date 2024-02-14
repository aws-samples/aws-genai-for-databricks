
#!/bin/bash
# sudo yum -y install python3 pip git
# git clone https://gitlab.com/seanwdc97/databricks-aws-workshop.git /home/ec2-user/databricks-aws-workshop
# bash /home/ec2-user/databricks-aws-workshop/user_data.sh
python3 -m venv /home/ec2-user/venv
source /home/ec2-user/venv/bin/activate
pip install streamlit
pip install --upgrade boto3 
pip install --upgrade botocore 
pip install --upgrade awscrt
python -m streamlit run /home/ec2-user/databricks-aws-workshop/app.py --server.port 8080