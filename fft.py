import glob
import os
import time
import numpy as np
from codeBRT.parsing.interface.generic_type import ChannelType, EventType
from codeBRT.parsing.brt.reader import BrtMeasurementReader
from scipy.fft import fft, fftfreq
from matplotlib import pyplot as plt

list_of_files = glob.glob('C:\ProgramData\OSG\BrainRT\Signals\Online\*.sig')
latest_file = ''
while(True):
	latest_file = max(list_of_files, key=os.path.getctime)
	if '-hdr.sig' in latest_file:
		break
	else:
		list_of_files.remove(latest_file)
# Define path to PSG sig files. Important: path should end with '-hdr.sig'!
#path = latest_file #r'%s' % latest_file
path = r'C:\ProgramData\OSG\BrainRT\Signals\Online\osg_00000_0000145-hdr.sig'

#TODO: probeer om np.mag(data) te gebruiken om amplitude signaal te vinden.
#TODO: oxymeter uitlezen

def npfft(path):
	# Define reader and get list of all channels
	result = []
	reader = BrtMeasurementReader(path)
	channels = reader.channel_list
	data_eeg = reader.read_data(ChannelType.EEG) # data of all EMG channels
	data = data_eeg["13"][0].data
	sampleRate = data_eeg["13"][0].sampling_rate
	N = len(data_eeg["13"][0].data)
	fftx = fftfreq(N,1/sampleRate).tolist()
	fftx = fftx[int(len(fftx)/2):]	#only look at second half of values, others are mirrored over zero, we only need positive values
	fftx = list(map(abs,fftx))		#take magnitude of complex numbers
	ffty = fft(data).tolist()
	ffty = ffty[int(len(ffty)/2):]	#only look at second half of values, others are mirrored over zero, we only need positive values
	ffty = list(map(abs,ffty))		#take magnitude of complex numbers
	maxindex = ffty.index(max(ffty))	#the same index in fftx should give the frequency of the ingoing signal
	print(int(fftx[maxindex]))
	indexes = []
	frequencies = []
	for i in range (len(ffty)):		#only look at second half of values, others are mirrored over zero, we only need positive values
		if ffty[i] > ffty[maxindex]/10 and round(fftx[i])>0:	#check if spike is higher than 10% of highest spike
			if not round(fftx[i]) in frequencies:
				frequencies.append(round(fftx[i]))
				print(fftx[i],ffty[i])
	print(frequencies)
	magnitude = max(data)
	print(magnitude)
	result.append(frequencies)
	return result

npfft(path)