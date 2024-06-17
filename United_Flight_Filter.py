from tika import parser
import re
import os

'''
Narrowed down
1,2,6,7,8,9,10,12,13,14,15,17,22,23,24,25,26
Narrowed down more
1,2,6,7,10,13,22 - 26
'''

class Trip:
    def __init__(self):
        self.date_of_opp = ''
        self.ID = ''
        self.dep_airports = []
        self.ari_airports = []
        self.lay_time = []
        self.acc_flight_time = []
        self.deadhead = False
        self.total_days = ''
        self.total_credit = ''
        self.total_flight_time = ''
        self.total_time_away = ''
        self.line_start = '' # this marks where the trip entry begins in the document
        self.line_end = '' # this marks where the trip entry ends in the document

    def print_trip(self):
        print(self.date_of_opp + ' ' + self.ID + ' \n' + 
              self.dep_airports[len(self.dep_airports)-1] + ' ' + self.ari_airports[len(self.ari_airports)-1]  + ' \n' +
              self.lay_time[len(self.lay_time)-1] + ' ' + self.acc_flight_time[len(self.acc_flight_time)-1] + ' \n' +
              str(self.deadhead) + ' ' + self.total_days + ' \n' + 
              self.total_credit + ' ' + self.total_flight_time + ' \n' + 
              self.total_time_away + ' ' + str(self.line_start)  + ' ' + str(self.line_end))


'''
html = []

for dirpath, dnames, fnames in os.walk("./pdf_location/"):
    for f in fnames:
        html.append(dirpath + f)
'''

html = ['example.txt']

if (len(html) < 1):
    print('no pdf files found')    
    exit()

LOT = [] # list of trips
cur_trip = -1 # current trip accessed at end of list
inside_trip = False # set if we have logged a ID, 
# otherwise could find match when we aren't below an ID
# like at the top of the document


for f_i_l_e in html:

    print(f_i_l_e)

    raw = parser.from_file(f_i_l_e)
    text = raw['content']
    lines = text.split('\n')

    for x in range(len(lines)):
        temp = re.search('ID L\d+', lines[x])
        if (temp != None):
            LOT.append(Trip())
            cur_trip += 1
            LOT[cur_trip].ID = temp.group(0)
            inside_trip = True

            LOT[cur_trip].line_start = x
        
        if (inside_trip == True):
            temp = re.search('EFF \d+\/\d+\/\d+ THRU \d+\/\d+\/\d+', lines[x])
            if (temp != None):
                LOT[cur_trip].date_of_opp = temp.group(0)

            # sometimes 10 & 13 data does not exist, base off spaces
            temp = re.search('\d+ \w\w\w \w\w\w \d+ \d+ .+', lines[x])
            if (temp != None):

                temp2 = re.search('DH\s+\d+ \w\w\w', lines[x])
                if (temp2 != None):
                    LOT[cur_trip].deadhead = True


                temp = temp.group(0)
                # need b/c trip number sometimes has 3 or 4 characters
                str_temp = re.search('\d+ \d+ .+', temp).group(0)
                
                temp = re.findall('[a-zA-Z][a-zA-Z][a-zA-Z]', temp)
                
                LOT[cur_trip].dep_airports.append(temp[0])
                LOT[cur_trip].ari_airports.append(temp[1])
                LOT[cur_trip].lay_time.append(str_temp[11:16])
                LOT[cur_trip].acc_flight_time.append(str_temp[31:35])
            
            temp = re.search("DAYS- \d CRD-[\d\s]+\.[\d\s]+\* FTM-[\d\s]+\.[\d\s]+\* TAFB-[\d\s]+\.[\d]+", lines[x])
            if (temp != None):
                temp = temp.group(0)
                LOT[cur_trip].total_days = temp[6:7]
                LOT[cur_trip].total_credit = temp[12:18]
                LOT[cur_trip].total_flight_time = temp[23:29]
                LOT[cur_trip].total_time_away = temp[35:42]

            temp = re.search('----+', lines[x])
            if (temp != None):
                LOT[cur_trip].line_end = x
                inside_trip = False

LOT[cur_trip].print_trip()

'''
    f = Flight(,,,
               ,,,
               ,,,
               ,,)
'''