import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="speedo",
    version="0.0.1",
    author="znstrider",
    author_email="mindfulstrider@gmail.com",
    description="Class to make speedometer plots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/znstrider/speedo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Matplotlib",
        "Topic :: Scientific/Engineering :: Visualization"
    ],
    python_requires='>=3.6',
)
