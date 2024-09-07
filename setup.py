from setuptools import find_packages, setup

setup(
    name="Ecommercebot",
    version="0.0.1",
    author="faizy",
    author_email="mfansari2395@gmail.com",
    packages=find_packages(),
    install_requires=['langchain-astradb','langchain ','langchain-google-genai','datasets','pypdf','python-dotenv','flask']
)