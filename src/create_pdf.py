import os 
import sys
import io
from requests.auth import HTTPBasicAuth
import PyPDF2
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from api.jira_api import JiraAPI
from dotenv import load_dotenv

load_dotenv()


class CreatePDFs:
    def __init__(self): 
        self.password = os.environ.get('PASSWORD')
        self.categories = ["Customer Name", "Customer Address", "RFL Card No.", 
                           "Customer Account Number", "Email Address", "Online Order Number[MetaPack]", 
                           "Subscription Order Number for Magazine[River]", "Instruction", 
                           "Date Confirmation Required by", "Authorised by"]
        self.jira_api = JiraAPI()

    def organise_customer_data(self) -> list:
        """Function to get ERASURE BOARD in-progress data for further file processing"""
        
        response = self.jira_api.connect_to_Jira()
        current_user = self.jira_api.get_current_user()

        if response and response.status_code == 200:
            data = response.json()  # Get the JSON response data
            print("Successful API request, data retrieved")

            all_customer_data = []

            # Process the response data as needed
            for issue in data["issues"]:
                key = issue["key"]
                id = issue["id"]
                fields = issue["fields"]

                # Access specific fields using their keys
                name = fields.get("customfield_10141")
                address = fields.get("customfield_10142")
                rewards_for_life_card = fields.get("customfield_10164")
                customer_account_number = fields.get("customfield_10165")
                customer_email = fields.get("customfield_10144")
                last_order_number = fields.get("customfield_10149")
                subscription_order_for_magazine = fields.get("customfield_10148")
                instruction = fields.get("customfield_10137", {}).get("value", "N/A")
                date = fields.get("customfield_10140")
                authorised_by = current_user

                # Include key in customer data as a value and organize other values within a dictionary
                customer_data = {
                    "Key": key,
                    "ID": id,
                    "Data": {
                        "Customer Name": name,
                        "Customer Address": address,
                        "RFL Card No.": rewards_for_life_card,
                        "Customer Account Number": customer_account_number,
                        "Email Address": customer_email,
                        "Online Order Number[MetaPack]": last_order_number,
                        "Subscription Order number for Magazine[River]": subscription_order_for_magazine,
                        "Instruction": instruction,
                        "Date Confirmation Required By": date,
                        "Authorised By": authorised_by,
                    }
                }

                all_customer_data.append(customer_data)
            print(all_customer_data)

            return all_customer_data
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return []

    def define_table_parameters(self):
        """Helper function to define table parameters"""
        table_style = TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),  # Font name for the entire table
        ('FONTSIZE', (0, 0), (-1, -1), 10),  # Font size for the entire table
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),  # Bottom padding for all cells
        ('TOPPADDING', (0, 0), (-1, -1), 10),  # Top padding for all cells
        ('LEFTPADDING', (0, 0), (-1, -1), 10),  # Left padding for all cells
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),  # Right padding for all cells
        ('BOX', (0, 0), (-1, -1), 1, colors.black),  # Border width and color for all cells
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),  # Inner grid lines for all cells
        ('LINEABOVE', (0, 0), (-1, 0), 1.0, colors.black),  # Line above title row
        ('LINEBELOW', (0, 0), (-1, -1), 1.0, colors.black),  # Line below each cell
        ('LINEBEFORE', (1, 0), (1, -1), 1.0, colors.black),  # Vertical line between columns
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Title row background color
    ])

        return table_style

    def define_title_parameters(self):
        """Helper function to define the title parameters for the PDF document."""
        title_style = ParagraphStyle(
            'Title',
            fontName='Helvetica-Bold',
            fontSize=12,
            textColor=colors.gray,
            spaceBefore=12,
            alignment=1
            )
        return title_style
    
    def create_password_protected_pdf(self, input_path, password):
        """Helper function to encrypt an existing PDF file with a password."""
        pdf = PyPDF2.PdfReader(input_path)

        for page in pdf.pages:
            # Remove any existing encryption (if present)
            if '/Encrypt' in page:
                page.pop('/Encrypt')
        
        output_buffer = io.BytesIO()
        writer = PyPDF2.PdfWriter()
        for page in pdf.pages:
            writer.add_page(page)

        writer.encrypt(password)

        writer.write(output_buffer)
        output_buffer.seek(0)

        # Overwrite the original file with the encrypted content
        with open(input_path, 'wb') as output_file:
            output_file.write(output_buffer.getvalue())

        print("Successfully encrypted PDF")

    def generate_pdfs(self) -> dict: 
        """Function will generate password protected PDFs, with data pulled and formattted from the Jira API."""
    
        all_customer_data = self.organise_customer_data()
        pdf_data_dict = {}  # Dictionary to store generated PDF file paths with issue IDs

        for customer_data in all_customer_data:
            # Create a new PDF document for each customer using their key as the filename
            erasure_key = customer_data["Key"]
            issue_id = customer_data["ID"]


            temp_output_path = f"/tmp/{erasure_key}.pdf"
            doc = SimpleDocTemplate(temp_output_path, pagesize=letter)

            # Create the table object
            table_data = [["Category", "Sensitive - High Priority"]]
            table_data += [[category, value] for category, value in customer_data["Data"].items()]
            table = Table(table_data)

            # Apply the table style
            table.setStyle(self.define_table_parameters())

            # Create the title
            title = Paragraph('Strictly Confidential - Addressee Only _GDPR IT INSTRUCTION FORM', style=self.define_title_parameters())

            # Add the title and table to the PDF document
            elements = [title, Spacer(1, 12)]
            elements.append(table)
            doc.build(elements)

            self.create_password_protected_pdf(temp_output_path, self.password) # same file path written over and encrypted with password

            pdf_data_dict[erasure_key] = {"issue_id": issue_id, "file_path": temp_output_path} # nested dict 
            print(f"Added to pdf_data_dict: {erasure_key} - {pdf_data_dict[erasure_key]}")
            print(f"Check Here : {pdf_data_dict}")  # Debugging print statement

        return pdf_data_dict

    def run_automation(self):
        """Function to generate each individual customer PDF file and post them to Jira."""
        try:
            pdf_data_dict = self.generate_pdfs()
            print("Successfully created and encrypted PDFs")
           
            #print("pdf_data_dict:", pdf_data_dict)

            # For each issue key, post the corresponding PDF as an attachment to the Jira issue
            for issue_key, data in pdf_data_dict.items():
                issue_id = data["issue_id"]
                file_path = data["file_path"]
                print(f'{file_path} with the Issue ID: {issue_id} is being encrypted and attached to Jira issue')
                print("")
                
                self.jira_api.post_protected_file(issue_id, file_path)

                break #POST one pdf issue back to Jira

        except Exception as e:
            print(f"Failed with error: {e}")
        finally:
            print("Process completed.")


if __name__== "__main__": 
    pdf_gen = CreatePDFs()
    
    #pdf_gen.organise_customer_data()

    #function to generate pdf files locally 
    pdf_gen.generate_pdfs() 

    #pdf_gen.run()

    
    




    
        

    

    
    



