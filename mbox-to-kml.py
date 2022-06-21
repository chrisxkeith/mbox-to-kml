import mailbox
import time

start = time.time()
mbox = mailbox.mbox(r"2020-10-emails.mbox")
for i, message in enumerate(mbox):
    end = time.time()
    print(float(end - start))
    print("from   :",message['from'])
    print("subject:",message['subject'])
    if message.is_multipart():
        content = 'multipart' # ''.join(part.get_payload(decode=True) for part in message.get_payload())
    else:
        content = message.get_payload(decode=True)
    print("content:",content)
    print("**************************************")

    if i == 2:
        break
