package api

import (
	"fmt"
	"github.com/go-resty/resty/v2"
	"lcsc/response"
	"log"
	"reflect"
)

func GetProductDetail(code string) {
	var data response.ProductDetailResponse

	response, err := resty.New().R().SetResult(&data).
		SetQueryString("productCode=" + code).
		Get(PRODUCT_DETAIL)
	if err != nil {
		log.Fatal(err)
	}

	if reflect.ValueOf(data.Result).IsZero() == true {
		fmt.Println("Empty Struct")
	}
	fmt.Println("GET Response:", response.Status())
	fmt.Println("GET Response:", data)
	// Check for an Empty Struct
	fmt.Println(reflect.ValueOf(data.Result).IsZero())

}

func GetProductSearch(page int, catalog int, capValue string) ([]response.ProductData, int) {
	var data response.ProductSearchResponse
	var body ProductSearchBody

	body.IsStock = true
	body.CurrentPage = page
	body.PageSize = 100
	body.IsStock = true
	//body.BrandID = make([]any, 0)
	//body.EncapValue = make([]string, 0)
	body.CatalogID = append(body.CatalogID, catalog)
	body.EncapValue = append(body.EncapValue, capValue)

	_, err := resty.New().R().SetResult(&data).
		SetBody(&body).
		Post(PRODUCT_SEARCH_LIST)
	if err != nil {
		log.Fatal(err)
	}

	if reflect.ValueOf(data.Result).IsZero() == true {
		fmt.Println("Empty Struct")
	}
	return data.Result.Data, data.Result.TotalPage

}
