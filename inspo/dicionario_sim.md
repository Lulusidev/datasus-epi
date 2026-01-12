1
TTAABBEELLAA:: DDOO
Os campos pintados em azul são campos novos da declaração de óbitos (DO)
Nome da coluna no
arquivo DBF
Nome da variáveis no
Tabwin
Nome do arquivo
CNV Tipo Tam Descrição
NUMERODO ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 8 Número da DO
NUMERODV ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 1 Número do Dígito Verificador
CODESTCART ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 7 Código da UF do cartório
CODMUNCART ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 7 Código do município do cartório
CODCART ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 8 Código do cartório
NUMREGCART ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 8 Número do registro do cartório
DTREGCART ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 8 Data do registro do cartório: dd mm aaaa
TIPOBITO Tipo Óbito TIPOBITO.CNV Caracter 1 Tipo do óbito: 1 – fetal; 2‐ não fetal.
DTOBITO Ano do Óbito ANO.CNV Caracter 8 Data do óbito: dd mm aaaa
Mês do Óbito MESES.CNV
HORAOBITO ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 5 Horário do óbito
NUMSUS ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 15 Número do cartão SUS
NATURAL Naturalidade NATURAL.CNV Caractere 3 Naturalidade
Naturalidade NAT1212.CNV
NOME ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 50 Nome do falecido
NOMEPAI ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 45 Nome do pai do falecido
NOMEMAE ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 45 Nome da mãe do falecido
DTNASC ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 8 Data do nascimento: dd mm aaaa
IDADE
Faixa Etária (13) FXIDADP.CNV
Caracter 3
Idade: composto de dois subcampos. O primeiro, de 1 dígito, indica
a unidade da idade, conforme a tabela a seguir. O segundo, de dois
dígitos, indica a quantidade de unidades: 0 – Idade menor de 1
hora, o subcampo varia de 01 e 59; 1 – Hora, o subcampo varia de
01 a 23; 2 – Dias, o subcampo varia de 01 a 29; 3 – Meses, o
subcampo varia de 01 a 11; 4 – Anos, o subcampo varia de 00 a 99;
5 – Anos (mais de 100 anos), o segundo subcampo varia de 0 a 99.
Faixa Etária (5) FXIDAD5.CNV
Faixa Etária (9) FXIDAD9.CNV
Faixa Etária OMS FXIDAWHO.CNV
Faixa Etária pad(5‐5) FXIDADP5.CNV
Fx.Etar.Infant.1 FXINFAN1.CNV
Fx.Etar.Infant.2 FXINFAN2.CNV
Idade Detalhada IDADE.CNV
SEXO Sexo SEXOC.CNV Caracter 1 Sexo: M – masculino; F – feminino; I ignorado.
RACACOR Raça/Cor RACA.CNV Caracter 1 Raça: 1 – Branca; 2 – Preta; 3 – Amarela; 4 – Parda; 5 – Indígena.
ESTCIV Estado Civil ESTCIV.CNV Caracter 1 Situação conjugal: 1 – Solteiro; 2 – Casado; 3 – Viúvo; 4 – Separado
judicialmente/divorciado; 5 – União estável; 9 – Ignorado.
ESC Grau de Instrução INSTRUC.CNV Caracter 1 Escolaridade em anos. Valores: 1 – Nenhuma; 2 – de 1 a 3 anos; 3 –
de 4 a 7 anos; 4 – de 8 a 11 anos; 5 – 12 anos e mais; 9 – Ignorado.
OCUP
Oc Gr Sist Antigo GRUPOCUP.CNV
Caracter 6 Ocupação habitual e ramo de atividade
Oc Subgrupo Princ GRUPO2.CNV
Ocup Grande Grupo GRUPO1.CNV
Ocup Sist Antigo OCUPA.CNV
Ocup Subgrupo 3d GRUPO3.CNV
Ocupac Familia 4d GRUPO4.CNV
Ocupacao CBO2002.CNV
CODESTRES ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 7 Código da UF de residência
CODMUNRES
Capital Res CAPITAIS.CNV
Caracter 7 Código do município de residência
Munic Res ‐ BRA MUNICBR.CNV
Munic Resid ‐ AC MUNICAC.CNV
Munic Resid ‐ AL MUNICAL.CNV
2
Munic Resid ‐ AM MUNICAM.CNV
Munic Resid ‐ AP MUNICAP.CNV
Munic Resid ‐ BA MUNICBA.CNV
Munic Resid ‐ CE MUNICCE.CNV
Munic Resid ‐ ES MUNICES.CNV
Munic Resid ‐ GO MUNICGO.CNV
Munic Resid ‐ MA MUNICMA.CNV
Munic Resid ‐ MG MUNICMG.CNV
Munic Resid ‐ MS MUNICMS.CNV
Munic Resid ‐ MT MUNICMT.CNV
Munic Resid ‐ PA MUNICPA.CNV
Munic Resid ‐ PB MUNICPB.CNV
Munic Resid ‐ PE MUNICPE.CNV
Munic Resid ‐ PI MUNICPI.CNV
Munic Resid ‐ PR MUNICPR.CNV
Munic Resid ‐ RJ MUNICRJ.CNV
Munic Resid ‐ RN MUNICRN.CNV
Munic Resid ‐ RO MUNICRO.CNV
Munic Resid ‐ RR MUNICRR.CNV
Munic Resid ‐ RS MUNICRS.CNV
Munic Resid ‐ SC MUNICSC.CNV
Munic Resid ‐ SE MUNICSE.CNV
Munic Resid ‐ SP MUNICSP.CNV
Munic Resid ‐ TO MUNICTO.CNV
Regiao Res REGIAO.CNV
RegMetr Res‐BR REGIAOC.CNV
UF Res Sigla RMETRBR.CNV
UF Resid UFC.CNV
UF Resid/Regiao UFREG.CNV
UF Residencia UFC.CNV
UF/Regiao UFREG.CNV
BAIRES ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 30 Bairro de residência
CODBAIRES ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 8 Código do bairro de residência
CODENDRES ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 12 Código do endereço de residência
ENDRES ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 40 Endereço de residência
CODREGRES ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 7 Código da região de residência
NUMRES ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 10 Número da residência
COMPLRES ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 40 Complemento da residência
CEPRES ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 8 Código de endereçamento postal
CODDISRES ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 8 Código do distrito de residência
CODPAISRES ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 8 Código do país de residência
LOCOCOR Local Ocorrencia LOCOCOR.CNV Caracter 1
Local de ocorrência do óbito: 1 – hospital; 2 – outros
estabelecimentos de saúde; 3 – domicílio; 4 – via pública; 5 –
outros; 9 – ignorado.
CODESTAB
Esfera Adm 2006 ESFERA.cnv
Caracter 8 Código de estabelecimentoEstab Saude 2006 ESTAB06.CNV
Natur Organiz 2006 NAT_ORG.CNV
CODESTOCOR ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 7 Código de estabelecimento de ocorrência
CODMUNOCOR Capital Ocor CAPITAIS.CNV Caracter 8 Código do município de ocorrência
Munic Ocor ‐ BRA MUNICAC.CNV
3
Munic Ocorr ‐ AC MUNICAL.CNV
Munic Ocorr ‐ AL MUNICAM.CNV
Munic Ocorr ‐ AM MUNICAP.CNV
Munic Ocorr ‐ AP MUNICBA.CNV
Munic Ocorr ‐ BA MUNICBR.CNV
Munic Ocorr ‐ CE MUNICCE.CNV
Munic Ocorr ‐ ES MUNICGO.CNV
Munic Ocorr ‐ GO MUNICMA.CNV
Munic Ocorr ‐ MA MUNICMG.CNV
Munic Ocorr ‐ MG MUNICMS.CNV
Munic Ocorr ‐ MS MUNICMT.CNV
Munic Ocorr ‐ MT MUNICPA.CNV
Munic Ocorr ‐ PA MUNICPB.CNV
Munic Ocorr ‐ PB MUNICPE.CNV
Munic Ocorr ‐ PE MUNICPI.CNV
Munic Ocorr ‐ PI MUNICPR.CNV
Munic Ocorr ‐ PR MUNICRJ.CNV
Munic Ocorr ‐ RJ MUNICRN.CNV
Munic Ocorr ‐ RN MUNICRO.CNV
Munic Ocorr ‐ RO MUNICRR.CNV
Munic Ocorr ‐ RR MUNICRS.CNV
Munic Ocorr ‐ RS MUNICSC.CNV
Munic Ocorr ‐ SC MUNICSE.CNV
Munic Ocorr ‐ SE MUNICSP.CNV
Munic Ocorr ‐ SP MUNICTO.CNV
Munic Ocorr ‐ TO REGIAO.CNV
Regiao Ocor REGIAOC.CNV
RegMetr Ocor‐BR RMETRBR.CNV
UF Ocor UF.CNV
BAIOCOR ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 20 Bairro de ocorrência
CODBAIOCOR ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 8 Código do bairro de ocorrência
ENDOCOR ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 20 Endereço de ocorrência
CODENDOCOR ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 12 Código do endereço de ocorrência
CODREGOCOR ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 7 Código da região de ocorrência
NUMENDOCOR ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 10 Número do endereço de ocorrência
COMPLOCOR ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 10 Complemento do endereço de ocorrência
CEPOCOR ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 8 CEP do endereço de ocorrência
CODDISOCOR ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 8 Código do distrito de ocorrência
IDADEMAE Idade Mãe IDADEMA.CNV Caracter 2 Idade da mãe
ESCMAE Escolaridade Mãe INSTRUC.CNV Caracter 1 Escolaridade em anos. Valores: 1 – Nenhuma; 2 – de 1 a 3 anos; 3 –
de 4 a 7 anos; 4 – de 8 a 11 anos; 5 – 12 anos e mais; 9 – Ignorado.
OCUPMAE Ocupação Mãe CBO2002.CNV Caracter 6 Ocupação da mãe
QTDFILVIVO Filhos Vivos FILTIDO.CNV Caracter 2 Número de filhos vivos
QTDFILMORT Filhos Mortos FILTIDO.CNV Caracter 2 Número de filhos mortos
GRAVIDEZ Gravidez GRAVIDEZ.CNV Caracter 1 Informar o tipo de gravidez: 1 – única; 2 – dupla; 3 – tripla e mais; 9
– ignorada.
GESTACAO Semanas Gestação SEMANAS.CNV Caracter 1
Faixa de semanas de gestação: 1 – Menos 22 semanas; 2 – 22 a 27
semanas; 3 – 28 a 31 semanas; 4 – 32 a 36 semanas; 5 – 37 a 41
semanas; 6 – 42 e + semanas.
PARTO Tipo Parto PARTO.CNV Caracter 1 Informar o tipo de parto: 1 – vaginal; 2 – cesáreo; 9 – ignorado.
OBITOPARTO Obito Parto OPARTO.CNV Caracter 1 Informar como foi a morte em relação ao parto: 1 – antes; 2 –
durante; 3 – depois; 9 – Ignorado.
PESO Peso Nascer PESO.CNV Caracter 4 Peso ao nascer em gramas
NUMERODN ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 8 Número da Declaração de Nascido Vivo
OBITOGRAV Obito na Gravidez OBITOGRA.CNV Caracter 1 Óbito na gravidez: 1 – sim; 2 – não; 9 – ignorado.
4
OBITOPUERP Obito no Puerp OBITOPUE.CNV Caracter 1 Óbito no puerpério: 1 – Sim, até 42 dias após o parto; 2 – Sim, de
43 dias a 1 ano; 3 – Não; 9 – Ignorado.
ASSISTMED Assist Medica ASSMEDIC.CNV Caracter 1 Assistência médica: 1 – sim; 2 – não; 9 – ignorado.
EXAME Exame complem EXAME.CNV Caracter 1 Exame: 1 – sim; 2 – não; 9 – ignorado.
CIRURGIA Cirurgia CIRURGIA.CNV Caracter 1 Cirurgia: 1 – sim; 2 – não; 9 – ignorado.
NECROPSIA Necropsia NECROPS.CNV Caracter 1 Confirmação do diagnóstico por necrópsia: 1 – sim; 2 – não; 9 –
ignorado.
LINHAA ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 20 CIDs informados na Linha A da DO
LINHAB ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 20 CIDs informados na Linha B da DO
LINHAC ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 20 CIDs informados na Linha C da DO
LINHAD ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 20 CIDs informados na Linha D da DO
LINHAII ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 30 CIDs informados na Parte II da DO
DSTEMPO ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 10 Tempo de duração dos CIDs informados
CAUSABAS
Acid transp GRP actragrp.CNV
Caracter 4 Causa básica da DO
C nao Codificadas CAUSABRA.CNV
Causa (Cap CID10) CID10CAC.CNV
‐‐‐‐‐‐‐‐‐‐‐‐ CID10CAP.CNV
Causa (CID10 3C) CID10_3D.CNV
Causa (CID10 BR) CID10_BR.CNV
‐‐‐‐‐‐‐‐‐‐‐‐ CID10BR.CNV
Causa (CID10 CAP) CID10CAP.CNV
causa inval cinvalid.cnv
Causas Determin CID10L.CNV
Causas presumiveis CAUPRESU.CNV
CID10 4C Cap 01 CID10_01.CNV
CID10 4C Cap 02 CID10_02.CNV
CID10 4C Cap 03 CID10_03.CNV
CID10 4C Cap 04 CID10_04.CNV
CID10 4C Cap 05 CID10_05.CNV
CID10 4C Cap 06 CID10_06.CNV
CID10 4C Cap 07 CID10_07.CNV
CID10 4C Cap 08 CID10_08.CNV
CID10 4C Cap 09 CID10_09.CNV
CID10 4C Cap 10 CID10_10.CNV
CID10 4C Cap 11 CID10_11.CNV
CID10 4C Cap 12 CID10_12.CNV
CID10 4C Cap 13 CID10_13.CNV
CID10 4C Cap 14 CID10_14.CNV
CID10 4C Cap 15 CID10_15.CNV
CID10 4C Cap 16 CID10_16.CNV
CID10 4C Cap 17 CID10_17.CNV
CID10 4C Cap 18 CID10_18.CNV
CID10 4C Cap 20 CID10_20.CNV
D Isquem Coracao ISQUEM.CNV
Homicidios HOMICID.CNV
Imunopreviniveis CAUMEN.CNV
Neoplasias NEOPLA.CNV
Presumiveis caupresu0509.cnv
Suicidios SUICID.CNV
DSEXPLICA ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 20 Descrição da explicação das regras de seleção da causa básica
MEDICO ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 10 Nome do médico
CRM ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 15 Nº do CRM
TPASSINA ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 1 ‐‐‐‐‐‐‐‐‐‐‐‐
CONTATO ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 10 Meio de contato do atestante (telefone, fax, email etc.).
DTATESTADO ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 8 Data do atestado: dd mm aaaa
CIRCOBITO Tipo de Violencia TIPOVIOL.CNV Caracter 1 Indicar qual foi a provável circunstância de morte não natural: 1 –
acidente; 2 – suicídio; 3 – homicídio; 4 – outros; 9 – ignorado.
5
ACIDTRAB Acid Trabalho ACIDTRAB.CNV Caracter 1 Indicar se foi acidente de trabalho: 1 – sim; 2 – não; 9 – ignorado.
FONTE Fonte Informac FONTINFO.CNV Caracter 1 Indicar a fonte da informação, conforme a tabela: 1 – boletim de
ocorrência; 2 – hospital; 3 – família; 4 – outra; 9 – ignorado.
DSEVENTO ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 10 Descrição sumária do acidente
ENDACID ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 10 Endereço do acidente
NUMEROLOTE ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 8 Número do lote
TPPOS Obito investigado INVESTIG.CNV Caracter 1 Óbito investigado: 1 – sim; 2 – não.
DTINVESTIG Mes de Investigac MESES.CNV Caracter 8 Data da investigação: dd mm aaaa
LINHAA_O ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 20 CIDs informados, originalmente, na Linha A da DO.
LINHAB_O ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 20 CIDs informados, originalmente, na Linha B da DO.
LINHAC_O ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 20 CIDs informados, originalmente, na Linha C da DO.
LINHAD_O ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 20 CIDs informados, originalmente, na Linha D da DO.
LINHAII_O ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 20 CIDs informados, originalmente, na Parte II da DO.
CAUSABAS_O Causa Orig Capit CID10CAP.CNV Caracter 4 Causa básica Original
Causa Original CID10_3D.CNV
DTCADASTRO Ano do Cadastro ANO.CNV Caracter 8 Data do cadastro: dd mm aaaa
Mes do Cadastro MESES.CNV
ATESTANTE Medico Atest ATESTANT.CNV Caracter 1 Indica se o médico que assina atendeu o paciente: 1 – Sim; 2 –
Substituto; 3 – IML; 4 – SVO; 5 – Outros.
DESCACID ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 20 Descrição do acidente
CODENDACID ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 6 Código de endereço do acidente
NUMENDACID ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 6 Número do endereço do acidente
COMPLACID ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 20 Complemento do endereço onde ocorreu o acidente
CEPACID ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 8 CEP do endereço do acidente
CONFPESO ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 1 ‐‐‐‐‐‐‐‐‐‐‐‐
CONFIDADE ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 1 ‐‐‐‐‐‐‐‐‐‐‐‐
CONFCAUSA ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 1 ‐‐‐‐‐‐‐‐‐‐‐‐
CONFCIDADE ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 1 ‐‐‐‐‐‐‐‐‐‐‐‐
CRITICA ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 2 ‐‐‐‐‐‐‐‐‐‐‐‐
CODINST
Instalacao CODINST.CNV Caracter
18
Código de configuração da instalação: – 1º caractere: nível de
instalação (M – municipal; R – regional; E – estadual); – 2º e 3º
caractere: UF de instalação; – 4º ao 9º caractere: código do
município de instalação; – 10º ao 13º caractere: nº da máquina de
instalação.
Munic Instal MUNICBR.CNV
MunicInst 1172 MUNICBRd.CNV
Numero Micro MICRO.CNV
UF Instal UFC.CNV
STCODIFICA Com Codificador CODIFICA.CNV Caracter 1 Status de instalação: se codificadora (valor: S) ou não (valor: N)
CODIFICADO Codificado CODIFICADO.CNV Caracter 1 Se estiver codificado (valor: S) ou não (valor: N)
VERSAOSIST Versão Sistema VERSAO.CNV Caracter 7 Versão do sistema
VERSAOSCB Versão SCB VERSCB.CNV Caracter 7 Versão do seletor de causa básica
RETROALIM Retroalimentacao RETRO.CNV Caracter 1 Retroalimentação
FONTEINV Fonte Investig FONTEINV.CNV Caracter 8
Fonte de investigação. Valores: 1 – Comitê de Morte Materna e/ou
Infantil; 2 – Visita domiciliar / Entrevista família; 3 –
Estabelecimento de Saúde / Prontuário; 4 – Relacionado com
outros bancos de dados; 5 – S V O; 6 – I M L; 7 – Outra fonte; 8 –
Múltiplas fontes; 9 – Ignorado.
DTRECEBIM Ano do recebimento ANO.CNV
Caracter 8 Data do recebimento: dd mm aaaaDia do recebimento DIAS.CNV
Mes do recebimento MESES.CNV
ATESTADO ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 50 CIDs informado no atestado
CAUSABAS_R Causa (Cap CID10 R) CID10CAC.CNV Caracter 4 Causa básica resselecionada
Causa (CID10 3C R) CID10_3DN.CNV
6
Causa (CID10 BR R) CID10_BR.CNV
Causa (CID10CAP R) CID10CAP.CNV
DTRESSELE
Ano Resselecao ANO.CNV
Caracter 8 Data da resseleção: dd mm aaaaDIA Resselecao DIAS.CNV
Mes Resselecao MESES.CNV
STRESSELE StatusRessel S N SIMNAO.CNV Caracter 1 Status da resseleção: 1 – sim; 2 – não.
EXPLICA_R ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 50 Explicação das regras de resseleção de causa básica
VRSRESSELE Versão Resselec VERSCB.CNV Caracter 7 Versão de resseleção
NRESSELE ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 50 Descrição da explicação da não resseleção da causa básica.
COMPARA_CB RESEL1.CNV Caracter 8 Compara causa básica resselecionada com a informada. Valores:
IGUAL, DIFER.
CB_PRE Causa(Cap CID10pre) CID10CAC.CNV Caracter 4 Causa básica informada antes da resseleção (NRESSELE)
Causa(CID10 BRpre) CID10_BR.CNV
Causa(CID103C pre) CID10_3D.CNV
Causa(CID10CAPpre) CID10CAP.CNV
NPROC Motivo N RESSELEC NPROC.CNV Caracter 2
Códigos da explicação da não resseleção da causa básica. Valores:
1 – Depende de perguntas; 2 – Causa externa; 3 – Procedimento
médico; 4 – Causa básica por CID de paralisia; 5 – Regra F; 6 – CID
temporário não pode ser causa básica.
DIFDATA Dias obt 1o receb difdata.cnv Caracter 8 Diferença entre a data de óbito e data do recebimento original da
DO ([DTOBITO] – [DTRECORIG])
Oport notif (30d) dias_notif.cnv
VERSCBPRE Versão Scb_Pre VERSCB.CNV Caracter 7 Versão do SCB da resseleção
DTRECORIG
Ano 1º Recebimento ANO.CNV
Caracter 8 Data do recebimento original: dd mm aaaaDia 1º Recebimento DIAS.CNV
Mes 1º Recebimento MESES.CNV
ESC2010 Escol series ESCSERIE.CNV Caracter 1
Escolaridade 2010. Valores: 0 – Sem escolaridade; 1 – Fundamental
I (1ª a 4ª série); 2 – Fundamental II (5ª a 8ª série); 3 – Médio
(antigo 2º Grau); 4 – Superior incompleto; 5 – Superior completo; 9
– Ignorado.
SERIESCFAL ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 1 Série escolar do falecido. Valores de 1 a 8.
ESCMAE2010 Esc Mae series ESCSERIE.CNV Caracter 1
Escolaridade 2010. Valores: 0 – Sem escolaridade; 1 – Fundamental
I (1ª a 4ª série); 2 – Fundamental II (5ª a 8ª série); 3 – Médio
(antigo 2º Grau); 4 – Superior incompleto; 5 – Superior completo; 9
– Ignorado.
SERIESCMAE ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 1 Série escolar da mãe. Valores de 1 a 8.
SEMAGESTAC Gestac Detalhada SGESTAC.CNV Caracter 3 Semanas de gestação
TPMORTEOCO Ob Mulher id Fert TPMORTEOCO Caracter 1
Informar quando a morte ocorreu: 1 – na gravidez; 2 – no parto; 3
– no aborto; 4 – até 42 dias após o parto; 5 – de 43 dias a 1 ano
após o parto; 8 – não ocorreu nestes períodos; 9 – ignorado.
COMUNSVOIM Munic IML/SVO MUNICBR.CNV Caracter 7 Código do município do SVO ou do IML
CODMUNNATU Munic Naturalid MUNICBR.CNV Caracter 7 Código do município de naturalidade do falecido
CAUSAMAT Causa mat Associada ST_MAT.CNV Caracter 4 Causa externa associada a uma causa materna
Matern Assoc C Ext CAUSAMAT.CNV
7
ESCMAEAGR1 Esc Mae ser agreg ESCAGR1.CNV Caracter 2
Escolaridade 2010 agregada. Valores: 00 – Sem Escolaridade; 01 –
Fundamental I Incompleto; 02 – Fundamental I Completo; 03 –
Fundamental II Incompleto; 04 – Fundamental II Completo; 05 –
Ensino Médio Incompleto; 06 – Ensino Médio Completo; 07 –
Superior Incompleto; 08 – Superior Completo; 09 – Ignorado; 10 –
Fundamental I Incompleto ou Inespecífico; 11 – Fundamental II
Incompleto ou Inespecífico; 12 – Ensino Médio Incompleto ou
Inespecífico.
ESCMAEAGR2 ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 1 Escolaridade em anos. Valores: 1 – Nenhuma; 2 – de 1 a 3 anos; 3 –
de 4 a 7 anos; 4 – de 8 a 11 anos; 5 – 12 anos e mais; 9 – Ignorado.
ESCFALAGR1 Escol series agreg ESCAGR1.CNV Caracter 2
Escolaridade 2010 agregada. Valores: 00 – Sem Escolaridade; 01 –
Fundamental I Incompleto; 02 – Fundamental I Completo; 03 –
Fundamental II Incompleto; 04 – Fundamental II Completo; 05 –
Ensino Médio Incompleto; 06 – Ensino Médio Completo; 07 –
Superior Incompleto; 08 – Superior Completo; 09 – Ignorado; 10 –
Fundamental I Incompleto ou Inespecífico; 11 – Fundamental II
Incompleto ou Inespecífico; 12 – Ensino Médio Incompleto ou
Inespecífico.
ESCFALAGR2 ‐‐‐‐‐‐‐‐‐‐‐‐ ‐‐‐‐‐‐‐‐‐‐‐‐ Caracter 1 Escolaridade em anos. Valores: 1 – Nenhuma; 2 – de 1 a 3 anos; 3 –
de 4 a 7 anos; 4 – de 8 a 11 anos; 5 – 12 anos e mais; 9 – Ignorado.
STDOEPIDEM DO epidemiologica DONOVA.CNV Caracter 1 Status de DO Epidemiológica. Valores: 1 – SIM; 0 – NÃO.
STDONOVA DO novo modelo DONOVA.CNV Caracter 1 Status de DO Nova. Valores: 1 – SIM; 0 – NÃO.