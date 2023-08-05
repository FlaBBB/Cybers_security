local function bxor(a, b)
    local xor = 0
    for i = 0, 31 do
        local x = a / 2 + b / 2
        if x ~= math.floor(x) then
            xor = xor + 2^i
        end
        a = math.floor(a / 2)
        b = math.floor(b / 2)
    end
    return xor
end

local function decrypt(v24, v25)
    local result = {}
    for v44 = 1, #v24 do
        local char1 = v24:sub(v44, v44)
        local char2 = v25:sub(1 + ((v44 - 1) % #v25), 1 + ((v44 - 1) % #v25))
        local byte1 = char1:byte()
        local byte2 = char2:byte()
        local decryptedByte = bxor(byte1, byte2) % 256
        result[v44] = string.char(decryptedByte)
    end
    return table.concat(result)
end

local v8 = _G["require"]
local v9 = _G["loadstring"]
local v10 = _G["load"]
local v11 = _G["pcall"]
local v12 = _G["setfenv"]
local v13 = _G["getfenv"]
local v14 = _G["coroutine"]["wrap"]
local v15 = _G["string"]["gsub"]
local v16 = _G["string"]["find"]
local v17 = _G["_VERSION"] or function() return _ENV end
local v18 = _G["collectgarbage"]
local v19 = _G["pairs"]
local v20 = _G["type"]
local v21 = _G["next"] or _G["pairs"]
local v22 = _G["error"]

local function execute(v28, v29, ...)
    local v30 = 0
    local v31
    local v32
    local v33
    local v34
    local v35
    local v36
    local v37
    local v38
    local v39
    local v40
    local v41
    local v42
    local v43

    while true do
        if v30 == 1 then
            v35 = nil
            v36 = nil
            v37 = nil
            v38 = nil
            v30 = 2
        end
        if v30 == 2 then
            v39 = nil
            v40 = nil
            v41 = nil
            v42 = nil
            v30 = 3
        end
        if v30 == 0 then
            v31 = 0
            v32 = nil
            v33 = nil
            v34 = nil
            v30 = 1
        end
        if v30 == 3 then
            v43 = nil
            while true do
                if v30 == 1 then
                    v43 = nil
                    v31 = 7
                    break
                end
                if v30 == 0 then
                    v42 = nil
                    function v42()
                        local v54 = 0
                        local v55
                        local v56
                        local v57
                        local v58
                        local v59
                        local v60
                        local v61

                        while true do
                            if v54 == 0 then
                                v55 = nil
                                v56 = nil
                                v57 = nil
                                v58 = nil
                                v59 = nil
                                v54 = 1
                            end
                            if v54 == 1 then
                                v60 = nil
                                v61 = nil
                                v54 = 2
                            end
                            if v54 == 2 then
                                v55 = nil
                                v56 = nil
                                v57 = nil
                                v58 = nil
                                v59 = nil
                                v54 = 3
                            end
                            if v54 == 3 then
                                v60 = nil
                                v61 = nil
                                v54 = 4
                            end
                            if v54 == 4 then
                                v54 = 5
                            end
                            if v54 == 5 then
                                return
                            end
                        end
                    end
                    return
                end
                if v30 == 2 then
                    v42()
                    v54 = 0
                end
                if v30 == 3 then
                    break
                end
            end
        end
        if v30 == 7 then
            return
        end
    end
end

-- execute("Obfuscated code here...")
execute("MATT1C3O0003063O00737472696E6703043O006368617203043O00627974652O033O0073756203053O0062697433322O033O0062697403043O0062786F7203053O007461626C6503063O00636F6E63617403063O00696E7365727403023O00696F03053O00777269746503293O00205O5F9O204O205F5O203O5F205O5F204O5F200A03293O007C3O202O5F7C3O5F203O5F203O5F7C207C3O5F7C3O207C5F3O205F7C2O202O5F7C0A03293O007C2O207C2O207C202E207C202E207C202E207C207C202D5F7C202D3C2O207C207C207C2O202O5F7C0A03293O007C5O5F7C3O5F7C3O5F7C5F2O207C5F7C3O5F7C3O5F7C207C5F7C207C5F7C3O200A032A3O009O205O207C3O5F7C7O205A65724D612O74202D206D697363200A03023O00409103083O007EB1A3BB4586DBA703013O007303043O007265616403373O00DF17EB31E4E81CC12FC4EF37F223D1C334CC39FAF22CD915C4C321D43EC0FF2CC92FFAFE22DE2FFAEF22C32EC7F33BF22FD6FF22DD2FD803053O009C43AD4AA503053O007072696E742O033O00711D9903073O002654D72976DC4603043O00D27F250703053O009E30764272004A3O00121B3O00013O0020185O000200121B000100013O00201800010001000300121B000200013O00201800020002000400121B000300053O0006160003000A000100010004033O000A000100121B000300063O00201800040003000700121B000500083O00201800050005000900121B000600083O00201800060006000A00060900073O000100062O00063O00064O00068O00063O00044O00063O00014O00063O00024O00063O00053O00121B0008000B3O00201800080008000C00120E0009000D4O000700080002000100121B0008000B3O00201800080008000C00120E0009000E4O000700080002000100121B0008000B3O00201800080008000C00120E0009000F4O000700080002000100121B0008000B3O00201800080008000C00120E000900104O000700080002000100121B0008000B3O00201800080008000C00120E000900114O000700080002000100121B0008000B3O00201800080008000C2O0006000900073O00120E000A00123O00120E000B00134O000F0009000B4O001C00083O000100121B0008000B3O0020180008000800152O001D000800010002001211000800143O00121B000800144O0006000900073O00120E000A00163O00120E000B00174O00190009000B000200060400080043000100090004033O0043000100121B000800184O0006000900073O00120E000A00193O00120E000B001A4O000F0009000B4O001C00083O00010004033O0049000100121B000800184O0006000900073O00120E000A001B3O00120E000B001C4O000F0009000B4O001C00083O00012O000C3O00013O00013O00023O00026O00F03F026O00704002284O000800025O00120E000300014O001200045O00120E000500013O0004150003002300012O000D00076O0006000800024O000D000900014O000D000A00024O000D000B00034O000D000C00044O0006000D6O0006000E00063O002005000F000600012O000F000C000F4O000B000B3O00022O000D000C00034O000D000D00044O0006000E00013O002001000F000600012O0012001000014O0013000F000F0010001017000F0001000F0020010010000600012O0012001100014O00130010001000110010170010000100100020050010001000012O000F000D00104O0014000C6O000B000A3O0002002002000A000A00022O00100009000A4O001C00073O000100040A0003000500012O000D000300054O0006000400024O001A000300046O00036O000C3O00017O00283O00093O000A3O000A3O000A3O000A3O000B3O000B3O000B3O000B3O000B3O000B3O000B3O000B3O000B3O000B3O000B3O000B3O000B3O000B3O000B3O000B3O000B3O000B3O000B3O000B3O000B3O000B3O000B3O000B3O000B3O000B3O000B3O000B3O000B3O000A3O000D3O000D3O000D3O000D3O000E3O004A3O00013O00013O00023O00023O00033O00033O00043O00043O00043O00043O00053O00063O00063O00073O00073O000E3O000E3O000E3O000E3O000E3O000E3O000E3O000F3O000F3O000F3O000F3O00103O00103O00103O00103O00113O00113O00113O00113O00123O00123O00123O00123O00133O00133O00133O00133O00143O00143O00143O00143O00143O00143O00143O00153O00153O00153O00153O00163O00163O00163O00163O00163O00163O00163O00173O00173O00173O00173O00173O00173O00173O00193O00193O00193O00193O00193O00193O001A3O00",
		v17(),
		...)