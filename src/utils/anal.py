"""
Analysis functions for reading scoresheets and combining stats.
"""

from db.model import Scoresheet, Statline

class PacketStats:

    def __init__(self, s: Scoresheet, overall = False):
        self.writer = s.writer
        if overall:
            self.writer = "Overall"
        self.stats : dict[str, Statline] = dict()
        questions = len(s.questions)

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
            if self.stats[player].written > 0 and new.stats[player].written > 0:
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

    return {key: stat_dict[key].sorted_stats() for key in stat_dict}