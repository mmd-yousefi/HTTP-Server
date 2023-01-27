import json

data = {
    "root":{
            "domains":{
                "network1.com":{
                    "ip":"192.168.1.36",
                    "port":"8080",
                    "subdomains":{
                        "sub1.network1.com":{
                            "ip":"192.168.1.37",
                            "port":"8081",
                        },
                        "sub2.network1.com":{
                            "ip":"192.168.1.38",
                            "port":"8082",
                        }
                    }
                },
                "network2.com":{
                    "ip":"192.168.1.40",
                    "port":"8090",
                    "subdomains":{
                        "sub1.network2.com":{
                            "ip":"192.168.1.41",
                            "port":"8091",
                        },
                        "sub2.network2.com":{
                            "ip":"192.168.1.42",
                            "port":"8092",
                        }
                    }
                }
            }            
    }
}
with open("DNS_DATA.json","w") as write_file:
    json.dump(data,write_file,indent=4)
