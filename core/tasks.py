from crewai import Task
class TasksAll(): 
    def extract_experiments_task(self, agent):
        return Task(
            
            description='''
            **OBJECTIVE**: Identify and extract ALL experiments (group comparisons) from the paper at {study_path}.
            
            **STEP-BY-STEP PROCESS**:
            
            1. **Search for Methods Section**:
                - Use the directory search tool to find "Methods", "Materials and Methods", or "Study Design"
                - Extract the full Methods section (if too long, chunk into 1000-word segments)
            
            2. **Search for Results Section**:
                - Find "Results" section
                - Look for subsections describing different analyses
            
            3. **Identify Study Design**:
                - Is this a case-control study? Cohort study? Intervention study?
                - What is the main condition/disease being studied?
                - What is the body site sampled?
            
            4. **Find ALL Group Comparisons**:
            Search for phrases like:
                - "patients with [condition] vs healthy controls"
                - "before treatment vs after treatment"
                - "high [symptom] group vs low [symptom] group"
                - "[condition] cases (n=X) and controls (n=Y)"
                - "stratified by [age/sex/severity]"
            
            5. **Extract Group Definitions**:
                For EACH comparison found, capture:

            a) **Group 0 (Control/Reference)**:
                    - Group name (exact label used in paper)
                    - Definition (diagnostic criteria, if available)
                    - Sample size (n=?)
            
            b) **Group 1 (Case/Exposed)**:
                    - Group name (exact label used in paper)
                    - Definition (FULL diagnostic criteria - thresholds, tools, inclusion criteria)
                    - Sample size (n=?)
            
            c) **Context**:
                    - Condition being studied (e.g., "Type 2 diabetes", "Infantile colic")
                    - Age range (if applicable)
                    - Statistical approach (crude, adjusted, covariate-adjusted)
                    - Subpopulation (e.g., "males only", "no antibiotics", "breastfed only")
                    - Timepoint (if longitudinal study)
            
            d) **Additional metadata**:
                    - Antibiotics exclusion criteria
                    - Any other exclusion criteria mentioned
            
            6. **Identify Multiple Experiments**:
                Look for evidence of multiple comparisons:
                - Different age groups analyzed separately
                - Sensitivity analyses (crude vs adjusted models)
                - Subgroup analyses (by sex, diet, medication status)
                - Multiple conditions tested (e.g., diabetes AND obesity)
                - Multiple timepoints (baseline, week 4, week 8)
            
            7. **Number Each Experiment**:
                - Assign sequential IDs (Experiment 1, 2, 3...)
                - Use logical ordering (main analyses first, then subgroups)
            
            **SEARCH QUERIES TO USE**:
            - "study population" OR "participants" OR "subjects"
            - "inclusion criteria" OR "exclusion criteria"
            - "case" AND "control"
            - "diagnostic criteria"
            - "[condition name]" AND "definition"
            - "statistical analysis" OR "statistical methods"
            - "subgroup" OR "stratified" OR "sensitivity analysis"
            
            **IMPORTANT NOTES**:
            - If the Methods section is >3000 words, process it in chunks
            - Pay attention to tables describing participant characteristics
            - Check figure legends for additional comparisons
            - Some experiments may only be mentioned in Results section
            - Look for supplementary methods for additional details
            
            **OUTPUT FORMAT**:
            Return a structured JSON with ALL experiments identified:
            ```json
                {
                "total_experiments": 28,
                "experiments": [
                    {
                    "experiment_id": 1,
                    "condition": "Constipation",
                    "group_0_name": "Low constipation >3d-crude (< 3months)",
                    "group_0_definition": "Infants <3 months with normal bowel movements",
                    "group_0_sample_size": 950,
                    "group_1_name": "High constipation > 3d-crude (< 3months)",
                    "group_1_definition": ">3 days without defecation in infants <3 months (full cohort)",
                    "group_1_sample_size": 114,
                    "age_range": "<3 months",
                    "statistical_approach": "crude model (unadjusted)",
                    "subpopulation": "full cohort",
                    "antibiotics_exclusion": "3 months",
                    "notes": "Primary analysis for constipation in youngest age group"
                    },
                    {
                    "experiment_id": 2,
                    "condition": "Functional abnormality of the gastrointestinal tract",
                    "group_0_name": "Low colic: wessel-crude (< 3months)",
                    "group_0_definition": "Infants <3 months not meeting Wessel's criteria",
                    "group_0_sample_size": null,
                    "group_1_name": "High colic: wessel-crude (< 3months)",
                    "group_1_definition": "Wessel's criteria applied to infants <3 months (Full cohort)",
                    "group_1_sample_size": null,
                    "age_range": "<3 months",
                    "statistical_approach": "crude model",
                    "subpopulation": "full cohort",
                    "antibiotics_exclusion": "3 months",
                    "notes": "Wessel's criteria = crying >3 hours/day, >3 days/week"
                    }
                    // ... continue for all experiments
                ],
                "extraction_metadata": {
                    "primary_experiments": 5,
                    "sensitivity_analyses": 10,
                    "subgroup_analyses": 13,
                    "confidence": "high",
                    "missing_data": ["sample sizes not reported for some subgroups"]
                }
                }
            ```
            ''',
            
            expected_output='''A complete JSON object containing ALL experiments identified 
            in the paper. Each experiment must include:
            - Unique experiment ID
            - Condition/phenotype studied
            - Both group names and definitions
            - Sample sizes (if available)
            - Context (age, statistical method, subpopulation)
            - Any relevant notes
            
            The output should clearly distinguish between primary experiments and 
            secondary/sensitivity analyses.''',
            
            agent=agent,            
            output_file='output/experiments.json'
        )
    
    
    
    def extract_signatures_task(self, agent):
        return Task(
            description='''
            **OBJECTIVE**: Extract ALL signatures (bacteria findings) for each experiment from the research paper at {study_path}.
            
            **STEP-BY-STEP PROCESS**:
            
            1. **Receive Experiment List**:
            - You will receive the list of experiments from the previous task
            - Each experiment has an ID and group definitions
            
            2. **Locate Data Sources** (Priority Order):
            
            **Priority 1: Supplementary Tables**
            - Search for "Supplementary Table", "Table S", "Additional file"
            - Look for files with extensions: .xlsx, .csv, .txt
            - Common table names: "Table S1", "Supplementary Data 1", "Additional Table 1"
            
            **Priority 2: Main Text Tables**
            - Search for "Table 1", "Table 2", etc.
            - Look for tables with bacterial names and statistical values
            
            **Priority 3: Figure Captions**
            - Search for "Figure 1", "Fig. 1", etc.
            - Extract captions that mention bacterial names
            
            **Priority 4: Results Text**
            - Search Results section for inline statistical findings
            - Look for patterns like "[Bacteria name] was significantly [increased/decreased]"
            
            3. **Process Each Data Source**:
            
            **For Tables**:
            a) Identify table structure:
                - Which column contains bacterial names?
                - Which column contains statistics (p-value, FDR, q-value)?
                - Which column shows direction/magnitude (fold-change, log2FC, coefficient)?
                - Which column indicates experiment/comparison?
            
            b) Extract significance indicators:
                - P-value < 0.05
                - FDR/q-value < 0.05
                - Asterisks (*) indicating significance
                - "significant" in text
            
            c) For each significant bacteria, extract:
                - Bacterial name (full taxonomic path if available)
                - Statistical values (p-value, fold-change, etc.)
                - Direction (increased/decreased in Group 1)
                - Which experiment this belongs to
            
            **For Figure Captions**:
            - Look for statements like:
                * "Bacteria enriched in [group]"
                * "[Bacteria] was significantly higher in [group]"
                * "Decreased abundance of [bacteria]"
            
            **For Results Text**:
            - Search for patterns:
                * "[Bacteria name] (p=0.XX)"
                * "[Bacteria] was significantly [higher/lower/enriched/depleted]"
                * "abundance of [bacteria] differed (p<0.05)"
            
            4. **Determine Direction of Change**:
            
            **INCREASED in Group 1** indicators:
            - Positive fold-change (>1)
            - Positive log2FC (>0)
            - Text: "enriched", "higher", "increased", "elevated", "more abundant"
            - Positive coefficient in regression
            
            **DECREASED in Group 1** indicators:
            - Negative fold-change (<1)
            - Negative log2FC (<0)
            - Text: "depleted", "lower", "decreased", "reduced", "less abundant"
            - Negative coefficient in regression
            
            5. **Extract Taxonomic Information**:
            - Identify taxonomic level:
                * Species: Two words (e.g., "Escherichia coli")
                * Genus: One word (e.g., "Bifidobacterium")
                * Family: Ends in -aceae (e.g., "Enterobacteriaceae")
                * Order: Ends in -ales (e.g., "Clostridiales")
                * Class: Ends in -ia (e.g., "Clostridia")
            
            - Handle full taxonomic paths:
                * "Bacteria;Firmicutes;Clostridia;Clostridiales;Lachnospiraceae;Roseburia"
                * Extract the LOWEST level: "Roseburia" (genus)
            
            6. **Map Signatures to Experiments**:
            - Use context clues to determine which experiment each signature belongs to:
                * Table/figure title mentions comparison
                * Column headers indicate groups
                * Text refers to specific analysis
            - If table shows multiple comparisons, create separate signatures for each
            
            7. **Handle Edge Cases**:
            - Outdated names: Note if taxonomic name seems old
            - Ambiguous taxonomy: Flag if only partial name given
            - Multiple testing: Check if MHT correction was applied
            - Non-significant findings: DO NOT extract (only significant ones)
            
            **SEARCH QUERIES TO USE**:
            - "supplementary table" OR "additional file" OR "table S"
            - "differential abundance" OR "significantly different"
            - "p-value" OR "FDR" OR "q-value"
            - "fold change" OR "log2FC" OR "odds ratio"
            - bacterial genus names (e.g., "Bifidobacterium", "Lactobacillus")
            - "enriched" OR "depleted" OR "increased" OR "decreased"
            
            **PROCESS CONSTRAINTS** (Important for DeepSeek's small context):
            - Process ONE table at a time
            - If table is very large (>100 rows), process in chunks of 50 rows
            - For each chunk, extract signatures and aggregate at the end
            - Never try to load entire supplementary materials at once
            
            **OUTPUT FORMAT**:
            Return structured JSON with ALL signatures:
            ```
            json
            {
            "total_signatures": 52,
            "signatures": [
                {
                "signature_id": 1,
                "experiment_id": 1,
                "microbe_name": "Enterococcus",
                "taxonomic_level": "genus",
                "direction": "increased",
                "direction_in_group": "increased abundance in High constipation > 3d-crude (< 3months)",
                "source": "Table S6",
                "source_description": "Results of regression models testing associations between one-month stool microbiota core genera and functional gastrointestinal symptoms",
                "statistics": {
                    "p_value": 0.001,
                    "fold_change": 2.3,
                    "method": "Logistic Regression"
                },
                "confidence": "high",
                "notes": null
                },
                {
                "signature_id": 2,
                "experiment_id": 1,
                "microbe_name": "Haemophilus",
                "taxonomic_level": "genus",
                "direction": "decreased",
                "direction_in_group": "decreased abundance in High constipation > 3d-crude (< 3months)",
                "source": "Table S6",
                "source_description": "Results of regression models testing associations between one-month stool microbiota core genera and functional gastrointestinal symptoms",
                "statistics": {
                    "p_value": 0.003,
                    "fold_change": 0.5,
                    "method": "Logistic Regression"
                },
                "confidence": "high",
                "notes": null
                },
                {
                "signature_id": 3,
                "experiment_id": 2,
                "microbe_name": "Mediterraneibacter gnavus",
                "taxonomic_level": "species",
                "direction": "increased",
                "direction_in_group": "increased abundance in High colic: wessel-crude (< 3months)",
                "source": "Table S6",
                "source_description": "Results of regression models testing associations between one-month stool microbiota core genera and functional gastrointestinal symptoms",
                "statistics": {
                    "p_value": null,
                    "significance": "p < 0.05",
                    "fold_change": null
                },
                "confidence": "medium",
                "notes": "Exact p-value not provided in table"
                }
                // ... continue for all signatures
            ],
            "extraction_metadata": {
                "signatures_per_experiment": {
                "1": 2,
                "2": 2,
                "3": 1,
                "4": 1
                // ... etc
                },
                "data_sources": {
                "tables": ["Table S6", "Table 3"],
                "figures": ["Figure 5C"],
                "text": ["Results section paragraph 3"]
                },
                "consistency_checks": {
                "repeated_bacteria": [
                    {
                    "microbe": "Bifidobacterium",
                    "appears_in_experiments": [2, 5, 13, 23],
                    "consistent_direction": true,
                    "direction": "decreased"
                    },
                    {
                    "microbe": "Mediterraneibacter gnavus",
                    "appears_in_experiments": [2, 3, 8],
                    "consistent_direction": true,
                    "direction": "increased"
                    }
                ]
                },
                "confidence": "high",
                "missing_data": ["exact fold-changes not provided for 5 signatures"]
            }
            }
            ```
            ''',
            
            expected_output='''A complete JSON object containing ALL signatures extracted 
            from the paper. Each signature must include:
            - Unique signature ID
            - Link to experiment ID
            - Microbe name and taxonomic level
            - Direction of change (increased/decreased)
            - Formatted direction string with group name
            - Source (table/figure reference)
            - Statistical values (if available)
            - Confidence level
            
            The output should include metadata about consistency checks (bacteria appearing 
            in multiple experiments) and data quality notes.''',
            agent=agent,            
            output_file='output/signatures.json'
        )