CreatePDFs: GDPR Erasure Board Automation

Overview
The CreatePDFs Python application automates the generation of password-protected PDFs for GDPR erasure requests.
It integrates with Jira to securely process customer data, generate encrypted PDF files, and attach them to Jira issues, streamlining compliance workflows.

Features
- **Data Integration**: Retrieves customer data directly from Jira using API calls.
- **Data Organization**: Extracts, formats, and organizes customer details for streamlined processing.
- **PDF Generation**: Creates password-protected PDFs with customer data displayed in a tabular format.
- **Encryption**: Applies secure encryption to PDFs before uploading to Jira.
- **Automation**: Orchestrates the entire workflow, minimizing manual intervention.


Key Design Principles and Patterns

## SOLID Principles- 

1. **Single Responsibility Principle (SRP)**
   - Each class and method has a specific, well-defined responsibility:
     - `CreatePDFs` orchestrates data retrieval, processing, and PDF generation.
     - Methods like `organise_customer_data` and `generate_pdfs` focus on discrete tasks such as data preparation and PDF creation.

2. **Open/Closed Principle (OCP)**
   - The system is designed for extensibility:
     - Adding new fields or categories to customer data involves minimal code changes.
     - PDF formatting and styling are modular, handled by helper methods like `define_table_parameters` and `define_title_parameters`.

3. **Liskov Substitution Principle (LSP)**
   - The `JiraAPI` class can be replaced with a mock or alternative implementation without affecting application logic.

4. **Interface Segregation Principle (ISP)**
   - The `JiraAPI` class handles only Jira-specific interactions, ensuring no unnecessary dependencies in the `CreatePDFs` class.

5. **Dependency Inversion Principle (DIP)**
   - High-level modules like `CreatePDFs` depend on abstractions rather than concrete implementations, enhancing flexibility and testability.

## Design Patterns-
Template Method
Provides a structured sequence for operations like organizing data, generating PDFs, encrypting files, and attaching them to Jira.

Adapter Pattern-
The JiraAPI class simplifies interaction with Jira's REST API.

Facade Pattern-
The CreatePDFs class hides complexity by providing a straightforward automation interface.

Builder Pattern (Partial)-
Constructs PDFs in steps, such as defining table and title parameters, before building the document.

Dependency Injection-
External dependencies like JiraAPI are passed into the class, making it easier to test and extend.


## Design Improvements

1. **Singleton Pattern**
   - Ensure a single instance of `JiraAPI` for consistent API interactions.

2. **Retry Logic**
   - Implement exponential back-off for API request retries to improve reliability.

3. **Structured Logging**
   - Replace existing print statements with Python’s `logging` module for better traceability and configurability.

4. **Refined Class Design**
   - Decouple responsibilities into dedicated classes:
     ```python
     class PDFManager:
         def generate_pdf(self, data): ...
         def encrypt_pdf(self, file_path): ...

     class JiraManager:
         def fetch_customer_data(self): ...
         def attach_file_to_issue(self, file_path): ...

     class CreatePDFs:
         def __init__(self):
             self.pdf_manager = PDFManager()
             self.jira_manager = JiraManager()

         def run_automation(self):
             data = self.jira_manager.fetch_customer_data()
             pdf_path = self.pdf_manager.generate_pdf(data)
             self.pdf_manager.encrypt_pdf(pdf_path)
             self.jira_manager.attach_file_to_issue(pdf_path)
     ```




## Setup Instructions 

Clone the repository:

git clone <repository-url>

Install dependencies:

pip install -r requirements.txt

Set up environment variables in .env:

JIRA_API_URL=https://your-jira-instance.atlassian.net
JIRA_API_TOKEN=your_api_token
JIRA_USERNAME=your_email@example.com
PDF_PASSWORD=your_password


## License
This project is licensed under the MIT License. See the LICENSE file for details.
     
