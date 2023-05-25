import glob
import os
import numpy as np
import settings as sets
from codeBRT.parsing.interface.generic_type import ChannelType, EventType, Spo2ChannelSubtype
from codeBRT.parsing.brt.reader import BrtMeasurementReader
from numpy.fft import fft, fftfreq
from matplotlib import pyplot as plt

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
	path = latest_file #r'%s' % latest_file
	print(path)
	return path


def np_fft(path,cursor,bip):
	#returns list containing a list for each channel containing a list with all unignorable frequencies and the amplitude of the highest signal
	freqAndAmp = []
	# Define reader and get list of all channels
	reader = BrtMeasurementReader(path)
	data_eeg = reader.read_data()#ChannelType.EEG)			#data of all EEG channels
	if not bip:
		cursor.execute("SELECT inputName FROM inputs WHERE testID = 0;")
	else:
		cursor.execute("SELECT inputName FROM inputs WHERE testID = 0 AND bip = 1;")
	channels = cursor.fetchall()
	print("inputs", channels)
	for i in range(len(channels)):
		if not bip:												#for a reference measurement, the first channel in channels will be the G2 (because of the structure of the DB), this channel doesn't have any data and will raise an error
			if i==0:
				continue
		data = data_eeg[channels[i][0]][0].data					#datapoints of signal on channel, 0 because I look at the first file, sometimes multiple files are made, does not apply on this project
		sampleRate = data_eeg[channels[i][0]][0].sampling_rate	#sample rate
		N = len(data_eeg[channels[i][0]][0].data)				#number of datapoints
		fftx = fftfreq(N,1/sampleRate).tolist()
		fftx = fftx[:int(len(fftx)/2)]							#only look at second half of values, others are mirrored over zero, we only need positive values
		ffty = fft(data).tolist()
		ffty = ffty[:int(len(ffty)/2)]							#only look at second half of values, others are mirrored over zero, we only need positive values
		ffty = 2/N * np.abs(ffty)								#get amplitude of fft
		maxindex = np.where(ffty == max(ffty))					#the same index in fftx should give the frequency of the ingoing signal
		amplitude = max(ffty)
		#plt.plot(fftx, np.abs(ffty))
		#plt.show()
		indexes = []
		frequencies = []
		for i in range (len(ffty)):									#only look at second half of values, others are mirrored over zero, we only need positive values
			if ffty[i] > ffty[maxindex]/10 and round(fftx[i])>0:	#check if spike is higher than 10% of highest spike
				if not round(fftx[i]) in frequencies:
					frequencies.append(round(fftx[i]))
		freqAndAmp.append([frequencies,amplitude])						# 3D list, contais lists containing a list (frequencies, only one when correct) and a value (amplitude)
	print(freqAndAmp)
	return freqAndAmp	

def oxyMeter(path):
	#returns a list: [saturation,heartrate]
	reader = BrtMeasurementReader(path)
	channels = reader.channel_list
	data_sao2 = reader.read_data(Spo2ChannelSubtype.SAO2)				#info about saturation
	data_heartrate = reader.read_data(Spo2ChannelSubtype.HEART_RATE)	#info about heartrate
	print(data_sao2['SaO2'][0].data)
	print(data_heartrate['Heartrate'][0].data)
	info = []
	info.append(findMostFrequent(data_sao2['SaO2'][0].data))			#take the value that appears most frequent, even with virtual patient, the heartrate can have some variation in the start or at the end of a measurement
	info.append(findMostFrequent(data_heartrate['Heartrate'][0].data))
	return info

def findMostFrequent(array):
	#returns the value that is the most frequent in the second half of an array, I use only the second half because the values need some time to settle
	# Sort the array
	arr=array[int(len(array)/2):]
	arr.sort()
	# find the max frequency using
	# linear traversal
	max_count = 1
	result = arr[0]
	curr_count = 1
	for i in range(1, len(arr)):
		if (arr[i] == arr[i - 1]):
			curr_count += 1
		else:
			curr_count = 1
		# If last element is most frequent
		if (curr_count > max_count):
			max_count = curr_count
			result = arr[i - 1]
	return result

#for testing purposes
#print(np_fft(r'C:\ProgramData\OSG\BrainRT\Signals\Online\osg_00000_0000145-hdr.sig'))
#print(oxyMeter('C:\ProgramData\OSG\BrainRT\Signals\Online\osg_00000_0000145-hdr.sig'))