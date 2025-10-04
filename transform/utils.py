import pandas as pd
import re

def desmembrar_endereco_petland(endereco_completo):
    try:
        if not isinstance(endereco_completo, str) or not endereco_completo.strip():
            return pd.Series(["", "", "", "", ""])
        
        e = endereco_completo.strip()
        e = re.sub(r"\s+", " ", e)
        e = e.replace("–", "-").replace("—", "-")
        e = e.replace(" ,", ",").replace(", ", ",").strip()

        # Extrai CEP, se existir
        cep_match = re.search(r"\d{5}-?\d{3}", e)
        cep = cep_match.group(0) if cep_match else ""
        if cep:
            e = e.replace(cep, "").strip(" ,–-")

        # Extrai estado (UF)
        estado_match = re.search(r"\b([A-Z]{2})\b", e[-10:])
        estado = estado_match.group(1) if estado_match else ""
        if estado:
            e = re.sub(r"[-/,]?\s*" + estado + r"$", "", e).strip(" ,–-")

        # Extrai cidade (palavras antes do estado)
        cidade = ""
        cidade_match = re.search(r"([A-ZÁÉÍÓÚÂÊÔÃÕÇa-záéíóúâêôãõç\s]+)[-/, ]*$", e)
        if cidade_match:
            cidade = cidade_match.group(1).strip()
            # Evita pegar bairro como cidade
            if len(cidade.split()) == 1 and cidade.lower() in ["centro", "jardim", "bairro"]:
                cidade = ""
            if cidade:
                e = e[:e.rfind(cidade)].strip(" ,–-")

        # Extrai bairro (se houver)
        bairro = ""
        bairro_match = re.search(r"[-,]\s*([A-ZÁÉÍÓÚÂÊÔÃÕÇa-záéíóúâêôãõç\s]+)$", e)
        if bairro_match:
            bairro = bairro_match.group(1).strip()
            if len(bairro.split()) > 4:  # se for muito longo, provavelmente inclui cidade
                bairro = ""
        
        # Remove bairro da string principal
        if bairro:
            e = re.sub(r"[-,]?\s*" + re.escape(bairro) + r"$", "", e).strip(" ,–-")

        # O que sobrar é a rua e número
        e = e.replace("nº", "").replace("n°", "").strip(" ,–-")
        rua = e

        return pd.Series([rua, bairro, cidade, estado, cep])
    
    except Exception as ex:
        print(f"Erro ao desmembrar '{endereco_completo}': {ex}")
        return pd.Series(["", "", "", "", ""])
    


def desmembrar_endereco_petlove(endereco_completo):
    try:
        partes = [p.strip() for p in endereco_completo.split(",")]
        
        # Rua
        rua = partes[0] if len(partes) > 0 else ""
        bairro = partes[1] if len(partes) > 1 else ""
        cidade_estado = partes[2] if len(partes) > 2 else ""
        cidade, estado = (cidade_estado.split("-") if "-" in cidade_estado else ("",""))
        cidade = cidade.strip()
        estado = estado.strip()
        cep = partes[3] if len(partes) > 3 else ""
        
        return pd.Series([rua, bairro, cidade, estado, cep])
    except Exception as e:
        print(f"Erro ao desmembrar '{endereco_completo}': {e}")
        return pd.Series(["","","","",""])