// ===============================================================================
// NASSAU CANDY DISTRIBUTOR - POWER QUERY M TRANSFORMATION SCRIPTS
// ===============================================================================

// -------------------------------------------------------------------------------
// 1. FACT_ORDERS TABLE M SCRIPT
// -------------------------------------------------------------------------------
let
    Source = Excel.Workbook(File.Contents("C:\Users\ayush\.gemini\antigravity-ide\scratch\nassau_candy_analytics\powerbi\Nassau_Candy_PowerBI_Model.xlsx"), null, true),
    Fact_Orders_Sheet = Source{[Item="Fact_Orders",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Fact_Orders_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"Row ID", Int64.Type}, 
        {"Order ID", type text}, 
        {"Order Date", type date}, 
        {"Ship Date", type date}, 
        {"Ship Mode", type text}, 
        {"Customer ID", type text}, 
        {"State/Province", type text}, 
        {"Region", type text}, 
        {"Division", type text}, 
        {"Product ID", type text}, 
        {"Product Name", type text}, 
        {"Sales", type number}, 
        {"Units", Int64.Type}, 
        {"Gross Profit", type number}, 
        {"Cost", type number}, 
        {"Gross Margin (%)", type number}, 
        {"Profit per Unit", type number}, 
        {"Cost per Unit", type number}, 
        {"Price per Unit", type number}, 
        {"Transit Days", Int64.Type}, 
        {"Factory", type text}
    })
in
    #"Changed Type"


// -------------------------------------------------------------------------------
// 2. DIM_PRODUCTS TABLE M SCRIPT
// -------------------------------------------------------------------------------
let
    Source = Excel.Workbook(File.Contents("C:\Users\ayush\.gemini\antigravity-ide\scratch\nassau_candy_analytics\powerbi\Nassau_Candy_PowerBI_Model.xlsx"), null, true),
    Dim_Products_Sheet = Source{[Item="Dim_Products",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Dim_Products_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"Product Name", type text}, 
        {"Division", type text}, 
        {"Factory", type text}, 
        {"Diagnostic Flag", type text}, 
        {"Quadrant", type text}
    })
in
    #"Changed Type"


// -------------------------------------------------------------------------------
// 3. DIM_FACTORIES TABLE M SCRIPT
// -------------------------------------------------------------------------------
let
    Source = Excel.Workbook(File.Contents("C:\Users\ayush\.gemini\antigravity-ide\scratch\nassau_candy_analytics\powerbi\Nassau_Candy_PowerBI_Model.xlsx"), null, true),
    Dim_Factories_Sheet = Source{[Item="Dim_Factories",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Dim_Factories_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"Factory", type text}, 
        {"Latitude", type number}, 
        {"Longitude", type number}, 
        {"City", type text}, 
        {"State", type text}
    })
in
    #"Changed Type"


// -------------------------------------------------------------------------------
// 4. DIM_GEOGRAPHY TABLE M SCRIPT
// -------------------------------------------------------------------------------
let
    Source = Excel.Workbook(File.Contents("C:\Users\ayush\.gemini\antigravity-ide\scratch\nassau_candy_analytics\powerbi\Nassau_Candy_PowerBI_Model.xlsx"), null, true),
    Dim_Geography_Sheet = Source{[Item="Dim_Geography",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Dim_Geography_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"State/Province", type text}, 
        {"Region", type text}, 
        {"Latitude", type number}, 
        {"Longitude", type number}
    })
in
    #"Changed Type"
