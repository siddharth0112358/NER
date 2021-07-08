# Run following commands in coomandline to run scispacy on virtual env
# Run as a python file and not in jupyter notebook - and never in jupyter
# !python3 -m venv env
# !source env/bin/activate
# !pip install scispacy
# !pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.4.0/en_core_sci_sm-0.4.0.tar.gz
# !pip install --no-binary :all: nmslib
# !pip install --upgrade pip
# !deactivate

from scispacy.linking import EntityLinker
import scispacy
from scispacy.abbreviation import AbbreviationDetector
from scispacy.umls_linking import UmlsEntityLinker
import spacy
nlp = spacy.load("en_core_sci_sm")
doc = nlp("Alterations in the hypocretin receptor 2 and preprohypocretin genes produce narcolepsy in some animals.")


# nlp = spacy.load("en_core_sci_sm")

# Add the abbreviation pipe to the spacy pipeline.
nlp.add_pipe("abbreviation_detector")

doc = nlp("Spinal and bulbar muscular atrophy (SBMA) is an \
           inherited motor neuron disease caused by the expansion \
           of a polyglutamine tract within the androgen receptor (AR). \
           SBMA can be caused by this easily.")

print("Abbreviation", "\t", "Definition")
for abrv in doc._.abbreviations:
	print(f"{abrv} \t ({abrv.start}, {abrv.end}) {abrv._.long_form}")


# nlp = spacy.load("en_core_sci_sm")

# # This line takes a while, because we have to download ~1GB of data
# # and load a large JSON file (the knowledge base). Be patient!
# # Thankfully it should be faster after the first time you use it, because
# # the downloads are cached.
# # NOTE: The resolve_abbreviations parameter is optional, and requires that
# # the AbbreviationDetector pipe has already been added to the pipeline. Adding
# # the AbbreviationDetector pipe and setting resolve_abbreviations to True means
# # that linking will only be performed on the long form of abbreviations.
# nlp.add_pipe("scispacy_linker", config={
#              "resolve_abbreviations": True, "name": "umls"})

# doc = nlp("Spinal and bulbar muscular atrophy (SBMA) is an \
#            inherited motor neuron disease caused by the expansion \
#            of a polyglutamine tract within the androgen receptor (AR). \
#            SBMA can be caused by this easily.")

# # Let's look at a random entity!
# entity = doc.ents[1]

# print("Name: ", entity)

# # Each entity is linked to UMLS with a score
# # (currently just char-3gram matching).
# linker = nlp.get_pipe("scispacy_linker")
# for umls_ent in entity._.kb_ents:
# 	print(linker.kb.cui_to_entity[umls_ent[0]])

nlp.add_pipe("scispacy_linker", config={
             "resolve_abbreviations": True, "name": "mesh"})

doc = nlp("Spinal and bulbar muscular atrophy (SBMA) is an \
           inherited motor neuron disease caused by the expansion \
           of a polyglutamine tract within the androgen receptor (AR). \
           SBMA can be caused by this easily.")

# Let's look at a random entity!
entity = doc.ents[1]

print("Name: ", entity)

# Each entity is linked to UMLS with a score
# (currently just char-3gram matching).
linker = nlp.get_pipe("scispacy_linker")
for umls_ent in entity._.kb_ents:
	print(linker.kb.cui_to_entity[umls_ent[0]])
