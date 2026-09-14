# Zenodo deposit checklist

1. Create a new Zenodo upload and select **Dataset**.
2. Upload `GC_TIDAL_MEMORY_REPRODUCIBILITY_PACKAGE_v1_0_0.zip`.
3. Use the title, creators, description, keywords, version, and license from
   `.zenodo.json`.
4. Confirm open access and CC BY 4.0 for the dataset/figures. The code files are
   separately marked MIT.
5. Do not add a manuscript file to this record.
6. Before publishing the record, inspect the file list and verify that no
   `main.tex`, manuscript PDF, journal style/class file, or historical
   `T6_LYAPUNOV_CHAOS_RAW_V1_0_3` file is present.
7. Publish the Zenodo record. Zenodo will assign the version DOI and concept DOI.
8. After the DOI exists, cite that DOI in the journal Data Availability section
   and, if desired, issue a metadata-only subsequent archive version containing
   the DOI in `CITATION.cff` and related identifiers.
