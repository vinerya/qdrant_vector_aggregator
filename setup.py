from setuptools import setup, find_packages

setup(
    name='qdrant_vector_aggregator',
    version='1.0.0',
    description='Advanced methods for aggregating multiple embeddings in Qdrant vector database',
    long_description=open('README_QDRANT.md').read(),
    long_description_content_type='text/markdown',
    author='Adapted for Qdrant',
    url='https://github.com/vinerya/faiss_vector_aggregator',
    packages=find_packages(),
    install_requires=[
        'qdrant-client>=1.7.0',
        'numpy>=1.21.0',
        'scipy>=1.7.0',
        'scikit-learn>=1.0.0',
        'python-dotenv>=0.19.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.8',
)
