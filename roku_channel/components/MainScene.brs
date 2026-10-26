sub init()
    m.body = m.top.findNode("body")
    m.beaconTask = createObject("roSGNode", "BeaconTask")
    m.beaconTask.url = "http://192.168.86.35:8777/beacon.json"
    m.beaconTask.observeField("content", "onBeacon")
    m.beaconTask.control = "RUN"
    m.refresh = m.top.findNode("refresh")
    m.refresh.observeField("fire", "onRefresh")
    m.refresh.control = "start"
end sub

sub onRefresh()
    m.beaconTask.control = "RUN"
end sub

sub onBeacon()
    raw = m.beaconTask.content
    if raw = invalid or raw = "" then return
    parsed = parseJson(raw)
    if parsed = invalid then return
    lines = []

    cells = parsed.Lookup("lattice_snapshot").Lookup("cells")
    for each key in cells.Keys()
        c = cells.Lookup(key)
        rep = c.reputation
        ton = c.ton
        lines.Push(key + "  rep " + itToStr(rep) + "  " + itToStr(int(ton * 100) / 100.0) + " ton")
    end for

    arts = parsed.Lookup("artifacts")
    for i = 0 to arts.Count() - 1
        a = arts[i]
        lines.Push("[ " + a.type + " ]  " + a.name + "  (" + itToStr(a.price_gstd) + " gstd)")
    end for

    m.body.text = lines.Join(chr(10))
end sub

function itToStr(v as integer) as string
    return stri(v).trim()
end function
