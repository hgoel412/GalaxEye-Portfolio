cat > setup.py << 'EOF'
from setuptools import setup, find_packages

setup(
    name="galaxeye",
    version="1.0.0",
    description="Satellite constellation design for maritime surveillance",
    author="Harshit Goel",
    author_email="hgoel412@gmail.com",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.5.0",
        "numpy>=1.24.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "scipy>=1.11.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Astronomy",
        "License :: OSI Approved :: MIT License",
    ],
)
EOF
