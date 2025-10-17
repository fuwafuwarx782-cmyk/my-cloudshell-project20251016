import json
import boto3
from datetime import datetime
import os

# S3バケット名を設定※統一
S3_BUCKET_NAME = 'location-logs-fuwafuwarx782'

def lambda_handler(event, context):
    s3 = boto3.client('s3')

    #API Gatewayから送られてきたJSONの値を取得しPythonのディクショナリに加工
    try:
        #JSON文字列をディクショナリへ
        request_data = json.loads(event['body']) 
    except Exception as e:
        # デバック用のダミー？
        request_data = {
            "timestamp": datetime.now()/isoformat(),
            "user_id": "dabug_user",
            "error": str(e)
        }

# S3に保存するファイル名とパスを決定
now = datetime.now()
# フォルダパス: logs/2025/10/17
date_path = now.strftime("logs/%Y/%m/%d")
# ファイル名: 20251017-123000-user_id.json
file_name = now.strftime("%YY%m%d-%H%M%S") + "-" + request_data.get("user_id", "unknown") + ".json"
    s3_key = f"{date_path}/{file_name}"

# 3. データをS3に書き込む
    s3.put_object(
        Bucket=S3_BUCKET_NAME,
        Key=s3_key,
        # S3に保存するデータはJSON形式で、見やすいように整形(indent=2)
        Body=json.dumps(request_data, indent=2),
        ContentType='application/json'
    )

    # CloudWatch Logsに出力（デバッグ用）
    print(f"S3に保存成功: s3://{S3_BUCKET_NAME}/{s3_key}")

    # 4. 応答をAPI Gatewayに返す
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'message': 'Location logged successfully'})
    }
