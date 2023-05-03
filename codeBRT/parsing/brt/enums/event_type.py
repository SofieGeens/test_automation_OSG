# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 16:59:51 2019

@author: JanA
"""

from codeBRT.parsing.brt.enums.brt_type import BrtType


class UndefinedSubtype(BrtType):
    UNDEFINED = 0, 'undefined'


class SystemSubtype(BrtType):
    UNDEFINED = 0, 'undefined'
    STORE = 1, 'store'
    REDUCTION = 2, 'reduction'
    KEEP_SIGNAL = 3, 'keep Signal'
    KEEP_VIDEO = 4, 'keep Video'
    BUTTON = 5, 'button'
    ORIGINAL_SIGNAL_SPAN = 6, 'original signal span'
    EVENT_CHANNEL_HASH_TABLE = 7, 'event channel hash table'
    NOTE_HASH_TABLE = 8, 'note hash table'
    KEEP_SIGNAL_AND_VIDEO = 9, 'keep signal and video'
    MATERIALIZED_CHANNEL_TABLE = 10, 'materialized channel table'
    ALARM_SUPPRESSION = 11, 'alarm suppression'
    SESSION_ID = 12, 'session ID'
    CONTEXT_ID = 13, 'context ID'
    EXPORT_RESULTS = 14, 'export results'


class MeasureSubtype(BrtType):
    UNDEFINED = 0, 'undefined'
    HEADBOX_1_DISCONNECTED = 19, 'headbox 1 disconnected'
    SAO2_MALFUNCTION = 1, 'SaO2 Malfunction'
    SAO2_OUT_OF_TRACK = 2, 'SaO2 out of track'
    SAO2_BAD_PULSE = 3, 'SaO2 bad pulse'
    SAO2_DISCONNECTED = 4, 'SaO2 disconnected'
    PHOTO_STIMULATOR = 21, 'photo stimulator'
    HEADBOX_1_BLOCKED = 17, 'headbox 1 blocked'
    HEADBOX_2_DISCONNECTED = 20, 'headbox 2 disconnected'
    TEMPERATURE_DISCONNECTED = 32, 'temperature disconnected'
    HEADBOX_2_BLOCKED = 18, 'headbox 2 blocked'


class AnalysisSubtype(BrtType):
    UNDEFINED = 0, 'undefined'
    PHASE_COHERENCE = 16, 'phase coherence'
    SLEEP = 1, 'sleep analysis'
    MSLT = 2, 'MSLT analysis'
    EPOCH = 32, 'analysis epoch'
    STATUS = 48, 'analysis status'
    EXTRA_DATA = 64, 'analysis extra data'


class ReportSubtype(BrtType):
    UNDEFINED = 0, 'undefined'
    EPOCH = 1, 'Report Epoch'


class RecorderSubtype(BrtType):
    UNDEFINED = 0, 'undefined'
    VIDEO = 1, 'video'
    PHOTIC_STIMULUS_PERIOD = 2, 'photic stimulus period'
    PHOTIC_STIMULUS_TRIGGER = 3, 'photic stimulus trigger'
    EXTERNAL_STIMULUS_PERIOD = 4, 'external stimulus period'
    EXTERNAL_STIMULUS_TRIGGER = 5, 'external stimulus trigger'
    TRIGGER_OUTPUT_1 = 6, 'trigger output 1'
    TRIGGER_INPUT_1 = 7, 'trigger input 1'
    TRIGGER_INPUT_2 = 8, 'trigger input 2'
    ELECTRODES_CONNECTED_TO_STIM_PERIOD = 9, 'electrodes connected to stim. period'
    ELECTRODES_CONNECTED_TO_STIM_TRIGGER = 10, 'electrodes connected to stim. trigger'
    SYNCHRONISATION_CHECK = 11, 'synchronisation check'


class NoteSubtype(BrtType):
    UNDEFINED = 0, 'undefined'
    NOTE = 1, 'note'


class NotificationSubtype(BrtType):
    UNDEFINED = 0, 'undefined'
    TCCO2_ALARM = 32, 'TcCO2 alarm'
    SYSTEM_ERROR = 1, 'system error'
    SYSTEM_WARNING = 2, 'system warning'
    DRIVER_ERROR = 48, 'driver error'
    TCO2_ALARM = 33, 'TcO2 alarm'
    ANALYSIS = 16, 'analysis notification'
    DRIVER_LOG = 49, 'driver log'
    EXTERNAL_EVENT = 50, 'external event notification'
    LOG_EVENT = 51, 'log event'
    SAO2_ALARM = 20, 'SaO2 alarm'
    HEART_RATE_ALARM = 21, 'heart rate alarm'
    OBSOLETE_HEART_RATE_ALARM = 22, 'obsolete heart rate alarm'
    SEIZURE_ALARM = 23, 'seizure alarm'
    NURSE_CALL_ALARM = 24, 'nurse call alarm'
    RESPIRATION_CALIBRATION_ALARM = 25, 'respiration calibration alarm'
    APNEA_ALARM = 26, 'apnea alarm'
    RECORDER_ALARM = 27, 'recorder alarm'
    TEMPERATURE_ALARM = 28, 'temperature alarm'
    CO2_ALARM = 29, 'CO2 alarm'
    BLOOD_PRESSURE_SYSTOLIC_ALARM = 30, 'blood pressure systolic alarm'
    BLOOD_PRESSURE_MEAN_ALARM = 31, 'blood pressure mean alarm'


class ImpedanceCheckSubtype(BrtType):
    UNDEFINED = 0, 'undefined'
    IMPEDANCE_CHECK = 1, 'impedance check'
    REQUEST = 65534, 'impedance check request'
    TRIGGER = 65535, 'impedance check trigger'


class VideoSubtype(BrtType):
    UNDEFINED = 0, 'undefined'
    VIDEO = 1, 'video'
    LINK = 2, 'video link'
    SYNC_SOURCE = 3, 'video sync source'
    SYNC_DESTINATION = 4, 'video sync destination'


class ChannelStateSubtype(BrtType):
    UNDEFINED = 0, 'undefined'
    DATA_INVALID = 1, 'data invalid'
    DATA_UNRELIABLE = 2, 'data unreliable'
    TEST_DATA = 3, 'test data'
    INFO = 4, 'channel info'


class HypnogramSubtype(BrtType):
    UNDEFINED = 0, 'undefined'
    N4 = 304, 'N4'
    WAKE = 2, 'Wake'
    ACTIVE_SLEEP = 211, 'active sleep'
    MOVEMENT_TIME = 101, 'movement time'
    QUIET_SLEEP = 311, 'quiet sleep'
    REM = 201, 'R'
    INVALID = 65535, 'invalid'
    NREM = 300, 'NREM'
    N1 = 301, 'N1'
    N2 = 302, 'N2'
    N3 = 303, 'N3'


class RespiratorySubtype(BrtType):
    UNDEFINED = 0, 'undefined'
    NON_CLASSIFIED_APNEA = 1, 'non classified apnea'
    CENTRAL_APNEA = 2, 'central apnea'
    OBSTRUCTIVE_APNEA = 3, 'obstructive apnea'
    MIXED_APNEA = 4, 'mixed apnea'
    NON_CLASSIFIED_HYPOPNEA = 5, 'non classified hypopnea'
    CENTRAL_HYPOPNEA = 6, 'central hypopnea'
    OBSTRUCTIVE_HYPOPNEA = 7, 'obstructive hypopnea'
    MIXED_HYPOPNEA = 8, 'mixed hypopnea'
    NEUTRAL_STATE = 9, 'neutral state'
    PARADOXYCAL_APNEA = 10, 'paradoxycal apnea'
    PARADOXYCAL_HYPOPNEA = 11, 'paradoxycal hypopnea'
    PERIODICAL_BREATHING = 12, 'periodical breathing'
    FLOW_LIMITATION = 13, 'flow limitation'
    CALIBRATION = 14, 'respiration calibration'
    ALERT_APNEA = 15, 'alert apnea'
    EFFORT_RELATED_AROUSAL = 16, 'respiratory effort - related arousal'
    HYPOVENTILATION = 17, 'hypoventilation'
    CSB = 18, 'csb'
    INVALID = 65535, 'invalid'


class SaturationSubtype(BrtType):
    UNDEFINED = 0, 'undefined'
    DIP = 1, 'Saturation dip'
    HYPOXYCAL_STATE = 2, 'Saturation hypoxycal state'
    CALIBRATION = 65534, 'Saturation calibration'
    INVALID = 65535, 'invalid'


class EcgSubtype(BrtType):
    UNDEFINED = 0, 'undefined'
    TACHYCARDIA = 1, 'tachycardia'
    BRADYCARDIA = 2, 'bradycardia'
    QRS_COMPLEX = 3, 'QRS complex'
    ICTAL_TACHY_PHASE = 4, 'ictal tachy phase'
    SINUS_TACHY = 5, 'sinus tachy'
    WC_TACHY = 6, 'wc tachy'
    NC_TACHY = 7, 'nc tachy'
    ASYSTOLE = 8, 'asystole'
    ATR_FIB = 9, 'atr fib'
    BRADY_L2 = 10, 'brady L2'
    DECELERATION = 11, 'deceleration'
    DEVELERATION_L2 = 12, 'develeration L2'
    CALIBRATION = 65534, 'ECG calibration'
    INVALID = 65535, 'invalid'


class EmgSubtype(BrtType):
    UNDEFINED = 0, 'undefined'
    MOVEMENT = 1, 'movement'
    LEFT_LEG_MOVEMENT = 2, 'left leg movement'
    RIGHT_LEG_MOVEMENT = 3, 'right leg movement'
    BGD_LEVEL = 4, 'EMG BGD level'
    PERIODIC_LEG_MOVEMENT_SERIES = 5, 'periodic leg movement series'
    PERIODIC_LEG_MOVEMENT = 6, 'periodic leg movement'
    PHASIC_EMG_ACTIVITY_DURING_REM = 7, 'phasic EMG Activity during R'
    BRUXISM = 8, 'bruxism'
    RHYTHMIC_MOVEMENT_DISORDER = 9, 'rhythmic movement disorder'
    TONIC_EMG_ACTIVITY_DURING_REM = 10, 'tonic EMG Activity during R'
    CALIBRATION = 65534, 'EMG calibration'
    INVALID = 65535, 'invalid'


class EegSubtype(BrtType):
    UNDEFINED = 0, 'undefined'
    SEIZURE_CANDIDATE = 256, 'seizure candidate'
    K_COMPLEX = 1, 'K complex'
    SPINDLE = 2, 'spindle'
    ALPHA = 3, 'alpha'
    THETA = 4, 'theta'
    BETA = 5, 'beta'
    DELTA = 6, 'delta'
    BURST_SUPPRESSION = 769, 'burst-suppression'
    INVALID = 65535, 'invalid'
    BURST_SUPPRESSION_CALIBRATION = 768, 'burst-suppression calibration'
    MEAN_PHASE_COHERENCE_CALIBRATION = 512, 'mean phase coherence calibration'


class EogSubtype(BrtType):
    UNDEFINED = 0, 'undefined'
    REM = 1, 'R'
    SEM = 2, 'SEM'
    BLINK = 3, 'blink'
    INVALID = 65535, 'invalid'


class ArousalSubtype(BrtType):
    UNDEFINED = 0, 'undefined'
    AROUSAL = 1, 'arousal'
    INVALID = 65535, 'invalid'


class SoundSubtype(BrtType):
    UNDEFINED = 0, 'undefined'
    SNORING = 1, 'snoring'
    PERIODS_OF_SNORING = 2, 'periods of snoring'
    SNORING_CALIBRATION = 65534, 'snoring calibration'
    INVALID = 65535, 'invalid'


class BodypositionSubtype(BrtType):
    UNDEFINED = 0, 'undefined'
    LEFT_SIDE = 1, 'left side'
    RIGHT_SIDE = 2, 'right side'
    BACK = 3, 'back'
    BELLY = 4, 'belly'
    STANDING_UP = 5, 'standing up'
    HEAD_DOWN = 6, 'head down'
    INVALID = 65535, 'invalid'


class CpapSubtype(BrtType):
    UNDEFINED = 0, 'undefined'
    CPAP = 1, 'CPAP'
    INVALID = 65535, 'invalid'


class SleepSubtype(BrtType):
    UNDEFINED = 0, 'undefined'
    LIGHTS_OUT = 1, 'lights out'
    TIME_IN_BED = 2, 'time in bed'
    PERIOD_TIME = 3, 'sleep period time'
    TOTAL_SLEEP_TIME = 4, 'total sleep time'


class DerivationSubtype(BrtType):
    UNDEFINED = 0, 'undefined'
    CHANGE = 1, 'Derivation Change'


class PhysiologicalCalibrationSubtype(BrtType):
    UNDEFINED = 0, 'undefined'
    PATIENT_IN_REST = 1, 'patient in rest'
    SNORING = 2, 'snoring'
    LEG_MOVEMENT = 3, 'leg movement'
    EYES_CLOSED = 4, 'eyes closed'
    EYE_BLINKS = 5, 'eye blinks'
    EYES_RIGHT = 6, 'eyes right'
    EYES_LEFT = 7, 'eyes left'
    EYES_DOWN = 8, 'eyes down'
    EYES_UP = 9, 'eyes up'
    NO_BREATHING = 10, 'no breathing'


class StimulationSubtype(BrtType):
    UNDEFINED = 0, 'undefined'
    STIMULATION = 1, 'stimulation'
    TARGET = 2, 'target'
    NON_TARGET = 3, 'non target'
    WARNING = 4, 'warning'
    IMPERATIVE = 5, 'imperative'
    TONE_1 = 6, 'tone 1'
    TONE_2 = 7, 'tone 2'
    TONE_3 = 8, 'tone 3'
    TONE_4 = 9, 'tone 4'


class ResponseSubtype(BrtType):
    UNDEFINED = 0, 'undefined'
    PATIENT_BUTTON_1 = 1, 'patient button 1'
    PATIENT_BUTTON_2 = 2, 'patient button 2'
    PATIENT_BUTTON_3 = 3, 'patient button 3'
    PATIENT_BUTTON_4 = 4, 'patient button 4'


class EmgLevelSubtype(BrtType):
    UNDEFINED = 0, 'undefined'
    UNKNOWN = 1, 'unknown EMG level'
    VERY_LOW = 2, 'very low EMG level'
    LOW = 3, 'low EMG level'
    MEDIUM = 4, 'medium EMG level'
    HIGH = 5, 'high EMG level'
    INVALID = 65535, 'invalid'


class BloodPressureSubtype(BrtType):
    UNDEFINED = 0, 'undefined'
    LOW = 1, 'low blood pressure'
    MEAN = 2, 'mean blood pressure'
    HIGH = 3, 'high blood pressure'
    INVALID = 65535, 'invalid'


class Co2Subtype(BrtType):
    UNDEFINED = 0, 'undefined'
    HIGH = 1, 'High CO2'
    INVALID = 65535, 'invalid'


class ObservationSubtype(BrtType):
    UNDEFINED = 0, 'undefined'
    MOVEMENT = 1, 'movement'
    ARTEFACT = 2, 'artefact'
    EYES_OPEN = 3, 'eyes open'
    EYES_CLOSED = 4, 'eyes closed'
    HYPERVENTILATION = 5, 'hyperventilation'
    SEIZURE = 6, 'seizure'
    FIST_RIGHT = 7, 'fist right'
    FIST_LEFT = 8, 'fist left'
    SLEEP = 9, 'sleep'
    ACOUSTIC_STIMULUS = 10, 'acoustic stimulus'
    PAIN_STIMULUS = 11, 'pain stimulus'
    SPEAKING = 12, 'speaking'
    ATTENTION = 13, 'attention'


class CalibrationEpochSubtype(BrtType):
    UNDEFINED = 0, 'undefined'
    LINEAR_CALIBRATION = 1, 'linear calibration'
    DC_CALIBRATION = 2, 'DC calibration'


class CalibrationDataSubtype(BrtType):
    UNDEFINED = 0, 'undefined'
    SAMPLE = 16, 'calibration sample'
    SAMPLE_DATA = 1, 'calibration sample-data'


class ImportedSubtype(BrtType):
    UNDEFINED = 0, 'undefined'
    GROUP_1 = 1, 'group 1'
    GROUP_2 = 2, 'group 2'
    GROUP_3 = 3, 'group 3'
    GROUP_4 = 4, 'group 4'
    GROUP_5 = 5, 'group 5'
    GROUP_6 = 6, 'group 6'
    GROUP_7 = 7, 'group 7'
    GROUP_8 = 8, 'group 8'


class BrtEventType(BrtType):
    UNDEFINED = 0, 'undefined', UndefinedSubtype
    SYSTEM = 1, 'system', SystemSubtype
    MEASURE = 16, 'measure', MeasureSubtype
    ANALYSIS = 32, 'analysis', AnalysisSubtype
    REPORT = 33, 'report', ReportSubtype
    RECORDER = 48, 'recorder', RecorderSubtype
    NOTE = 64, 'note', NoteSubtype
    NOTIFICATION = 65, 'notification', NotificationSubtype
    IMPEDANCE_CHECK = 66, 'impedance Check', ImpedanceCheckSubtype
    VIDEO = 67, 'video', VideoSubtype
    CHANNEL_STATE = 68, 'channel state', ChannelStateSubtype
    HYPNOGRAM = 128, 'hypnogram', HypnogramSubtype
    RESPIRATORY = 129, 'respiratory', RespiratorySubtype
    SATURATION = 130, 'saturation', SaturationSubtype
    ECG = 131, 'ECG', EcgSubtype
    EMG = 132, 'EMG', EmgSubtype
    EEG = 133, 'EEG', EegSubtype
    EOG = 134, 'EOG', EogSubtype
    AROUSAL = 135, 'arousal', ArousalSubtype
    SOUND = 136, 'sound', SoundSubtype
    BODYPOSITION = 137, 'bodyposition', BodypositionSubtype
    CPAP = 138, 'CPAP', CpapSubtype
    SLEEP = 139, 'sleep', SleepSubtype
    DERIVATION = 140, 'derivation', DerivationSubtype
    PHYSIOLOGICAL_CALIBRATION = 141, 'physiological calibration', PhysiologicalCalibrationSubtype
    STIMULATION = 142, 'stimulation', StimulationSubtype
    RESPONSE = 143, 'response', ResponseSubtype
    EMG_LEVEL = 144, 'EMG Level', EmgLevelSubtype
    BLOOD_PRESSURE = 145, 'blood pressure', BloodPressureSubtype
    CO2 = 1024, 'CO2', Co2Subtype
    OBSERVATION = 1025, 'observation', ObservationSubtype
    CALIBRATION_EPOCH = 1280, 'calibration epoch', CalibrationEpochSubtype
    CALIBRATION_DATA = 1281, 'calibration data', CalibrationDataSubtype
    IMPORTED = 1282, 'imported', ImportedSubtype
