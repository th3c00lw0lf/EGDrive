from setuptools import setup


setup(
    name='EGDrive',
    version='0.1.2',
    author='th3c00lw0lf',
    author_email='business.mam@outlook.com',
    packages=['EGDrive'],
    url='https://github.com/th3c00lw0lf/EGDrive',
    license='LICENSE.txt',
    description='A Simplified Google Drive API.',
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    install_requires=[rq.strip()
                      for rq in open("requirements.txt", "r").readlines()],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Communications :: File Sharing",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
    ],
)
