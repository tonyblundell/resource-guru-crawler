import argparse
from BeautifulSoup import BeautifulSoup
import config
import mechanize
import re
import sys

class BookingsPrinter:
    weeks = 1
    br = None

    def __init__(self, weeks=1):
        self.weeks = weeks
        br = self.setup_browser()

    def run(self):
        for week in range(self.weeks):
            self.print_week(week)
        
    def setup_browser(self):
        self.br = mechanize.Browser()
        self.br.open(config.URL)
        self.br.select_form(nr=0)
        self.br['session[email]'] = config.EMAIL
        self.br['session[password]'] = config.PASSWORD
        self.br.submit()

    def print_week(self, week):
        nr = 1 if week > 0 else 0
        if week > 0: 
            print '-'*80
        r = re.compile('view=week$')
        link = self.br.find_link(url_regex=r, nr=nr)
        self.br.follow_link(link)
        self.print_bookings()
        
    def print_bookings(self):
        html = self.br.response().read()
        soup = BeautifulSoup(html)
        table = soup.find('table')
        header_cells = table.find('thead').find('tr').findAll('th')
        rows = table.find('tbody').findAll('tr')
        for row in rows:
            for i, td in enumerate(row.findAll('td')):
                if td.text: 
                    day, dom = header_cells[i].string.rsplit(' ', 1)
                    suffix = self.get_day_suffix(int(dom))
                    printable = '{0} {1}{2}'.format(day, dom, suffix)
                    divs = td.findAll('div', {'class': 'involves_user_resource booking'})
                    for j, div in enumerate(divs):
                        time_cell = div.find('div', {'class': 'time'})
                        proj_cell = div.find('div', {'class': 'project ellipsify'})
                        if not proj_cell:
                            proj_cell = div.find('div', {'class': 'description ellipsify'})
                        if time_cell and proj_cell:
                            booking = '{0} {1}'.format(time_cell.string, proj_cell.string[:66]) 
                            if j < 1:
                                printable += ' | '
                            else:
                                printable += '\n         | '
                            printable += time_cell.string + ' ' +  proj_cell.string[:66]
                    print printable

    def get_day_suffix(self, i):
        if 4 <= i <= 20 or 24 <= i <= 30:
            return "th"
        return ["st", "nd", "rd"][i % 10 - 1]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--weeks', type=int, default=1, dest='weeks',
        help='specify the number of weeks to show')
    args = parser.parse_args()
    printer = BookingsPrinter(args.weeks)
    printer.run()
