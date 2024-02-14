# databricks-aws-workshop



## Getting started
Clone the repository into your local machine, and create a Python Virtual environment, and run the following commands

```
pip install streamlit
pip install boto3
python -m streamlit run app.py
```

## Additional Information
<<<<<<< HEAD
This application only runs if it is connected to the S3 bucket s3://streamlit-aws-databricks-bucket. This requires credentials to the AWS Account 868972407689, I have sent account credentials with S3 full access for this.
=======
This application only runs if it is connected to the S3 bucket s3://streamlit-aws-databricks-bucket. This requires credentials on your local machine. 
>>>>>>> 5f54008 (main changes have been made)

The application will only return "The Answer is 42". I have commented out the line that sends a request to a databricks endpoint. Changes will have to be made and tested here.

I have also deployed the application to an ec2 instance on our shared AWS account.

http://3.106.216.159:8501/