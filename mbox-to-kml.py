import mailbox
import time
import base64
import re

class mboxToKml:
    def run(self):
        start = time.time()
        for self.year in {'2020-10-emails'}: # '2020', '2021', '2022'}: 
            self.oneYear()
        self.print_elapsed_time('Full run', start)

    def oneYear(self):
        filesWritten = {}
        start = time.time()
        mbox = mailbox.mbox(self.year + '.mbox')
        for i, message in enumerate(mbox):
            if i == 0:
                self.print_elapsed_time('Open mbox file: ' + self.year + '.mbox', start)
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
                                if not fname:
                                    fname = str(i)
                                if fname in filesWritten.keys():
                                    pngData = self.extract_png_data(thePart)
                                    if pngData == filesWritten[fname]['pngData']:
                                        print('***** dup: ' + fname + ': for subject: "' + message['subject'] + '"')
                                    else:
                                        print('***** dup name but not data: ' + fname + ': for subject: "' + message['subject'] + '"')
                                else:
                                    # strt = time.time()
                                    # self.convert_to_png(fname, thePart)
                                    # secs = round(time.time() - strt, 0)
                                    # print(str(secs) + ': ' + fname)
                                    filesWritten[fname] = { 'subject' : message['subject'], 'date' : message['date'], 'pngData' : self.extract_png_data(thePart)}
                        else:
                            print('Message# : ' + str(i) + ': unhandled: ' + part._default_type)
                else:
                    print('Message# : ' + str(i) + ': not multipart')
        self.print_elapsed_time('Total run time', start)
        print('converted: ' + str(len(filesWritten)))
        self.write_kml(filesWritten)

    def write_kml(self, fnames):
        kml = '<?xml version="1.0" encoding="UTF-8"?>\n\
<kml xmlns="http://www.opengis.net/kml/2.2">\n\
  <Document>\n'
        for fn, headers in fnames.items():
            kml = kml + ('    <Placemark>\n' +
'      <name>' + fn.replace('.png', '') + '</name>\n' +
'      <description>' + headers['date'] + '</description>\n' +
'      <styleUrl>#icon-1899-0288D1</styleUrl>\n' +
'      <Point>\n' +
'        <coordinates>\n' +
'        </coordinates>\n' +
'      </Point>\n' +
'    </Placemark>\n')
        kml = kml + ('  </Document>\n' +
'</kml>')
        g = open(self.year + '.kml', "w")
        g.write(kml)
    
    def print_elapsed_time(self, msg, start):
        secs = round(time.time() - start, 0)
        s = format(int(round(secs / 60)), '02d') + ':' + format(int(round(secs % 60)), '02d')
        print(msg + ': ' + s + ' mm:ss')

    def create_file_name(self, subject):
        subject = subject.replace(' ', 'xxxxx')
        subject = re.sub(r'Re: ', '', subject)
        subject = re.sub(r'Seen on a past walk', '', subject)
        fname = re.sub(r'\W', '', subject) + '.png'
        fname = fname.replace('xxxxx', ' ')
        fname = fname.replace('Seen on todays walk ', '')
        return fname

    def extract_png_data(self, thePart):
        pastHeaders = False
        pngData = ''
        for aLine in thePart.split('\n'):
            if pastHeaders:
                pngData = pngData + (aLine + '\n')
            if aLine == '':
                pastHeaders = True
        return pngData
 
    def convert_to_png(self, fname, thePart):
        g = open('photos\\' + fname, "wb")
        g.write(base64.b64decode(base64.b64decode(self.extract_png_data(thePart))))
 
mboxToKml().run()
