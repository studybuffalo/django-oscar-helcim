"""Tests for the gateway module."""
# pylint: disable=missing-docstring, protected-access

from unittest.mock import patch

from helcim import exceptions as helcim_exceptions, gateway


class MockPostResponse():
    def __init__(self, url, data):
        self.content = """<?xml version="1.0"?>
            <message>
                <response>1</response>
                <responseMessage>APPROVED</responseMessage>
                <notice></notice>
                <transaction>
                    <transactionId>1111111</transactionId>
                    <type>purchase</type>
                    <date>2018-01-01</date>
                    <time>12:00:00</time>
                    <cardHolderName>Test Person</cardHolderName>
                    <amount>100.00</amount>
                    <currency>CAD</currency>
                    <cardNumber>5454********5454</cardNumber>
                    <cardToken>80defad45bae30e557da0e</cardToken>
                    <expiryDate>0125</expiryDate>
                    <cardType>MasterCard</cardType>
                    <avsResponse>X</avsResponse>
                    <cvvResponse>M</cvvResponse>
                    <approvalCode>T6E1ST</approvalCode>
                    <orderNumber>INV1000</orderNumber>
                    <customerCode>CST1000</customerCode>
                </transaction>
            </message>
            """
        self.status_code = 200
        self.url = url
        self.data = data

class MockDjangoModel():
    def __init__(self, **kwargs):
        self.data = kwargs

API_DETAILS = {
    'url': 'https://www.test.com',
    'account_id': '12345678',
    'token': 'abcdefg',
    'terminal_id': '98765432',
}

@patch('helcim.gateway.requests.post', MockPostResponse)
@patch(
    'helcim.gateway.models.HelcimTransaction.objects.create',
    MockDjangoModel
)
def test_purchase_processing():
    details = {
        'amount': 100.00,
        'customer_code': 'CST1000',
    }

    purchase = gateway.Purchase(api_details=API_DETAILS, **details)
    response = purchase.process()

    assert isinstance(response, MockDjangoModel)

def test_determine_purchase_payment_details_token():
    details = {
        'token': 'abcdefghijklmnopqrstuvw',
        'customer_code': 'CST1000',
        'token_f4l4': '11119999',
    }

    purchase = gateway.Purchase(api_details=API_DETAILS, **details)
    purchase.validate_fields()
    purchase._determine_payment_details()

    assert len(purchase.cleaned) == 3
    assert purchase.cleaned['token'] == details['token']
    assert purchase.cleaned['customer_code'] == details['customer_code']
    assert purchase.cleaned['token_f4l4'] == details['token_f4l4']

def test_determine_payment_details_token_with_f4l4_skip():
    details = {
        'token': 'abcdefghijklmnopqrstuvw',
        'customer_code': 'CST1000',
        'token_f4l4_skip': True,
    }

    purchase = gateway.Purchase(api_details=API_DETAILS, **details)
    purchase.validate_fields()
    purchase._determine_payment_details()

    assert len(purchase.cleaned) == 3
    assert purchase.cleaned['token'] == details['token']
    assert purchase.cleaned['customer_code'] == details['customer_code']
    assert purchase.cleaned['token_f4l4_skip'] == 1

def test_determine_payment_details_token_f4l4_missing_error():
    details = {
        'token': 'abcdefghijklmnopqrstuvwxyz',
        'customer_code': 'CST1000',
    }

    try:
        purchase = gateway.Purchase(api_details=API_DETAILS, **details)
        purchase.validate_fields()
        purchase._determine_payment_details()
    except ValueError:
        assert True
    else:
        assert False

def test_determine_payment_details_customer():
    details = {
        'customer_code': 'CST1000',
    }

    purchase = gateway.Purchase(api_details=API_DETAILS, **details)
    purchase.validate_fields()
    purchase._determine_payment_details()

    assert len(purchase.cleaned) == 1
    assert purchase.cleaned['customer_code'] == details['customer_code']

def test_determine_payment_details_cc():
    details = {
        'cc_number': '1234567890123456',
        'cc_expiry': '0125',
    }

    purchase = gateway.Purchase(api_details=API_DETAILS, **details)
    purchase.validate_fields()
    purchase._determine_payment_details()

    assert len(purchase.cleaned) == 2
    assert purchase.cleaned['cc_number'] == details['cc_number']
    assert purchase.cleaned['cc_expiry'] == details['cc_expiry']

