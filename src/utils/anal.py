"""
Analysis functions for reading scoresheets and combining stats.
"""

from db.model import Scoresheet, Statline, OverallStatline

class PacketStats:

    def __init__(self, s: Scoresheet, overall = False):
        self.writer = s.writer
        self.room = s.room
        if overall:
            self.writer = "Overall"
        self.stats : dict[str, Statline] = dict()
        questions = len(s.questions)

        if self.room == 1:
            self.stats[s.writer] = Statline(name=s.writer, written=questions)
        if s.reader != None:
            self.stats[s.reader] = Statline(name=s.reader, read=questions)
        for player in s.roster:
            self.stats[player] = Statline(name=player, played=questions)

        for q in s.questions:
            for b in q:
                self.stats[b.player].add_buzz(b.points)

    def merge_stats(self, new: PacketStats):
        for player in new.stats:
            if player not in self.stats:
                self.stats[player] = Statline(name=player)
            if new.room != 1 and new.stats[player].written > 0:
                continue
            self.stats[player].add_stats(new.stats[player])

    def sorted_stats(self):
        def points_key(s: Statline):
                return s.points()
        
        return sorted([self.stats[player] for player in self.stats], reverse=True, key=points_key)

def compile_stats(scoresheets: list[Scoresheet]):
    """
    Return sorted statline lists for each packet and overall results
    """
    stat_dict : dict[str, PacketStats] = {
        "Overall": None
    }

    for s in scoresheets:
        pack_stats = PacketStats(s)
        if stat_dict["Overall"] == None:
            stat_dict["Overall"] = PacketStats(s, True)
        else:
            stat_dict["Overall"].merge_stats(pack_stats)
        if s.writer in stat_dict:
            stat_dict[s.writer].merge_stats(pack_stats)
        else:
            stat_dict[s.writer] = pack_stats

    return [{
        "writer": key,
        "stats": stat_dict[key].sorted_stats()
    } for key in stat_dict]

def player_stats(player: str, scoresheets: list[Scoresheet]):
    """
    Return player statlines for each toast
    """
    stat_dict: dict[str, Statline] = {}

    for s in scoresheets:
        if s.toast not in stat_dict:
            stat_dict[s.toast] = Statline(name=player)
        stat_dict[s.toast].add_stats(s.player_statline(player))

    overall = OverallStatline(name=player)
    for toast in stat_dict:
        overall.add_stats(stat_dict[toast])
    stat_dict["Overall"] = overall
    return [{
        "toast": key,
        "stats": stat_dict[key]
    } for key in stat_dict]
    
        