# -*- coding: utf-8 -*-
from dataclasses import dataclass

from codeBRT.parsing.brt.components.base import Component
from codeBRT.parsing.brt.enums.brt_type import BrtType
from codeBRT.parsing.brt.enums.channel_type import BrtChannelType
from codeBRT.parsing.interface.generic_type import ChannelType, GenericType


@dataclass(frozen=True)
class ScalingParams(Component):
    """
    Scaling parameters of a measured channel.
    These parameters describe a difference in scale between two measuring steps.

    Formula:
        representation * unit_factor_numer / unit_factor_denom = true value
        (If numerator and denominator aren't both zero.)

    Attributes:
        range_min: minimal measurable physical value, corresponding to -32768
        range_max: maximal measurable physical value, corresponding to 32768
        unit: name of the physical unit in which the values are expressed
        unit_factor_numer: numerator of the unit conversion factor
        unit_factor_denom: denominator of the unit conversion factor

        type_string: "integer, integer, 18 characters, integer, integer"
    """
    range_min: int
    range_max: int
    _unit: str
    unit_factor_numer: int
    unit_factor_denom: int

    @property
    def unit(self) -> str:
        """true wide character representation of the unit"""
        return self.parse_wchar(self._unit)

    type_string = '=ii18sii'


@dataclass(frozen=True)
class AmplifierMapping(Component):
    """
    Characteristics of the hardware channel used as the active channel.

    Attributes:
        electrode: the channel code of the active channel
        reference: the channel code of the reference for the channel

        type_string: "unsigned integer, unsigned integer"
    """
    electrode: int
    reference: int

    type_string = '=II'


@dataclass(frozen=True)
class Position(Component):
    """
    The position of a physical position of a channel at a patient.

    Attributes:
        coordinate_system: an index describing the coordinate system by which
            the three coordinates can be interpreted
        coordinate_1: first coordinate of the position
        coordinate_2: second coordinate of the position
        coordinate_3: third coordinate of the position

        type_string: "short, long, long, long"
    """
    coordinate_system: int
    coordinate_1: int
    coordinate_2: int
    coordinate_3: int

    type_string = '=hlll'


@dataclass(frozen=True)
class PatientMapping(Component):
    """
    Description of the channel and how it relates to the patient.

    Attributes:
        type_string: "unsigned short, unsigned short, 14 bytes"

    Properties:
        channel_type: BrainRT type of the channel
        channel_subtype: BrainRT subtype of the channel
        position: physical position of the channel
    """
    channel_type_id: int
    channel_subtype_id: int
    _position: bytes

    @property
    def channel_type(self) -> BrtChannelType:
        return BrtChannelType(self.channel_type_id)

    @property
    def channel_subtype(self) -> BrtType:
        return self.channel_type.subtype(self.channel_subtype_id)

    @property
    def position(self) -> Position:
        """Position representation of the physical position of the channel"""
        return Position.parse(self._position)

    type_string = '=HH14s'


@dataclass(frozen=True)
class ViewSettings(Component):
    """
    Display settings for a specific channel, how it should be drawn.

    Properties:
        scaling_params: the scale at which to draw, expressed in cm

    Attributes:
        pen_color: the color of the data curve
        pen_width: the width of the data curve, in pixels

        type_string: "unsigned long, unsigned character, 34 bytes"
    """
    pen_color: int
    pen_width: int
    _scaling_params: bytes

    @property
    def scaling_params(self) -> ScalingParams:
        """ScalingParams representation of the display scale of a channel"""
        return ScalingParams.parse(self._scaling_params)

    type_string = '=LB34s'


@dataclass(frozen=True)
class BrtChannel(Component):
    """
    Complete description of a BrainRT channel.
    The definition of this file is translated from "BaseDefsSub2.h".

    Attributes:
        name: name of the channel
        amplifier_code: index of the amplifier from a list of all amplifiers
            responsible for registering this channel
        adc_type: type of additional data in the channel
        selectable: boolean indicating whether the channel is composed of
            selectable hardware channels
        sampling_rate: sampling frequency of the channel
        number_of_bits: the number of bits used per channel, always 16

        hb_scale: scale difference between the Headbox and the physical reality
            hb_scale.range_min is the real value of headbox value -32768
            hb_scale.range_max is the real value of headbox value 32768
        rd_scale: scale difference between the real data and the stored data,
            rd_scale.range_min is the real value represented by the value -32768
            rd_scale.range_max is the real value represented by the value 32768

        mf_DA: multiplication factor of the transition between the headbox scale
            and the raw data scale
        af_DA: addition term of the transition between the headbox scale
            and the raw data scale
        scale_DA: scale factor of the transition between the amplifiers and the
            driver
        mf_PV: multiplication factor to calculate real data from raw data
        af_PV: addition term to calculate real data from raw data

        has_high_pass_filter: determines whether the raw data from this channel
            was high pass filtered
        high_pass_frequency: frequency of said high pass filter, if any
        has_low_pass_filter: determines whether the raw data from this channel
            was low pass filtered
        low_pass_frequency: frequency of said low pass filter, if any
        has_notch: determines whether a notch filter was applied to the raw data

        amplifier_map: defines how a registered channel is mapped on hardware
        patient_map: maps the position of this channel on the patient
            More importantly, it stores the channel type and subtype!
        view_settings: definition of the draw method for this channel

        type_string: characters that define the way these attributes are stored.
    """
    _name: bytes
    amplifier_code: int
    adc_type: int
    selectable: int
    sampling_rate: int
    number_of_bits: int

    _hb_scale: bytes
    _rd_scale: bytes

    mf_DA: int
    af_DA: int
    scale_DA: int
    mf_PV: float
    af_PV: float

    has_high_pass_filter: bool
    high_pass_frequency: float
    has_low_pass_filter: bool
    low_pass_frequency: float
    has_notch: bool

    _amplifier_map: bytes
    _patient_map: bytes
    _view_settings: bytes

    @property
    def name(self) -> str:
        return self.parse_wchar(self._name)

    @property
    def hb_scale(self) -> ScalingParams:
        """Headbox scale"""
        return ScalingParams.parse(self._hb_scale)

    @property
    def rd_scale(self) -> ScalingParams:
        """Real data scale"""
        return ScalingParams.parse(self._rd_scale)

    @property
    def amplifier_map(self) -> AmplifierMapping:
        """Mapping of the Hardware channels."""
        return AmplifierMapping.parse(self._amplifier_map)

    @property
    def patient_map(self) -> PatientMapping:
        """Locator of the channel and description of the type of channel."""
        return PatientMapping.parse(self._patient_map)

    @property
    def view_settings(self) -> ViewSettings:
        """Display settings for this channel."""
        return ViewSettings.parse(self._view_settings)

    @property
    def generic_type(self) -> GenericType:
        """Generic type of this specific channel."""
        _map = self.patient_map
        _type = ChannelType(_map.channel_type_id)
        _subtype = _type.subtype(_map.channel_subtype_id) \
            if _type.subtype is not None else ChannelType.UNDEFINED
        return _subtype if _subtype is not ChannelType.UNDEFINED else _type

    type_string = '=66sHi?iB34s34siiidd?i?i?8s18s39s'
