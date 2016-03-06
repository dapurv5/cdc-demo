# es-scripts


### Data Sources
- https://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/DE_Syn_PUF.html


gen_docs.py (to generate documents from raw data)
gen_codes.py (generates a file which contains sorted list of all diagnostic codes)
gen_code_embeddings.py (generates a file with vector representation for each of the code)

update_docs.py (reads code embeddings and the documents and indexes them in es along with metadata)


gen_code_products.py (generates products of vector representations of all pairs of codes)