import pandas as pd
from pathlib import Path
from config.para import Parameters
from openpyxl.styles import PatternFill
from openpyxl.utils import get_column_letter
from openpyxl import load_workbook
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 25)


class InvoiceValidator:
    def __init__(self, invoice_file_path: str, jira_file_path: str, sheet_name: str = "Deckblatt"):
        """
        Initialize InvoiceValidator with file paths
        
        Args:
            invoice_file_path (str): Path to the invoice Excel file
            jira_file_path (str): Path to the Jira data Excel file
            sheet_name (str): Sheet name in the invoice file (default: "Deckblatt")
        """
        self.invoice_file_path = Path(invoice_file_path)
        self.jira_file_path = Path(jira_file_path)
        self.sheet_name = sheet_name
        self.mapping = Parameters.mapping
        
        # Load data
        self._load_data()
        
    def _load_data(self):
        """Load and prepare the data from both files"""
        # Load invoice data
        df_raw = pd.read_excel(self.invoice_file_path, sheet_name=self.sheet_name, header=None)
        header_row_index = self._find_header_row(df_raw)
        
        if header_row_index is None:
            raise ValueError("Could not locate header row with expected columns.")
            
        # Load with proper header
        self.df = pd.read_excel(self.invoice_file_path, sheet_name=self.sheet_name, header=header_row_index)
        
        # Load Jira data
        self.df_jira = pd.read_excel(self.jira_file_path)
        
        # Store header row index for later use
        self.header_row_index = header_row_index
        
    def _find_header_row(self, df):
        """Find the header row containing expected column names"""
        header_keywords = {"Amount", "Unit", "Price per unit", "Total"}
        for i, row in df.iterrows():
            if header_keywords.issubset(set(map(str, row.values))):
                return i
        return None

    def extract_main_table_from_excel(self):
        """Extract and clean the main table from the invoice data"""
        # Rename unnamed columns
        self.df.columns = [f"Column_{i}" if "Unnamed" in str(col) else str(col) for i, col in enumerate(self.df.columns)]

        # Find end of data (3 consecutive empty rows in description column)
        desc_col_index = 2
        end_index = len(self.df)
        empty_streak = 0
        threshold = 3

        for idx, row in self.df.iterrows():
            value = row.iloc[desc_col_index]
            if pd.isna(value) or str(value).strip() == "":
                empty_streak += 1
                if empty_streak >= threshold:
                    end_index = idx - threshold + 1
                    break
            else:
                empty_streak = 0

        # Trim data to end_index
        self.df = self.df.iloc[:end_index].copy()
        
        # Add Excel row numbers for precise positioning
        self.df["__excel_row__"] = self.df.index + self.header_row_index + 1
        
        # Remove completely empty rows
        self.df.dropna(subset=['Column_0', 'Column_1', 'Column_2', 'Amount', 'Unit', 'Price per unit', 'Total'], 
                      how='all', inplace=True)

    def map_column_values(self, column_name):
        """Map values in a column based on the provided mapping dictionary"""
        if column_name not in self.df_jira.columns:
            print(f"Column '{column_name}' not found in dataframe")
            return self.df_jira
        
        # Create a new column with mapped values
        mapped_column_name = f"{column_name}_Mapped"
        self.df_jira[mapped_column_name] = self.df_jira[column_name].map(self.mapping)
        
        # Fill NaN values with original values (for unmapped items)
        self.df_jira[mapped_column_name] = self.df_jira[mapped_column_name].fillna(self.df_jira[column_name])
        
        print(f"Mapped {self.df_jira[column_name].notna().sum()} values in column '{column_name}'")
        print(f"Unique mapped values: {self.df_jira[mapped_column_name].unique()}")
          
    def prepare_data_from_jira(self):
        """Prepare and aggregate Jira data"""
        self.map_column_values('Product')
        self.jira_count = self.df_jira.groupby('Product_Mapped').agg({'Product': 'count'}).reset_index()

    def consolidate_data(self):
        """Merge invoice and Jira data and calculate differences"""
        self.final = self.df.merge(self.jira_count, left_on='Column_2', right_on='Product_Mapped', how='left')
        self.final.rename(columns={"Product": "Actual Amount"}, inplace=True)
        self.final['Difference'] = (self.final['Actual Amount'] - self.final['Amount'])
        self.final['Difference Percentage'] = (self.final['Actual Amount'] - self.final['Amount']) * 100 / self.final['Amount']

    def write_computed_columns_to_excel(self, df, start_col_letter='H', header_row=None):
        """Write computed columns to Excel with color coding using __excel_row__ for precise positioning"""
        wb = load_workbook(self.invoice_file_path)
        ws = wb[self.sheet_name]
        
        # Define colors for different percentage ranges
        green_fill = PatternFill(start_color='90EE90', end_color='90EE90', fill_type='solid')  # Light green
        yellow_fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')  # Yellow
        red_fill = PatternFill(start_color='FFB6C1', end_color='FFB6C1', fill_type='solid')     # Light red
        
        # Column headers and their positions
        columns_to_write = ['Actual Amount', 'Difference', 'Difference Percentage']
        
        # Determine header row position
        if header_row is None:
            # Default: place header above the first data row
            if '__excel_row__' in df.columns and not df['__excel_row__'].isna().all():
                header_row = int(df['__excel_row__'].min()) - 1
            else:
                header_row = 0  # Default to first row
        
        # Write headers
        for i, col_name in enumerate(columns_to_write):
            col_letter = get_column_letter(ord(start_col_letter) - ord('A') + i + 1)
            ws[f"{col_letter}{header_row + 1}"] = col_name
        
        # Write data and apply color coding using __excel_row__
        for _, row in df.iterrows():
            if '__excel_row__' in row and pd.notna(row['__excel_row__']):
                excel_row = int(row['__excel_row__']) + 1  # Convert to Excel 1-based index
                
                for i, col_name in enumerate(columns_to_write):
                    col_letter = get_column_letter(ord(start_col_letter) - ord('A') + i + 1)
                    cell = ws[f"{col_letter}{excel_row}"]
                    
                    if col_name in row and pd.notna(row[col_name]):
                        cell.value = row[col_name]
                        
                        # Apply color coding for Difference Percentage column
                        if col_name == 'Difference Percentage':
                            abs_percentage = abs(row[col_name])
                            if abs_percentage < 10:
                                cell.fill = green_fill
                            elif abs_percentage <= 30:
                                cell.fill = yellow_fill
                            else:
                                cell.fill = red_fill
        
        # Save with validated suffix
        output_path = self.invoice_file_path.parent / f"{self.invoice_file_path.stem}_validated.xlsx"
        wb.save(output_path)
        print(f"Written computed columns to Excel starting from column {start_col_letter}")
        print(f"Header row: {header_row + 1}")
        print("Color coding applied: Green (<10%), Yellow (10-30%), Red (>30%)")
        print(f"Used __excel_row__ for precise positioning")
        print(f"Output saved to: {output_path}")
        
        return str(output_path)

    def run(self):
        """Run the complete validation process"""
        print(f"Starting invoice validation for: {self.invoice_file_path}")
        print(f"Using Jira data from: {self.jira_file_path}")
        
        self.extract_main_table_from_excel()
        self.prepare_data_from_jira()
        self.consolidate_data()
        output_path = self.write_computed_columns_to_excel(self.final)
        
        print("Validation completed successfully!")
        return output_path

    def get_results(self):
        """Get the final results DataFrame without writing to Excel"""
        self.extract_main_table_from_excel()
        self.prepare_data_from_jira()
        self.consolidate_data()
        return self.final.copy()


# Example usage
# if __name__ == "__main__":
#     # Example paths - adjust these to your actual file paths
#     base = Path(__file__).parents[1]
#     base_data = base/'data'
    
#     invoice_file = base_data/'Monthly-Report-Dish-2025-06-01-bis-2025-06-30_actual.xlsx'
#     jira_file = base_data/'Product Moves (Stock Move Line) (stock.move.line) (11).xlsx'
    
#     # Create validator instance
#     validator = InvoiceValidator(
#         invoice_file_path=str(invoice_file),
#         jira_file_path=str(jira_file),
#         sheet_name="Deckblatt"
#     )
    
#     # Run validation and get output file path
#     output_file = validator.run()
#     print(f"Validation completed! Output file: {output_file}")
    
    # Alternative: Get results as DataFrame without writing to Excel
    # results_df = validator.get_results()
    # print(results_df.head())
  