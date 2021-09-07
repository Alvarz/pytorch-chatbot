import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytorch_chatbot",
    version="0.0.1",
    author="Carlos Alvarez",
    author_email="carlosxviii@gmail.com",
    description="A pytorch based contextual chatbot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Bebop-robot/pytorch-chatbot",
    project_urls={
        "Bug Tracker": "https://github.com/Bebop-robot/pytorch-chatbot/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)
