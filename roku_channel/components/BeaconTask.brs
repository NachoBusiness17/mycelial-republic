sub init()
    m.top.functionName = "fetch"
end sub

sub fetch()
    m.top.content = fetchToString(m.top.url)
end sub

function fetchToString(url as string) as string
    ut = createObject("roUrlTransfer")
    ut.setUrl(url)
    ut.setCertificatesFile("common:/certs/ca-bundle.crt")
    ut.initClientCertificates()
    ut.setRequest("GET")
    return ut.getToString()
end function
