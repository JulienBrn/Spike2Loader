import pathlib
import sonpy
import logging
import os
import errno
import time
# import scimath.units.time
import pandas

logger = logging.getLogger(__name__)

def get_sonpy_object(file : pathlib.Path) -> sonpy.lib.SonFile:
    """Retrieve a sonpy object from a file. May raise FileNotFoundError or RuntimeError."""

    if(not file.exists()) :
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), str(file))
    smrx = sonpy.lib.SonFile(sName=str(file), bReadOnly=True)
    if("Empty <sonpy.SonFile> object." in str(smrx)) :
        raise  RuntimeError("Problem while loading SonFile {}. Message provided is :\n{}".format(file, smrx))
    return smrx


# def get_channels(sonpy_object : sonpy.lib.SonFile) :
#     res=[]
#     for channel in range(sonpy_object.MaxChannels()):
        
#         ctype= sonpy_object.ChannelType(channel)
#         if(ctype == sonpy.lib.DataType.Off):
#             continue
#         else :
#             logger.info("----------------------------{}, {}------------------------------".format(sonpy_object.GetChannelTitle(channel), ctype))

#         if(ctype == sonpy.lib.DataType.Adc):
#             continue
#             res.append(read_adc_channel(sonpy_object, channel))
#         elif(ctype == sonpy.lib.DataType.Off):
#             pass
#         elif(ctype == sonpy.lib.DataType.EventBoth):
#             res.append(read_event_channel(sonpy_object, channel))
#         else:
#             logger.warning("Passing through non implemented channel type. Type is {}".format(sonpy_object.ChannelType(channel)))


# def read_adc_channel(sonpy_object : sonpy.lib.SonFile, channel : int):
#     if(not(0<= channel < sonpy_object.MaxChannels())) :
#         raise IndexError("Sonpy object only has {} channels, but trying to read channel {}".format(sonpy_object.MaxChannels(), channel))
#     if(sonpy_object.ChannelType(channel) != sonpy.lib.DataType.Adc) :
#         raise IndexError("Channel {} with name \"{}\" has incorrect type. Expecting {} got {}.".format
#             (channel, sonpy_object.GetChannelTitle(channel), sonpy.lib.DataType.Adc, sonpy_object.ChannelType(channel)))
    
#     divide = sonpy_object.ChannelDivide(channel)
#     idealRate = sonpy_object.GetIdealRate(channel)
#     max_time = sonpy_object.ChannelMaxTime(channel)
#     first_time = sonpy_object.FirstTime(channel, 0, max_time)
#     timeBase=sonpy_object.GetTimeBase() 
#     period=divide*timeBase
#     if('%.3g' % (1/idealRate) != '%.3g' % period):
#         logger.warning("Suggested rate is {} Hz (period of {} ms) but sampling period is {} ms ({} Hz).".format(idealRate, 1./idealRate * 1000, period*1000, 1./period) +
#             "They do not match. Continuing using sampling period.")
#     nb_frames=(max_time-first_time)/divide +1
#     logger.info("ADC Channel is {} with starting time {}s, sampling period {}ms, max time {}s. Expecting {} frames".format(sonpy_object.GetChannelTitle(channel), timeBase*first_time, period*1000, timeBase*max_time, nb_frames))
#     start=time.time()
#     arr=sonpy_object.ReadInts(chan=channel, nMax=10**9, tFrom=first_time, tUpto=max_time+1)
#     end=time.time()
#     logger.info("Read a total of {} frames in {} ms".format(len(arr), (end-start) * 10**3))
#     if(nb_frames!= len(arr)):
#         logger.warning("Total number of frames read is different than expected number. Got {} and expected is {}".format(len(arr), nb_frames))

#     return {"data" : arr, "start" : first_time * timeBase * scimath.units.time.sec, "period" : period * scimath.units.time.sec, "end" : scimath.units.time.sec}


