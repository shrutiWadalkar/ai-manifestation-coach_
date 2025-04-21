try:
    import polars as pl
    from pathlib import Path
except ImportError as e:
    raise ImportError(
        "Required packages not found. Please install with:\n"
        "pip install polars pyarrow\n"
        f"Original error: {str(e)}"
    )

def process_transcripts(input_dir="data/raw", output_dir="data/processed"):
    """Process transcript files with error handling"""
    try:
        Path(output_dir).mkdir(exist_ok=True)
        
        for txt_file in Path(input_dir).glob("*.txt"):
            try:
                # Read with polars (falls back to pandas if needed)
                df = pl.read_csv(txt_file, separator="\t", has_header=False)
                
                # Processing logic here
                df = df.with_columns(
                    pl.col("column_1").str.strip().alias("clean_text")
                )
                
                output_path = Path(output_dir) / f"processed_{txt_file.name}"
                df.write_parquet(output_path)
                
            except Exception as e:
                print(f"Error processing {txt_file.name}: {str(e)}")
                continue
                
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        raise

if __name__ == "__main__":
    process_transcripts()