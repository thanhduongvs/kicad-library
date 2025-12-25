package response

type ProductPrice struct {
	Ladder              int64   `json:"ladder"`
	ProductPrice        string  `json:"productPrice"`
	DiscountRate        string  `json:"discountRate"`
	CurrencyPrice       float64 `json:"currencyPrice"`
	UsdPrice            float64 `json:"usdPrice"`
	CurrencySymbol      string  `json:"currencySymbol"`
	CnyProductPriceList any     `json:"cnyProductPriceList"`
	IsForeignDiscount   any     `json:"isForeignDiscount"`
	LadderLevel         any     `json:"ladderLevel"`
}

type ParamVO struct {
	ParamCode             string  `json:"paramCode"`
	ParamName             string  `json:"paramName"`
	ParamNameEn           string  `json:"paramNameEn"`
	ParamValue            string  `json:"paramValue"`
	ParamValueEn          string  `json:"paramValueEn"`
	ParamValueEnForSearch float64 `json:"paramValueEnForSearch"`
	IsMain                bool    `json:"isMain"`
	SortNumber            int64   `json:"sortNumber"`
}

type ProductDetail struct {
	ProductID         int64          `json:"productId"`
	ProductCode       string         `json:"productCode"`
	ProductModel      string         `json:"productModel"`
	ParentCatalogID   int64          `json:"parentCatalogId"`
	ParentCatalogName string         `json:"parentCatalogName"`
	CatalogID         int64          `json:"catalogId"`
	CatalogName       string         `json:"catalogName"`
	BrandID           int64          `json:"brandId"`
	BrandNameEn       string         `json:"brandNameEn"`
	EncapStandard     string         `json:"encapStandard"`
	Split             int64          `json:"split"`
	ProductUnit       string         `json:"productUnit"`
	MinPacketUnit     string         `json:"minPacketUnit"`
	MinBuyNumber      int64          `json:"minBuyNumber"`
	MaxBuyNumber      int64          `json:"maxBuyNumber"`
	MinPacketNumber   int64          `json:"minPacketNumber"`
	IsEnvironment     bool           `json:"isEnvironment"`
	AllHotLevel       any            `json:"allHotLevel"`
	IsHot             bool           `json:"isHot"`
	IsPreSale         bool           `json:"isPreSale"`
	IsReel            bool           `json:"isReel"`
	ReelPrice         int64          `json:"reelPrice"`
	StockNumber       int64          `json:"stockNumber"`
	ShipImmediately   int64          `json:"shipImmediately"`
	Ship3Days         int64          `json:"ship3Days"`
	StockSz           int64          `json:"stockSz"`
	StockJs           int64          `json:"stockJs"`
	WmStockHk         int64          `json:"wmStockHk"`
	ProductPrice      []ProductPrice `json:"productPriceList"`
	ProductImages     []string       `json:"productImages"`
	PdfURL            string         `json:"pdfUrl"`
	ProductDescEn     any            `json:"productDescEn"`
	ProductIntroEn    string         `json:"productIntroEn"`
	ProductArrange    string         `json:"productArrange"`
	ProductWeight     float64        `json:"productWeight"`
	ForeignWeight     any            `json:"foreignWeight"`
	Weight            float64        `json:"weight"`
	IsForeignOnsale   bool           `json:"isForeignOnsale"`
	IsAutoOffsale     bool           `json:"isAutoOffsale"`
	IsHasBattery      bool           `json:"isHasBattery"`
	Title             string         `json:"title"`
	IsFavorite        bool           `json:"isFavorite"`
	ParamVO           []ParamVO      `json:"paramVOList"`
	IsAddNotice       any            `json:"isAddNotice"`
	SubscribeQuantity any            `json:"subscribeQuantity"`
	Eccn              string         `json:"eccn"`
	CurrencyType      string         `json:"currencyType"`
	CurrencySymbol    string         `json:"currencySymbol"`
}

type ProductDetailResponse struct {
	Code     uint64        `json:"code"`
	Messages string        `json:"msg"`
	Result   ProductDetail `json:"result"`
}
