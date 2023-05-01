-- USBエンドポイント1から送信されたパケットのペイロードの抽出
local usb_endpoint = 2
local usb_payloads = {}

function usb_capture_listener()
    local tap = Listener.new(nil, "usb.endpoint_number == " .. usb_endpoint)
    function tap.packet(pinfo, tvb)
        local payload = tvb:range()
        table.insert(usb_payloads, payload)
    end
end

-- スクリプトの実行
usb_capture_listener()

-- 結果の表示
for i, payload in ipairs(usb_payloads) do
    print(string.format("Payload %d: %s", i, tostring(payload)))
end