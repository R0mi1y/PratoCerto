import os
import shutil

def delete_python_cache(start_dir='./', skip_dirs=None):
    """
    Deleta todas as pastas __pycache__ e arquivos .pyc, ignorando diretórios especificados.
    
    Args:
        start_dir (str): Diretório inicial para busca (padrão: './')
        skip_dirs (list): Lista de diretórios para pular (ex: ['.git', 'venv'])
    """
    if skip_dirs is None:
        skip_dirs = []
    
    skip_dirs = [os.path.normpath(d) for d in skip_dirs]  # Normaliza os caminhos
    
    for root, dirs, files in os.walk(start_dir, topdown=True):
        # Remove diretórios da lista de busca se estiverem em skip_dirs
        dirs[:] = [d for d in dirs if os.path.normpath(os.path.join(root, d)) not in skip_dirs]
        
        # Deleta arquivos .pyc, .pyo e .pyd
        for file in files:
            if file.endswith(('.pyc', '.pyo', '.pyd')):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Arquivo deletado: {file_path}")
                except Exception as e:
                    print(f"Erro ao deletar {file_path}: {e}")

        # Deleta pastas __pycache__
        if '__pycache__' in dirs:
            cache_dir = os.path.join(root, '__pycache__')
            try:
                shutil.rmtree(cache_dir)
                print(f"Pasta deletada: {cache_dir}")
            except Exception as e:
                print(f"Erro ao deletar {cache_dir}: {e}")

if __name__ == '__main__':
    DIRETORIOS_PULAR = [
        '.git',
        '.venv',
        'venv',
        'env',
        'node_modules',
        'dist',
        'build',
    ]
    
    print("Limpando cache do Python...")
    delete_python_cache(start_dir='./', skip_dirs=DIRETORIOS_PULAR)
    print("Limpeza concluída!")