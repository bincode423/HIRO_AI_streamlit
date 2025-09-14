import os
from datetime import datetime
import moduls.clocker as ck



emails = {}
download = {}
while True:
    file_names = os.listdir("./database/email_code")
    for file in file_names:
        if file not in emails:
            with open(f'./database/email_code/{file}', "r", encoding="utf-8") as f:
                content = f.read()
            emails[file] = (content, ck.clock_class())
            print('new_email code:',file)
        else:
            with open(f'./database/email_code/{file}', "r", encoding="utf-8") as f:
                content = f.read()
            if content == emails[file][0]:
                try:
                    now = datetime.now()
                    diff = (now - emails[file][1]).total_seconds()
                    if diff >= 300:
                        os.remove(f"./database/email_code/{file}")
                        print('delete_email code:',file)
                except:
                    pass
            else:
                emails[file] = (content, ck.clock_class())
                print('change_email code:',file)
    
    file_names = os.listdir("./download")
    for file in file_names:
        if file not in download:
            download[file] = ck.clock_class()
        else:
            try:
                now = datetime.now()
                diff = (now-download[file]).total_seconds()
                if diff >= 2:
                    os.remove(f'./download/{file}')
                    print('delete_download :',file)
            except:
                pass