
import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
setup(
  name="shopee_wrapper",
  version="0.2",
  description="Library that wrap shopee.co.id api using http.client",
  long_description=README,
  long_description_content_type="text/markdown",
  author="Hariz Sufyan Munawar",
  author_email="munawarhariz@gmail.com",
  license="Apache License",
  packages=["shopee_wrapper"],
  zip_safe=False,
)