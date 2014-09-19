import urllib.request
import csv
from tkinter import *
from tkinter.ttk import Combobox

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        root.title("NHL Stats to CSV")
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        
        frame1 = Frame(self)
        season_frame = Frame(frame1)
        self.seasonlabel = Label(season_frame, text="Season")
        season_list = ('2013-2014', '2012-2013', '2011-2012', '2010-2011',
                       '2009-2010', '2008-2009', '2007-2008', '2006-2007',
                       '2005-2006', '2003-2004', '2002-2003', '2001-2002',
                       '2000-2001', '1999-2000', '1998-1999', '1997-1998')
        self.season = Combobox(season_frame, values=season_list, state='readonly')
        self.season.current(0)
        self.seasonlabel.pack()
        self.season.pack()
        season_frame.pack(side=LEFT, padx=5, pady=5)

        position_frame = Frame(frame1)
        self.positionlabel = Label(position_frame, text="Position")
        position_list = ('All Skaters', 'Goalies', 'Forwards', 'Defenseman',
                         'Center', 'Left Wing', 'Right Wing')
        self.position = Combobox(position_frame, values=position_list, state='readonly')
        self.position.current(0)
        self.positionlabel.pack()
        self.position.pack()
        position_frame.pack(side=LEFT, padx=5, pady=5)
        frame1.pack(side=TOP)

        frame2 = Frame(self)
        gameType_frame = Frame(frame2)
        self.gameTypelabel = Label(gameType_frame, text="Game Type")
        gameType_list = ('Regular Season', 'Playoffs')
        self.gameType = Combobox(gameType_frame, values=gameType_list, state='readonly')
        self.gameType.current(0)
        self.gameTypelabel.pack()
        self.gameType.pack()
        gameType_frame.pack(side=LEFT, padx=5, pady=5)

        grouping_frame = Frame(frame2)
        self.groupinglabel = Label(grouping_frame, text="Grouping")
        grouping_list = ('By League', 'By Team')
        self.grouping = Combobox(grouping_frame, values=grouping_list, state='readonly')
        self.grouping.current(0)
        self.groupinglabel.pack()
        self.grouping.pack()
        grouping_frame.pack(side=LEFT, padx=5, pady=5)
        frame2.pack(side=TOP)

        frame3 = Frame(self)
        self.progress = Label(frame3, text="Choose Options and Press Start", relief=SUNKEN, width=30)
        self.progress.pack()
        frame3.pack(side=TOP, padx=5, pady=5)

        frame4 = Frame(self)
        self.start = Button(frame4, text="Start", command=self.start)
        self.QUIT = Button(frame4, text="Quit", command=self.quit)
        self.start.pack(side=LEFT)
        self.QUIT.pack(side=LEFT)
        frame4.pack(side=TOP)

    def quit(self):
        root.destroy()

    def start(self):
        self.progress.config(text="Working...")
        season_fn = self.season.get()
        season = season_fn.replace("-", "")
        gameType = self.gameType.get()
        if gameType == "Regular Season":
            gameType = "2"
        else:
            gameType = "3"
        grouping = self.grouping.get()
        position = self.position.get()
        if position == "All Skaters":
            position = "S"
        position = position[0]

        # For csv filename
        gameTypes = {"2": "regularseason", "3": "playoffs"}

        positions = {"S": "skater", "G": "goalie", "F": "forward", "D": "defenseman",
                     "C": "center", "L": "leftwing", "R": "rightwing"}

        gameType_fn = gameTypes[gameType]
        position_fn = positions[position]
        grouping_fn = ""
        if grouping == "By League":
            grouping_fn = "byleague"
        else:
            grouping_fn = "byteam"

        self.filename = "nhl_" + season_fn + "_" + gameType_fn + "_" + position_fn + "stats" + "_" + grouping_fn + ".csv"

        # Stat column headings
        skater_header = [['Rank', 'Player', 'Team', 'Pos', 'GP', 'G', 'A', 'Pts',
                           '+/-', 'PIM', 'PPG', 'PPP', 'SHG', 'SHP', 'GW', 'OT', 'S',
                           'S%', 'TOI/G', 'Sft/G', 'FO%']]

        skater_header2 = [['Rank', 'Player', 'Team', 'Pos', 'GP', 'G', 'A', 'Pts',
                           '+/-', 'PIM', 'PPG', 'PPP', 'SHG', 'SHP', 'GW', 'GT', 'OT',
                           'S', 'S%', 'TOI/G', 'Sft/G', 'FO%']]

        goalie_header = [['Team Rank', 'Player', 'Team', 'GP', 'GS', 'W', 'L',
                           'OT', 'SA', 'GA', 'GAA', 'Sv', 'Sv%', 'SO', 'G', 'A',
                           'PIM', 'TOI']]

        goalie_header2 = [['Team Rank', 'Player', 'Team', 'GP', 'GS', 'W', 'L', 'T',
                           'OT', 'SA', 'GA', 'GAA', 'Sv', 'Sv%', 'SO', 'G', 'A',
                           'PIM', 'TOI']]

        # Pre-lockout seasons had an extra stat column for regular season only.
        if gameType == "2" and season in ['20032004', '20022003', '20012002',
                      '20002001', '19992000', '19981999', '19971998']:
            if position == "G":
                header = goalie_header2
            else:
                header = skater_header2
        else:
            if position == "G":
                header = goalie_header
            else:
                header = skater_header

        with open(self.filename, 'w', newline='', encoding='utf-8') as fp:
                a = csv.writer(fp, delimiter=",")
                a.writerows(header)
                
        # URL Pieces
        url1 = "http://www.nhl.com/ice/playerstats.htm?season="  # 20132014, 20122013
        url2 = "&gameType="   # 2 (Regular), 3 (Playoffs)
        url3 = "&team="       # ANA, BOS
        url4 = "&position="   # S, G, C, L, R, F
        url5 = "&country=&status=&viewName=summary#"

        # Calls statgrab with 'byleague' or 'byteam'
        if grouping == "By League":
            url = url1 + season + url2 + gameType + url3 + url4 + position + url5
            self.statgrab(url, season, gameType, position)
        elif grouping == "By Team":
            teams = ["ANA", "ARI", "BOS", "BUF", "CGY", "CAR", 
                    "CHI", "COL", "CBJ", "DAL", "DET", "EDM", 
                    "FLA", "LAK", "MIN", "MTL", "NSH", "NJD", 
                    "NYI", "NYR", "OTT", "PHI", "PIT", "SJS",
                    "STL", "TBL", "TOR", "VAN", "WSH", "WPG"]
            teams = self.removeteams(teams, season, gameType)
            for t in teams:
                url = url1 + season + url2 + gameType + url3 + t + url4 + position + url5
                self.statgrab(url, season, gameType, position, t)
        self.progress.config(text="Finished")

    def statgrab(self, url, season, gameType, position, t=""):
        """Grabs the stats and stores each player in
        playerstats and puts all of those into allstats."""

        allstats = []

        # Pre-lockout seasons had an extra stat column for regular season only.

        if gameType == "2" and season in ['20032004', '20022003', '20012002',
                                          '20002001', '19992000', '19981999', '19971998']:
            if position == "G":
                columns = 19
            else:
                columns = 22
        else:
            if position == "G":
                columns = 18
            else:
                columns = 21

        page = urllib.request.urlopen(url)
        text = page.read().decode("utf8")   
        index = text.find(">1</td><td colspan=")
        lastindex = text.find("statsLegend")
        totalplayers_pos = text.find("results.")
        totalplayers_of_pos = text.rfind("of ", 0, totalplayers_pos)
        totalplayers = int(text[(totalplayers_of_pos + 3):(totalplayers_pos - 1)])
        doneplayers = 0
        newpage = 30
        pagenum = 1

        while doneplayers < totalplayers:
            playerstats = []

            while len(playerstats) < columns:
                if position == "G" and gameType == "3" and season in ['20022003', '20012002', '20002001', 
                                                                       '19992000', '19981999', '19971998']:
                    usecolumn = [1, 4, 8, 11, 13, 15, 17, 19, 21,
                                 23, 25, 27, 29, 31, 33, 35, 37, 39]
                    uc = 0
                    
                    while uc < 42:
                        uc += 1
                        start = text.find(">", index) + 1
                        index = start
                        end = text.find("<", index)
                        index = end
                    
                        playerdata = (text[start:end])
                        if uc in usecolumn:
                            playerstats.append(playerdata)
                    
                else:
                    start = text.find(">", index) + 1
                    index = start
                    end = text.find("<", index)
                    index = end
                
                    playerdata = (text[start:end])
                    if playerdata:
                        playerstats.append(playerdata)

            allstats.append(playerstats)
            doneplayers += 1

            if doneplayers == newpage:
                np1 = "http://www.nhl.com/ice/playerstats.htm?fetchKey="
                np_season = str(season[4:])
                np_position = position + "A" + position
                np2 = "ALL&viewName=summary&sort=points&pg="
                pagenum += 1
                newpage += 30
                if t != "":
                    url = np1 + np_season + gameType + t + np_position + np2 + str(pagenum)
                else:
                    url = np1 + np_season + gameType + t + "ALL" + np_position + np2 + str(pagenum)
                page = urllib.request.urlopen(url)
                text = page.read().decode("utf8")
                index = text.find(">" + str(doneplayers + 1) + "</td><td colspan=")
                lastindex = text.find("statsLegend")

        with open(self.filename, 'a', newline='', encoding='utf-8') as fp:
            a = csv.writer(fp, delimiter=",")
            a.writerows(allstats)

    def removeteams(self, teams, season, gameType):
        # Removes expansion teams from specific years
        if season == "19992000":
            for r in ["CBJ", "MIN"]:
                teams.remove(r)
        elif season == "19981999":
            for r in ["CBJ", "MIN", "WPG"]:
                teams.remove(r)
        elif season == "19971998":
            for r in ["CBJ", "MIN", "WPG", "NSH"]:
                teams.remove(r)
        # Removes non-playoff teams for playoffs stats from specific years
        if gameType == "3":
            if season == "20132014":
                for r in ["WSH", "NJD", "OTT", "TOR", "CAR", "NYI", "FLA",
                          "BUF", "ARI", "NSH", "WPG", "VAN", "CGY", "EDM"]:
                    teams.remove(r)
            elif season == "20122013":
                for r in ["WPG", "PHI", "NJD", "BUF", "CAR", "TBL", "FLA",
                          "CBJ", "ARI", "DAL", "EDM", "CGY", "NSH", "COL"]:
                    teams.remove(r)
            elif season == "20112012":
                for r in ["BUF", "TBL", "WPG", "CAR", "TOR", "NYI", "MTL",
                          "CGY", "DAL", "COL", "MIN", "ANA", "EDM", "CBJ"]:
                    teams.remove(r)
            elif season == "20102011":
                for r in ["CAR", "TOR", "NJD", "WPG", "OTT", "NYI", "FLA",
                          "DAL", "CGY", "STL", "MIN", "CBJ", "COL", "EDM"]:
                    teams.remove(r)
            elif season == "20092010":
                for r in ["NYR", "WPG", "CAR", "TBL", "NYI", "FLA", "TOR",
                          "STL", "CGY", "ANA", "DAL", "MIN", "CBJ", "EDM"]:
                    teams.remove(r)
            elif season == "20082009":
                for r in ["FLA", "BUF", "OTT", "TOR", "WPG", "TBL", "NYI",
                          "MIN", "NSH", "EDM", "DAL", "ARI", "LAK", "COL"]:
                    teams.remove(r)
            elif season == "20072008":
                for r in ["CAR", "BUF", "FLA", "TOR", "NYI", "WPG", "TBL",
                          "EDM", "CHI", "VAN", "ARI", "CBJ", "STL", "LAK"]:
                    teams.remove(r)
            elif season == "20062007":
                for r in ["TOR", "MTL", "CAR", "FLA", "BOS", "WSH", "PHI",
                          "COL", "STL", "CBJ", "EDM", "CHI", "LAK", "ARI"]:
                    teams.remove(r)
            elif season == "20052006":
                for r in ["TOR", "WPG", "FLA", "NYI", "BOS", "WSH", "PIT",
                          "VAN", "LAK", "MIN", "ARI", "CBJ", "CHI", "STL"]:
                    teams.remove(r)
            elif season == "20032004":
                for r in ["BUF", "WPG", "CAR", "FLA", "NYR", "WSH", "PIT",
                          "EDM", "MIN", "LAK", "ANA", "ARI", "CBJ", "CHI"]:
                    teams.remove(r)
            elif season == "20022003":
                for r in ["NYR", "MTL", "WPG", "BUF", "FLA", "PIT", "CAR",
                          "CHI", "LAK", "ARI", "CGY", "NSH", "SJS", "CBJ"]:
                    teams.remove(r)
            elif season == "20012002":
                for r in ["WSH", "BUF", "NYR", "PIT", "TBL", "FLA", "WPG",
                          "EDM", "DAL", "CGY", "MIN", "ANA", "NSH", "CBJ"]:
                    teams.remove(r)
            elif season == "20002001":
                for r in ["BOS", "NYR", "MTL", "FLA", "WPG", "TBL", "NYI",
                          "ARI", "NSH", "CGY", "CHI", "CBJ", "MIN", "ANA"]:
                    teams.remove(r)
            elif season == "19992000":
                for r in ["CAR", "MTL", "NYR", "BOS", "NYI", "TBL", "WPG",
                          "ANA", "VAN", "CHI", "CGY", "NSH"]:
                    teams.remove(r)
            elif season == "19981999":
                for r in ["FLA", "NYR", "MTL", "WSH", "NYI", "TBL", "CGY",
                          "CHI", "LAK", "NSH", "VAN"]:
                    teams.remove(r)
            elif season == "19971998":
                for r in ["CAR", "NYI", "NYR", "FLA", "TBL", "CHI", "TOR",
                          "CGY", "ANA", "VAN"]:
                    teams.remove(r)
        return(teams)                        

root = Tk()
app = Application(master=root)
app.mainloop()

