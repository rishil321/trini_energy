import glob
from pathlib import Path
import logging
import re
import sys
from typing import Any, List, Optional, Tuple
import pandas as pd
import pdfplumber
import tabula
from pypdf import PdfReader


MONTHLY_BULLETINS_LOCATION: str = "meei_documents/monthly_bulletins/"
LOGGER: logging.Logger = logging.getLogger(__name__)


def read_natural_gas_production_from_all_bulletins(
    all_monthly_bulletins: list[str],
):
    for monthly_bulletin in all_monthly_bulletins:
        page_num_with_natural_gas_production_data = (
            determine_page_with_natural_gas_production(monthly_bulletin)
        )
        table_with_gas_production: pd.DataFrame = extract_natural_gas_production_data(
            monthly_bulletin, page_num_with_natural_gas_production_data
        )
        cleaned_table: pd.DataFrame = extract_gas_production_data_from_table(
            table_with_gas_production
        )
        LOGGER.info(f"Successfully parsed gas production data from {monthly_bulletin}")


def extract_gas_production_data_from_table(table: pd.DataFrame) -> pd.DataFrame:
    # transpose the table to get the values for each company as a column
    table = table.transpose()
    # reset the index to get the dates as a column
    table.reset_index(inplace=True)
    # set the column names to the values in the first row
    table.columns = table.iloc[0]
    # drop the first row which is now the column names
    table.drop(table.index[0], inplace=True)
    # rename the company column to date
    table.rename(columns={"COMPANY": "DATE"}, inplace=True)
    # drop the last row since it only contains averages for the year
    table = table[:-1]
    # parse the months to proper dates
    table["DATE"] = pd.to_datetime(table["DATE"], format="%b-%y")
    table["DATE"] = table["DATE"] + pd.offsets.MonthEnd()
    # drop the last column since it's just totals
    table = table.drop(table.columns[-1], axis=1)
    return table


def keep_visible_lines(obj):
    if obj["object_type"] == "rect":
        # Slightly tweaked here, because this PDF uses RGB values instead of grayscale values
        return obj["non_stroking_color"] == (0.5,)
    return True


def adjust_parameters_for_each_year(monthly_bulletin: str, page_num: int) -> Tuple:
    normalized_document_name: str = monthly_bulletin.replace("-", "_").replace(
        ".pdf", ""
    )
    document_year: int = int(normalized_document_name.split("_")[5])
    horizontal_strategy = "lines"
    vertical_strategy = "lines"
    join_tolerance = 3
    snap_tolerance = 3
    intersection_tolerance = 3
    pdf = pdfplumber.open(monthly_bulletin)
    page = pdf.pages[page_num - 1]
    if document_year < 2010:
        horizontal_strategy = "text"
        vertical_strategy = "text"
    if document_year in [2020]:
        horizontal_strategy = "lines"
        vertical_strategy = "lines"
    return (
        horizontal_strategy,
        vertical_strategy,
        join_tolerance,
        snap_tolerance,
        intersection_tolerance,
        page,
    )


def extract_natural_gas_production_data(
    monthly_bulletin: str, page_num: int
) -> pd.DataFrame:
    (
        horizontal_strategy,
        vertical_strategy,
        join_tolerance,
        snap_tolerance,
        intersection_tolerance,
        page,
    ) = adjust_parameters_for_each_year(monthly_bulletin, page_num)
    all_tables_on_page = page.extract_tables(
        table_settings={
            "horizontal_strategy": horizontal_strategy,
            "vertical_strategy": vertical_strategy,
            "join_tolerance": join_tolerance,
            "snap_tolerance": snap_tolerance,
            "intersection_tolerance": intersection_tolerance,
        }
    )
    if not all_tables_on_page:
        raise RuntimeError(
            f"Could not read any tables on the page {page_num} for {monthly_bulletin}"
        )
    # some tables have a header row that needs to be removed
    if "TABLE" in all_tables_on_page[0][0][0]:  # type: ignore
        all_tables_on_page[0].pop(0)
    # some tables are joined with the utilization table, so we need to split them up based on the total row
    total_row_index = [
        index
        for index, row_data in enumerate(all_tables_on_page[0])
        if "TOTAL" in row_data
    ]
    if total_row_index:
        total_row_index = total_row_index[0]
    else:
        total_row_index = len(all_tables_on_page[0][0])
    gas_production_table = pd.DataFrame(
        all_tables_on_page[0][1:total_row_index], columns=all_tables_on_page[0][0]
    )
    LOGGER.debug(gas_production_table)
    return gas_production_table


def determine_page_with_natural_gas_production(
    monthly_bulletin: str,
) -> int:
    # find the page with the natural gas production by company
    page_num_with_natural_gas_production_by_company: Optional[int] = None
    # open the pdf file
    reader = PdfReader(monthly_bulletin)
    # extract text and do the search
    for index, page in enumerate(reader.pages):
        text = page.extract_text()
        matching_text_found_on_page = re.search(
            "Natural Gas Production By Company", text, re.IGNORECASE
        )
        if not matching_text_found_on_page:
            continue
        page_num_with_natural_gas_production_by_company = index + 1
    if not page_num_with_natural_gas_production_by_company:
        raise RuntimeError(
            f"Could not find Natural Gas Production By Company on any page in the monthly bulletin {monthly_bulletin}."
        )
    return page_num_with_natural_gas_production_by_company


def read_all_monthly_bulletin_pdfs_in_directory() -> list:
    all_monthly_bulletins: list = glob.glob(f"{MONTHLY_BULLETINS_LOCATION}*.pdf")
    if len(all_monthly_bulletins) == 0:
        raise RuntimeError(
            f"No monthly bulletins found in {MONTHLY_BULLETINS_LOCATION}. Please ensure directory is populated and script is called from correct working directory."
        )
    return all_monthly_bulletins


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logging.getLogger("pdfminer").setLevel(logging.INFO)
    all_monthly_bulletins = read_all_monthly_bulletin_pdfs_in_directory()
    read_natural_gas_production_from_all_bulletins(all_monthly_bulletins)


if __name__ == "__main__":
    main()
