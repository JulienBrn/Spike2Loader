from pathlib import Path
import logging, sys, tqdm.auto as tqdm
from sonpy import lib as sp
import pandas as pd, numpy as np
from typing import Union, Mapping, Sequence, AbstractSet, Literal, Tuple
import types

logger = logging.getLogger(__name__)

events_channel_types = [sp.DataType.EventFall, sp.DataType.EventRise, sp.DataType.EventBoth]
continuous_channel_types =  [sp.DataType.Adc]


def as_python_data(
        file: Union[str, Path], 
        channels: AbstractSet[Union[int, str]] =[...], 
        channel_types: AbstractSet[Union[str, sp.DataType]] =[...], 
        progress:bool=True
) -> Tuple[pd.DataFrame, Mapping[str, np.ndarray]]:
    
    path = Path(file)
    MyFile = sp.SonFile(str(path), True)
    rev = ... in channel_types
    channel_types = set(channel_types) - set((...,))
    all_channels = {MyFile.GetChannelTitle(i):i  for i in range(MyFile.MaxChannels()) if MyFile.ChannelType(i) != sp.DataType.Off and ((MyFile.ChannelType(i) in channel_types) != rev )}
    channels = set(all_channels[c] if isinstance(c, str) else c for c in channels)
    if ... in channels:
        channels = set(all_channels.values()) - channels

    time_base = MyFile.GetTimeBase()
    df_data = []
    channel_data = {}
    for i in tqdm.tqdm(channels, desc="Loading data", disable=not progress):
        name=MyFile.GetChannelTitle(i)
        type=MyFile.ChannelType(i)
        unit=MyFile.GetChannelUnits(i)
        size=MyFile.ChannelBytes(i)
        item_size=MyFile.ItemSize(i)
        scale=MyFile.GetChannelScale(i)/6553.6
        offset=MyFile.GetChannelOffset(i)
        divide = MyFile.ChannelDivide(i)
        # max_time = MyFile.ChannelMaxTime(i)


        n_expected_data = int(size/item_size)
        n_queried_data = int(n_expected_data*1.1) + 100

        if n_expected_data == 0:
            logger.warning(f"No data expected in channel {name}. Removing it.")
            continue

        if type in events_channel_types:
            data_kind="Event"
            fs = pd.NA
            data = np.array(sp.SonFile.ReadEvents(MyFile, i, n_queried_data, 0)).astype(float) * time_base
            n_data = data.size
            if type == sp.DataType.EventBoth:
                if not data.size % 2== 0:
                    logger.warning(f"Not as many rise as fall events for channel {name}. Continuing by adding a NaN")
                    data = np.concatenate([data, [np.nan]])
                data = data.reshape(-1, 2, order="C")
        elif type in continuous_channel_types:
            data_kind="RegularSampling"
            fs = 1/(divide*time_base)
            data = np.array(sp.SonFile.ReadInts(MyFile, i, n_queried_data, 0)) * scale + offset
            n_data = data.size
        else:
            logger.warning(f"Ignoring channel {name} because unsupported")

        if n_data >= n_queried_data:
            raise Exception(f"Some data will be missing in channel {name}")
        
        df_data.append(dict(name=name, data_kind=data_kind, smrx_channel_num=i, smrx_type=str(type), unit=str(unit), n_data=n_data, fs=fs))
        channel_data[name]=data
    df = pd.DataFrame(df_data).set_index("name")
    return df, channel_data

def smrx2python():
    import beautifullogger, argparse, string
    parser = argparse.ArgumentParser(description='Converts smrx files into a tsv file and a set of numpy files')
    # parser.add_argument('verbose', metavar='v', type=str, default="Info",
    #                 help='change logging level possibilities are [Debug, Info, Warning, Error]')
    parser.add_argument('-i', type=str, required=True,
                    help='input smrx file to convert')
    parser.add_argument('-o', type=str, default="{smrx_path}.tsv", required=False,
                    help='output destination of the dataframe file')
    parser.add_argument('-onp', type=str, default="{smrx_path}_data",required=False,
                    help='output folder of the array files')
    args = parser.parse_args(sys.argv[1:])
    input= Path(args.i)
    keys = dict(smrx_path=input.parent/input.stem)
    ouputtsv = Path(string.Formatter().format(args.o, **keys))
    ouputnpy = Path(string.Formatter().format(args.onp, **keys))
    beautifullogger.setup(displayLevel=logging.INFO)


    logger.info("Starting")
    df, d = as_python_data(input)
    logger.info(f"Dataframe is\n{df}")
    logger.info(f"Saving dataframe")
    df.to_csv(ouputtsv, index=True, sep="\t")
    ouputnpy.mkdir(parents=True, exist_ok=True)
    logger.info(f"Saving npys")
    for k,v in tqdm.tqdm(d.items(), desc="Saving npys"):
        np.save(ouputnpy / f"{k}.npy", v)

    logger.info("Done")