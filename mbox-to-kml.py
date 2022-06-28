import mailbox
import time
import base64
import re

class mboxToKml:
    def run(self):
        filesWritten = {}
        start = time.time()
        mbox = mailbox.mbox(r'2020.mbox')
        for i, message in enumerate(mbox):
            if i == 0:
                self.print_elapsed_seconds('Open mbox file', start)
            if message['from'] == 'Christopher Keith <chris.keith@gmail.com>' and \
                    not message['subject'].startswith('Re:'):
                if message.is_multipart():
                    for part in message.get_payload():
                        if part._default_type == 'text/plain':
                            thePart = part.as_string()
                            if isinstance(thePart,str):
                                theStr = thePart
                            else:
                                theStr = thePart.as_string()
                            if 'image/png' in theStr:
                                fname = self.create_file_name(message['subject'])
                                if fname in filesWritten.keys():
                                    print("***** dup: " + fname + ': for subject: "' + message["subject"] + '" and "' + filesWritten[fname] + '"')
                                else:
                                    strt = time.time()
                                    self.convert_to_png(fname, thePart)
                                    secs = round(time.time() - strt, 0)
                                    print(str(secs) + ': ' + fname)
                                    filesWritten[fname] = message["subject"]
                        else:
                            print('Message# : ' + str(i) + ': unhandled: ' + part._default_type)
                else:
                    print('Message# : ' + str(i) + ': not multipart')
        self.print_elapsed_seconds('Total run time', start)
        print('converted: ' + str(len(filesWritten)))

    def print_elapsed_seconds(self, msg, start):
        secs = round(time.time() - start, 0)
        print(msg + ': ' + str(secs) + ' seconds')

    def create_file_name(self, subject):
        subject = subject.replace(' ', 'xxxxx')
        subject = re.sub(r'Re: ', '', subject)
        subject = re.sub(r'Seen on a past walk', '', subject)
        fname = re.sub(r'\W', '', subject) + '.png'
        fname = fname.replace('xxxxx', ' ')
        fname = fname.replace('Seen on todays walk ', '')
        return fname

    def convert_to_png(self, fname, thePart):
        pastHeaders = False
        pngData = ''
        for aLine in thePart.split('\n'):
            if pastHeaders:
                pngData = pngData + (aLine + '\n')
            if aLine == '':
                pastHeaders = True
        g = open(fname, "wb")
        g.write(base64.b64decode(pngData))
 
mboxToKml().run()
