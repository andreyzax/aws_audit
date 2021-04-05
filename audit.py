#!/usr/bin/env python3

import boto3
from datetime import datetime, timezone


s3  = boto3.resource('s3')
iam = boto3.resource('iam')
now = datetime.now(timezone.utc)

def isPublic(grants):
   grants = [ grantee['Grantee'] for grantee in grants ] # Cleanup the acl a bit, prevent nested key refrences in loop below
   for grantee in grants:
      if grantee['Type'] == 'Group' and grantee['URI'] == 'http://acs.amazonaws.com/groups/global/AllUsers':
         return True

   return False

for bucket in s3.buckets.all():
   for obj in bucket.objects.all():
      print(f's3://{bucket.name}/{obj.key} | {isPublic(obj.Acl().grants)}')

print('------------------------------------------------------------------')

for user in iam.users.all():
   for accessKey in user.access_keys.all():
      age = now - accessKey.create_date
      print(f'{accessKey.user_name}@{accessKey.access_key_id} : {age.days}')
