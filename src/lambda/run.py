import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from src.create_pdf import CreatePDFs


def run(event=None, context=None): 
    try:
        print("Checkpoint 1")
        # load_dependencies(['_imaging'])
        pdf_gen = CreatePDFs()
        pdf_gen.organise_customer_data()
        print("Checkpoint 2")

        #function to generate pdf files locally 
        #pdf_gen.generate_pdfs() 

        #pdf_gen.run_automation()
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__=="__main__":
    # print(f"Project root: {project_root}")
    run()
