#!/usr/bin/env python3

import boto3


s3  = boto3.resource('s3')

def isPublic(grants):
   grants = [ grantee['Grantee'] for grantee in grants ] # Cleanup the acl a bit, prevent nested key refrences in loop below
   for grantee in grants:
      if grantee['Type'] == 'Group' and grantee['URI'] == 'http://acs.amazonaws.com/groups/global/AllUsers':
         return True

   return False

for bucket in s3.buckets.all():
   for obj in bucket.objects.all():
      print(f's3://{bucket.name}/{obj.key} | {isPublic(obj.Acl().grants)}')
