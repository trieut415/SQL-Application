from setuptools import setup, find_packages

setup(
    name="chat_sql_assistant",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai",
        "pandas"
    ],
    entry_points={
        "console_scripts": [
            "chat-sql=main:main"
        ]
    },
    author="Trieu Tran",
    description="A natural language to SQL assistant for SQLite databases.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
