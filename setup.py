from setuptools import setup
import codecs

def readme():
    with codecs.open('README.rst', 'r', encoding='utf-8') as f:
        return f.read()

setup(name='mapapi',
      version='0.1.2',
      description='map web api, current support baidu',
      long_description=readme(),
      keywords='map baidu',
      url='https://github.com/starplanet/mapapi',
      author='zhangjinjie',
      author_email='zhangjinjie@yimian.com.cn',
      license='MIT',
      packages=['mapapi', 'mapapi/baidu'],
      install_requires=[
          'requests',
      ],
      include_package_data=True,
      zip_safe=False)
