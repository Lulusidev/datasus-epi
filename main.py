from scripts.taxas import obter_taxa_sinasc

def main():
    resultado = obter_taxa_sinasc(
        anos=[2020, 2021],
        cid="Q20",
        tempo="ano",
        estratos=["UFINFORM"]
    )
    print(resultado)

if __name__ == "__main__":
    main()
