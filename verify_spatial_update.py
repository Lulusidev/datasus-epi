
import sys
import os

# Add the project root to sys.path
sys.path.append(os.getcwd())

from api.analysis.spatial import obter_geometria_municipios, juntar_com_geometria
import inspect

def check_signature():
    print("Checking obter_geometria_municipios signature...")
    sig = inspect.signature(obter_geometria_municipios)
    print(sig)
    assert 'uf' in sig.parameters, "uf parameter missing in obter_geometria_municipios"
    
    print("Checking juntar_com_geometria signature...")
    sig = inspect.signature(juntar_com_geometria)
    print(sig)
    assert 'uf' in sig.parameters, "uf parameter missing in juntar_com_geometria"
    
    print("Verification successful!")

if __name__ == "__main__":
    check_signature()
