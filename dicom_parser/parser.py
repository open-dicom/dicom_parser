"""
Definition of the :class:`~dicom_parser.parser.Parser` class, used to parse
the raw :class:`~pydicom.dataelem.DataElement` values into "pythonic" types.

"""

import array
import warnings

from datetime import datetime
from dicom_parser.utils.code_strings import (
    Modality,
    Sex,
    PatientPosition,
    ScanningSequence,
    SequenceVariant,
)
from dicom_parser.utils.parse_tag import parse_tag
from dicom_parser.utils.siemens.csa.header import CsaHeader
from dicom_parser.utils.value_representation import ValueRepresentation
from enum import Enum
from pydicom.dataelem import DataElement
from pydicom.sequence import Sequence
from pydicom.valuerep import PersonName


class Parser:
    """
    A default parser to be used by the :class:`~dicom_parser.header.Header` class.
    This class can easily be replaced with custom parser classes, as long as they
    expose the expected :meth:`~dicom_parser.parser.Parser.parse` method.

    """

    # Code String (CS) data elements are best represented by an Enum, so this
    # dictionary keeps a reference to the appropriate Enums by tag.
    CODE_STRINGS_DICT = {
        ("0008", "0060"): Modality,
        ("0018", "5100"): PatientPosition,
        ("0018", "0020"): ScanningSequence,
        ("0018", "0021"): SequenceVariant,
        ("0010", "0040"): Sex,
    }

    # N_IN_YEAR is used by the parse_age_string method in order to convert Age
    # String (AS) data elements into a uniform format (age in years).
    N_IN_YEAR = {"Y": 1, "M": 12, "W": 52.1429, "D": 365.2422}

    # This dictionary keeps a reference from the various DICOM header information
    # value-representations (VRs) to the appropriate parsing method.
    PARSING_METHOD = {
        ValueRepresentation.AS: "parse_age_string",
        ValueRepresentation.CS: "parse_code_string",
        ValueRepresentation.DA: "parse_date",
        ValueRepresentation.DS: "parse_decimal_string",
        ValueRepresentation.DT: "parse_datetime",
        ValueRepresentation.IS: "parse_integer_string",
        ValueRepresentation.OW: "parse_other_word",
        ValueRepresentation.PN: "parse_person_name",
        ValueRepresentation.SQ: "parse_sequence_of_items",
        ValueRepresentation.TM: "parse_time",
        ValueRepresentation.UN: "parse_unknown",
    }

    def __init__(self, verbose_code_strings: bool = True):
        """
        Initializes the :class:`~dicom_parser.parser.Parser` class.

        Parameters
        ----------
        verbose_code_strings : bool, optional
            Whether to return verbose Code String (CS) value or not, by default True
        """

        self.verbose_code_strings = verbose_code_strings

    def parse_age_string(self, value: str, **kwargs) -> float:
        """
        Parses Age String (AS) data element values into a float representation of the
        age in years.

        Parameters
        ----------
        value : str
            DICOM Age String (AS) data element value

        Returns
        -------
        float
            Age in years
        """

        duration, units = float(value[:-1]), value[-1]
        return duration / self.N_IN_YEAR[units]

    def parse_decimal_string(self, value: str, **kwargs):
        """
        Parses Decimal String (DS) data elements to floats. In case the
        `Value Multiplicity`_ (VM) is greater than one, returns a list of floats.

        .. _Value Multiplicity: http://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.4.html

        Parameters
        ----------
        value : str
            DICOM Decimal String (DS) data element value

        Returns
        -------
        float
            Decimal string value
        """

        return float(value)

    def parse_integer_string(self, value: str, **kwargs) -> int:
        """
        Parses DICOM Integer String (IS) data element value to integer.

        Parameters
        ----------
        element : str
            DICOM Integer String (IS) data element value

        Returns
        -------
        int
            Integer string value
        """

        return int(value)

    def parse_date(self, value: str, **kwargs) -> datetime.date:
        """
        Parses a Date (DA) data element value to date object.

        Parameters
        ----------
        element : str
            DICOM Date (DA) data element value

        Returns
        -------
        datetime.date
            Native python date object
        """

        try:
            return datetime.strptime(value, "%Y%m%d").date()
        except ValueError:
            # If the value is not empty, raise an error indicating the data is not valid
            if value:
                raise ValueError(f"Failed to parse '{value}' into a valid date object")
            # If empty string, returns None
        except TypeError:
            # If the value is None, simply return None, else raise TypeError
            if value:
                raise

    def parse_time(self, value: str, **kwargs) -> datetime.time:
        """
        Parses Time (TM) data elements to time objects.

        Parameters
        ----------
        element : str
            DICOM Time (TM) data element value

        Returns
        -------
        datetime.time
            Native python time object
        """

        try:
            # Try to parse according to the default time representation
            return datetime.strptime(value, "%H%M%S.%f").time()
        except ValueError:
            # If the value is not empty, try to parse with the fractional part
            if value:
                try:
                    return datetime.strptime(value, "%H%M%S").time()
                except ValueError:
                    raise ValueError(
                        f"Failed to parse '{value}' into a valid time object!"
                    )
            # If the value is empty string, simply return None
        except TypeError:
            # If the value is empty, simply return None, else raise TypeError
            if value:
                raise

    # TODO: Find a DICOM with a DT element so this method can be tested and uncommented.
    # def parse_datetime(self, element: DataElement) -> datetime:
    #     """
    #     Parses Date Time (DT) data elements to datetime objects.

    #     Parameters
    #     ----------
    #     element : DataElement
    #         DICOM Date Time (DT) data element.

    #     Returns
    #     -------
    #     datetime.time
    #         Native python datetime object.
    #     """

    #     return datetime.strptime(element.value, "%Y%m%d%H%M%S.%f")

    def get_code_string_representation(self, value: str, enum: Enum) -> str:
        """
        Returns a Code String (CS) data element value's according to the
        class's *verbose_code_strings* attribute value. If True, returns the
        corresponding Enum's value. Otherwise, simply returns the name itself (raw value).

        Parameters
        ----------
        value : str
            Code String (CS) value
        enum : enum.Enum
            Code String (CS) valid values

        Returns
        -------
        str
            Parsed value in coded or verbose form
        """

        return enum[value].value if self.verbose_code_strings else value

    def warn_invalid_code_string_value(self, exception: KeyError, enum: Enum) -> None:
        """
        Displays a warning for invalid Code String (CS) values.

        Parameters
        ----------
        exception : KeyError
            The exception raised when trying to parse the invalid value
        enum : enum.Enum
            An Enum representing the element's valid values
        """

        field_name = enum.__name__
        warnings.warn(f"'{exception.args[0]}' is not a valid {field_name} value!")

    def parse_code_string_with_enum(self, value: str, enum: Enum):
        """
        Parses a Code String (CS) data element using

        Parameters
        ----------
        element : str
            Code String (CS) data element value
        enum : enum.Enum
            An Enum representing the element's valid values

        Returns
        -------
        str or set
            Parsed value/s.
        """

        try:
            return self.get_code_string_representation(value, enum)
        except KeyError as exception:
            self.warn_invalid_code_string_value(exception, enum)
            return str(value)

    def parse_code_string(self, value: str, tag: tuple, **kwargs):
        """
        Parses Code String (CS) data elements to a more readable string or set
        of strings. This method relies on an Enum representation of the data element's
        possible values to be registered in the Parser's CODE_STRINGS_DICT by tag.
        If no Enum is registered, will return try to parse out a value or a set of values.

        Parameters
        ----------
        element : :class:`~pydicom.dataelem.DataElement`
            DICOM Code String (CS) data element.

        Returns
        -------
        str or set
            Parsed value/s.
        """

        enum = self.CODE_STRINGS_DICT.get(tag)
        return self.parse_code_string_with_enum(value, enum) if enum else value

    def parse_other_word(self, value: bytes, **kwargs) -> list:
        return [v for v in value]

    def parse_sequence_of_items(self, value: Sequence):
        return [self.parse(subelement) for dataset in value for subelement in dataset]

    def parse_person_name(self, value: PersonName, **kwargs):
        if isinstance(value, PersonName):
            components = (
                "name_prefix",
                "given_name",
                "middle_name",
                "family_name",
                "name_suffix",
            )
            return {component: getattr(value, component) for component in components}
        return value

    # Custom parsing methods (tag dependent rather than value-representation dependant)
    def parse_siemens_slice_timing(self, value: bytes, **kwargs) -> list:
        """
        Parses a SIEMENS MR image's slice timing as saved in the private
        (0019, 1029) `MosaicRefAcqTimes`_ tag to a list of floats representing
        slice times in milliseconds.

        .. _MosaicRefAcqTimes: https://en.wikibooks.org/wiki/SPM/Slice_Timing#Siemens_scanners

        Parameters
        ----------
        value : bytes
            SIEMENS private MosaicRefAcqTimes data element

        Returns
        -------
        list
            Slice times in milliseconds
        """

        return [round(slice_time, 5) for slice_time in list(array.array("d", value))]

    def parse_siemens_gradient_direction(self, value: bytes, **kwargs) -> list:
        """
        Parses a SIEMENS MR image's B-vector as represented in the private
        (0019, 100E) `DiffusionGradientDirection`_ DICOM tag.

        .. _DiffusionGradientDirection: https://na-mic.org/wiki/NAMIC_Wiki:DTI:DICOM_for_DWI_and_DTI#Private_vendor:_Siemens

        Parameters
        ----------
        value : bytes
            SIEMENS private DiffusionGradientDirection data element.

        Returns
        -------
        list
            Gradient directions (B-vector)
        """

        return [float(value) for value in list(array.array("d", value))]

    def parse_unknown(self, value, tag: tuple, **kwargs):
        """
        Parses private tags and other Unknown (UN) data elememts.

        Parameters
        ----------
        value : type
            DICOM Unknown (UN) data element

        """

        #
        # Siemens private tags
        #
        # DTI
        # https://na-mic.org/wiki/NAMIC_Wiki:DTI:DICOM_for_DWI_and_DTI
        # Number of Images in Mosaic
        if tag == ("0019", "100a"):
            return int.from_bytes(value, byteorder="little")
        # Slice Measurement Duration
        elif tag == ("0019", "100b"):
            return float(value)
        # B Value
        elif tag == ("0019", "100c"):
            return int(value)
        # Diffusion Directionality / Gradient Mode
        elif tag in (("0019", "100d"), ("0019", "100f")):
            if value:
                return value.decode("utf-8").strip()
        # Diffusion Gradient Direction
        elif tag == ("0019", "100e"):
            return self.parse_siemens_gradient_direction(value)
        # B Matrix
        elif tag == ("0019", "1027"):
            return list(array.array("d", value))
        # Bandwidth per Pixel Phase Encode
        elif tag == ("0019", "1028"):
            return array.array("d", value)[0]
        # Slice Timing
        # https://en.wikibooks.org/wiki/SPM/Slice_Timing#Siemens_scanners
        elif tag == ("0019", "1029"):
            return self.parse_siemens_slice_timing(value)
        #
        # CSA Headers
        # https://nipy.org/nibabel/dicom/siemens_csa.html
        elif tag in (("0029", "1010"), ("0029", "1020")):
            return CsaHeader(value).parsed

        #
        # GE Private Tags
        #
        # Dates encoded as seconds since epoch
        elif tag in (("0009", "1027"), ("0009", "10e9")):
            seconds_since_epoch = int.from_bytes(value, byteorder="little")
            return datetime.fromtimestamp(seconds_since_epoch)
        # Other Binary (OB) encoded data
        elif tag == ("0043", "1029"):
            return [v for v in value]

        #
        # Other
        #
        # Try to decode bytes
        elif isinstance(value, bytes):
            try:
                return value.decode().replace("\x00", "").strip()
            except UnicodeDecodeError:
                pass

        # If no parsing method exists for this DICOM attribute, simply return
        # the raw value.
        return value

    def get_value_representation(self, element: DataElement) -> ValueRepresentation:
        """
        Gets the given :class:`~pydicom.dataelem.DataElement`'s
        :class:`~dicom_parser.utils.value_representation.ValueRepresentation`.

        Parameters
        ----------
        element : :class:`~pydicom.dataelem.DataElement`
            DICOM data element

        Returns
        -------
        :class:`~dicom_parser.utils.value_representation.ValueRepresentation`
            Corresponding data representation enum

        Raises
        ------
        NotImplementedError
            Unknown value represenation
        """

        try:
            return ValueRepresentation[element.VR]
        except KeyError:
            raise NotImplementedError(
                f"{element.VR} is not a supported value-representation!"
            )

    def handle_unregistered_vr(self, value, **kwargs):
        return value

    def call_parsing_method(
        self, element: DataElement, value_representation: ValueRepresentation
    ):
        """
        Calls the appropriate parsing method for the
        :class:`~pydicom.dataelem.DataElement` based on the provided
        :class:`~dicom_parser.utils.value_representation.ValueRepresentation`.

        Parameters
        ----------
        element : :class:`~pydicom.dataelem.DataElement`
            DICOM data element
        value_representation : :class:`~dicom_parser.utils.value_representation.ValueRepresentation`
            Data element's value representation

        Returns
        -------
        [type]
            Parsed value
        """

        value_multiplicity = getattr(element, "VM", 1)
        tag = parse_tag(element.tag)
        method_name = self.PARSING_METHOD.get(
            value_representation, "handle_unregistered_vr"
        )
        method = getattr(self, method_name)
        if value_multiplicity > 1:
            return [method(value, tag=tag) for value in element.value]
        return method(element.value, tag=tag)

    def parse(
        self,
        element: DataElement,
        index: int = None,
        ignore_warnings: bool = False,
        return_warnings: bool = False,
    ):
        """
        Tries to parse a pydicom_ DICOM data element using its value-representation
        (VR) attribute. If no parser method is registered for the VR under the
        PARSING_METHOD dictionary, will simply return the raw value.

        .. _pydicom: https://github.com/pydicom/pydicom

        Parameters
        ----------
        element : DataElement
            DICOM data element as represented by pydicom.

        Returns
        -------
        type
            Parsed DICOM data element value.
        """

        value_representation = self.get_value_representation(element)
        with warnings.catch_warnings():
            warnings.filterwarnings("error")
            try:
                value = self.call_parsing_method(element, value_representation)
            except Warning as w:
                warnings.filterwarnings("ignore")
                value = self.call_parsing_method(element, value_representation)
                value = value if index is None else value[index]
                if ignore_warnings:
                    return value
                elif return_warnings:
                    return value, str(w)
            else:
                value = value if index is None else value[index]
                if return_warnings:
                    return value, None
                return value
