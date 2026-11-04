import logging
import io
import pandas as pd
from pathlib import Path
from modules.invoice_validator import InvoiceValidator

logger = logging.getLogger(__name__)


class InvoiceValidatorService:
    """Service class for invoice validation operations."""
    
    def __init__(self):
        """Initialize the InvoiceValidatorService."""
        # Import mapping from config
        try:
            from config.para import Parameters
            self.mapping = Parameters.mapping
        except ImportError:
            # Fallback mapping if config not available
            self.mapping = {}
        
        self.header_row_index = None
    
    def validate_invoice(self, invoice_file_path: str, jira_file_path: str, sheet_name: str = "Deckblatt") -> dict:
        """
        Validate an invoice against Jira data and generate a validated Excel file.
        
        Args:
            invoice_file_path: Path to the invoice Excel file
            jira_file_path: Path to the Jira data Excel file
            sheet_name: Sheet name in the invoice file to process
            
        Returns:
            dict: Contains output file path, validation summary, and processing info
        """
        try:
            # Validate file paths exist
            if not Path(invoice_file_path).exists():
                raise ValueError(f"Invoice file not found: {invoice_file_path}")
            
            if not Path(jira_file_path).exists():
                raise ValueError(f"Jira file not found: {jira_file_path}")
            
            # Create validator instance
            validator = InvoiceValidator(
                invoice_file_path=invoice_file_path,
                jira_file_path=jira_file_path,
                sheet_name=sheet_name
            )
            
            # Run validation and get output file path
            output_file_path = validator.run()
            
            # Get results for summary
            results_df = validator.get_results()
            
            # Generate validation summary
            total_items = len(results_df)
            items_with_differences = len(results_df[results_df['Difference'] != 0])
            
            if items_with_differences > 0:
                min_diff_pct = results_df['Difference Percentage'].min()
                max_diff_pct = results_df['Difference Percentage'].max()
                validation_summary = f"Validation completed successfully! Found {items_with_differences} out of {total_items} items with differences ranging from {min_diff_pct:.1f}% to {max_diff_pct:.1f}%"
            else:
                validation_summary = f"Validation completed successfully! All {total_items} items match exactly with Jira data."
            
            # Generate processing info
            jira_records = len(validator.df_jira)
            processing_info = f"Processed {total_items} invoice items against {jira_records} Jira records. Output saved to: {output_file_path}"
            
            return {
                "output_file_path": output_file_path,
                "validation_summary": validation_summary,
                "processing_info": processing_info,
                "is_temp_file": True  # Flag to indicate this is a temporary file that should be cleaned up
            }
            
        except Exception as e:
            logger.error(f"Error validating invoice: {str(e)}")
            raise
    
    def get_validation_results(self, invoice_file_path: str, jira_file_path: str, sheet_name: str = "Deckblatt") -> dict:
        """
        Get validation results as a DataFrame without writing to Excel.
        
        Args:
            invoice_file_path: Path to the invoice Excel file
            jira_file_path: Path to the Jira data Excel file
            sheet_name: Sheet name in the invoice file to process
            
        Returns:
            dict: Contains the validation results DataFrame and summary statistics
        """
        try:
            # Validate file paths exist
            if not Path(invoice_file_path).exists():
                raise ValueError(f"Invoice file not found: {invoice_file_path}")
            
            if not Path(jira_file_path).exists():
                raise ValueError(f"Jira file not found: {jira_file_path}")
            
            # Create validator instance
            validator = InvoiceValidator(
                invoice_file_path=invoice_file_path,
                jira_file_path=jira_file_path,
                sheet_name=sheet_name
            )
            
            # Get results as DataFrame
            results_df = validator.get_results()
            
            # Convert DataFrame to dict for JSON serialization
            results_dict = results_df.to_dict('records')
            
            # Generate summary statistics
            total_items = len(results_df)
            items_with_differences = len(results_df[results_df['Difference'] != 0])
            
            if items_with_differences > 0:
                min_diff_pct = results_df['Difference Percentage'].min()
                max_diff_pct = results_df['Difference Percentage'].max()
                avg_diff_pct = results_df['Difference Percentage'].mean()
                summary = f"Found {items_with_differences} out of {total_items} items with differences (avg: {avg_diff_pct:.1f}%, range: {min_diff_pct:.1f}% to {max_diff_pct:.1f}%)"
            else:
                summary = f"All {total_items} items match exactly with Jira data."
            
            return {
                "results": results_dict,
                "summary": summary,
                "total_items": total_items,
                "items_with_differences": items_with_differences
            }
            
        except Exception as e:
            logger.error(f"Error getting validation results: {str(e)}")
            raise
    
    def validate_invoice_in_memory(self, invoice_content: bytes, jira_content: bytes, sheet_name: str = "Deckblatt") -> dict:
        """
        Validate invoice and Jira data in memory without creating temporary files.
        Returns the original invoice structure with computed columns added.
        
        Args:
            invoice_content: Raw bytes of the invoice Excel file
            jira_content: Raw bytes of the Jira Excel file
            sheet_name: Sheet name in the invoice file to process
            
        Returns:
            dict: Contains the validated DataFrame with original structure and computed columns
        """
        try:
            # Create temporary file-like objects in memory
            invoice_buffer = io.BytesIO(invoice_content)
            jira_buffer = io.BytesIO(jira_content)
            
            # Read Excel files from memory
            df_raw = pd.read_excel(invoice_buffer, sheet_name=sheet_name, header=None)
            df_jira = pd.read_excel(jira_buffer)
            
            # Find header row
            header_keywords = {"Amount", "Unit", "Price per unit", "Total"}
            header_row_index = None
            for i, row in df_raw.iterrows():
                if header_keywords.issubset(set(map(str, row.values))):
                    header_row_index = i
                    break
            
            if header_row_index is None:
                raise ValueError("Could not locate header row with expected columns.")
            
            # Load with proper header
            invoice_buffer.seek(0)  # Reset buffer position
            df = pd.read_excel(invoice_buffer, sheet_name=sheet_name, header=header_row_index)
            
            # Store header row index for later use
            self.header_row_index = header_row_index
            
            # Process the data using the original InvoiceValidator logic
            # Rename unnamed columns
            df.columns = [f"Column_{i}" if "Unnamed" in str(col) else str(col) for i, col in enumerate(df.columns)]

            # Find end of data (3 consecutive empty rows in description column)
            desc_col_index = 2
            end_index = len(df)
            empty_streak = 0
            threshold = 3

            for idx, row in df.iterrows():
                value = row.iloc[desc_col_index]
                if pd.isna(value) or str(value).strip() == "":
                    empty_streak += 1
                    if empty_streak >= threshold:
                        end_index = idx - threshold + 1
                        break
                else:
                    empty_streak = 0

            # Trim data to end_index
            df = df.iloc[:end_index].copy()
            
            # Add Excel row numbers for precise positioning
            df["__excel_row__"] = df.index + self.header_row_index + 1
            
            # Remove completely empty rows
            df.dropna(subset=['Column_0', 'Column_1', 'Column_2', 'Amount', 'Unit', 'Price per unit', 'Total'], 
                      how='all', inplace=True)
            
            # Process Jira data using original mapping logic
            # Map column values
            if 'Product' in df_jira.columns:
                # Create a new column with mapped values
                mapped_column_name = "Product_Mapped"
                df_jira[mapped_column_name] = df_jira['Product'].map(self.mapping)
                
                # Fill NaN values with original values (for unmapped items)
                df_jira[mapped_column_name] = df_jira[mapped_column_name].fillna(df_jira['Product'])
            
            # Aggregate Jira data
            jira_count = df_jira.groupby('Product_Mapped').agg({'Product': 'count'}).reset_index()

            # Merge and calculate differences
            final = df.merge(jira_count, left_on='Column_2', right_on='Product_Mapped', how='left')
            final.rename(columns={"Product": "Actual Amount"}, inplace=True)
            final['Difference'] = (final['Actual Amount'] - final['Amount'])
            final['Difference Percentage'] = (final['Actual Amount'] - final['Amount']) * 100 / final['Amount']
            
            # Generate summary
            total_items = len(final)
            items_with_differences = len(final[final['Difference'] != 0])
            
            if items_with_differences > 0:
                min_diff_pct = final['Difference Percentage'].min()
                max_diff_pct = final['Difference Percentage'].max()
                validation_summary = f"Validation completed successfully! Found {items_with_differences} out of {total_items} items with differences ranging from {min_diff_pct:.1f}% to {max_diff_pct:.1f}%"
            else:
                validation_summary = f"Validation completed successfully! All {total_items} items match exactly with Jira data."
            
            return {
                "validated_df": final,
                "validation_summary": validation_summary,
                "total_items": total_items,
                "items_with_differences": items_with_differences,
                "header_row_index": self.header_row_index
            }
            
        except Exception as e:
            logger.error(f"Error validating invoice in memory: {str(e)}")
            raise 