'''
Copyright 2014 Demp <lidor.demp@gmail.com>
This file is part of nautilus.

nautilus is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

nautilus is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with nautilus. If not, see <http://www.gnu.org/licenses/>.
'''

import wolframalpha
from core import botutils
from local_settings import wolframalpha_api_key

class wolframalphaClass(botutils.baseClass):

    Client = None
    FirstPodsToShow = None
    Results = None
    Titles = None

    def __init__(self, arg):
        apikey = wolframalpha_api_key
        self.Client = wolframalpha.Client(apikey)
        self.FirstPodsToShow = 3
        botutils.baseClass.__init__(self, arg)

    def SendQuery(self, Query):      
        # Execute the query
        Response = self.Client.query(Query)
        QueryPods = Response.pods
        CountPods = 1
        self.Results = []
        self.Titles = []

        if len(QueryPods) == 0:
            return False

        for Pod in QueryPods:
            if Pod.text != "None" and Pod.text != None:
                self.Results.append("\x0307 (%d) \x0301\x1F%s\x1F: %s" % (CountPods, Pod.title, Pod.text.replace("\n", " | ")))
                self.Titles.append("\x0307(%d) \x0301%s" % (CountPods, Pod.title))
                CountPods += 1

        return True

    def onPRIVMSG(self, address, target, text):
        first_word = text.strip().split(" ")[0]
        if botutils.prefix.match(first_word[0]) != None and first_word[1:] == "wa":

            # If single result is wanted
            if len(text.strip().split(" ")) == 2:
                second_word = int(text.strip().split(" ")[1])
                if second_word in range(0, len(self.Results) + 1):
                    self.irc.msg(target, ("%s" % self.Results[second_word - 1]))

                # If there's new query request
                else:
                    Query = " ".join(text.strip().split(" ")[1:])
                    
                    if self.SendQuery(Query):
                        if len(self.Results) <= self.FirstPodsToShow:
                            self.irc.msg(target, ("\x02\x0304Wolfram\x0307Alpha\x0301:\x02%s" % "".join(self.Results)))
                        else:
                            self.irc.msg(target, ("\x02\x0304Wolfram\x0307Alpha\x0301:\x02%s" % "".join(self.Results[:self.FirstPodsToShow])))
                            self.irc.msg(target, ("Additional results are available in the following categories: %s" % " | ".join(self.Titles[self.FirstPodsToShow:])))
                    else:
                        self.irc.msg(target, "\x02\x0304Wolfram\x0307Alpha\x0301: \x02doesn't know how to interpret your input.")

MODCLASSES = [wolframalphaClass]