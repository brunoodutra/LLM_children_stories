from setuptools import setup
from setuptools.command.install import install
import subprocess

class CustomInstallCommand(install):
    def run(self):
        # Executa o script de instalação do Ollama
        subprocess.check_call(['./install_ollama.sh'])
        install.run(self)

setup(
    name='my_app',
    version='1.0',
    description='Minha Aplicação Streamlit',
    cmdclass={'install': CustomInstallCommand},
)
