# Scripts

## Build Pipeline

Run these scripts in order to build the system from scratch:

1. **process_all_documents.py** - Process raw documents into chunks
   ```bash
   python scripts/build/process_all_documents.py
   ```

2. **generate_embeddings.py** - Generate embeddings from chunks
   ```bash
   python scripts/build/generate_embeddings.py
   ```

3. **build_retrieval_system.py** - Build FAISS index from embeddings
   ```bash
   python scripts/build/build_retrieval_system.py
   ```

## Testing

- **verify_data.py** - Verify data quality and corpus statistics
  ```bash
  python scripts/tests/verify_data.py
  ```

- **test_comprehensive_100_queries.py** - Run comprehensive 100-query evaluation
  ```bash
  python scripts/tests/test_comprehensive_100_queries.py
  ```

## Main Entry Points (in root)

- **app.py** - Streamlit web interface
  ```bash
  streamlit run app.py
  ```

- **run_all_experiments.py** - Run all 4 research experiments
  ```bash
  python run_all_experiments.py
  ```
