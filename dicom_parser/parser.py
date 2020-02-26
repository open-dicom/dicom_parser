import array

from datetime import datetime
from dicom_parser.utils.code_strings import (
    Modality,
    Sex,
    PatientPosition,
    ScanningSequence,
    SequenceVariant,
)
from dicom_parser.utils.siemens.csa.header import CsaHeader
from dicom_parser.utils.value_representation import ValueRepresentation
from pydicom.dataelem import DataElement


class Parser:
    # N_IN_YEAR is used by the parse_age_string method in order to convert Age
    # String (AS) data elements into a uniform format (age in years).
    N_IN_YEAR = {"Y": 1, "M": 12, "W": 52.1429, "D": 365.2422}

    # Code String (CS) data elements are best represented by an Enum, so this
    # dictionary keeps a reference to the appropriate Enums by tag.
    CODE_STRINGS_DICT = {
        "(0008, 0060)": Modality,
        "(0018, 5100)": PatientPosition,
        "(0018, 0020)": ScanningSequence,
        "(0018, 0021)": SequenceVariant,
        "(0010, 0040)": Sex,
    }
    SINGLE_VALUE_CODE_STRINGS = ["(0010, 0040)", "(0018, 5100)", "(0008, 0060)"]

    # This dictionary keeps a reference from the various DICOM header information
    # value-representations (VRs) to the appropriate parsing method.
    PARSING_METHOD = {
        ValueRepresentation.AGE_STRING: "parse_age_string",
        ValueRepresentation.DATE: "parse_date",
        ValueRepresentation.TIME: "parse_time",
        ValueRepresentation.DATE_TIME: "parse_datetime",
        ValueRepresentation.INTEGER_STRING: "parse_integer_string",
        ValueRepresentation.DECIMAL_STRING: "parse_decimal_string",
        ValueRepresentation.UNKNOWN: "parse_unknown",
        ValueRepresentation.CODE_STRING: "parse_code_string",
        # ValueRepresentation.SEQUENCE_OF_ITEMS: list,
        # Sequence of Items (SQ) attributes need to be listed, but then
        # they return a list of data elements, which are also divided into
        # groups. Not sure yet what would be the best way to parse it, but it
        # might be a list of dictionaries.
    }

    def parse_age_string(self, element: DataElement) -> float:
        """
        Parses Age String (AS) data elements into a float representation of the
        age in years.

        Parameters
        ----------
        element : DataElement
            DICOM Age String (AS) data element.

        Returns
        -------
        float
            The age in years.
        """

        value = element.value
        duration, units = float(value[:-1]), value[-1]
        return duration / self.N_IN_YEAR[units]

    def parse_decimal_string(self, element: DataElement):
        """
        Parses Decimal String (DS) data elements to floats. In case the
        `Value Multiplicity`_ (VM) is greater than one, returns a list of floats.

        .. _Value Multiplicity: http://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.4.html

        Parameters
        ----------
        element : DataElement
            DICOM Decimal String (DS) data element.

        Returns
        -------
        float or list
            Data element value/s.
        """

        try:
            return float(element.value)

        # If VM > 1, element.value will return a list.
        except TypeError:
            return [float(value) for value in element.value]

    def parse_integer_string(self, element: DataElement) -> int:
        """
        Parses DICOM Integer String (IS) data elements to integers.

        Parameters
        ----------
        element : DataElement
            DICOM Integer String (IS) data element.

        Returns
        -------
        int
            Data element value.
        """

        return int(element.value)

    def parse_date(self, element: DataElement) -> datetime.date:
        """
        Parses Date (DA) data elements to date objects.

        Parameters
        ----------
        element : DataElement
            DICOM Date (DA) data element.

        Returns
        -------
        datetime.date
            Native python date object.
        """

        try:
            return datetime.strptime(element.value, "%Y%m%d").date()
        except ValueError:
            # If the value is not empty, raise an error indicating the data is not valid
            if element.value:
                raise ValueError(
                    f"Failed to parse {element.name} with value '{element.value}' into a valid date object"
                )
            # If empty string, returns None
        except TypeError:
            # If the value is None, simply return None, else raise TypeError
            if element.value:
                raise

    def parse_time(self, element: DataElement) -> datetime.time:
        """
        Parses Time (TM) data elements to time objects.

        Parameters
        ----------
        element : DataElement
            DICOM Time (TM) data element.

        Returns
        -------
        datetime.time
            Native python time object.
        """

        try:
            # Try to parse according to the default time representation
            return datetime.strptime(element.value, "%H%M%S.%f").time()
        except ValueError:
            # If the value is not empty, try to parse with the fractional part
            if element.value:
                try:
                    return datetime.strptime(element.value, "%H%M%S").time()
                except ValueError:
                    raise ValueError(
                        f"Failed to parse {element.name} with value '{element.value}' into a valid time object!"
                    )
            # If the value is empty string, simply return None
        except TypeError:
            # If the value is empty, simply return None, else raise TypeError
            if element.value:
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

    def parse_code_string(self, element: DataElement):
        """
        Parses Code String (CS) data elements to a more readable string or list
        of strings. This method relies on an Enum representation of the data element's
        possible values to be registered in the Parser's CODE_STRINGS_DICT by tag.
        If no Enum is registered, will return `None`.

        Parameters
        ----------
        element : DataElement
            DICOM Code String (CS) data element.

        Returns
        -------
        str or list
            Parsed value/s.
        """

        # We're relying on the CODE_STRINGS_DICT to associate an Enum by tag
        tag = str(element.tag)
        values_enum = self.CODE_STRINGS_DICT.get(tag)
        if values_enum:
            try:
                value = values_enum[element.value].name
                if tag in self.SINGLE_VALUE_CODE_STRINGS:
                    return value
                # If the element isn't listed in SINGLE_VALUE_CODE_STRING, return
                # it within a list.
                return [value]

            # If the value has a value multiplicity (VM) greater than one, getting
            # the Enum attribute will fail with a TypeError, and then we can simply
            # iterate over the multiple values.
            except TypeError:
                return [values_enum[value].name for value in element.value]

        # If no Enum exists, simply return the code-string value
        return element.value

    # Custom parsing methods (tag dependent rather than value-representation dependant)
    def parse_siemens_slice_timing(self, value: bytes) -> list:
        """
        Parses a SIEMENS MR image's slice timing as saved in the private
        (0019, 1029) `MosaicRefAcqTimes`_ tag to a list of floats representing
        slice times in milliseconds.

        .. _MosaicRefAcqTimes: https://en.wikibooks.org/wiki/SPM/Slice_Timing#Siemens_scanners

        Parameters
        ----------
        value : bytes
            SIEMENS private MosaicRefAcqTimes data element.

        Returns
        -------
        list
            Slice times in milliseconds.
        """

        return [round(slice_time, 5) for slice_time in list(array.array("d", value))]

    def parse_siemens_gradient_direction(self, value: bytes) -> list:
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
            Gradient directions (B-vector).
        """

        return [float(value) for value in list(array.array("d", value))]

    def parse_unknown(self, element: DataElement):
        """
        Parses private tags and other Unknown (UN) data elememts.

        Parameters
        ----------
        element : DataElement
            DICOM Unknown (UN) data element.

        """

        #
        # Siemens private tags
        #
        # DTI
        # https://na-mic.org/wiki/NAMIC_Wiki:DTI:DICOM_for_DWI_and_DTI
        # Number of Images in Mosaic
        if element.tag == ("0019", "100a"):
            return int.from_bytes(element.value, byteorder="little")
        # Slice Measurement Duration
        elif element.tag == ("0019", "100b"):
            return float(element.value)
        # B Value
        elif element.tag == ("0019", "100c"):
            return int(element.value)
        # Diffusion Directionality / Gradient Mode
        elif element.tag in (("0019", "100d"), ("0019", "100f")):
            if element.value:
                return element.value.decode("utf-8").strip()
        # Diffusion Gradient Direction
        elif element.tag == ("0019", "100e"):
            return self.parse_siemens_gradient_direction(element.value)
        # B Matrix
        elif element.tag == ("0019", "1027"):
            return list(array.array("d", element.value))
        # Bandwidth per Pixel Phase Encode
        elif element.tag == ("0019", "1028"):
            return array.array("d", element.value)[0]
        # Slice Timing
        # https://en.wikibooks.org/wiki/SPM/Slice_Timing#Siemens_scanners
        elif element.tag == ("0019", "1029"):
            return self.parse_siemens_slice_timing(element.value)
        #
        # CSA Headers
        # https://nipy.org/nibabel/dicom/siemens_csa.html
        elif element.tag in (("0029", "1010"), ("0029", "1020")):
            return CsaHeader(element.value).parsed

        # If no parsing method exists for this DICOM attribute, simply return
        # the raw value.
        return element.value

    def parse(self, element: DataElement):
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

        try:
            value_representation = ValueRepresentation(element.VR)
            try:
                method_name = self.PARSING_METHOD[value_representation]
                method = getattr(self, method_name)
                return method(element)
            except KeyError:
                return element.value
        except ValueError:
            raise NotImplementedError(
                f"{element.VR} is not a supported value-representation!"
            )
