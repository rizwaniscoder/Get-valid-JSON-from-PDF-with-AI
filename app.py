import streamlit as st
import pdfplumber
import os
from openai import OpenAI
from json import JSONDecodeError

def extract_text_from_pdf(file):
    """
    Function to extract text from a PDF.
    Now handles files that can't be opened.
    """
    extracted_text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or " "
                extracted_text += page_text
    except Exception as e:
        st.error(f"Failed to read the PDF. Error details: {str(e)}")
        return None
    return extracted_text

def generate_ai_response(input_text, api_key):
    """
    Function to interact with OpenAI API and get a response.
    Handles exceptions for a smoother user experience.
    """
    example_json = """

{
"id": "PMSB6R2EWFBFBBBIICKUD2EQAM0Z0",
"history_id": "VZXJQQWTMBHA5E6DWR3X2IWGXE0Z0",
"shared_id": "PMSB6R2EWFBFBBBIICKUD2EQAM0Z1",
"local_details": {
"version": 3,
"external_references": [
{
"reference": [
{
"reference_id": "MA.10062",
"system": "LIKEZERO",
"reference_label": "Agreement Family Reference"
},
{
"reference_id": "MA.10062.1",
"system": "LIKEZERO",
"reference_label": "Agreement Reference"
},
{
"reference_id": "Full Submission",
"system": "LIKEZERO",
"user_defined_label": "Legal Agreement Scope"
},
{
"reference_id": "800022",
"system": "BNPP",
"user_defined_label": "BNPP Document Reference"
},
{
"reference_id": "1",
"system": "LIKEZERO",
"user_defined_label": "batchNumber"
}
]
}
],
"agreement_attachment": [
{
"attachment_id": "B4ZNNHVYINHNHPYJXPNUVK5T3I0",
"file_name": "800022_BNPP.Allianz CTA (Euroclear) (fully executed).pdf",
"create_time": "2022-08-24T09:43:43.380Z"
}
],
"direction": "Outgoing",
"local_parties": [
"m10002012277lz54b"
],
"view_party": "A",
"minified_links": [
1,
2,
4,
6,
11,
12,
17
]
},
"bilateral_details": {
"version": 3,
"parties": {
"on_behalf_party": "A",
"contractual_parties_a": [
{
"entity_id": "m10002012277lz54b",
"entity_LEI": "R0MUWSFPU8MPRO8K5P83",
"entity_legal_name": "BNP Paribas S.A.",
"submitted_entity_legal_name": "BNP Paribas",
"entity_short_name": "BNPP",
"group_id": "m10002012277lz3z3",
"group_name": "BNP Paribas"
}
],
"contractual_parties_b": [
{
"entity_id": "prd44bwt9beh",
"entity_LEI": "DKBD555YIJCQ30PMHF22",
"entity_beneficial_owner_LEI": "529900K9B0N5BT694847",
"entity_legal_name": "ALLIANZ LIFE INSURANCE COMPANY OF NORTH AMERICA",
"group_id": "prd440ehe8vp",
"group_name": "Allianz SE"
}
]
},
"agreement_long_name": "MA.10062.1 BNP Paribas vs ALLIANZ LIFE INSURANCE COMPANY OF NORTH AMERICA 20210901 Posting Parties A Initial Margin 2019 Collateral Transfer Agreement",
"agreement_short_name": "MA.10062.1 Collateral Transfer Agreement 2019 Belgian Law",
"agreement_type": {
"agreement_type": "ISDA CSA",
"ISDA_CSA": {
"master_agreement_date": "2000-07-18",
"CSA_document_version": {
"CSA_document_name": "Collateral Transfer Agreement",
"publisher": "ISDA and Euroclear",
"governing_law": "Belgian Law",
"margin_type": "Initial Margin",
"CSA_version": "2019",
"CSA_label": "Collateral Transfer Agreement"
},
"CSA_agreement_date": "2021-09-01",
"posting_parties": [
"A"
],
"calculation_currency": [
{
"party": "A",
"currency": "USD"
},
{
"party": "B",
"currency": "USD"
}
],
"base_currency": [
{
"currency": "USD"
}
],
"covered_transactions": [
{
"party": "A",
"exchange_principal_on_cross_ccy_swaps": false,
"exposure_treatment": "Gross",
"sensitivity_approach": [
{
"type": [
"Equity ETFs",
"Equity Indices",
"Equity Mutual Funds"
],
"delta_applied_to": "Individual"
},
{
"type": [
"Commodities Indices"
],
"delta_applied_to": "Individual"
}
]
},
{
"party": "A",
"all_transactions": true,
"exposure_treatment": "Gross",
"sensitivity_approach": [
{
"type": [
"Equity ETFs",
"Equity Indices",
"Equity Mutual Funds"
],
"delta_applied_to": "Individual"
},
{
"type": [
"Commodities Indices"
],
"delta_applied_to": "Individual"
}
]
},
{
"party": "A",
"exposure_treatment": "Gross",
"exposure_valuation_method": [
{
"valuation_method": "SIMM"
}
],
"sensitivity_approach": [
{
"type": [
"Equity ETFs",
"Equity Indices",
"Equity Mutual Funds"
],
"delta_applied_to": "Individual"
},
{
"type": [
"Commodities Indices"
],
"delta_applied_to": "Individual"
}
]
},
{
"party": "A",
"regimes": [
"European Supervisory Authorities"
],
"exposure_treatment": "Gross",
"exposure_valuation_method": [
{
"valuation_method": "Schedule"
}
],
"sensitivity_approach": [
{
"type": [
"Equity ETFs",
"Equity Indices",
"Equity Mutual Funds"
],
"delta_applied_to": "Individual"
},
{
"type": [
"Commodities Indices"
],
"delta_applied_to": "Individual"
}
]
},
{
"party": "A",
"regimes": [
"US Prudential Regulators"
],
"included_transaction_types": [
{
"asset_class": [
"Equity",
"Credit"
],
"base_product": [
"Index"
],
"sub_product": [
"Recovery CDS"
]
}
],
"included_branches": [
"Credit recovery lock CDS, dividend swaps on an index or dividend swaps on a single stock or a basket of equities"
],
"exposure_treatment": "Gross",
"exposure_valuation_method": [
{
"valuation_method": "Schedule"
}
],
"sensitivity_approach": [
{
"type": [
"Equity ETFs",
"Equity Indices",
"Equity Mutual Funds"
],
"delta_applied_to": "Individual"
},
{
"type": [
"Commodities Indices"
],
"delta_applied_to": "Individual"
}
]
},
{
"party": "B",
"exchange_principal_on_cross_ccy_swaps": false,
"exposure_treatment": "Gross",
"sensitivity_approach": [
{
"type": [
"Equity ETFs",
"Equity Indices",
"Equity Mutual Funds"
],
"delta_applied_to": "Individual"
},
{
"type": [
"Commodities Indices"
],
"delta_applied_to": "Individual"
}
]
},
{
"party": "B",
"all_transactions": true,
"exposure_treatment": "Gross",
"sensitivity_approach": [
{
"type": [
"Equity ETFs",
"Equity Indices",
"Equity Mutual Funds"
],
"delta_applied_to": "Individual"
},
{
"type": [
"Commodities Indices"
],
"delta_applied_to": "Individual"
}
]
},
{
"party": "B",
"exposure_treatment": "Gross",
"exposure_valuation_method": [
{
"valuation_method": "SIMM"
}
],
"sensitivity_approach": [
{
"type": [
"Equity ETFs",
"Equity Indices",
"Equity Mutual Funds"
],
"delta_applied_to": "Individual"
},
{
"type": [
"Commodities Indices"
],
"delta_applied_to": "Individual"
}
]
},
{
"party": "B",
"regimes": [
"European Supervisory Authorities"
],
"exposure_treatment": "Gross",
"exposure_valuation_method": [
{
"valuation_method": "Schedule"
}
],
"sensitivity_approach": [
{
"type": [
"Equity ETFs",
"Equity Indices",
"Equity Mutual Funds"
],
"delta_applied_to": "Individual"
},
{
"type": [
"Commodities Indices"
],
"delta_applied_to": "Individual"
}
]
},
{
"party": "B",
"regimes": [
"US Prudential Regulators"
],
"included_transaction_types": [
{
"asset_class": [
"Equity",
"Credit"
],
"base_product": [
"Index"
],
"sub_product": [
"Recovery CDS"
]
}
],
"included_branches": [
"Credit recovery lock CDS, dividend swaps on an index or dividend swaps on a single stock or a basket of equities"
],
"exposure_treatment": "Gross",
"exposure_valuation_method": [
{
"valuation_method": "Schedule"
}
],
"sensitivity_approach": [
{
"type": [
"Equity ETFs",
"Equity Indices",
"Equity Mutual Funds"
],
"delta_applied_to": "Individual"
},
{
"type": [
"Commodities Indices"
],
"delta_applied_to": "Individual"
}
]
}
],
"credit_support_obligations": [
{
"margin_terms": [
{
"party": "A",
"thresholds": [
{
"currency": "USD",
"amount": "5000000",
"method": "Flat Amount",
"additional_details": "unless otherwise agreed between the parties"
}
],
"minimum_transfer_amounts": [
{
"currency": "USD",
"amount": "250000",
"method": "Flat Amount"
},
{
"amount": "0",
"method": "Flat Amount",
"additional_details": "Zero Credit Support Amount"
}
],
"margin_approach": "Distinct"
},
{
"party": "B",
"thresholds": [
{
"currency": "USD",
"amount": "5000000",
"method": "Flat Amount",
"additional_details": "unless otherwise agreed between the parties"
}
],
"minimum_transfer_amounts": [
{
"currency": "USD",
"amount": "250000",
"method": "Flat Amount"
},
{
"amount": "0",
"method": "Flat Amount",
"additional_details": "Zero Credit Support Amount"
}
],
"margin_approach": "Distinct"
}
]
}
],
"conditions_precedent": [
{
"party": "A",
"condition_precedent_applied": "CSA Standard",
"termination_currency": [
{
"currency": "USD"
}
]
},
{
"party": "B",
"condition_precedent_applied": "CSA Standard",
"termination_currency": [
{
"currency": "EUR"
}
]
},
{
"party": "A",
"termination_currency": [
{
"currency": "USD"
}
],
"termination_event": [
{
"termination_event_type": [
"Illegality"
]
}
]
},
{
"party": "B",
"termination_currency": [
{
"currency": "EUR"
}
],
"termination_event": [
{
"termination_event_type": [
"Illegality"
]
}
]
},
{
"party": "A",
"termination_currency": [
{
"currency": "USD"
}
],
"termination_event": [
{
"termination_event_type": [
"Tax Event"
]
}
]
},
{
"party": "B",
"termination_currency": [
{
"currency": "EUR"
}
],
"termination_event": [
{
"termination_event_type": [
"Tax Event"
]
}
]
},
{
"party": "A",
"termination_currency": [
{
"currency": "USD"
}
],
"termination_event": [
{
"termination_event_type": [
"Tax Event Merger"
]
}
]
},
{
"party": "B",
"termination_currency": [
{
"currency": "EUR"
}
],
"termination_event": [
{
"termination_event_type": [
"Tax Event Merger"
]
}
]
},
{
"party": "A",
"termination_currency": [
{
"currency": "USD"
}
],
"termination_event": [
{
"termination_event_type": [
"Credit Event Merger"
]
}
]
},
{
"party": "B",
"termination_currency": [
{
"currency": "EUR"
}
],
"termination_event": [
{
"termination_event_type": [
"Credit Event Merger"
]
}
]
},
{
"party": "A",
"termination_currency": [
{
"currency": "USD"
}
],
"termination_event": [
{
"termination_event_type": [
"Additional Event"
]
}
]
},
{
"party": "B",
"termination_currency": [
{
"currency": "EUR"
}
],
"termination_event": [
{
"termination_event_type": [
"Additional Event"
]
}
]
}
],
"dispute_resolution": [
{
"resolution_time_trigger": "Dispute notification received",
"resolution_time_offset": 1,
"resolution_time_day_type": "Business Day",
"resolution_time": "13:00",
"resolution_time_zone": "America/New_York",
"resolution_value": [
{
"description": "Consultation Procedure"
}
],
"resolution_alternative": [
"CSA Standard"
]
}
],
"credit_support_offsets": [
{
"credit_support_offset": false
}
],
"demands_and_notices": [
{
"party": "A",
"entity_contact": [
{
"contact_name": "Collateral Management",
"contact_email": "bnppnycollateralmgmt@americas.bnpparibas.com",
"contact_phone": "201 850 5630"
}
],
"entity_address": {
"address_line1": "525 Washington Blvd",
"address_city": "Jersey",
"address_country": "US",
"address_postal_or_zip_code": "NJ 07310"
}
},
{
"party": "B",
"entity_contact": [
{
"contact_name": "Investments",
"contact_phone": "763 765 6500"
}
],
"entity_address": {
"address_line1": "5701 Golden Hills Drive",
"address_city": "Minneapolis",
"address_country": "US",
"address_postal_or_zip_code": "MN 55416"
}
}
],
"regimes": [
{
"party": "A",
"not_applicable_regimes": [
"Financial Market Supervisory"
]
},
{
"party": "B",
"not_applicable_regimes": [
"Financial Market Supervisory"
]
},
{
"party": "A",
"not_applicable_regimes": [
"Japanese Financial Services"
]
},
{
"party": "B",
"not_applicable_regimes": [
"Japanese Financial Services"
]
},
{
"party": "A",
"not_applicable_regimes": [
"Australian Prudential Regulation Authority"
]
},
{
"party": "B",
"not_applicable_regimes": [
"Australian Prudential Regulation Authority"
]
},
{
"party": "A",
"not_applicable_regimes": [
"Hong Kong Monetary Authority"
]
},
{
"party": "B",
"not_applicable_regimes": [
"Hong Kong Monetary Authority"
]
},
{
"party": "A",
"not_applicable_regimes": [
"Monetary Authority of Singapore"
]
},
{
"party": "B",
"not_applicable_regimes": [
"Monetary Authority of Singapore"
]
},
{
"party": "A",
"applicable_regime": "US Prudential Regulators",
"simm_exception": true,
"simm_exception_applicable_method": [
"Mandatory Method"
]
},
{
"party": "B",
"applicable_regime": "US Prudential Regulators",
"simm_exception": true,
"simm_exception_applicable_method": [
"Mandatory Method"
]
},
{
"party": "A",
"not_applicable_regimes": [
"Commodity Futures Trading Commission"
]
},
{
"party": "B",
"not_applicable_regimes": [
"Commodity Futures Trading Commission"
]
},
{
"party": "A",
"not_applicable_regimes": [
"Securities Exchange Commission"
]
},
{
"party": "B",
"not_applicable_regimes": [
"Securities Exchange Commission"
]
},
{
"party": "A",
"not_applicable_regimes": [
"Office of the Superintendent of Financial Institutions"
]
},
{
"party": "B",
"not_applicable_regimes": [
"Office of the Superintendent of Financial Institutions"
]
},
{
"party": "A",
"applicable_regime": "European Supervisory Authorities",
"simm_exception": true,
"simm_exception_applicable_method": [
"Fallback to Mandatory Method"
]
},
{
"party": "B",
"applicable_regime": "European Supervisory Authorities",
"simm_exception": true,
"simm_exception_applicable_method": [
"Fallback to Mandatory Method"
]
}
]
}
}
},
"business_state": "Created",
"action": "Local Change",
"last_modified_party": "A",
"create_time": "2022-08-24T09:43:43.380Z",
"modify_time": "2023-11-20T09:11:07.019Z",
"expire_time": "+292278994-08-17T07:12:55.807Z",
"create_user_id": "prd7o61auoo9",
"modify_user_id": "prd7o61auoo9",
"modify_username": "DIGITIZATION.API@BNP Paribas",
"publicized": false
}
]
"""
    try:
        client = OpenAI(api_key=api_key)
        input_messages = [
            {"role": "system", "content": f"Please output a valid JSON. The data contains Legal Agreement. Here is the sample JSON response to get inspiration from: {example_json}, please extract all the information from the data in such that all the information get stored properly in valid JSON"},
            {"role": "user", "content": input_text},
        ]
        response_from_ai, *_ = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=input_messages,
            response_format={"type": "json_object"}
        ).choices
        if response_from_ai:
            return response_from_ai.message.content
        else:
            return {"error": "No response from AI."}
    except Exception as e:
        st.error(f"Failed to get an AI response. Error details: {str(e)}")
        return {"error": "Failed to get an AI response."}

def main():
    """
    Main function to control the flow
    """
    st.title('Get valid JSON from PDF with AI')

    api_key = st.text_input("Enter your OpenAI API key:", type="password")


    # Upload a PDF file
    pdf_file = st.file_uploader("Please upload a PDF file", type=['pdf'])

    # A button to start the analysis
    if st.button("Start Analysis"):
        if pdf_file is not None:
            with st.spinner("Analyzing the content in the PDF..."):
                extracted_text = extract_text_from_pdf(pdf_file)
                if extracted_text:
                    ai_response = generate_ai_response(extracted_text, api_key)
                    if ai_response:
                        try:
                            st.json(ai_response)
                            # Download JSON response
                            st.download_button(
                                label="Download JSON response",
                                data=ai_response,
                                file_name='ai_response.json',
                                key='download_json'
                            )
                        except JSONDecodeError as e:
                            st.error(f"Failed to convert AI response to JSON. Error details: {str(e)}")
                else:
                    st.warning("No readable text found in the uploaded PDF. Consider uploading a different file.")
        else:
            st.warning("No file uploaded. Please upload a PDF file.")

if __name__ == '__main__':
    main()
