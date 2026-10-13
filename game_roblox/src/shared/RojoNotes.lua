--[[
    Rojo project file — place this as default.project.json in the root
    for syncing with Rojo (the standard Roblox development tool)

    Install Rojo: https://rojo.space/
    Serve: rojo serve
    Sync: open Roblox Studio → Rojo plugin → Connect
]]

-- This file documents the sync structure:
--[[
{
    "name": "TheLedgerOfEmptyChairs",
    "tree": {
        "$className": "DataModel",
        "ReplicatedStorage": {
            "GameConfig": {
                "$path": "src/shared/GameConfig.lua"
            }
        },
        "ServerScriptService": {
            "ServerMain": {
                "$path": "src/server/ServerMain.lua"
            },
            "ShadowLedger": {
                "$path": "src/server/ShadowLedger.lua"
            },
            "TheAnswer": {
                "$path": "src/server/TheAnswer.lua"
            },
            "HallOfSupper": {
                "$path": "src/server/HallOfSupper.lua"
            }
        }
    }
}
]]
