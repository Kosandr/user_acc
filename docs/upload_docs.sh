#!/bin/bash

rm -r source/autoapidoc build/html

sphinx-apidoc -o source/autoapidoc ..
make html
rm -r /sec/web/tmp/dbt_docs_acc
mv build/html/ /sec/web/tmp/dbt_docs_acc/

