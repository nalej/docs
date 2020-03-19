from setuptools import find_packages, setup

setup(
    name='nalej-docs',
    version='0.5.0',
    author='Nalej',
    author_email='hello@nalej.com',
    description=('Documentation for the Nalej Platform'),
    long_description=get_readme(),
    long_description_content_type='text/markdown',  # Optional (see note above)

    license='BSD',
    keywords='nalej edge computing documentation',
    url='',
    packages=find_packages(),
    install_requires=[
        'markdown==2.6.5',
        'mkdocs-windmill'],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

    ],
    # Specify which Python versions you support. In contrast to the
    # 'Programming Language' classifiers above, 'pip install' will check this
    # and refuse to install the project if the version does not match. If you
    # do not support Python 2, you can simplify this to '>=3.5' or similar, see
    # https://packaging.python.org/guides/distributing-packages-using-setuptools/#python-requires
    python_requires='>=2.7',

)