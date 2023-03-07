import sys, os
#sys.path.append(os.path.realpath('../venv/Lib/site-package'))
#os.environ["PATH"]=('' if 'pywin32_system32' in os.environ["PATH"] else (os.path.realpath('../venv/Lib/site-package/pywin32_system32')+";"))+os.environ["PATH"]
#print(os.environ["PATH"])


import datetime
import win32com.client

path = os.path.dirname(os.path.realpath(sys.argv[0]))
today = datetime.date.today()

outlook = win32com.client.Dispatch('Outlook.Application').GetNamespace('MAPI')
inbox = outlook.GetDefaultFolder(6)
messages = inbox.Items

def save_attachments(subject):
    for message in messages:
        if message.Subject == subject and message.Senton.date() == today:
            for attatchment in message.Attachments:
                incrementing_save(attatchment)
                if message.Unread:
                    message.Unread = False

def incrementing_save(attatchment):
        i = 1
        while os.path.exists(os.path.join(path, str(attatchment).split('.')[0] + f'({i}).pdf')):
            i += 1
        attatchment.SaveAsFile(os.path.join(path, str(attatchment).split('.')[0] + f'({i}).pdf'))

if __name__ == '__main__':
    save_attachments('')
