#!/usr/bin/env python3

import argparse
import boto3
from datetime import datetime, timezone

argparser = argparse.ArgumentParser(description='Audit aws account for security policy vaiolations')
argparser.add_argument('-d', '--days', required=True, metavar='Days', type=int, help='Report aws keypairs older then this number of days')
args = argparser.parse_args()


s3  = boto3.resource('s3')
iam = boto3.resource('iam')
now = datetime.now(timezone.utc)
max_allowed_age = args.days

def isPublic(grants):
   grants = [ grantee['Grantee'] for grantee in grants ] # Cleanup the acl a bit, prevent nested key refrences in loop below
   for grantee in grants:
      if grantee['Type'] == 'Group' and grantee['URI'] == 'http://acs.amazonaws.com/groups/global/AllUsers':
         return True

   return False

def auditS3Objects():
   print('-'*14 + 'Publicly accessible objects' + '-'*14)
   for bucket in s3.buckets.all():
      for obj in bucket.objects.all():
         if isPublic(obj.Acl().grants):
            print(f's3://{bucket.name}/{obj.key}')

def auditAccessKeys():
   print('-'*14 + 'Old Access Keys' + '-'*14)
   for user in iam.users.all():
      for accessKey in user.access_keys.all():
         age = now - accessKey.create_date
         if age.days > max_allowed_age:
             print(f'{accessKey.user_name}@{accessKey.access_key_id} : {age.days}')

auditS3Objects()
auditAccessKeys()
