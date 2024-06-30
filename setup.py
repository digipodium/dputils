from setuptools import setup, find_packages

setup(
    name='dputils',
    version='1.0.1',
    description='This library is utility library from digipodium',
    author='Team Digipodium, Zaid Kamil, AkulS1008',
    author_email='xaidmetamorphos@gmail.com',
    url='https://github.com/digipodium/dputils',
    packages=find_packages(),
    install_requires=[
        'docx2txt>=0.8',
        'pdfminer.six>=20220524',
        'fpdf2>=2.5.4',
        'bs4>=0.0.1',
        'python-docx>=0.8.11',
        'httpx[http2]>=0.25.1',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)