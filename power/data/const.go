package data

const PATH_POWER string = "../symbol/symbol_power.kicad_sym"
const PATH_POWER_IN string = "../symbol/symbol_power_in.kicad_sym"
const PATH_POWER_OUT string = "../symbol/symbol_power_out.kicad_sym"

const PowerText string = `  (symbol "POWER_NAME" (power) (pin_names (offset 0)) (in_bom yes) (on_board yes)
    (property "Reference" "#PWR" (id 0) (at 0 -3.81 0)
	  (effects (font (size 1.27 1.27)) hide)
    )
    (property "Value" "POWER_NAME" (id 1) (at 0 3.81 0)
	  (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (id 2) (at 0 0 0)
	  (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" "" (id 3) (at 0 0 0)
	  (effects (font (size 1.27 1.27)) hide)
    )
    (property "ki_keywords" "power-flag" (id 4) (at 0 0 0)
	  (effects (font (size 1.27 1.27)) hide)
    )
    (property "ki_description" "Power symbol creates a global label with name \"POWER_NAME\"" (id 5) (at 0 0 0)
	  (effects (font (size 1.27 1.27)) hide)
    )
    (symbol "POWER_NAME_0_1"
	  (polyline
	    (pts
		  (xy -1.27 2.54)
		  (xy 1.27 2.54)
	    )
	    (stroke (width 0.1524) (type default) (color 0 0 0 0))
	    (fill (type none))
	  )
	  (polyline
	    (pts
		  (xy 0 0)
		  (xy 0 2.54)
	    )
	    (stroke (width 0.1524) (type default) (color 0 0 0 0))
	    (fill (type none))
	  )
    )
    (symbol "POWER_NAME_1_1"
	  (pin power_in line (at 0 0 90) (length 0) hide
	    (name "POWER_NAME" (effects (font (size 1.27 1.27))))
	    (number "1" (effects (font (size 1.27 1.27))))
	  )
    )
  )
)`

const PowerInText string = `  (symbol "POWER_NAME" (power) (pin_names (offset 0)) (in_bom yes) (on_board yes)
    (property "Reference" "#PWR" (id 0) (at 0 -3.81 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Value" "POWER_NAME" (id 1) (at 0 3.81 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (id 2) (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" "" (id 3) (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "ki_keywords" "power-flag" (id 4) (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "ki_description" "Power symbol creates a global label with name \"POWER_NAME\"" (id 5) (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (symbol "POWER_NAME_0_1"
      (polyline
        (pts
          (xy -1.27 2.54)
          (xy 1.27 2.54)
        )
        (stroke (width 0.1524) (type default) (color 0 0 0 0))
        (fill (type none))
      )
      (polyline
        (pts
          (xy 0 0)
          (xy 0 2.54)
        )
        (stroke (width 0.1524) (type default) (color 0 0 0 0))
        (fill (type none))
      )
      (polyline
        (pts
          (xy 0 0)
          (xy 1.27 1.905)
          (xy 0 1.27)
          (xy -1.27 1.905)
          (xy 0 0)
        )
        (stroke (width 0.1524) (type default) (color 0 0 0 0))
        (fill (type outline))
      )
    )
    (symbol "POWER_NAME_1_1"
      (pin power_in line (at 0 0 90) (length 0) hide
        (name "POWER_NAME" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
    )
  )
)
`
const PowerOutText string = `  (symbol "POWER_NAME" (power) (pin_names (offset 0)) (in_bom yes) (on_board yes)
    (property "Reference" "#PWR" (id 0) (at 0 -3.81 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Value" "POWER_NAME" (id 1) (at 0 3.81 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (id 2) (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" "" (id 3) (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "ki_keywords" "power-flag" (id 4) (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "ki_description" "Power symbol creates a global label with name \"POWER_NAME\"" (id 5) (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (symbol "POWER_NAME_0_1"
      (polyline
        (pts
          (xy -1.27 2.54)
          (xy 1.27 2.54)
        )
        (stroke (width 0.1524) (type default) (color 0 0 0 0))
        (fill (type none))
      )
      (polyline
        (pts
          (xy 0 0)
          (xy 0 2.54)
        )
        (stroke (width 0.1524) (type default) (color 0 0 0 0))
        (fill (type none))
      )
      (polyline
        (pts
          (xy 0 1.905)
          (xy -1.27 0)
          (xy 0 0.635)
          (xy 1.27 0)
          (xy 0 1.905)
        )
        (stroke (width 0.1524) (type default) (color 0 0 0 0))
        (fill (type outline))
      )
    )
    (symbol "POWER_NAME_1_1"
      (pin power_in line (at 0 0 90) (length 0) hide
        (name "POWER_NAME" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
    )
  )
  (symbol "P3V3_ENET" (power) (pin_names (offset 0)) (in_bom yes) (on_board yes)
    (property "Reference" "#PWR" (id 0) (at 0 -3.81 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Value" "P3V3_ENET" (id 1) (at 0 3.81 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (id 2) (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" "" (id 3) (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "ki_keywords" "power-flag" (id 4) (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "ki_description" "Power symbol creates a global label with name \"P3V3\"" (id 5) (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (symbol "P3V3_ENET_0_1"
      (polyline
        (pts
          (xy -1.27 2.54)
          (xy 1.27 2.54)
        )
        (stroke (width 0.1524) (type default) (color 0 0 0 0))
        (fill (type none))
      )
      (polyline
        (pts
          (xy 0 0)
          (xy 0 2.54)
        )
        (stroke (width 0.1524) (type default) (color 0 0 0 0))
        (fill (type none))
      )
      (polyline
        (pts
          (xy 0 1.905)
          (xy -1.27 0)
          (xy 0 0.635)
          (xy 1.27 0)
          (xy 0 1.905)
        )
        (stroke (width 0.1524) (type default) (color 0 0 0 0))
        (fill (type outline))
      )
    )
    (symbol "P3V3_ENET_1_1"
      (pin power_in line (at 0 0 90) (length 0) hide
        (name "P3V3_ENET" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
    )
  )
)`
