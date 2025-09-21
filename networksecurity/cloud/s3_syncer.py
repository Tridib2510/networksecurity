# This file is responsible for syncing with the aws s3 bucket
import os
class S3Sync:
    def sync_folder_to_s3(self,folder,aws_bucket_url):
        command=f"aws s3 sync {folder} {aws_bucket_url}"
        # aws_bucket_url=is the folder in the s3 bucket

        os.system(command)
        # os.system is going to run the command in the terminal

    def sync_folder_from_s3(self,aws_bucket_url,folder):
        command=f"aws s3 sync {aws_bucket_url} {folder}"
        os.system(command)
        