def test_determine_payment_details_cc_with_details():
    details = {
        'cc_number': '1234567890123456',
        'cc_expiry': '0125',
        'cc_name': 'Test Person',
        'cc_cvv': '123',
        'cc_address': '100 Fake Street',
        'cc_postal_code': 'T1T 1T1',
    }

    purchase = gateway.Purchase(api_details=API_DETAILS, **details)
    purchase.validate_fields()
    purchase._determine_payment_details()

    assert len(purchase.cleaned) == 6
    assert purchase.cleaned['cc_number'] == details['cc_number']
    assert purchase.cleaned['cc_expiry'] == details['cc_expiry']
    assert purchase.cleaned['cc_name'] == details['cc_name']
    assert purchase.cleaned['cc_cvv'] == details['cc_cvv']
    assert purchase.cleaned['cc_address'] == details['cc_address']
    assert purchase.cleaned['cc_postal_code'] == details['cc_postal_code']

def test_determine_payment_details_mag_encrypted():

    details = {
        'mag_enc': 'iscySW5ks7LeQQ8r4Tz7vb6el6QFpuQMbxGbh1==',
        'mag_enc_serial_number': 'SERIAL1230129912',
    }

    purchase = gateway.Purchase(api_details=API_DETAILS, **details)
    purchase.validate_fields()
    purchase._determine_payment_details()

    assert len(purchase.cleaned) == 2
    assert purchase.cleaned['mag_enc'] == details['mag_enc']
    assert (
        purchase.cleaned['mag_enc_serial_number']
        == details['mag_enc_serial_number']
    )

def test_determine_payment_details_mag():
    details = {
        'mag': '%B45**********SENSITIVE*DATA******************01?2',
    }

    purchase = gateway.Purchase(api_details=API_DETAILS, **details)
    purchase.validate_fields()
    purchase._determine_payment_details()

    assert len(purchase.cleaned) == 1
    assert purchase.cleaned['mag'] == details['mag']

def test_determine_payment_details_value_error():
    details = {}

    try:
        purchase = gateway.Purchase(api_details=API_DETAILS, **details)
        purchase.validate_fields()
        purchase._determine_payment_details()
    except ValueError:
        assert True
    else:
        assert False

def test_determine_payment_details_token_priority():
    details = {
        'token': 'abcdefghijklmnopqrstuvw',
        'token_f4l4': '11119999',
        'customer_code': 'CST1000',
        'cc_number': '1234567890123456',
        'cc_expiry': '0125',
        'mag_enc': 'iscySW5ks7LeQQ8r4Tz7vb6el6QFpuQMbxGbh1==',
        'mag_enc_serial_number': 'SERIAL1230129912',
        'mag': '%B45**********SENSITIVE*DATA******************01?2',
    }

    purchase = gateway.Purchase(api_details=API_DETAILS, **details)
    purchase.validate_fields()
    purchase._determine_payment_details()

    assert len(purchase.cleaned) == 3
    assert 'token' in purchase.cleaned

def test_determine_payment_details_customer_priority():
    details = {
        'customer_code': 'CST1000',
        'cc_number': '1234567890123456',
        'cc_expiry': '0125',
        'mag_enc': 'iscySW5ks7LeQQ8r4Tz7vb6el6QFpuQMbxGbh1==',
        'mag_enc_serial_number': 'SERIAL1230129912',
        'mag': '%B45**********SENSITIVE*DATA******************01?2',
    }

    purchase = gateway.Purchase(api_details=API_DETAILS, **details)
    purchase.validate_fields()
    purchase._determine_payment_details()

    assert len(purchase.cleaned) == 1
    assert 'customer_code' in purchase.cleaned

def test_determine_payment_details_cc_priority():
    details = {
        'cc_number': '1234567890123456',
        'cc_expiry': '0125',
        'mag_enc': 'iscySW5ks7LeQQ8r4Tz7vb6el6QFpuQMbxGbh1==',
        'mag_enc_serial_number': 'SERIAL1230129912',
        'mag': '%B45**********SENSITIVE*DATA******************01?2',
    }

    purchase = gateway.Purchase(api_details=API_DETAILS, **details)
    purchase.validate_fields()
    purchase._determine_payment_details()

    assert len(purchase.cleaned) == 2
    assert 'cc_number' in purchase.cleaned

def test_determine_payment_details_mag_encrypted_priority():
    details = {
        'mag_enc': 'iscySW5ks7LeQQ8r4Tz7vb6el6QFpuQMbxGbh1==',
        'mag_enc_serial_number': 'SERIAL1230129912',
        'mag': '%B45**********SENSITIVE*DATA******************01?2',
    }

    purchase = gateway.Purchase(api_details=API_DETAILS, **details)
    purchase.validate_fields()
    purchase._determine_payment_details()

    assert len(purchase.cleaned) == 2
    assert 'mag_enc' in purchase.cleaned

def test_process_error_response_purchase():
    purchase_request = gateway.Purchase()

    try:
        purchase_request.process_error_response('')
    except helcim_exceptions.PaymentError:
        assert True
    else:
        assert False