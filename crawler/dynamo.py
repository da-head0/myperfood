from crawler import crawl
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-2',aws_access_key_id='AKIAVD5PTSLAQQ6R5ORH',aws_secret_access_key='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')
#access_key_pair = dynamodb.AccessKeyPair('aimb','AKIAVD5PTSLAQQ6R5ORH','xj/XF1d6GSzm0uZWsqiQYvbfyEA/Xuvk46Gr7RLp')
#account_password_policy = dynamodb.AccountPasswordPolicy()
#response = access_key_pair.activate()

table = dynamodb.Table('petfood')
for i in range(1200,1250): #1099,1199
  data = crawl(i)
  #title = data['title']
  #if table.get_item(Key={'title': title}) is None:
  table.put_item(Item=data)