import skia

def is_variable_font(typeface: skia.Typeface) -> bool:
    try:
        return bool(typeface.getVariationDesignParameters())
    except:
        return False
