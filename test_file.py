from datapackage_attrs.generate import generate_attrs

simple_path = "/Users/mjr/Documents/code/libraries/frictionless/datapackage-attrs/test_simple_schema.json"

Simple = generate_attrs("Simple", simple_path, "A simple tableschema")

simple: Simple = Simple(bar="fooo")
