import datetime
import json
import boto3

s3 = boto3.client('s3')
BUCKET_NAME = 'loger_sample_bucket_20251021'
#基本的に引数のやり取りはキーワード引数で行う
def generate_log_message(location, user, current_time): #定義だけされて、ハンドラが動くまで動作しない
    
    current_time_object = current_time #現在の日時をハンドラ関数から
    time_display_format = "%Y-%m-%d %H:%M:%S" #strftime()に渡す日時の表記を年・月・日・時・分・秒に指定する
    now_string = current_time_object.strftime(time_display_format) #取得した日時情報をstrftime()で変換する 
    message = f"[{now_string}] User '{user}' logged in from '{location}'." #f-stringでログメッセージを作成    
    return message #関数の呼び出しもとであるハンドラ関数にログメッセージを返す

def lambda_handler(event, context): #Javaのmainメソッドみたいなもの
    now_time = datetime.datetime.now()

    try: #まず実行してみるコードブロック
        request_body = json.loads(event['body']) #呼び出し元がAPIに送ったキーbodyのデータをJSON文字列からディクショナリに変換
        user_name = request_body.get('user', 'UnknownUser') #キーbodyがあれば取り出し、なければ代わりにUnknownUserを返す
        location_info = request_body.get('location', 'UnknownLocation') #キーlocationがあれば取り出し、なければ代わりにUnknownLocationを返す

    except Exception as e: #例外が発生した場合の処理をeと名付ける
        return { #呼び出し元に返す
            'statusCode': 400, #HTTPのエラーコード400※送られてきたデータが不正※ディクショナリ
            'body': json.dumps({'error': 'Invalid request body format', 'detail': str(e)}) #エラーメッセージをJSON形式で作成
        }
    
    log_message = generate_log_message(
        location = location_info, 
        user = user_name,
        current_time = now_time
        )
    #generate_log_message1関数を呼び出し
    #実引数としてlocationとuserを渡す※それぞれにlocation_infoとuser_nameを代入

    file_key = f"logs/{user_name}/{now_time.strftime('%Y/%m/%d/%H%M%S')}.json"
    #S3はフォルダ構造がパス
    #logsがフォルダ名、user_nameがサブフォルダ、datetime.strftime()がファイル名の一部として使うユニークな情報
    #同時刻でデータの上書きが起こらないよう後でミリ秒追加予定

    s3_data = { #S3に保存するディクショナリを準備
        'timestamp': now_time.strftime("%Y-%m-%d %H:%M:%S"),
        'user': user_name,
        'location_info': location_info,
        'log_message': log_message
    }

    try: #S3と通信するブロック
        s3.put_object( #s3=boto3.client('s3')で定義したs3クライアントにファイルを配置する命令
            Bucket = BUCKET_NAME, #S3に保存するバケット名を指定する引数※事前に名前は設定してある
            Key = file_key,
            Body = json.dumps(s3_data, ensure_ascii = False)
            )
    except Exception as e:
        #S3への保存に失敗した場合の応答
        print(f"S3 put_object failed: {e}") # CloudWatchのログに標準出力※lambdaのprint()の機能
        return { #returnの値はAPIゲートウェイに返されて
            'statusCode': 500, 
            'body': json.dumps({'error': 'Failed to save log to S3', 'detail': str(e)})
        }

    return { #もしexceptが起動していたら返さない※関数の実行が終了しているから
        'statusCode': 200, #HTTPステータスコードの200はリクエスト成功の意味
        'headers': { #返すデータの種類がJSONだと知らせる
            'Content-Type': 'application/json'
        },
        'body': json.dumps({ #クライアントが求めているデータの本体をJSON文字列に変換
            'status': 'OK', #処理は成功
            'generated_log': log_message #最終的なログメッセージを示す変数
        })
    }