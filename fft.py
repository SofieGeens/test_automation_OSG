import glob
import os
import time
import numpy as np
import settings as sets
from Brt2Python.codeBRT.parsing.interface.generic_type import ChannelType, EventType
from Brt2Python.codeBRT.parsing.brt.reader import BrtMeasurementReader
from scipy.fft import fft, fftfreq
from matplotlib import pyplot as plt

def getPath():
	list_of_files = glob.glob('C:\ProgramData\OSG\BrainRT\Signals\Online\*.sig')
	latest_file = ''
	while(True):
		latest_file = max(list_of_files, key=os.path.getctime)
		if '-hdr.sig' in latest_file:
			break
		else:
			list_of_files.remove(latest_file)
	# Define path to PSG sig files. Important: path should end with '-hdr.sig'!
	path = latest_file #r'%s' % latest_file
	return path

#TODO: probeer om np.mag(data) te gebruiken om amplitude signaal te vinden.
#TODO: oxymeter uitlezen

def fft(path):
	freqAndAmp = []
	for channel in sets.channelList:
		# Define reader and get list of all channels
		result = []
		reader = BrtMeasurementReader(path)
		channels = reader.channel_list
		data_eeg = reader.read_data(ChannelType.EEG)	#data of all EMG channels
		data = data_eeg[channel][0].data
		sampleRate = data_eeg[channel][0].sampling_rate
		N = len(data_eeg[channel][0].data)
		fftx = fftfreq(N,1/sampleRate).tolist()
		fftx = fftx[int(len(fftx)/2):]					#only look at second half of values, others are mirrored over zero, we only need positive values
		ffty = fft(data).tolist()
		ffty = ffty[int(len(ffty)/2):]					#only look at second half of values, others are mirrored over zero, we only need positive values
		ffty = 2/N * np.abs(ffty)						#get amplitude of fft
		maxindex = ffty.index(max(ffty))				#the same index in fftx should give the frequency of the ingoing signal
		amplitude = max(ffty)
		print(int(fftx[maxindex]))
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