import glob
import os
import numpy as np
import settings as sets
from codeBRT.parsing.interface.generic_type import ChannelType, EventType, Spo2ChannelSubtype
from codeBRT.parsing.brt.reader import BrtMeasurementReader
from scipy.fft import fft, fftfreq
import scipy

def getPath():
	#returns the most recent file ending in -hrd.sig, this is the filetype needed to use Brt2python
	list_of_files = glob.glob('C:\ProgramData\OSG\BrainRT\Signals\Online\*.sig')		#get all .sig files from correct path
	latest_file = ''
	while(True):
		latest_file = max(list_of_files, key=os.path.getctime)
		if '-hdr.sig' in latest_file:
			break
		else:
			list_of_files.remove(latest_file)
	#TODO: does this work? 
	path = latest_file #r'%s' % latest_file
	return path


def np_fft(path):
	#returns list containing a list for each channel containing a list with all unignorable frequencies and the amplitude of the highest signal
	freqAndAmp = []
	#TODO: get this information from DB
	
	# Define reader and get list of all channels
	result = []
	reader = BrtMeasurementReader(path)
	channels = reader.channel_list
	data_eeg = reader.read_data(ChannelType.EEG)	#data of all EEG channels
	for channel in sets.channelList:
		data = data_eeg[channel][0].data				#datapoints of signal on channel, 0 because I look at the first file, sometimes multiple files are made, does not apply on this project
		sampleRate = data_eeg[channel][0].sampling_rate	#sample rate
		N = len(data_eeg[channel][0].data)				#number of datapoints
		fftx = fftfreq(N,1/sampleRate).tolist()
		fftx = fftx[:int(len(fftx)/2)]					#only look at second half of values, others are mirrored over zero, we only need positive values
		ffty = scipy.fft.fft(data).tolist()
		ffty = ffty[:int(len(ffty)/2)]					#only look at second half of values, others are mirrored over zero, we only need positive values
		ffty = 2/N * np.abs(ffty)						#get amplitude of fft
		print(type(ffty))
		maxindex = np.where(ffty == max(ffty))				#the same index in fftx should give the frequency of the ingoing signal
		amplitude = max(ffty)
		print(int(fftx[maxindex[0][0]]))
		import matplotlib.pyplot as plt
		plt.plot(fftx, ffty)
		plt.grid()
		plt.show()
		indexes = []
		frequencies = []
		for i in range (len(ffty)):						#only look at second half of values, others are mirrored over zero, we only need positive values
			if ffty[i] > ffty[maxindex]/10 and round(fftx[i])>0:	#check if spike is higher than 10% of highest spike
				if not round(fftx[i]) in frequencies:
					frequencies.append(round(fftx[i]))
					print(fftx[i],ffty[i])
		result.append(frequencies)
		freqAndAmp.append([result,amplitude])			# 3D list, contais lists containing a list (frequencies, only one when correct) and a value (amplitude)
	return freqAndAmp	

def oxyMeter(path):
	#returns a list: [saturation,heartrate]
	reader = BrtMeasurementReader('C:\ProgramData\OSG\BrainRT\Signals\Online\osg_00000_0000009-hdr.sig')
	channels = reader.channel_list
	data_sao2 = reader.read_data(Spo2ChannelSubtype.SAO2)				#info about saturation
	data_heartrate = reader.read_data(Spo2ChannelSubtype.HEART_RATE)	#info about heartrate
	info = []
	info.append(findMostFrequent(data_sao2['SaO2'][0].data))			#take the value that appears most frequent, even with virtual patient, the heartrate can have some variation in the start or at the end of a measurement
	info.append(findMostFrequent(data_heartrate['Heartrate'][0].data))
	return info

def findMostFrequent(arr):
	#returns the value that is the most frequent in an array
    # Sort the array
    arr.sort()
    # find the max frequency using
    # linear traversal
    max_count = 1
    res = arr[0]
    curr_count = 1
    for i in range(1, len(arr)):
        if (arr[i] == arr[i - 1]):
            curr_count += 1
        else:
            curr_count = 1
         # If last element is most frequent
        if (curr_count > max_count):
            max_count = curr_count
            res = arr[i - 1]
    return res

#for testing purposes
#print(np_fft(r'C:\ProgramData\OSG\BrainRT\Signals\Online\osg_00000_0000145-hdr.sig'))
#print(oxyMeter('C:\ProgramData\OSG\BrainRT\Signals\Online\osg_00000_0000145-hdr.sig'))