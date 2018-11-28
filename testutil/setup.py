from setuptools import setup, find_packages

setup(
    name='testutil-python',
    version='1.0',
    packages=['', 'common', 'pymeter', 'telnet', 'file_io', 'pyedis'],
    package_dir={'': 'testutil'},
    url='F:/Testing/testutil-python',
    license='',
    author='KelvinYe',
    author_email='',
    description='测试共用工具模块', install_requires=['fire']
)
