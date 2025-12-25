# home/currency/get

- request: https://wmsc.lcsc.com/wmsc/home/currency/get
- method: GET
- response:
```json
{
    "code": 200,
    "msg": null,
    "result": [
        {
            "currencyCode": "USD",
            "currencySymbol": "$",
            "currencyName": "美元"
        },
        {
            "currencyCode": "CNY",
            "currencySymbol": "￥",
            "currencyName": "人民币"
        },
        {
            "currencyCode": "EUR",
            "currencySymbol": "€",
            "currencyName": "欧元"
        },
        {
            "currencyCode": "HKD",
            "currencySymbol": "HK$",
            "currencyName": "港币"
        }
    ]
}
```