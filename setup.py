from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='qdrant-vector-aggregator',
    version='1.0.1',
    description='Aggregate embeddings in Qdrant collections with smart content concatenation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Moudather Chelbi',
    author_email='moudather.chelbi@gmail.com',
    url='https://github.com/vinerya/qdrant_vector_aggregator',
    project_urls={
        'Bug Tracker': 'https://github.com/vinerya/qdrant_vector_aggregator/issues',
        'Documentation': 'https://github.com/vinerya/qdrant_vector_aggregator#readme',
        'Source Code': 'https://github.com/vinerya/qdrant_vector_aggregator',
    },
    packages=find_packages(exclude=['tests*', 'examples*']),
    install_requires=[
        'qdrant-client>=1.7.0',
        'numpy>=1.21.0',
        'scipy>=1.7.0',
        'scikit-learn>=1.0.0',
        'python-dotenv>=0.19.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'black>=22.0.0',
            'flake8>=5.0.0',
            'mypy>=0.990',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Database',
    ],
    keywords='qdrant vector embeddings aggregation semantic-search nlp machine-learning',
    python_requires='>=3.7',
    license='MIT',
)
