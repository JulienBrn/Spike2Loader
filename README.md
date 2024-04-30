# Spike2Loader

A simple loader for Spike2 files (.smrx). Note that this package uses the sonpy package provided by spike2 which requires python 3.9.

It provides one executable named `smrx2python` that directly operates on files and a function named `as_python_data` to load an smrx file as a pandas table and numpy arrays.


## smrx2python executable

The usage is the following:

`smrx2python -i MYFILE.smrx`, where *MYFILE.smrx* is the path to your spike2 file.

It will create a tsv file *MYFILE.tsv* and a folder named *MYFILE_data* in the same folder as *MYFILE.smrx*. The contents are:
- *MYFILE.tsv* contains metadata for each channel
- *MYFILE_data* contains an `.npy` file (numpy array) for each channel. 
    - For event channels, the contents of the array are the timing of the events in seconds. 
    Note if the channel is registered as a rise and fall event (*EventBoth* on spike2), then the array will have two columns, one for rise and one for fall.
    - For continuous channels the arrays are simply the set of values at the given sampling frequency (given by *fs* (in Hertz) from *MYFILE.tsv*)


## as_python_data function

Similar to `smrx2python -i MYFILE.smrx` but returns the pandas dataframe and a dictionary of numpy array instead of files.