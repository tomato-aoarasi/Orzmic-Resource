function add_commas(number)
    local formatted_number = tostring(number)
    local k = #formatted_number % 3
    local result = k > 0 and formatted_number:sub(1, k) or "0"
    
    for i = k + 1, #formatted_number, 3 do
        result = result .. "," .. formatted_number:sub(i, i + 2)
    end
    
    return result
end

-- 示例
local number = 1234
local formatted = add_commas(number)
print(formatted)