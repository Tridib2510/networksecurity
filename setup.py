'''
The setup.py file is an essential part of packaging and distributing Python objects.
It is used by setuptools(or disutils in older Python versions) to define the configuration
of your project, such as its metadata,dependencies, and more

'''

from setuptools import find_packages,setup
# find_packages-->It will scan through all the folders and when it find a __ini__.py
# The parent folder will be considered as a package itself

from typing import List

def get_requirements()->List[str]:
    """
    This function will return the list of requirements
    """
    requirement_lst:List[str]=[]
    try:
        with open('requirements.txt','r') as file:
            #Read line from the file
            lines=file.readlines()
            # Process each line
            for line in lines:
                requirement=line.strip()
                #ignore the empty lines and -e .
                if requirement and requirement!='-e .':
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found")

    return requirement_lst

setup(
    name="NetworkSecurity",
    version="0.0.1",
    author="Tridib Roy Chowdhury",
    author_email="tridibroychowdhury9@gmail.com",
    packages=find_packages(),#responsible for searching all the packages
    install_requires=get_requirements()#Make sure that it install all the libraries

)