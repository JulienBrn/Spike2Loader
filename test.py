import logging
import beautifullogger
import spike2loader
import pathlib
import matplotlib.pyplot as plt

logger=logging.getLogger(__name__)
beautifullogger.setup(displayLevel=logging.WARNING)

evs = spike2loader.to_event_dataframe(pathlib.Path("rat70_20220706_7600.smrx"))
evs.to_csv("events.csv", sep="\t", index=False)


from event_dataframe import EventData, draw_events, ChannelInfo

evd = EventData()
channels_dict = {n:ChannelInfo(n, "state", start_value=0) for n in evs["event_name"].unique().tolist()}
evd.from_channels_and_dataframe(channels_dict, evs)

evd.dataframe.to_csv("events.tsv", sep="\t", index=False)
print(evd.get_summary())
d=evd.dataframe
d2=d[((d["event_name"]!="Pad Droi") & (d["event_name"]!="Pad_Gauc") )| (d["duration"]>1)]

evd2=EventData()
evd2.from_channels_and_dataframe(channels_dict, d2)
print(evd2.get_summary())
evd2.draw_plot()
plt.show()