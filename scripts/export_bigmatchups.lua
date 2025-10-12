local function export_table_to_excel_csv()
    local tableName = "bigmatchups"  -- Change this to your table
    local outputFile = string.format("D:\\Projects\\Fifa15_AI\\exported_%s.csv", tableName)

    if not GetDBTableRows then
        print("Error: Database function not available.")
        return
    end

    local rows = GetDBTableRows(tableName)
    if not rows or #rows == 0 then
        print("Error: Table is empty or does not exist.")
        return
    end

    local file = io.open(outputFile, "w")
    if not file then
        print("Error: Could not open file for writing.")
        return
    end

    -- Get headers from first row
    local headers = {}
    for key, _ in pairs(rows[1]) do
        table.insert(headers, key)
    end

    -- Write header row (Excel prefers quoted headers too)
    local function quote(str)
        str = tostring(str or "")
        str = str:gsub('"', '""')  -- Escape quotes
        return '"' .. str .. '"'
    end
    local quotedHeaders = {}
    for _, h in ipairs(headers) do
        table.insert(quotedHeaders, quote(h))
    end
    file:write(table.concat(quotedHeaders, ",") .. "\n")

    -- Function to format cell values
    local function format_cell(value)
        -- Handle nested table with .value
        if type(value) == "table" and value.value then
            value = value.value
        end

        if value == nil then
            value = ""
        end

        -- Determine if numeric
        if type(value) == "number" then
            return tostring(value)
        else
            value = tostring(value)
            value = value:gsub('"', '""')  -- Escape quotes
            return '"' .. value .. '"'
        end
    end

    -- Write rows
    for _, row in ipairs(rows) do
        local rowData = {}
        for _, column in ipairs(headers) do
            table.insert(rowData, format_cell(row[column]))
        end
        file:write(table.concat(rowData, ",") .. "\n")
    end

    file:close()
    print("Excel-compatible CSV exported successfully to " .. outputFile)
end

export_table_to_excel_csv()
