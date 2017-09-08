import requests
import time
import datetime
import pytz
import bs4


class Contest:
    def __init__(self, title, start_time, end_time, judge):
        self._title= title
        self._start_time= start_time
        self._end_time= end_time
        self._judge= judge

        self._status= 'Running' if start_time <= time.time() <= end_time else 'Scheduled'


    @property
    def title(self):
        return self._title

    @property
    def start_time(self):
        return self._start_time

    @property
    def end_time(self):
        return self._end_time

    @property
    def duration(self):
        return self._end_time-self._start_time

    @property
    def status(self):
        return self._status

    @property
    def judge(self):
        return self._judge


    # comparing should be done based on start time
    def __lt__(self, other):
        return self._start_time < other._start_time


    def __str__(self):
        return '%s %s %s' % (self._title, self._start_time, self._judge)

class DataFetcher:
    """
    Common base class for classes that fetch data from different sources
    """
    DATA_SOURCE = 'NOT_SET'
    JUDGE_NANE = 'NOT_SET'
    def __init__(self):
        self.last_updated_data= None
        self.future_contests_list = []


    def getFutureContests(self):
        """
        :return: a list of upcoming Contests
        """


# todo handle server downs
class CodeForcesDataFetcher(DataFetcher):
    DATA_SOURCE = 'http://codeforces.com/'
    JUDGE_NANE= 'Code Forces'

    def __init__(self):
        super().__init__()

    def getFutureContests(self):
        # keys in the json object that code forces sends back
        # ['id', 'name', 'type', 'phase', 'frozen', 'durationSeconds', 'startTimeSeconds', 'relativeTimeSeconds']
        m = 'http://codeforces.com/api/contest.list'
        resp = requests.get(m)

        j = resp.json()

        contests= []
        for jsondict in j['result']:

            start = jsondict['startTimeSeconds']
            duration = jsondict['durationSeconds']
            title= jsondict['name']

            # only include future and running contests
            if start + duration > time.time():
                contests.append(Contest(title, start, start+duration, self.JUDGE_NANE))

        return contests



class CodeChefDataFetcher(DataFetcher):
    DATA_SOURCE = 'https://www.codechef.com/'
    JUDGE_NANE = 'Code Chef'
    CODECHEF_DATE_TIME_FORMAT= '%Y-%m-%dT%H:%M:%S'


    def getFutureContests(self):
        contest_page = self.getContestPage()
        soup = bs4.BeautifulSoup(contest_page , 'lxml')
        tables = soup.findAll('table')

        dataTablesRead = 0  #keep count of how many tables have been read,
        contests= []
        for table in tables:
            # only need to read the first two tables with class set to 'dataTable'
            if dataTablesRead >= 2: break

            try:
                # if this table does not have class attribute set to dataTable
                if not 'dataTable' in table['class']:
                    continue
            except KeyError:
                # in case the table has no class attribute
                continue

            contests.extend(self.processTable(table))
            dataTablesRead+= 1

        return contests

    # Helper methods
    def getContestPage(self):
        resp= requests.get('https://www.codechef.com/contests')
        if resp.status_code != requests.codes['ok']: return ''

        return resp.text

    def processTable(self, table):
        """
        :param table: a BeautifulSoup object representing a table
        :return: list of contests extracted from the table
        """
        tbody = table.tbody

        contests= []
        for row in tbody.findAll('tr'):
            # print(row.contents[1])
            name= row.contents[3].a.string  # name
            start_time= row.contents[5]['data-starttime'] # start date
            end_time= row.contents[7]['data-endtime']  # end date

            unix_start_time = self.convertISTtoUCT(start_time)
            unix_end_time= self.convertISTtoUCT(end_time)

            contests.append(Contest(name, unix_start_time, unix_end_time, self.JUDGE_NANE))

        return contests

    def convertISTtoUCT(self, ist_time):    #todo complete this
        """
        :param ist_time: time in string format: '2017-09-30T19:30:00+05:30' in IST
        :return: UTC in seconds from epoch
        """

        temp = datetime.datetime(1999, 1, 1, 1)
        time_format = '%Y-%m-%dT%H:%M:%S'

        str_t, diff = ist_time.split('+')

        local_tzname = pytz.country_timezones('IN')[0]  #since time is in IST
        local = pytz.timezone(local_tzname)

        tt = temp.strptime(str_t, time_format)
        local_dt = local.localize(tt, is_dst=None)

        utc_dt = local_dt.astimezone(pytz.utc)  # convert localized time to utc time
        utc_dt= utc_dt.replace(tzinfo= None)    # make datetime time zone naive

        utc_epoch = datetime.datetime(1970,1,1) # unix epoch datetime

        # return seconds since epoch (the subtraction returns a timedelta object)
        return (utc_dt - utc_epoch).total_seconds()

class ContestDataCollector:
    def __init__(self):
        self.sources= []
        self.sources.append(CodeForcesDataFetcher())
        self.sources.append(CodeChefDataFetcher())

    def getFutureContests(self):
        """
        :return: a list of future scheduled contests in fetchers list, list is sorted in start time
        """

        contests= []
        for fetch in self.sources:
            contests.extend(fetch.getFutureContests())

        #sorting the contests based on start time
        contests.sort()
        return contests
