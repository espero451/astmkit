import pytest
from astmkit.parser import extract_record, enumerate_fields


# Tests for extract_record
@pytest.mark.parametrize(
    "records, record_type, expected",
    [
        (["H|1|HeaderData", "P|1|PatientData", "O|1|OrderData"], "P", "P|1|PatientData"),
        (["H|1|HeaderData", "P|1|PatientData", "O|1|OrderData"], "H", "H|1|HeaderData"),
        (["H|1|HeaderData", "P|1|PatientData", "O|1|OrderData"], "O", "O|1|OrderData"),
        (["H|1|HeaderData", "P|1|PatientData"], "O", None),
        ([], "H", None),
    ]
)
def test_extract_record(records, record_type, expected):
    assert extract_record(records, record_type) == expected


# Tests for enumerate_fields
@pytest.mark.parametrize(
    "record, expected",
    [
        (
            "P|1|SomeValue|AnotherValue",
            "P|1|SomeValue|AnotherValue\n"
            "P1: P\n"
            "P2: 1\n"
            "P3: SomeValue\n"
            "P4: AnotherValue"
        ),
        ("H", "H\nH1: H")
    ]
)
def test_enumerate_fields(record, expected):
    assert enumerate_fields(record) == expected

