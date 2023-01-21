
import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
setup(
  name="shopee_scraper",
  version="0.1",
  description="Library that wrap shopee.co.id api using http.client",
  long_description=README,
  long_description_content_type="text/markdown",
  author="Hariz Sufyan Munawar",
  author_email="munawarhariz@gmail.com",
  license="Apache License",
  packages=["wrapper"],
  zip_safe=False,
)