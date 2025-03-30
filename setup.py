from setuptools import setup, find_packages

setup(
    name='pivotea',
    version="0.1.1",
    description="Create Pivot Table Easily",
    author='Toshikazu Matsumura',
    packages=find_packages(),
    license='MIT',
    install_requires=["pandas"],
    entry_points={
        "console_scripts": [
            "pivot = pivoteapy.pivot:pivot"
        ],
        "gui_scripts": [
            "pivot = pivoteapy.pivot:pivot"
        ]
    }
)
