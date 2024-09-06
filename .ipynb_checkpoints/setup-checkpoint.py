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

import ollama  # Certifique-se de que a biblioteca está corretamente importada

def model_exists(model_name):
    # Obtém a lista de modelos
    models = ollama.list().get('models', [])
    
    # Verifica se o modelo desejado está na lista
    for model in models:
        if model_name in model['name']:
            return True
    return False

# Nome do modelo a ser verificado
model_name = 'llama3.1'

if model_exists(model_name):
    print(f"Modelo {model_name} está disponível.")
else:
    print(f"Modelo {model_name} não encontrado.")
    ollama.pull(model_name)
    
    