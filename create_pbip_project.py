import os
import json
import subprocess

def build_pbip_project():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    powerbi_dir = os.path.join(base_dir, "powerbi")
    pbip_dir = os.path.join(powerbi_dir, "Nassau_Candy_Analytics")
    dataset_dir = os.path.join(powerbi_dir, "Nassau_Candy_Analytics.Dataset")
    report_dir = os.path.join(powerbi_dir, "Nassau_Candy_Analytics.Report")

    os.makedirs(powerbi_dir, exist_ok=True)
    os.makedirs(dataset_dir, exist_ok=True)
    os.makedirs(report_dir, exist_ok=True)

    # 1. Root PBIP File
    pbip_path = os.path.join(powerbi_dir, "Nassau_Candy_Analytics.pbip")
    pbip_content = {
        "version": "1.0",
        "dataset": {
            "byPath": {
                "path": "Nassau_Candy_Analytics.Dataset"
            }
        },
        "report": {
            "byPath": {
                "path": "Nassau_Candy_Analytics.Report"
            }
        }
    }
    with open(pbip_path, "w", encoding="utf-8") as f:
        json.dump(pbip_content, f, indent=2)

    # 2. Dataset Folder Files
    with open(os.path.join(dataset_dir, "definition.pbidataset"), "w", encoding="utf-8") as f:
        json.dump({"version": "1.0", "dataset": {"byPath": {"path": "model.bim"}}}, f, indent=2)

    with open(os.path.join(dataset_dir, "item.metadata.json"), "w", encoding="utf-8") as f:
        json.dump({"type": "dataset", "displayName": "Nassau_Candy_Analytics Dataset"}, f, indent=2)

    with open(os.path.join(dataset_dir, "item.config.json"), "w", encoding="utf-8") as f:
        json.dump({"version": "1.0"}, f, indent=2)

    # Excel Path for M Queries
    excel_path = os.path.join(powerbi_dir, "Nassau_Candy_PowerBI_Model.xlsx").replace("\\", "\\\\")

    # model.bim
    model_bim = {
        "name": "Nassau_Candy_Analytics",
        "compatibilityLevel": 1550,
        "model": {
            "culture": "en-US",
            "tables": [
                {
                    "name": "Fact_Orders",
                    "columns": [
                        {"name": "Row ID", "dataType": "int64", "sourceColumn": "Row ID"},
                        {"name": "Order ID", "dataType": "string", "sourceColumn": "Order ID"},
                        {"name": "Order Date", "dataType": "dateTime", "sourceColumn": "Order Date"},
                        {"name": "Ship Date", "dataType": "dateTime", "sourceColumn": "Ship Date"},
                        {"name": "Ship Mode", "dataType": "string", "sourceColumn": "Ship Mode"},
                        {"name": "Customer ID", "dataType": "string", "sourceColumn": "Customer ID"},
                        {"name": "State/Province", "dataType": "string", "sourceColumn": "State/Province"},
                        {"name": "Region", "dataType": "string", "sourceColumn": "Region"},
                        {"name": "Division", "dataType": "string", "sourceColumn": "Division"},
                        {"name": "Product ID", "dataType": "string", "sourceColumn": "Product ID"},
                        {"name": "Product Name", "dataType": "string", "sourceColumn": "Product Name"},
                        {"name": "Sales", "dataType": "double", "sourceColumn": "Sales"},
                        {"name": "Units", "dataType": "int64", "sourceColumn": "Units"},
                        {"name": "Gross Profit", "dataType": "double", "sourceColumn": "Gross Profit"},
                        {"name": "Cost", "dataType": "double", "sourceColumn": "Cost"},
                        {"name": "Gross Margin (%)", "dataType": "double", "sourceColumn": "Gross Margin (%)"},
                        {"name": "Profit per Unit", "dataType": "double", "sourceColumn": "Profit per Unit"},
                        {"name": "Cost per Unit", "dataType": "double", "sourceColumn": "Cost per Unit"},
                        {"name": "Price per Unit", "dataType": "double", "sourceColumn": "Price per Unit"},
                        {"name": "Transit Days", "dataType": "int64", "sourceColumn": "Transit Days"},
                        {"name": "Factory", "dataType": "string", "sourceColumn": "Factory"}
                    ],
                    "partitions": [
                        {
                            "name": "Fact_Orders-Partition",
                            "mode": "import",
                            "source": {
                                "type": "m",
                                "expression": [
                                    "let",
                                    f'    Source = Excel.Workbook(File.Contents("{excel_path}"), null, true),',
                                    '    Fact_Orders_Sheet = Source{[Item="Fact_Orders",Kind="Sheet"]}[Data],',
                                    '    #"Promoted Headers" = Table.PromoteHeaders(Fact_Orders_Sheet, [PromoteAllScalars=true]),',
                                    '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Row ID", Int64.Type}, {"Order ID", type text}, {"Order Date", type date}, {"Ship Date", type date}, {"Ship Mode", type text}, {"Customer ID", type text}, {"State/Province", type text}, {"Region", type text}, {"Division", type text}, {"Product ID", type text}, {"Product Name", type text}, {"Sales", type number}, {"Units", Int64.Type}, {"Gross Profit", type number}, {"Cost", type number}, {"Gross Margin (%)", type number}, {"Profit per Unit", type number}, {"Cost per Unit", type number}, {"Price per Unit", type number}, {"Transit Days", Int64.Type}, {"Factory", type text}})',
                                    "in",
                                    '    #"Changed Type"'
                                ]
                            }
                        }
                    ]
                },
                {
                    "name": "Dim_Products",
                    "columns": [
                        {"name": "Product Name", "dataType": "string", "sourceColumn": "Product Name"},
                        {"name": "Division", "dataType": "string", "sourceColumn": "Division"},
                        {"name": "Factory", "dataType": "string", "sourceColumn": "Factory"},
                        {"name": "Diagnostic Flag", "dataType": "string", "sourceColumn": "Diagnostic Flag"},
                        {"name": "Quadrant", "dataType": "string", "sourceColumn": "Quadrant"}
                    ],
                    "partitions": [
                        {
                            "name": "Dim_Products-Partition",
                            "mode": "import",
                            "source": {
                                "type": "m",
                                "expression": [
                                    "let",
                                    f'    Source = Excel.Workbook(File.Contents("{excel_path}"), null, true),',
                                    '    Dim_Products_Sheet = Source{[Item="Dim_Products",Kind="Sheet"]}[Data],',
                                    '    #"Promoted Headers" = Table.PromoteHeaders(Dim_Products_Sheet, [PromoteAllScalars=true]),',
                                    '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Product Name", type text}, {"Division", type text}, {"Factory", type text}, {"Diagnostic Flag", type text}, {"Quadrant", type text}})',
                                    "in",
                                    '    #"Changed Type"'
                                ]
                            }
                        }
                    ]
                },
                {
                    "name": "Dim_Factories",
                    "columns": [
                        {"name": "Factory", "dataType": "string", "sourceColumn": "Factory"},
                        {"name": "Latitude", "dataType": "double", "sourceColumn": "Latitude"},
                        {"name": "Longitude", "dataType": "double", "sourceColumn": "Longitude"},
                        {"name": "City", "dataType": "string", "sourceColumn": "City"},
                        {"name": "State", "dataType": "string", "sourceColumn": "State"}
                    ],
                    "partitions": [
                        {
                            "name": "Dim_Factories-Partition",
                            "mode": "import",
                            "source": {
                                "type": "m",
                                "expression": [
                                    "let",
                                    f'    Source = Excel.Workbook(File.Contents("{excel_path}"), null, true),',
                                    '    Dim_Factories_Sheet = Source{[Item="Dim_Factories",Kind="Sheet"]}[Data],',
                                    '    #"Promoted Headers" = Table.PromoteHeaders(Dim_Factories_Sheet, [PromoteAllScalars=true]),',
                                    '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Factory", type text}, {"Latitude", type number}, {"Longitude", type number}, {"City", type text}, {"State", type text}})',
                                    "in",
                                    '    #"Changed Type"'
                                ]
                            }
                        }
                    ]
                },
                {
                    "name": "Dim_Geography",
                    "columns": [
                        {"name": "State/Province", "dataType": "string", "sourceColumn": "State/Province"},
                        {"name": "Region", "dataType": "string", "sourceColumn": "Region"},
                        {"name": "Latitude", "dataType": "double", "sourceColumn": "Latitude"},
                        {"name": "Longitude", "dataType": "double", "sourceColumn": "Longitude"}
                    ],
                    "partitions": [
                        {
                            "name": "Dim_Geography-Partition",
                            "mode": "import",
                            "source": {
                                "type": "m",
                                "expression": [
                                    "let",
                                    f'    Source = Excel.Workbook(File.Contents("{excel_path}"), null, true),',
                                    '    Dim_Geography_Sheet = Source{[Item="Dim_Geography",Kind="Sheet"]}[Data],',
                                    '    #"Promoted Headers" = Table.PromoteHeaders(Dim_Geography_Sheet, [PromoteAllScalars=true]),',
                                    '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"State/Province", type text}, {"Region", type text}, {"Latitude", type number}, {"Longitude", type number}})',
                                    "in",
                                    '    #"Changed Type"'
                                ]
                            }
                        }
                    ]
                },
                {
                    "name": "_Measures",
                    "measures": [
                        {"name": "Total Sales", "expression": "SUM(Fact_Orders[Sales])", "formatString": "\\$#,##0.00"},
                        {"name": "Total Cost", "expression": "SUM(Fact_Orders[Cost])", "formatString": "\\$#,##0.00"},
                        {"name": "Total Gross Profit", "expression": "SUM(Fact_Orders[Gross Profit])", "formatString": "\\$#,##0.00"},
                        {"name": "Gross Margin %", "expression": "DIVIDE([Total Gross Profit], [Total Sales], 0)", "formatString": "0.0%"},
                        {"name": "Total Units", "expression": "SUM(Fact_Orders[Units])", "formatString": "#,##0"},
                        {"name": "Profit per Unit", "expression": "DIVIDE([Total Gross Profit], [Total Units], 0)", "formatString": "\\$#,##0.00"},
                        {"name": "Price per Unit", "expression": "DIVIDE([Total Sales], [Total Units], 0)", "formatString": "\\$#,##0.00"},
                        {"name": "Cost per Unit", "expression": "DIVIDE([Total Cost], [Total Units], 0)", "formatString": "\\$#,##0.00"},
                        {"name": "Total Orders", "expression": "COUNTROWS(Fact_Orders)", "formatString": "#,##0"},
                        {"name": "Avg Transit Days", "expression": "AVERAGE(Fact_Orders[Transit Days])", "formatString": "0.0"},
                        {"name": "Revenue Share %", "expression": "DIVIDE([Total Sales], CALCULATE([Total Sales], ALL(Dim_Products)), 0)", "formatString": "0.0%"},
                        {"name": "Profit Share %", "expression": "DIVIDE([Total Gross Profit], CALCULATE([Total Gross Profit], ALL(Dim_Products)), 0)", "formatString": "0.0%"},
                        {"name": "Financial Imbalance Index", "expression": "[Profit Share %] - [Revenue Share %]", "formatString": "+0.0%;-0.0%;0.0%"},
                        {"name": "Cumulative Profit", "expression": "VAR CurrentProfit = [Total Gross Profit] RETURN CALCULATE([Total Gross Profit], FILTER(ALL(Dim_Products[Product Name]), [Total Gross Profit] >= CurrentProfit))", "formatString": "\\$#,##0.00"},
                        {"name": "Cumulative Profit %", "expression": "DIVIDE([Cumulative Profit], CALCULATE([Total Gross Profit], ALL(Dim_Products)), 0)", "formatString": "0.0%"},
                        {"name": "Pareto Profit Category", "expression": "IF([Cumulative Profit %] <= 0.80, \"Top 80% Profit Driver\", \"Bottom 20% Profit Drag\")"},
                        {"name": "Diagnostic Flag DAX", "expression": "SWITCH(TRUE(), [Gross Margin %] < 0.25 && [Total Sales] > 5000, \"Reprice Immediately\", DIVIDE([Total Cost], [Total Sales], 0) > 0.65, \"Renegotiate Cost\", [Gross Margin %] < 0.20 && [Profit Share %] < 0.02, \"Discontinuation Review\", [Gross Margin %] >= 0.45, \"High Efficiency Driver\", \"Stable Core Product\")"},
                        {"name": "Strategic Quadrant DAX", "expression": "VAR MedianSales = MEDIANX(ALL(Dim_Products), [Total Sales]) VAR MedianMargin = MEDIANX(ALL(Dim_Products), [Gross Margin %]) VAR CurrentSales = [Total Sales] VAR CurrentMargin = [Gross Margin %] RETURN IF(CurrentSales >= MedianSales, IF(CurrentMargin >= MedianMargin, \"Stars (High Profit & Volume)\", \"Volume Drivers (High Sales, Low Margin)\"), IF(CurrentMargin >= MedianMargin, \"Niche Drivers (Low Sales, High Margin)\", \"Laggards (Low Sales, Low Profit)\"))"}
                    ],
                    "partitions": [
                        {
                            "name": "_Measures-Partition",
                            "mode": "import",
                            "source": {
                                "type": "m",
                                "expression": [
                                    "let",
                                    '    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Column1 = _t]),',
                                    '    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Column1", type text}})',
                                    "in",
                                    '    #"Changed Type"'
                                ]
                            }
                        }
                    ]
                }
            ],
            "relationships": [
                {
                    "name": "Fact_Orders_Dim_Products",
                    "fromTable": "Fact_Orders",
                    "fromColumn": "Product Name",
                    "toTable": "Dim_Products",
                    "toColumn": "Product Name"
                },
                {
                    "name": "Fact_Orders_Dim_Factories",
                    "fromTable": "Fact_Orders",
                    "fromColumn": "Factory",
                    "toTable": "Dim_Factories",
                    "toColumn": "Factory"
                },
                {
                    "name": "Fact_Orders_Dim_Geography",
                    "fromTable": "Fact_Orders",
                    "fromColumn": "State/Province",
                    "toTable": "Dim_Geography",
                    "toColumn": "State/Province"
                }
            ]
        }
    }

    with open(os.path.join(dataset_dir, "model.bim"), "w", encoding="utf-8") as f:
        json.dump(model_bim, f, indent=2)

    # 3. Report Folder Files
    with open(os.path.join(report_dir, "definition.pbidataset"), "w", encoding="utf-8") as f:
        json.dump({"version": "1.0", "datasetReference": {"byPath": {"path": "../Nassau_Candy_Analytics.Dataset"}}}, f, indent=2)

    with open(os.path.join(report_dir, "item.metadata.json"), "w", encoding="utf-8") as f:
        json.dump({"type": "report", "displayName": "Nassau_Candy_Analytics Report"}, f, indent=2)

    with open(os.path.join(report_dir, "item.config.json"), "w", encoding="utf-8") as f:
        json.dump({"version": "1.0"}, f, indent=2)

    # Visual Pages Configuration in report.json
    report_json = {
        "config": json.dumps({
            "version": "5.45",
            "themeCollection": {"baseTheme": {"name": "CY24SU08", "version": "5.54", "type": 2}}
        }),
        "layoutOptimization": 0
    }

    with open(os.path.join(report_dir, "report.json"), "w", encoding="utf-8") as f:
        json.dump(report_json, f, indent=2)

    print("Power BI Project (.pbip) built successfully at:", pbip_path)
    return pbip_path

if __name__ == "__main__":
    pbip_file = build_pbip_project()
    # Launch PBIDesktop with the .pbip project file!
    pbi_exe = r"C:\Program Files\Microsoft Power BI Desktop\bin\PBIDesktop.exe"
    if os.path.exists(pbi_exe):
        print(f"Launching Power BI Desktop with {pbip_file}...")
        subprocess.Popen([pbi_exe, pbip_file])
