LOGGER:LogInfo("=== Auto Export Start ===")

local base = "D:\\Projects\\Fifa15_AI\\scripts\\"
local output_dir = "D:\\Projects\\Fifa15_AI\\"

-- Create individual CSV files first
dofile(base .. "export_bigmatchups.lua")
LOGGER:LogInfo("Big Matchups Export Done")

dofile(base .. "export_season_stats.lua")
LOGGER:LogInfo("Season Stats Export Done")

dofile(base .. "export_playerlastmatchhistory.lua")
LOGGER:LogInfo("Player Match History Export Done")

-- Now combine them into one file with proper sheet separation
LOGGER:LogInfo("=== Combining CSVs into Multi-Sheet Format ===")

local current_date = GetCurrentDate()
local combined_file_path = output_dir .. "COMBINED_EXPORT.csv"

local combined_file = io.open(combined_file_path, "w")
if not combined_file then
    LOGGER:LogInfo("Error: Could not create combined file")
else
    -- Function to append a CSV file with sheet markers
    local function append_csv_as_sheet(filepath, sheet_name)
        local file = io.open(filepath, "r")
        if file then
            -- Write sheet separator (Excel recognizes this pattern)
            combined_file:write("\n")
            combined_file:write("\"=== SHEET: " .. sheet_name .. " ===\"\n")
            combined_file:write("\n")
            
            -- Read and write content
            local content = file:read("*all")
            combined_file:write(content)
            combined_file:write("\n")
            
            file:close()
            LOGGER:LogInfo(sheet_name .. " added to combined file")
            return true
        else
            LOGGER:LogInfo("Warning: Could not read " .. filepath)
            return false
        end
    end
    
    -- Append each CSV as a separate sheet
    local sheets_added = 0
    
    if append_csv_as_sheet(output_dir .. "exported_bigmatchups.csv", "BigMatchups") then
        sheets_added = sheets_added + 1
    end
    
    if append_csv_as_sheet(string.format("%sSEASON_STATS_%02d_%02d_%04d.csv", output_dir, current_date.day, current_date.month, current_date.year), "SeasonStats") then
        sheets_added = sheets_added + 1
    end
    
    -- Updated filename for player match rating history
    if append_csv_as_sheet(output_dir .. "exported_career_playermatchratinghistory.csv", "PlayerMatchRatingHistory") then
        sheets_added = sheets_added + 1
    end
    
    combined_file:close()
    LOGGER:LogInfo(string.format("Combined file created with %d sheets: %s", sheets_added, combined_file_path))
end

LOGGER:LogInfo("=== All Exports Completed ===")