# def read_event_channel(sonpy_object : sonpy.lib.SonFile, channel : int):
#     if(not(0<= channel < sonpy_object.MaxChannels())) :
#         raise IndexError("Sonpy object only has {} channels, but trying to read channel {}".format(sonpy_object.MaxChannels(), channel))
#     if(sonpy_object.ChannelType(channel) != sonpy.lib.DataType.EventBoth) :
#         raise IndexError("Channel {} with name \"{}\" has incorrect type. Expecting {} got {}.".format
#             (channel, sonpy_object.GetChannelTitle(channel), sonpy.lib.DataType.EventBoth, sonpy_object.ChannelType(channel)))
    
#     # divide = sonpy_object.ChannelDivide(channel)
#     # idealRate = sonpy_object.GetIdealRate(channel)
#     max_time = sonpy_object.ChannelMaxTime(channel)
#     first_time = sonpy_object.FirstTime(channel, 0, max_time)
#     timeBase=sonpy_object.GetTimeBase()
#     # period=divide*timeBase
#     # if('%.3g' % (1/idealRate) != '%.3g' % period):
#     #     logger.warning("Suggested rate is {} Hz (period of {} ms) but sampling period is {} ms ({} Hz).".format(idealRate, 1./idealRate * 1000, period*1000, 1./period) +
#     #         "They do not match. Continuing using sampling period.")
#     # nb_frames=(max_time-first_time)/divide +1
#     # logger.info("Event Channel is {} with starting time {}s, sampling period {}ms, max time {}s.".format(sonpy_object.GetChannelTitle(channel), timeBase*first_time, period*1000, timeBase*max_time, nb_frames))
#     start=time.time()
#     res_arr=[]
#     block_size=10**3
#     while True:
#         arr=sonpy_object.ReadEvents(chan=channel, nMax=block_size, tFrom=first_time, tUpto=max_time+1)
#         res_arr+=arr
#         if len(arr)<block_size:
#             break

#     end=time.time()
#     logger.warning(25, "Read a total of {} frames in {} ms".format(len(arr), (end-start) * 10**3))
#     return {"data" : arr, "start" : first_time * timeBase * scimath.units.time.sec, "end" : scimath.units.time.sec}

# logging.basicConfig(level=logging.DEBUG)
# logger.info('Started')
# res = get_sonpy_object(pathlib.Path(
#     "/run/user/1000/gvfs/smb-share:server=n-e4-nas-nicom.local,share=ecube/Julien_Exemple/Rat70_20220706_Clara//ephys/rat70_20220706_7600.smrx"
# ))
# get_channels(res)
# logger.info('Finished')


def to_event_dataframe(path: pathlib.Path):
    sonpy_object = get_sonpy_object(path)
    d = pandas.DataFrame(columns=["T", "event_name", "value"])
    for channel in range(sonpy_object.MaxChannels()):
        ctype= sonpy_object.ChannelType(channel)
        if ctype == sonpy.lib.DataType.EventBoth:
            logger.info("----------------------------{}, {}------------------------------".format(sonpy_object.GetChannelTitle(channel), ctype))
            max_time = sonpy_object.ChannelMaxTime(channel)
            first_time = sonpy_object.FirstTime(channel, 0, max_time)
            timeBase=sonpy_object.GetTimeBase()
            block_size=10**3
            cur_time=first_time
            res_arr=[]
            while True:
                arr=sonpy_object.ReadEvents(chan=channel, nMax=block_size, tFrom=cur_time, tUpto=max_time+1)
                if len(arr)!=0:
                    res_arr+=arr
                    cur_time=int(res_arr[-1])
                if len(arr)<block_size:
                    break
            df=pandas.DataFrame()
            df["T"] = [t*timeBase for t in res_arr]
            df["event_name"] = sonpy_object.GetChannelTitle(channel)
            df["value"] = (df.index +1)% 2
            d=pandas.concat([d, df], ignore_index=True)
        elif ctype != sonpy.lib.DataType.Off:
            logger.info("Channel: {}, type: {}".format(sonpy_object.GetChannelTitle(channel), ctype))
    d.sort_values(by=["T"], inplace=True, ignore_index=True)
    return d

