import os
import discord
import boto3
from botocore.exceptions import ClientError

TOKEN = os.environ['DISCORD_TOKEN']

AWS_AKI = os.environ['AWS_ACCESS_KEY_ID']
AWS_SAK = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_REG = os.environ['AWS_AWS_REGION']
INSTANCE_ID = os.environ['AWS_INSTANCE_ID']

client = discord.Client()

ec2 = boto3.client('ec2',aws_access_key_id=AWS_AKI,aws_secret_access_key=AWS_SAK,region_name=AWS_REG)

# 起動時に動作する処理
@client.event
async def on_ready():
    print('login')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    if message.author.bot:  
        return
    if client.user in message.mentions:
        await message.channel.send('こんにちは！')
    if message.content == '/start':
        ec2_start()
        await message.channel.send('起動します')
    if message.content == '/shutdown':
        ec2_stop()
        await message.channel.send('終了します')

# インスタンス起動
def ec2_start():    
    print('starting ec2-server...')
    try:    # 起動確認
        responce = ec2.start_instances(InstanceIds=[INSTANCE_ID],DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    try:
        responce = ec2.start_instances(InstanceIds=[INSTANCE_ID],DryRun=False)
        print(responce)
    except ClientError as e:
        print(e)

# インスタンス停止
def ec2_stop():    
    print('shutdown ec2-server...')
    try:    # 停止確認
        responce = ec2.stop_instances(InstanceIds=[INSTANCE_ID],DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    try:
        responce = ec2.stop_instances(InstanceIds=[INSTANCE_ID],DryRun=False)
        print(responce)
    except ClientError as e:
        print(e)

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)