from fastapi import APIRouter, HTTPException, UploadFile, File, Form, BackgroundTasks
from starlette import status
from starlette.responses import JSONResponse, FileResponse
import logging
import tempfile
import os
from pathlib import Path

from models import InvoiceValidatorRequest, InvoiceValidatorResponse, ErrorResponse
from services.invoice_validator_service import InvoiceValidatorService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/invoice-validator", tags=["Invoice Validator"])


@router.post(
    "/validate",
    status_code=status.HTTP_200_OK,
    summary="Validate Invoice",
    description=""" This service is created for Supply-Chain Operations: 
                    Upload invoice and Jira Excel files and validate them. 
                    Returns a downloadable Excel file with computed columns showing differences.
                    Processes files in memory without cluttering temp storage.""",
    responses={
        200: {
            "description": "Successfully validated invoice - Excel file will be downloaded",
            "content": {
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": {
                    "schema": {
                        "type": "string",
                        "format": "binary"
                    }
                }
            }
        },
        500: {
            "description": "Internal server error",
            "model": ErrorResponse
        }
    }
)
async def validate_invoice(
    background_tasks: BackgroundTasks,
    invoice_file: UploadFile = File(..., description="Invoice Excel file to validate"),
    jira_file: UploadFile = File(..., description="Jira data Excel file for comparison"),
    sheet_name: str = Form("Deckblatt", description="Sheet name in the invoice file to process")
):
    """
    Upload and validate an invoice Excel file against Jira data and return a downloadable Excel file.
    Processes files in memory without cluttering temp storage.
    """
    try:
        # Validate file types
        if not invoice_file.filename.lower().endswith(('.xlsx', '.xls')):
            raise HTTPException(status_code=400, detail="Invoice file must be an Excel file (.xlsx or .xls)")
        
        if not jira_file.filename.lower().endswith(('.xlsx', '.xls')):
            raise HTTPException(status_code=400, detail="Jira file must be an Excel file (.xlsx or .xls)")
        
        # Create temporary files
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_invoice:
            temp_invoice.write(invoice_file.file.read())
            temp_invoice_path = temp_invoice.name
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_jira:
            temp_jira.write(jira_file.file.read())
            temp_jira_path = temp_jira.name
        
        try:
            # Process validation using the original InvoiceValidator
            invoice_service = InvoiceValidatorService()
            result = invoice_service.validate_invoice(
                invoice_file_path=temp_invoice_path,
                jira_file_path=temp_jira_path,
                sheet_name=sheet_name
            )
            
            # Get the output file path from the result
            output_file_path = result["output_file_path"]
            
            # Return the file as a downloadable response
            filename = f"invoice_validated_{sheet_name}.xlsx"
            
            # Add cleanup task for the output file
            def cleanup_output_file(file_path: str):
                try:
                    if os.path.exists(file_path):
                        os.unlink(file_path)
                        logger.info(f"Cleaned up output file: {file_path}")
                except OSError as e:
                    logger.warning(f"Could not clean up output file {file_path}: {e}")
            
            # Schedule cleanup after response is sent
            background_tasks.add_task(cleanup_output_file, output_file_path)
            
            return FileResponse(
                path=output_file_path,
                filename=filename,
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
        finally:
            # Clean up temporary files immediately after processing
            try:
                os.unlink(temp_invoice_path)
                os.unlink(temp_jira_path)
                logger.info(f"Cleaned up temporary files: {temp_invoice_path}, {temp_jira_path}")
            except OSError as e:
                logger.warning(f"Could not clean up temporary files: {e}")
        
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Validation error in invoice validation: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in invoice validation: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"Unexpected error validating invoice: {str(e)}"}
        )


@router.post(
    "/results",
    status_code=status.HTTP_200_OK,
    summary="Get Validation Results",
    description="Upload invoice and Jira Excel files and get validation results as JSON data without generating an Excel file.",
    responses={
        200: {
            "description": "Successfully retrieved validation results",
            "content": {
                "application/json": {
                    "example": {
                        "results": [
                            {
                                "Column_0": "1",
                                "Column_1": "Product A",
                                "Column_2": "Software License",
                                "Amount": 100,
                                "Unit": "piece",
                                "Price per unit": 100.0,
                                "Total": 10000.0,
                                "Actual Amount": 95,
                                "Difference": -5,
                                "Difference Percentage": -5.0
                            }
                        ],
                        "summary": "Found 15 out of 20 items with differences (avg: 8.5%, range: -5.2% to +25.1%)",
                        "total_items": 20,
                        "items_with_differences": 15
                    }
                }
            }
        },
        500: {
            "description": "Internal server error",
            "model": ErrorResponse
        }
    }
)
async def get_validation_results(
    invoice_file: UploadFile = File(..., description="Invoice Excel file to validate"),
    jira_file: UploadFile = File(..., description="Jira data Excel file for comparison"),
    sheet_name: str = Form("Deckblatt", description="Sheet name in the invoice file to process")
):
    """
    Upload invoice and Jira Excel files and get validation results as JSON data.
    """
    try:
        # Validate file types
        if not invoice_file.filename.lower().endswith(('.xlsx', '.xls')):
            raise HTTPException(status_code=400, detail="Invoice file must be an Excel file (.xlsx or .xls)")
        
        if not jira_file.filename.lower().endswith(('.xlsx', '.xls')):
            raise HTTPException(status_code=400, detail="Jira file must be an Excel file (.xlsx or .xls)")
        
        # Create temporary files
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_invoice:
            temp_invoice.write(invoice_file.file.read())
            temp_invoice_path = temp_invoice.name
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_jira:
            temp_jira.write(jira_file.file.read())
            temp_jira_path = temp_jira.name
        
        try:
            # Process validation using the original InvoiceValidator
            invoice_service = InvoiceValidatorService()
            result = invoice_service.get_validation_results(
                invoice_file_path=temp_invoice_path,
                jira_file_path=temp_jira_path,
                sheet_name=sheet_name
            )
            
            return JSONResponse(content=result)
            
        finally:
            # Clean up temporary files immediately after processing
            try:
                os.unlink(temp_invoice_path)
                os.unlink(temp_jira_path)
                logger.info(f"Cleaned up temporary files: {temp_invoice_path}, {temp_jira_path}")
            except OSError as e:
                logger.warning(f"Could not clean up temporary files: {e}")
        
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Validation error in getting results: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in getting results: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"Unexpected error getting validation results: {str(e)}"}
        ) 