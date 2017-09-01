import requests
import time

class Contest:
    def __init__(self, title, start_time, duration, judge):
        self._title= title
        self._start_time= start_time
        self._duration= duration
        self._judge= judge

        self._status= 'Running' if start_time <= time.time() <= start_time+duration else 'Scheduled'


    @property
    def title(self):
        return self._title

    @property
    def time(self):
        return self._start_time

    @property
    def duration(self):
        return self._duration

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
        return '%s %s %s' % (self._title, self._start_time)


class DataFetcher:
    """
    Common base class for classes that fetch data from different sources
    """
    DATA_SOURCE = 'NOT_SET'
    JUDGE = 'NOT_SET'
    def __init__(self):
        self.last_updated_data= None
        self.future_contests_list = []

    def getAllContests(self):
        """
        :return: a list of Contests from a source
        """

    def getFutureContests(self):
        """
        :return: a list of upcoming Contests
        """
    def dataUpdated(self):
        pass # todo implemetn


# todo handle server downs
class CodeForcesDataFetcher(DataFetcher):
    DATA_SOURCE = 'http://codeforces.com/'
    JUDGE= 'Code Forces'

    def __init__(self):
        super().__init__()

    def getFutureContests(self):
        # keys in the json object that code forces sends back
        # ['id', 'name', 'type', 'phase', 'frozen', 'durationSeconds', 'startTimeSeconds', 'relativeTimeSeconds']
        m = 'http://codeforces.com/api/contest.list'
        resp = requests.get(m)

        j = resp.json()

        # print(j['result'][0])

        contests= []
        for jsondict in j['result']:
            if jsondict['startTimeSeconds'] + jsondict['durationSeconds'] > time.time():
                contests.append(Contest(jsondict['name'],jsondict['startTimeSeconds'], jsondict['durationSeconds'], self.JUDGE))

        return contests

class ContestDataCollector:
    def __init__(self):
        self.sources= []
        self.sources.append(CodeForcesDataFetcher())

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
