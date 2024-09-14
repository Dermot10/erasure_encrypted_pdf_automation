import pytest
import sys
import os
import tempfile
# import pypdf
import PyPDF2
import requests_mock
from unittest.mock import patch, MagicMock
from unittest.mock import MagicMock
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from src.create_pdf import CreatePDFs


class TestPDFGenerator:
    @pytest.fixture
    def pdf_gen(self):
        return CreatePDFs()
   
    def test_organised_customer_data(self, pdf_gen):
        """Test function to test the structure of data recieved from the API.
        
        Returns:
            list - list of dictornaries containing the customer information.
            {
            "Key": str,                      # The Erasure ID (e.g., "ERASURE-123")
            "ID": int,                       # The Jira issue ID (e.g., ISSUE-1)
            "Data": {
                "Customer Name": str,        
                "Customer Address": str,
                ...
                }
            }
        """
                     
        organised_customer_data = pdf_gen.organise_customer_data()
        print("Organised Customer Data: ")
        
        assert 'Key' in organised_customer_data[0]
        assert 'ERASURE' in organised_customer_data[0]['Key']
        assert 'ID' in  organised_customer_data[0]
        assert 'Data' in organised_customer_data[0]
        assert len(organised_customer_data[0]['Data']) == 10
        assert isinstance(organised_customer_data[0]['Key'], str)
        assert isinstance(organised_customer_data[0]['ID'], str)
        assert isinstance(organised_customer_data[0]['Data'], dict)
        data_keys = ['Customer Name', 'Customer Address', 'RFL Card No.', 'Customer Account Number', 'Email Address',
             'Online Order Number[MetaPack]', 'Subscription Order number for Magazine[River]', 'Instruction',
             'Date Confirmation Required By', 'Authorised By']
        assert all(key in organised_customer_data[0]['Data'] for key in data_keys)
        
    def test_generate_pdfs(self, pdf_gen):
        """Test function to test the generation of pdf files.
        Returns: 
            dict - each dictionary has an Erasure ID as the Key :
            "ERASURE ID": {
                "ID": Issue ID ,       # The Jira issue key (e.g., "ISSUE-123")               
                "File Path": File path to the PDF file (e.g., "/path/to/file.")
            }
            
            """
        pdf_data_dict = pdf_gen.generate_pdfs()
        print(pdf_data_dict)
        assert isinstance(pdf_data_dict, dict)
        assert len(pdf_data_dict) > 0

        for issue_id, file_info in pdf_data_dict.items():
            assert isinstance(issue_id, str)
            assert isinstance(file_info, dict)

            file_path = file_info.get('file_path')
            assert file_path is not None
            assert isinstance(file_path, str)
            assert file_path.endswith(".pdf")

