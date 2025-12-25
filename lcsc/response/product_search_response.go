package response

type ProductData struct {
	Eccn               string  `json:"eccn"`
	ProductID          int     `json:"productId"`
	ProductCode        string  `json:"productCode"`
	ProductWeight      float64 `json:"productWeight"`
	ForeignWeight      any     `json:"foreignWeight"`
	Weight             float64 `json:"weight"`
	IsOnsale           bool    `json:"isOnsale"`
	DollarLadderPrice  any     `json:"dollarLadderPrice"`
	IsForeignOnsale    bool    `json:"isForeignOnsale"`
	MinBuyNumber       int     `json:"minBuyNumber"`
	MaxBuyNumber       int     `json:"maxBuyNumber"`
	IsAutoOffsale      bool    `json:"isAutoOffsale"`
	MinPacketUnit      string  `json:"minPacketUnit"`
	ProductUnit        string  `json:"productUnit"`
	ProductArrange     string  `json:"productArrange"`
	MinPacketNumber    int     `json:"minPacketNumber"`
	EncapStandard      string  `json:"encapStandard"`
	ProductModel       string  `json:"productModel"`
	BrandID            int     `json:"brandId"`
	BrandNameEn        string  `json:"brandNameEn"`
	CatalogID          int     `json:"catalogId"`
	CatalogName        string  `json:"catalogName"`
	ParentCatalogID    int     `json:"parentCatalogId"`
	ParentCatalogName  string  `json:"parentCatalogName"`
	ProductDescEn      any     `json:"productDescEn"`
	ProductIntroEn     string  `json:"productIntroEn"`
	IsHasBattery       bool    `json:"isHasBattery"`
	IsDiscount         bool    `json:"isDiscount"`
	IsHot              bool    `json:"isHot"`
	IsEnvironment      bool    `json:"isEnvironment"`
	IsPreSale          bool    `json:"isPreSale"`
	ProductLadderPrice any     `json:"productLadderPrice"`
	LadderDiscountRate any     `json:"ladderDiscountRate"`
	ProductPriceList   []struct {
		Ladder              int     `json:"ladder"`
		ProductPrice        string  `json:"productPrice"`
		DiscountRate        string  `json:"discountRate"`
		CurrencyPrice       float64 `json:"currencyPrice"`
		UsdPrice            float64 `json:"usdPrice"`
		CurrencySymbol      string  `json:"currencySymbol"`
		CnyProductPriceList any     `json:"cnyProductPriceList"`
		IsForeignDiscount   any     `json:"isForeignDiscount"`
		LadderLevel         any     `json:"ladderLevel"`
	} `json:"productPriceList"`
	StockJs         int `json:"stockJs"`
	StockSz         int `json:"stockSz"`
	StockHk         int `json:"stockHk"`
	WmStockHk       int `json:"wmStockHk"`
	DomesticStockVO struct {
		Total           int `json:"total"`
		ShipImmediately int `json:"shipImmediately"`
		Ship3Days       int `json:"ship3Days"`
	} `json:"domesticStockVO"`
	OverseasStockVO struct {
		Total           int `json:"total"`
		ShipImmediately int `json:"shipImmediately"`
		Ship3Days       int `json:"ship3Days"`
	} `json:"overseasStockVO"`
	ShipImmediately    int      `json:"shipImmediately"`
	Ship3Days          int      `json:"ship3Days"`
	SmtAloneNumberSz   any      `json:"smtAloneNumberSz"`
	SmtAloneNumberJs   any      `json:"smtAloneNumberJs"`
	StockNumber        int      `json:"stockNumber"`
	Split              int      `json:"split"`
	ProductImageURL    string   `json:"productImageUrl"`
	ProductImageURLBig string   `json:"productImageUrlBig"`
	PdfURL             string   `json:"pdfUrl"`
	ProductImages      []string `json:"productImages"`
	ParamVOList        []struct {
		ParamCode             string  `json:"paramCode"`
		ParamName             string  `json:"paramName"`
		ParamNameEn           string  `json:"paramNameEn"`
		ParamValue            string  `json:"paramValue"`
		ParamValueEn          string  `json:"paramValueEn"`
		ParamValueEnForSearch float64 `json:"paramValueEnForSearch"`
		IsMain                bool    `json:"isMain"`
		SortNumber            int     `json:"sortNumber"`
	} `json:"paramVOList"`
	IsReel                bool    `json:"isReel"`
	ReelPrice             float64 `json:"reelPrice"`
	ProductModelHighlight any     `json:"productModelHighlight"`
	ProductCodeHighlight  any     `json:"productCodeHighlight"`
	CatalogCode           string  `json:"catalogCode"`
	ParentCatalogCode     string  `json:"parentCatalogCode"`
	PdfLinkURL            any     `json:"pdfLinkUrl"`
	URL                   string  `json:"url"`
	ShareCostPrice        any     `json:"shareCostPrice"`
	ActivityID            any     `json:"activityId"`
	ActivityName          any     `json:"activityName"`
	ActivityStartTime     any     `json:"activityStartTime"`
	ActivityEndTime       any     `json:"activityEndTime"`
	StockPrice            any     `json:"stockPrice"`
	IsFavorite            bool    `json:"isFavorite"`
}

type ProductSearch struct {
	CurrPage   int           `json:"currPage"`
	PageRow    int           `json:"pageRow"`
	TotalPage  int           `json:"totalPage"`
	TotalRow   int           `json:"totalRow"`
	Data       []ProductData `json:"dataList"`
	PageBounds struct {
		Offset             int   `json:"offset"`
		Limit              int   `json:"limit"`
		Page               int   `json:"page"`
		Orders             []any `json:"orders"`
		ContainsTotalCount bool  `json:"containsTotalCount"`
		AsyncTotalCount    any   `json:"asyncTotalCount"`
	} `json:"pageBounds"`
}

type ProductSearchResponse struct {
	Code     int           `json:"code"`
	Messages string        `json:"msg"`
	Result   ProductSearch `json:"result"`
}
