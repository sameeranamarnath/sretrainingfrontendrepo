import os
import subprocess
import os
import boto3
from botocore.exceptions import NoCredentialsError

import mimetypes 

# Configuration
app_name = "employee-management"
docker_image = f"{app_name}:latest"
ecr_repository = "your-ecr-repo-url"  # Replace with your ECR repository URL
namespace = "default"  # Kubernetes namespace
bucket_name= "trinettrainingfrontendnew20250103022016337800000004"


# Define a mapping of file extensions to content types
CONTENT_TYPE_MAPPING = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon',
    # Add more mappings as needed
}

def get_content_type(file_path):
    """Get the content type based on the file extension."""
    _, ext = os.path.splitext(file_path)
    return CONTENT_TYPE_MAPPING.get(ext, 'application/octet-stream')

def upload_files_to_s3(directory, bucket_name):
    s3_client = boto3.client('s3')
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            s3_key = os.path.relpath(file_path, directory)
            content_type = get_content_type(file_path)
            print(file_path,"  has content_type ",content_type)
           
            try:
                s3_client.upload_file(file_path, bucket_name, s3_key,ExtraArgs={'ContentType': content_type})
                print(f"Uploaded {file_path} to s3://{bucket_name}/{s3_key}")
            except FileNotFoundError:
                print(f"File not found: {file_path}")
            except NoCredentialsError:
                print("Credentials not available")


def run_command(command):
    """Run a shell command and print its output."""
    result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
    print(result.stdout)
    return result

def build_angular_app():
    """Build the Angular application."""
    print("Building Angular application...")
    run_command("ng build ")

def build_docker_image():
    """Build the Docker image."""
    print("Building Docker image...")
    run_command(f"docker build -t {docker_image} .")

def push_docker_image():
    """Push the Docker image to ECR."""
    print("Pushing Docker image to ECR...")
    run_command(f"aws ecr get-login-password --region your-region | docker login --username AWS --password-stdin {ecr_repository}")
    run_command(f"docker tag {docker_image} {ecr_repository}/{docker_image}")
    run_command(f"docker push {ecr_repository}/{docker_image}")

def deploy_to_eks():
    """Deploy the application to EKS."""
    print("Deploying to EKS...")
    deployment_yaml = f"""
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {app_name}
  namespace: {namespace}
spec:
  replicas: 2
  selector:
    matchLabels:
      app: {app_name}
  template:
    metadata:
      labels:
        app: {app_name}
    spec:
      containers:
      - name: {app_name}
        image: {ecr_repository}/{docker_image}
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: {app_name}
  namespace: {namespace}
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 80
  selector:
    app: {app_name}
"""
    with open("deployment.yaml", "w") as f:
        f.write(deployment_yaml)

    run_command("kubectl apply -f deployment.yaml")

def main():
    #optimising the image size and performance requires
    #understanding of the underlying os which runs the application 
    #artifact => ensures reusability and maintenance as well as easy updates
    #base image (artifactories)
    build_angular_app() 
    #build_springboot_app()  // build _django_app() 
    #build_docker_image() #use the same tags and config as your infra script
    #push_docker_image() #push the updated image to the same ecr as before 
    #deploy_to_eks()
    upload_files_to_s3("dist/frontend",bucket_name)
    #the deploy script can be customised 
    # to run on local stack as well as aws 

if __name__ == "__main__":
    main()