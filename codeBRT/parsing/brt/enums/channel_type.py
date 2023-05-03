# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 16:59:12 2019

@author: JanA
"""

from codeBRT.parsing.brt.enums.brt_type import BrtType


class UnspecifiedSubtype(BrtType):
    UNSPECIFIED = 0, 'unspecified'
    SPECIAL = 1, 'special'


class EegSubtype(BrtType):
    UNSPECIFIED = 0, 'EEG unspecified'
    SPECIAL = 1, 'EEG special'
    SURFACE = 2, 'EEG surface'
    INTRACRANIAL = 3, 'EEG intracranial'


class EmgSubtype(BrtType):
    UNSPECIFIED = 0, 'EMG unspecified'
    SPECIAL = 1, 'EMG special'
    TIBIALR_ENV = 50, 'EMG TibialR env'
    CHIN = 19, 'EMG chin'
    TIBIALL = 20, 'EMG TibialL'
    TIBIALR = 21, 'EMG TibialR'
    CHIN_ENV = 48, 'EMG chin env'
    ARML = 24, 'EMG ArmL'
    ARMR = 25, 'EMG ArmR'
    TIBIALL_ENV = 49, 'EMG TibialL env'


class EcgSubtype(BrtType):
    UNSPECIFIED = 0, 'ECG unspecified'
    SPECIAL = 1, 'ECG special'


class EogSubtype(BrtType):
    UNSPECIFIED = 0, 'EOG unspecified'
    SPECIAL = 1, 'EOG special'
    EAR_REF = 18, 'EOG ear ref'
    LEFT = 16, 'EOG left'
    COMBINED = 17, 'EOG combined'
    VERTICAL = 13, 'EOG vertical'
    HORIZONTAL = 14, 'EOG horizontal'
    RIGHT = 15, 'EOG right'


class RespiratorySubtype(BrtType):
    UNSPECIFIED = 0, 'resp unspecified'
    SPECIAL = 1, 'resp special'
    CO2 = 34, 'resp CO2'
    MOUTH_FLOW = 35, 'resp mouth flow'
    MOUTH_NOSE_VOLUME = 4, 'resp mouth nose volume'
    NOSE_VOLUME = 5, 'resp nose volume'
    MOUTH_VOLUME = 6, 'resp mouth volume'
    ABDOMEN_EFFORT = 7, 'resp abdomen effort'
    THORAX_EFFORT = 8, 'resp thorax effort'
    SUM_FLOW = 41, 'resp sum flow'
    ABDOMEN_FLOW = 39, 'resp abdomen flow'
    SUM_VOLUME = 40, 'resp sum volume'
    NOSE_FLOW = 36, 'resp nose flow'
    CANNULA_RAW = 33, 'resp cannula raw'
    THORAX_FLOW = 38, 'resp thorax flow'
    CPAP_FLOW = 29, 'resp CPAP flow'
    CANNULA_FLOW = 30, 'resp cannula flow'
    MOUTH_NOSE_FLOW = 37, 'resp mouth nose flow'


class Spo2Subtype(BrtType):
    UNSPECIFIED = 0, 'Spo2 unspecified'
    SPECIAL = 1, 'Spo2 special'
    PLETHYSMOGRAM_ENV = 51, 'Spo2 plethysmogram envelope'
    TRANS_O2 = 68, 'Spo2 trans O2'
    STATUS = 9, 'Spo2 status'
    HEART_RATE = 10, 'Spo2 heart rate'
    PLETHYSMOGRAM = 11, 'Spo2 plethysmogram'
    SAO2 = 12, 'Spo2 SaO2'
    TRANS_CO2 = 42, 'Spo2 trans CO2'


class SoundSubtype(BrtType):
    UNSPECIFIED = 0, 'sound unspecified'
    SPECIAL = 1, 'sound special'
    CANNULA_SNORE = 32, 'cannula snore'
    RAW = 22, 'sound raw'
    ENVELOPE = 23, 'sound envelope'
    CPAP_SNORE = 31, 'sound CPAP snore'


class MarkerSubtype(BrtType):
    UNSPECIFIED = 0, 'marker unspecified'
    SPECIAL = 1, 'marker special'


class PressureSubtype(BrtType):
    UNSPECIFIED = 0, 'press unspecified'
    SPECIAL = 1, 'press special'
    CPAP = 26, 'press CPAP'
    OESOPHAGUS = 27, 'press Oesophagus'
    CPAP_RAW = 28, 'press CPAP raw'


class BodypositionSubtype(BrtType):
    UNSPECIFIED = 0, 'bodyposition unspecified'
    SPECIAL = 1, 'bodyposition special'


class TemperatureSubtype(BrtType):
    UNSPECIFIED = 0, 'temp unspecified'
    SPECIAL = 1, 'temp special'


class LightSubtype(BrtType):
    UNSPECIFIED = 0, 'light unspecified'
    SPECIAL = 1, 'light special'


class ConcentrationSubtype(BrtType):
    UNSPECIFIED = 0, 'concentration unspecified'
    SPECIAL = 1, 'concentration special'


class DeviceParameters2Subtype(BrtType):
    UNSPECIFIED = 0, 'device param unspecified'
    SPECIAL = 1, 'device param special'
    SIGNAL_BUFFER = 52, 'device param signal buffer'
    CPU = 53, 'device param CPU'
    MEMORY = 54, 'device param memory'
    APP_CPU = 55, 'device param app CPU'
    APP_MEMORY = 56, 'device param app memory'
    APP_VIRTUAL_MEMORY = 57, 'device param app virtual memory'
    NETWORK = 58, 'device param network'
    DEV_CONTROL = 61, 'device param dev control'
    REC_CONTROL = 62, 'device param rec control'
    REC_CRC = 63, 'device param rec crc'


class BloodPressureSubtype(BrtType):
    UNSPECIFIED = 0, 'blood press unspecified'
    SPECIAL = 1, 'blood press special'
    DIASTOLIC = 66, 'blood press diastolic'
    MEAN = 67, 'blood press mean'
    SYSTOLIC = 65, 'blood press systolic'
    RAW = 59, 'blood pressure raw'


class DeviceParametersSubtype(BrtType):
    UNSPECIFIED = 0, 'device param unspecified'
    SPECIAL = 1, 'device param special'
    BATTERY = 60, 'device param battery'


class PulseSubtype(BrtType):
    UNSPECIFIED = 0, 'pulse unspecified'
    SPECIAL = 1, 'pulse special'


class RefSubtype(BrtType):
    UNSPECIFIED = 0, 'ref unspecified'
    SPECIAL = 1, 'ref special'


class BrtChannelType(BrtType):
    UNSPECIFIED = 0, 'unspecified', UnspecifiedSubtype
    EEG = 1, 'EEG', EegSubtype
    EMG = 2, 'EMG', EmgSubtype
    ECG = 3, 'ECG', EcgSubtype
    EOG = 4, 'EOG', EogSubtype
    RESPIRATORY = 5, 'respiratory', RespiratorySubtype
    SPO2 = 6, 'SpO2', Spo2Subtype
    SOUND = 7, 'sound', SoundSubtype
    MARKER = 8, 'marker', MarkerSubtype
    PRESSURE = 9, 'pressure', PressureSubtype
    BODYPOSITION = 10, 'bodyposition', BodypositionSubtype
    TEMPERATURE = 11, 'temperature', TemperatureSubtype
    LIGHT = 12, 'light', LightSubtype
    CONCENTRATION = 13, 'concentration', ConcentrationSubtype
    DEVICE_PARAMETERS_2 = 14, 'device parameters 2', DeviceParameters2Subtype
    BLOOD_PRESSURE = 15, 'blood pressure', BloodPressureSubtype
    DEVICE_PARAMETERS = 16, 'device parameters', DeviceParametersSubtype
    PULSE = 17, 'pulse', PulseSubtype
    REF = 65535, 'ref', RefSubtype
