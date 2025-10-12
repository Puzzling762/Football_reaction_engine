LOGGER:LogInfo("=== Auto Export Start ===")

local base = "D:\\Projects\\Fifa15_AI\\scripts\\"

-- Run Big Matchups exporter
dofile(base .. "export_bigmatchups.lua")
LOGGER:LogInfo("Big Matchups Export Done")

-- Run Season Stats exporter
dofile(base .. "export_season_stats.lua")
LOGGER:LogInfo("Season Stats Export Done")

-- Run Player Last Match History exporter (when you make it)
dofile(base .. "export_playerlastmatchhistory.lua")
LOGGER:LogInfo("Player Match History Export Done")

LOGGER:LogInfo("=== All Exports Completed ===")
