import mailbox
import time

start = time.time()
mbox = mailbox.mbox(r"2020-10-emails.mbox")
for i, message in enumerate(mbox):
    if i == 0:
        end = time.time()
        print(str(end - start) + ' seconds')
    print("from   :", message['from'])
    print("subject:", message['subject'])
    if message.is_multipart():
        content = 'multipart'
        for part in message.get_payload():
            s = str(i) + ': ' + part._default_type
            if part._default_type == 'text/plain':
                s += ': ' + part.as_string()[:60]
            print(s)
    else:
        content = message.get_payload(decode=True)
    print("content:", content)
    print("**************************************")

    if i == 2:
        break
