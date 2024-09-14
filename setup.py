import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    version                       = "0.0.1"               , # change this on every release
    name                          = "Erasure Phase 1 PDF Generator",
    author                        = "Dermot Bruce Agbeko",
    author_email                  = "dermotag@hotmail.com",
    description                   = "Automate password protected PDF generation for Erasure Phase 1",
    long_description              = long_description,
    long_description_content_type = "text/markdown",
    url                           = "https://gitlab.com/HnBI/cyber-sec/hb-security-automations/erasure_phase1_pdf_generator",
    packages                      = setuptools.find_packages(),
    classifiers                   = [ "Programming Language :: Python :: 3"   ,
                                      "License :: OSI Approved :: MIT License",
                                      "Operating System :: OS Independent"   ])
