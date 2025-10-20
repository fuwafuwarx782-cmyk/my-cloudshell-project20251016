import datetime
import json

def generate_log_message(location, user): #定義だけされて、ハンドラが動くまで動作しない
    
    current_time_object = datetime.datetime.now() #現在の日時をdatetimeモジュール内のdatetimeクラスのnow()を呼び出して取得
    time_display_format = "%Y-%m-%d %H:%M:%S" #strftime()に渡す日時の表記を年・月・日・時・分・秒に指定する
    now_string = current_time_object.strftime(time_display_format) #取得した日時情報をstrftime()で変換する 
    message = f"[{now_string}] User '{user}' logged in from '{location}'." #f-stringでログメッセージを作成    
    return message #関数の呼び出しもとであるハンドラ関数にログメッセージを返す

def lambda_handler(event, context): #Javaのmainメソッドみたいなもの
    
    try: #まず実行してみるコードブロック
        request_body = json.loads(event['body']) #呼び出し元がAPIに送ったキーbodyのデータをJSON文字列からディクショナリに変換
        user_name = request_body.get('user', 'UnknownUser') #キーbodyがあれば取り出し、なければ代わりにUnknownUserを返す
        location_info = request_body.get('location', 'UnknownLocation') #キーlocationがあれば取り出し、なければ代わりにUnknownLocationを返す

    except Exception as e: #例外が発生した場合の処理をeと名付ける
        return { #呼び出し元に返す
            'statusCode': 400, #HTTPのエラーコード400※送られてきたデータが不正※ディクショナリ
            'body': json.dumps({'error': 'Invalid request body format', 'detail': str(e)}) #エラーメッセージをJSON形式で作成
        }
    
    log_message = generate_log_message(location=location_info, user=user_name)
    #generate_log_message1関数を呼び出し
    #実引数としてlocationとuserを渡す※それぞれにlocation_infoとuser_nameを代入
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
